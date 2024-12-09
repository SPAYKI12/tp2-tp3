import yaml
from datetime import datetime

from Borrow import Borrow
from Mediatheque import Mediatheque
from Person import User, Administrator
from Media import Book,CD,Vinyl



class MessageManager:
    def __init__(self, file_path="YML/gestion_console.yml"):
        self.messages = self.load_messages(file_path)

    @staticmethod
    def load_messages(file_path):
        with open(file_path, 'r') as file:
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
    def __init__(self, mediatheque, message_manager):
        self.mediatheque = mediatheque
        self.message_manager = message_manager
        self.current_user = None

    def authenticate_user(self):
        login = input(self.message_manager.get_message("authentication.login"))
        password = input(self.message_manager.get_message("authentication.password"))
        user = next((u for u in self.mediatheque.users if u.authenticate(login, password)), None)
        if user:
            self.current_user = user
            print(self.message_manager.get_message("authentication.success", user=user.login))
            return True
        print(self.message_manager.get_message("authentication.failed"))
        return False

    def display_menu_admin(self):
        print("\n=== " + self.message_manager.get_message("administrator.menu-title") + " ===")
        print(self.message_manager.get_message("administrator.command-list.1"))
        print(self.message_manager.get_message("administrator.command-list.2"))
        print(self.message_manager.get_message("administrator.command-list.5"))
        print(self.message_manager.get_message("administrator.command-list.0"))

    def display_menu_user(self):
        print("\n=== " + self.message_manager.get_message("user.menu-title") + " ===")
        print(self.message_manager.get_message("user.command-list.1"))
        print(self.message_manager.get_message("user.command-list.2"))
        print(self.message_manager.get_message("administrator.command-list.0"))

    def ajouter_utilisateur(self):
        login = input(self.message_manager.get_message("authentication.login"))
        pwd = input(self.message_manager.get_message("authentication.password"))
        last_name = input(self.message_manager.get_message("user.last-name"))
        first_name = input(self.message_manager.get_message("user.first-name"))
        email = input(self.message_manager.get_message("user.email"))
        utilisateur = User(login, pwd, last_name, first_name, len(self.mediatheque.users) + 1, email, datetime.now().date())
        print(self.mediatheque.register_person(utilisateur))

    def ajouter_media(self):
        title = input(self.message_manager.get_message("media.title"))
        media_type = input(self.message_manager.get_message("media.type"))
        media = None

        if media_type.lower() == "book":
            media = Book(title, len(self.mediatheque.media) + 1, "available")
        elif media_type.lower() == "cd":
            media = CD(title, len(self.mediatheque.media) + 1, "available")
        elif media_type.lower() == "vinyl":
            media = Vinyl(title, len(self.mediatheque.media) + 1, "available")
        else:
            print(self.message_manager.get_message("error.invalid-media-type"))
            return

        self.mediatheque.add_media(media)
        print(self.message_manager.get_message("media.added-success", media=title))

    def emprunter_media(self):
        media_title = input(self.message_manager.get_message("media.title"))
        media = next((m for m in self.mediatheque.media if m.title == media_title), None)

        if media:
            borrow = Borrow(datetime.now().date(), self.current_user, media)
            self.mediatheque.history.append(borrow)
            print(self.message_manager.get_message("user.borrow-success", media=media.title, user=self.current_user.login))
        else:
            print(self.message_manager.get_message("error.invalid-choice"))

    def retourner_media(self):
        media_title = input(self.message_manager.get_message("media.title"))
        borrow = next((b for b in self.mediatheque.history if b.user == self.current_user and b.media.title == media_title), None)

        if borrow:
            print(self.mediatheque.return_media(borrow))
        else:
            print(self.message_manager.get_message("error.invalid-choice"))

    def avertir_utilisateurs(self):
        warnings = self.mediatheque.warn_users()
        for warning in warnings:
            print(warning)

    def sauvegarder_et_quitter(self):
        self.mediatheque.save_state('mediatheque_state.yaml')
        print(self.message_manager.get_message("administrator.command-list.0"))

    def run_admin_menu(self):
        while True:
            self.display_menu_admin()
            choice = input(self.message_manager.get_message("administrator.prompt"))

            if choice == "1":
                self.ajouter_utilisateur()
            elif choice == "2":
                self.ajouter_media()
            elif choice == "5":
                self.avertir_utilisateurs()
            elif choice == "0":
                self.sauvegarder_et_quitter()
                break
            else:
                print(self.message_manager.get_message("error.invalid-choice"))

    def run_user_menu(self):
        while True:
            self.display_menu_user()
            choice = input(self.message_manager.get_message("user.prompt"))

            if choice == "1":
                self.emprunter_media()
            elif choice == "2":
                self.retourner_media()
            elif choice == "0":
                self.sauvegarder_et_quitter()
                break
            else:
                print(self.message_manager.get_message("error.invalid-choice"))

    def run(self):
        print(self.message_manager.get_message("authentication.start"))
        if self.authenticate_user():
            if isinstance(self.current_user, Administrator):
                self.run_admin_menu()
            elif isinstance(self.current_user, User):
                self.run_user_menu()

mediatheque = Mediatheque()
message_manager = MessageManager()
gestion = Gestion(mediatheque, message_manager)

gestion.run()