import unittest

from Gestion import MessageManager, Gestion
from Mediatheque import Mediatheque

if __name__ == '__main__':
    mediatheque = Mediatheque()
    message_manager = MessageManager()
    gestion = Gestion(mediatheque, message_manager)
    gestion.run()
