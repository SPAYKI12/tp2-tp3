import os
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

import bcrypt
import yaml

from Borrow import Borrow
from Media import Book, Cd, Vinyl
from Person import User, Administrator


class MessageManager:
    def __init__(self, file_path="YML/gestion_console.yml"):
        self.messages = self.load_messages(file_path)

    @staticmethod
    def load_messages(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def get_message(self, key, **kwargs):
        keys = key.split('.')
        msg = self.messages
        for k in keys:
            msg = msg.get(k, {})
        if isinstance(msg, str):
            return msg.format(**kwargs)
        return "[Message not found]"


class Gestion:
    def __init__(self, mediatheque, message_manager, user_file="users.yml", state_file="connected_user.yml"):
        self.mediatheque = mediatheque
        self.message_manager = message_manager
        self.current_user = None
        self.state_file = state_file
        self.user_file = user_file

    def authenticate_user(self):

        login = input(self.message_manager.get_message("authentication.login_prompt"))
        password = input(self.message_manager.get_message("authentication.password_prompt"))

        # Chercher un utilisateur avec le login et le mot de passe donnés
        for user in self.mediatheque.users:
            if user._login == login and user.authenticate(login, password):
                self.current_user = user
                print(self.message_manager.get_message("authentication.success", user=user._login))
                return True

        print(self.message_manager.get_message("authentication.failure"))
        return False

    def authenticate_admin(self):
        login = input(self.message_manager.get_message("authentication.login_prompt"))
        password = input(self.message_manager.get_message("authentication.password_prompt"))

        # Charger le super admin depuis YAML et vérifier les identifiants
        with open("YML/super_admin.yml", 'r') as file:
            super_admin_data = yaml.safe_load(file)["super_admin"]
            if login == super_admin_data["login"] and password == super_admin_data["password"]:  # Vérification en clair
                # Créer et enregistrer le super admin (seulement si l'authentification est réussie)
                super_admin = Administrator(login, password, "Admin", "Super", 1)  # Pas de hachage

                self.current_user = super_admin
                print(self.message_manager.get_message("authentication.success", user=super_admin._login))
                return True

        print(self.message_manager.get_message("authentication.failure"))
        return False

    def logout(self):
        if self.current_user:
            print(self.message_manager.get_message("authentication.logout", user=self.current_user._login))
            self.current_user = None


    def display_menu_admin(self):
        print("\n=== " + self.message_manager.get_message("administrator.menu-title") + " ===")
        print(self.message_manager.get_message("administrator.command-list.ajouter_utilisateur"))
        print(self.message_manager.get_message("administrator.command-list.ajouter_media"))
        print(self.message_manager.get_message("administrator.command-list.afficher_liste_utilisateurs"))
        print(self.message_manager.get_message("administrator.command-list.afficher_liste_medias"))
        print(self.message_manager.get_message("administrator.command-list.avertir_utilisateurs"))
        print(self.message_manager.get_message("administrator.command-list.retourner_media"))  # Ajout pour l'admin
        print(self.message_manager.get_message("administrator.command-list.quitter"))

    def display_menu_user(self):
        print("\n=== " + self.message_manager.get_message("user.menu-title") + " ===")
        print(self.message_manager.get_message("user.command-list.emprunter_media"))  # Ajout pour l'user
        print(self.message_manager.get_message("user.command-list.afficher_historique_emprunts"))
        print(self.message_manager.get_message("user.command-list.afficher_medias_disponibles"))
        print(self.message_manager.get_message("user.command-list.modify_passwords"))
        print(self.message_manager.get_message("user.command-list.quitter"))

    def ajouter_utilisateur(self):
        login = input(self.message_manager.get_message("administrator.add-user.login"))
        pwd = input(self.message_manager.get_message("administrator.add-user.password"))
        last_name = input(self.message_manager.get_message("administrator.add-user.last_name"))
        first_name = input(self.message_manager.get_message("administrator.add-user.first_name"))
        email = input(self.message_manager.get_message("administrator.add-user.email"))

        # Hash the password
        hashed_pwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

        utilisateur = User(login, hashed_pwd, last_name, first_name, len(self.mediatheque.users) + 1, email,
                           datetime.now().date())
        print(self.mediatheque.register_person(utilisateur))

    def ajouter_media(self):
        title = input(self.message_manager.get_message("media.title"))
        media_type = input(self.message_manager.get_message("media.type"))
        author = input(self.message_manager.get_message("media.author"))

        # Demande de l'état du média
        state = input(self.message_manager.get_message("media.state"))

        media = None

        if media_type.lower() == "book":
            media = Book(title, len(self.mediatheque.media) + 1, state, author)
        elif media_type.lower() == "cd":
            media = Cd(title, len(self.mediatheque.media) + 1, state, author)
        elif media_type.lower() == "vinyl":
            media = Vinyl(title, len(self.mediatheque.media) + 1, state, author)
        else:
            print(self.message_manager.get_message("error.invalid-media-type"))
            return

        self.mediatheque.add_media(media)
        print(self.message_manager.get_message("media.added-success", media=title))

    def emprunter_media(self):
        media_id = int(input("ID du média à emprunter : "))  # Demander l'ID du média
        media = next((m for m in self.mediatheque.media if m.id == media_id), None)

        if self.mediatheque.media_est_disponible(media):
            borrow = Borrow(datetime.now().date(), None, media, self.current_user)
            self.mediatheque.record_borrow(borrow)
            print(self.message_manager.get_message("user.borrow-success", media=media.title,
                                                   user=self.current_user._login))
        else:
            print(self.message_manager.get_message("error.invalid-choice"))


    def modify_password(self):
        """Permet à l'utilisateur actuel de changer son mot de passe."""

        ancien_mot_de_passe = input("Ancien mot de passe : ")

        # Vérifier l'ancien mot de passe
        if not bcrypt.checkpw(ancien_mot_de_passe.encode(), self.current_user._password):
            print("Ancien mot de passe incorrect.")
            return

        nouveau_mot_de_passe = input("Nouveau mot de passe : ")
        confirmation_mot_de_passe = input("Confirmation du nouveau mot de passe : ")

        if nouveau_mot_de_passe != confirmation_mot_de_passe:
            print("Les mots de passe ne correspondent pas.")
            return

        # Hasher le nouveau mot de passe
        hashed_pwd = bcrypt.hashpw(nouveau_mot_de_passe.encode(), bcrypt.gensalt())
        self.current_user._password = hashed_pwd

        self.mediatheque.save_data()  # Sauvegarder les données mises à jour
        print("Mot de passe changé avec succès.")

    def retourner_media(self):
        # Afficher la liste des médias empruntés
        print("Médias actuellement empruntés :")
        for borrow in self.mediatheque.history:
            if borrow._return_date is None:  # Vérifier si le média n'a pas déjà été retourné
                print(f"- ID: {borrow.media.id}, Titre: {borrow.media.title}, Emprunteur: {borrow.user._login}")

        media_id = int(input("ID du média à retourner : "))  # Demander l'ID du média

        # Correction : utiliser borrow.user._user_id pour filtrer les emprunts
        borrow = next((b for b in self.mediatheque.history if b.media.id == media_id and b._return_date is None), None)

        if borrow:
            while True:  # Boucle pour la vérification de l'état
                etat_saisi = input(self.message_manager.get_message("media.state") + " : ")
                if etat_saisi == borrow.media.state:  # Vérification de l'état par rapport au média emprunté
                    borrow._return_date = datetime.now().date()  # Set the return date
                    self.mediatheque.save_data()  # Save the updated borrow data
                    print(self.message_manager.get_message("user.return-success", media=borrow.media.title))
                    break  # Sortir de la boucle si l'état est conforme
                else:
                    print(self.message_manager.get_message("media.etat_ok"))
        else:
            print(self.message_manager.get_message("error.invalid-choice"))

    def avertir_utilisateurs(self):
        warnings = self.mediatheque.warn_users()
        for warning in warnings:
            print(warning)

    def afficher_medias(self, filtre=None):
        """Affiche tous les médias de la médiathèque.

        Args:
            filtre (str, optional): Filtre par type de média (book, cd, vinyl). Defaults to None.
        """
        print(self.message_manager.get_message("media.liste_medias"))
        for media in self.mediatheque.media:
            if filtre is None or isinstance(media, eval(filtre.capitalize())):
                print(f"{media.id} - {media.title} ({media.__class__.__name__})")

    def afficher_utilisateurs(self):
        """Affiche la liste des utilisateurs enregistrés."""
        print("Liste des utilisateurs:")
        for user in self.mediatheque.users:
            print(f"- ID: {user._user_id}, Nom: {user._first_name} {user._last_name}, Login: {user._login}")

    def run_admin_menu(self):
        while True:
            self.display_menu_admin()
            choice = input(self.message_manager.get_message("administrator.prompt"))

            if choice == "1":
                self.ajouter_utilisateur()
            elif choice == "2":
                self.ajouter_media()
            elif choice == "3":
                self.afficher_utilisateurs()
            elif choice == "4":
                self.afficher_medias()
            elif choice == "5":
                self.avertir_utilisateurs()
            elif choice == "6":
                self.retourner_media()
            elif choice == "0":
                self.logout()
                break
            else:
                print(self.message_manager.get_message("error.invalid-choice"))



    def run_user_menu(self):
        while True:
            if self.current_user.first_time:
                print(self.message_manager.get_message("user.first-time"))
                self.current_user.first_time = False
                self.mediatheque.save_data()

            self.display_menu_user()
            choice = input(self.message_manager.get_message("user.prompt"))

            if choice == "1":
                self.afficher_medias()
                self.emprunter_media()
            elif choice == "2":
                self.afficher_historique_emprunts()
            elif choice == "3":
                self.afficher_medias_disponibles()
            elif choice == "4":
                self.modify_password()
            elif choice == "0":
                self.logout()  # Logout before quitting
                break
            else:
                print(self.message_manager.get_message("error.invalid-choice"))

    def afficher_historique_emprunts(self):
        """Displays the borrow history of the current user."""
        print(self.message_manager.get_message("user.historique_title"))
        history = self.current_user.view_borrow_history()
        if history:
            for borrow in history:
                print(borrow)
        else:
            print(self.message_manager.get_message("user.no_borrow_history"))

    def afficher_medias_disponibles(self):
        """Affiche la liste des médias disponibles."""
        print("Médias disponibles:")
        for media in self.mediatheque.media:
            if self.mediatheque.media_est_disponible(media):  # Appel de la nouvelle fonction
                print(f" {media.id}- {media.title} ({media.__class__.__name__})")



    def run(self):
        print(self.message_manager.get_message("authentication.start"))

        # Check if there are any users registered
        if not self.mediatheque.users:
            print(self.message_manager.get_message("no_users"))
            # Create the initial administrator account
            self.ajouter_utilisateur()

        while True:
            user_type = input("Are you an admin or user? (admin/user): ").lower()
            if user_type == "admin":
                if self.authenticate_admin():  # Call authenticate_admin for admins
                    self.run_admin_menu()
            elif user_type == "user":
                if self.authenticate_user():
                    self.run_user_menu()
            else:
                print("Invalid user type. Please enter 'admin' or 'user'.")