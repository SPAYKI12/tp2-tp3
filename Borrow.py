# Borrow class
from datetime import date

class Borrow:
    def __init__(self, borrow_date, return_date, media, user, attribute):
        self.__borrow_date = borrow_date
        self.__return_date = return_date
        self.__media = media
        self.__user = user
        self.__attribute = attribute

    def is_overdue(self):
        return date.today() > self.__borrow_date + self.__media

