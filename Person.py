from datetime import datetime
import bcrypt  # For password hashing

class Person:
    def __init__(self, login, password, last_name, first_name, user_id):
        self._login = login
        self._password = password.encode() if isinstance(password, str) else password  # Ensure password is bytes
        self._last_name = last_name
        self._first_name = first_name
        self._user_id = user_id


    def authenticate(self, login, password):
        return self._login == login and bcrypt.checkpw(password.encode(), self._password)

    def to_dict(self):
        return {
            "login": self._login,
            "password": self._password.decode(),  # Decode when saving to YAML
            "last_name": self._last_name,
            "first_name": self._first_name,
            "user_id": self._user_id,
        }

class Administrator(Person):
    def __init__(self, login, password, last_name, first_name, user_id):
        super().__init__(login, password, last_name, first_name, user_id)


class User(Person):
    def __init__(self, login, password, last_name, first_name, user_id, email="", registration_date=datetime.now(), first_time=True):
        super().__init__(login, password, last_name, first_name, user_id)
        self._email = email
        self._registration_date = registration_date
        self._borrow_history = []
        self._first_time = first_time


    @property
    def first_time(self):
        return self._first_time
    @first_time.setter
    def first_time(self, bool):
        self._first_time = bool

    def add_borrow(self, borrow):
        self._borrow_history.append(borrow)

    def view_borrow_history(self):
        return [str(borrow) for borrow in self._borrow_history]

    def to_dict(self):
        data = super().to_dict()
        data["email"] = self._email
        data["first_time"] = self._first_time
        if isinstance(self._registration_date, datetime):
            data["registration_date"] = self._registration_date.isoformat()
        else:
            data["registration_date"] = self._registration_date  # Handle non-datetime case
        return data

    def __str__(self):
        return f"User: {self._login}, Email: {self._email}, Registered on: {self._registration_date}"

