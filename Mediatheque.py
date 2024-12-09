# Mediatheque class

class Mediatheque:
    def __init__(self):
        self.__history = []
        self.__users = []
        self.__media = []

    @property
    def history(self):
        return self.__history

    @property
    def users(self):
        return self.__users

    @property
    def media(self):
        return self.__media

    def check_history(self, targetId):
        return self.__history

    def warn_users(self, targetId):
        warnings = []
        for borrow in self.__history:
            if borrow.is_overdue():
                warnings.append(f"User {borrow.user.login} has overdue media: {borrow.media.title}")
        return warnings

    def return_media(self, borrow):
        if borrow in self.__history:
            self.__history.remove(borrow)
            return f"Media {borrow.media.title} returned by {borrow.user.login}"
        return "Borrow record not found"

    def register_person(self, person):
        self.__users.append(person)
        return f"Person {person.login} registered"

    def add_media(self, media):
        self.__media.append(media)
        return f"Media {media.title} added"



