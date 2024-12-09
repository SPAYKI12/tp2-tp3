from abc import ABC, abstractmethod
from datetime import date, timedelta

class Media(ABC):
    def __init__(self, title, media_id, state):
        self.__title = title
        self.__id = media_id
        self.__state = state
        self.__return_period_days = 7  # Valeur par défaut pour CD et Vinyl

    @property
    def title(self):
        return self.__title

    @property
    def id(self):
        return self.__id

    @property
    def state(self):
        return self.__state

    @abstractmethod
    def borrow(self):
        pass

    @abstractmethod
    def return_media(self):
        pass

class Book(Media):
    def __init__(self, title, media_id, state):
        super().__init__(title, media_id, state)
        self.__return_period_days = 21  # 3 semaines pour un livre

    def borrow(self):
        self.__state = "borrowed"
        return f"Book '{self.__title}' borrowed"

    def return_media(self):
        self.__state = "available"
        return f"Book '{self.__title}' returned"

class CD(Media):
    def __init__(self, title, media_id, state):
        super().__init__(title, media_id, state)
        self.__return_period_days = 7  # 1 semaine pour un CD

    def borrow(self):
        self.__state = "borrowed"
        return f"CD '{self.__title}' borrowed"

    def return_media(self):
        self.__state = "available"
        return f"CD '{self.__title}' returned"

class Vinyl(Media):
    def __init__(self, title, media_id, state):
        super().__init__(title, media_id, state)
        self.__return_period_days = 7  # 1 semaine pour un Vinyl

    def borrow(self):
        self.__state = "borrowed"
        return f"Vinyl '{self.__title}' borrowed"

    def return_media(self):
        self.__state = "available"
        return f"Vinyl '{self.__title}' returned"
