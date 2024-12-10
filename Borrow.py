from datetime import date, timedelta, datetime

from Media import Book


class Borrow:
    def __init__(self, borrow_date, return_date, media, user):
        self._borrow_date = borrow_date
        self._return_date = return_date
        self._media = media
        self._user = user

    def to_dict(self):
        return {
            "borrow_date": self._borrow_date.isoformat(),  # Convert date to string for YAML
            "return_date": self._return_date.isoformat() if self._return_date else None,
            "media_id": self._media.id,  # Assuming media has an ID
            "user_id": self._user._user_id,  # Assuming user has an ID
        }

    @property
    def due_date(self):
        days = 7  # Default for CD and Vinyl
        if isinstance(self._media, Book):
            days = 21
        return self._borrow_date + timedelta(days=days)

    def is_overdue(self):
        today = date.today()  # Get today's date
        due_date = self.due_date.date() if isinstance(self.due_date, datetime) else self.due_date
        return today >= due_date

    @property
    def media(self):
        return self._media

    @property
    def user(self):
        return self._user

    def __str__(self):
        return f"User: {self._user._login}, Media: {self._media.title}, Borrowed on: {self._borrow_date}, Due on: {self.due_date}"

