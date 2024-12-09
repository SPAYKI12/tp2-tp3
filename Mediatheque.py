# Mediatheque class
from Person import Administrator


class Mediatheque:
    def __init__(self):
        self.__history = []
        self.__users = []
        self    .__media = []

    def check_history(self, targetId):
        return self.__history

    def warn_users(self, targetId):
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