from app.config import database
from .repository.repository import BirthdayRepository


class Service:
    def __init__(self):
        self.repository = BirthdayRepository(database)


def get_service():
    svc = Service()
    return svc
