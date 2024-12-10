import json
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import yaml

from Borrow import Borrow
from Media import Book, Vinyl, Cd
from Person import User


class Mediatheque:
    def __init__(self, filename="YML/mediatheque.yml"):
        self.filename = filename
        self.__users = self.load_users()
        self.__media = self.load_media_from_json()
        self.__history = self.load_history()

    @property
    def media(self):
        return self.__media

    def send_email(self, recipient, subject, message):
        """Sends an email using Free SMTP Servers.

        Args:
          recipient: The recipient's email address.
          subject: The subject of the email.
          message: The email message body.
        """

        sender_email = "your_email@example.com"  # Replace with your email

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient

        try:
            with smtplib.SMTP('smtp.freesmtpservers.com', 25) as server:
                server.sendmail(sender_email, recipient, msg.as_string())
            print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def media_est_disponible(self, media):
        """Vérifie si un média est disponible en consultant l'historique des emprunts.

        Args:
          media: Le média à vérifier.

        Returns:
          True si le média est disponible, False sinon.
        """
        for emprunt in self.__history:
            if emprunt._media == media and emprunt._return_date is None:
                # Le média a été emprunté et n'a pas encore été retourné
                return False
        return True  # Le média n'a pas d'emprunt actif, donc il est disponible

    def load_media_from_json(self, media_files=["book.json", "cd.json", "vinyl.json"]):
        all_media = []
        for fichier in media_files:
            try:
                with open("JSON/" + fichier, 'r') as f:
                    data = json.load(f)
                    for media_data in data:
                        media_type = fichier.split('.')[0].lower()  # Extract media type from filename
                        status = media_data.get('status', 'OK')
                        if media_type == "book":
                            media = Book( media_data['title'], media_data['id'], status, media_data.get('author', None))
                        elif media_type == "cd":
                            media = Cd(media_data['title'], media_data['id'],  status, media_data.get('author', None))
                        elif media_type == "vinyl":
                            media = Vinyl(media_data['title'], media_data['id'], status, media_data.get('author', None))
                        else:
                            print(f"Type de média inconnu : {media_type}")
                            continue
                        all_media.append(media)
            except FileNotFoundError:
                print(f"Le fichier {fichier} n'a pas été trouvé.")
            except json.JSONDecodeError:
                print(f"Erreur lors du parsing du fichier {fichier}.")
        return all_media

    def save_media_to_json(self, media_files=["book.json", "cd.json", "vinyl.json"]):
        for media_type, file_name in zip(["book", "cd", "vinyl"], media_files):
            media_data = [media.to_json() for media in self.media if isinstance(media, eval(media_type.capitalize()))]
            with open("JSON/" + file_name, 'w', encoding='utf-8') as f:
                json.dump(media_data, f, indent=4)

    def load_users(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                if data is None:
                    return []
                users = []
                for user_data in data.get("users", []):
                    user_data["password"] = user_data["password"].encode()
                    users.append(User(**user_data))
                return users
        except Exception as e:
            print(f"Failed to load users: {e}")
            return []

    def afficher_medias(self):
        """Affiche tous les médias de la médiathèque."""
        for media in self.media:
            print(media)  # Use the __str__ method of the Media class

    def load_history(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                history = []
                for borrow_data in data.get("history", []):
                    media = self.get_media_by_id(borrow_data["media_id"])
                    user = next((u for u in self.__users if u._user_id == borrow_data["user_id"]), None)
                    if media and user:
                        borrow = Borrow(
                            datetime.fromisoformat(borrow_data["borrow_date"]),
                            datetime.fromisoformat(borrow_data["return_date"]) if borrow_data["return_date"] else None,
                            media,
                            user
                        )
                        history.append(borrow)
                    else:
                        print(f"Warning: Could not find media or user for borrow record: {borrow_data}")
                return history
        except Exception as e:
            print(f"Failed to load history: {e}")
            return []

    def save_data(self):
        data = {
            "users": [user.to_dict() for user in self.__users],
            "history": [borrow.to_dict() for borrow in self.__history]
        }
        with open(self.filename, 'w', encoding='utf-8') as file:
            yaml.safe_dump(data, file, default_flow_style=False, allow_unicode=True)

    def add_media(self, media):
        self.__media.append(media)
        self.save_media_to_json()

    def register_person(self, person):
        self.__users.append(person)
        self.save_data()  # Save user data after registration

    def get_overdue_users(self):
        overdue_users = []
        for borrow in self.__history:
            if borrow.is_overdue():
                overdue_users.append(borrow.user)
        return overdue_users

    def record_borrow(self, borrow):
        self.__history.append(borrow)
        self.save_data()  # Save borrow history

    def return_media(self, borrow):
        try:
            self.__history.remove(borrow)
            self.save_data()  # Save borrow history after return
            return "Media returned successfully!"
        except ValueError:
            return "Error: Borrow record not found."

    def warn_users(self):
        """Avertit les utilisateurs ayant des médias en retard par email."""
        warnings = []
        for borrow in self.__history:
            if borrow.is_overdue():
                user = borrow.user
                message = f"Warning: User {user._login}, the media '{borrow.media.title}' is overdue!"
                warnings.append(message)

        for borrow in self.__history:
            if borrow.is_overdue():
                user = borrow.user
                message = f"Bonjour {user._first_name} {user._last_name},\n\n"
                message += f"Le média '{borrow.media.title}' est en retard.\n"
                message += "Veuillez le retourner dès que possible à la médiathèque.\n\n"
                message += "Cordialement,\nLa Médiathèque"

                subject = "Média en retard - Médiathèque"

                self.send_email(user._email, subject, message)

        return warnings


    # Accessors for users
    @property
    def users(self):
        return self.__users

    # Accessors for history
    @property
    def history(self):
        return self.__history

    # Additional accessor for specific media by ID
    def get_media_by_id(self, media_id):
        for media in self.__media:
            if media.id == media_id:
                return media
        return None