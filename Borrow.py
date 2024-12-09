from datetime import date

class Borrow:
    def __init__(self, borrow_date, return_date, media, user):
        self.__borrow_date = borrow_date
        self.__return_date = return_date
        self.__media = media
        self.__user = user

    def is_overdue(self):
        return date.today() > self.__return_date

    @property
    def media(self):
        return self.__media

    @property
    def user(self):
        return self.__user

    def __str__(self):
        return f"User: {self.__user.login}, Media: {self.__media.title}, Borrowed on: {self.__borrow_date}, Due on: {self.__return_date}"
