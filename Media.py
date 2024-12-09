from abc import abstractmethod, ABC


class Media(ABC):
    def __init__(self, title, id, state):
        self.__return_period_days = 7
        self.__title = title
        self.__id = id
        self.__state = state

    @abstractmethod
    def borrow(self):
        pass

    @abstractmethod
    def return_media(self):
        pass

class Book(Media):
    def __init__(self, title, id, state):
        super().__init__(title, id, state)
        self.__return_period_days = 21

    def borrow(self):
        return f"Livre '{self.__title}' borrowed"

    def return_media(self):
        return f"Livre '{self.__title}' returned"

class CD(Media):
    def borrow(self):
        return f"CD '{self._Media__title}' borrowed"

    def return_media(self):
        return f"CD '{self._Media__title}' returned"

class Vinyl(Media):
    def borrow(self):
        return f"Vinyle '{self._Media__title}' borrowed"

    def return_media(self):
        return f"Vinyle '{self._Media__title}' returned"

