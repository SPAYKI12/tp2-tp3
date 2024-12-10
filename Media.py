from abc import ABC, abstractmethod
from datetime import date, timedelta


class Media(ABC):
    def __init__(self, title, id, state, author):
        self._title = title
        self._id = id
        self._state = state
        self._author = author

    def to_json(self):
        return {
            "title": self._title,
            "id": self._id,
            "state": self._state,
            "author": self._author
        }

    @classmethod
    def from_json(cls, data):
        return cls(data["title"], data["id"], data["state"])

    @property
    def title(self):
        return self._title

    @property
    def id(self):
        return self._id

    @property
    def state(self):
        return self._state

    @abstractmethod
    def borrow(self):
        pass

    @abstractmethod
    def return_media(self):
        pass


class Book(Media):
    def __init__(self, title, id, state, author):
        super().__init__(title, id, state, author)

    def borrow(self):
        self._state = "borrowed"
        return f"Book '{self._title}' borrowed"

    def return_media(self):
        self._state = "available"
        return f"Book '{self._title}' returned"


class Cd(Media):
    def __init__(self, title, id, state, author):
        super().__init__(title, id, state, author)

    def borrow(self):
        self.__state = "borrowed"
        return f"CD '{self._title}' borrowed"

    def return_media(self):
        self.__state = "available"
        return f"CD '{self._title}' returned"


class Vinyl(Media):
    def __init__(self, title, id, state, author):
        super().__init__(title, id, state, author)

    def borrow(self):
        self.__state = "borrowed"
        return f"Vinyl '{self._title}' borrowed"

    def return_media(self):
        self.__state = "available"
        return f"Vinyl '{self._title}' returned"
