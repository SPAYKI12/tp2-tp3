from abc import ABC, abstractmethod
from datetime import date

class Person(ABC):
    def __init__(self, login, pwd, last_name, first_name, id):
        self.__login = login
        self.__pwd = pwd
        self.__last_name = last_name
        self.__first_name = first_name
        self.__id = id

    def authenticate(self, login, password):
        if self.__login == login and self.__pwd == password:
            print(f"{self.__class__.__name__} {self.__login} authenticated")
            return True
        return False

    def modify_password(self, new_password):
        self.__pwd = new_password

class Administrator(Person):
    pass

class User(Person):
    def __init__(self, login, pwd, last_name, first_name, id, mail, date_inscription):
        super().__init__(login, pwd, last_name, first_name, id)
        self.__mail = mail
        self.__date_inscription = date_inscription






