from abc import abstractmethod, ABC


class Media(ABC):
    def __init__(self, title, id, state, return_period_days=7):
        self.__return_period_days = return_period_days
        self.__title = title
        self.__id = id
        self.__state = state

    @abstractmethod
    def borrow(self):
        pass

    @abstractmethod
    def return_media(self):
        pass

class Livre(Media):
    def borrow(self):
        return f"Livre '{self.__title}' borrowed"

    def return_media(self):
        return f"Livre '{self.__title}' returned"

class CD(Media):
    def borrow(self):
        return f"CD '{self._Media__title}' borrowed"

    def return_media(self):
        return f"CD '{self._Media__title}' returned"

class Vinyles(Media):
    def borrow(self):
        return f"Vinyle '{self._Media__title}' borrowed"

    def return_media(self):
        return f"Vinyle '{self._Media__title}' returned"

# Borrow class
class Borrow:
    def __init__(self, borrow_date, return_date, media, user, attribute):
        self.__borrow_date = borrow_date
        self.__return_date = return_date
        self.__media = media
        self.__user = user
        self.__attribute = attribute

    def is_overdue(self):
        return date.today() > self.__return_date

# Mediatheque class
class Mediatheque:
    def __init__(self):
        self.__history = []
        self.__users = []
        self.__media = []

    def check_history(self):
        return self.__history

    def warn_users(self):
        warnings = []
        for borrow in self.__history:
            if borrow.is_overdue():
                warnings.append(f"User {borrow._Borrow__user._Person__login} has overdue media: {borrow._Borrow__media._Media__title}")
        return warnings

    def return_media(self, borrow):
        if borrow in self.__history:
            self.__history.remove(borrow)
            return f"Media {borrow._Borrow__media._Media__title} returned by {borrow._Borrow__user._Person__login}"
        return "Borrow record not found"

    def register_person(self, person):
        self.__users.append(person)
        return f"Person {person._Person__login} registered"