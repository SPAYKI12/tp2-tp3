class Mediatheque:
    def __init__(self):
        self.__users = []
        self.__media = []
        self.__history = []

    def add_media(self, media):
        self.__media.append(media)

    def register_person(self, person):
        self.__users.append(person)

    def get_overdue_users(self):
        overdue_users = []
        for borrow in self.__history:
            if borrow.is_overdue():
                overdue_users.append(borrow)
        return overdue_users

    def record_borrow(self, borrow):
        self.__history.append(borrow)

    def return_media(self, borrow):
        self.__history.remove(borrow)
