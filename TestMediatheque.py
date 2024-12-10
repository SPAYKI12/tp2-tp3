import os
import unittest
from datetime import datetime, timedelta

import bcrypt

from Mediatheque import Mediatheque
from Person import User
from Media import Book
from Borrow import Borrow


# Vider le yml

class TestMediatheque(unittest.TestCase):
    def setUp(self):
        self.mediatheque = Mediatheque("YML/mediatheque.yml")  # Use a separate file for testing

    def test_asave_and_load_users(self):
        user1 = User("alice", bcrypt.hashpw("password".encode(), bcrypt.gensalt()), "Doe", "Alice", 1)
        self.mediatheque.register_person(user1)
        self.mediatheque.save_data()

        # Reload the mediatheque
        new_mediatheque = Mediatheque("YML/mediatheque.yml")
        self.assertEqual(len(new_mediatheque.users), 1)
        self.assertEqual(new_mediatheque.users[0]._login, "alice")

    def test_borrow_and_return(self):
        book = Book("Le Petit Prince", 1, "available")
        self.mediatheque.add_media(book)
        user = User("bob", bcrypt.hashpw("password".encode(), bcrypt.gensalt()), "Smith", "Bob", 2)
        self.mediatheque.register_person(user)

        borrow_date = datetime.now().date()
        return_date = borrow_date + timedelta(days=21)


if __name__ == '__main__':
    unittest.main()
