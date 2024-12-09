from datetime import date

class Person:
    def __init__(self, login, password, last_name, first_name, user_id):
        self.__login = login
        self.__password = password
        self.__last_name = last_name
        self.__first_name = first_name
        self.__user_id = user_id

    def authenticate(self, login, password):
        return self.__login == login and self.__password == password

class Administrator(Person):
    def __init__(self, login, password, last_name, first_name, user_id):
        super().__init__(login, password, last_name, first_name, user_id)

class User(Person):
    def __init__(self, login, password, last_name, first_name, user_id, email, registration_date):
        super().__init__(login, password, last_name, first_name, user_id)
        self.__email = email
        self.__registration_date = registration_date
        self.__borrow_history = []

    def add_borrow(self, borrow):
        self.__borrow_history.append(borrow)

    def view_borrow_history(self):
        return [str(borrow) for borrow in self.__borrow_history]

    def __str__(self):
        return f"User: {self.__login}, Email: {self.__email}, Registered on: {self.__registration_date}"
