from abc import *
from user import User


class Repository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_user(self, discord_id: str):
        raise NotImplementedError()

    @abstractmethod
    def create_user(self, discord_id: str):
        raise NotImplementedError()

    @abstractmethod
    def update_user(self, user: User):
        raise NotImplementedError()

    @abstractmethod
    def delete_user(self, discord_id: str):
        raise NotImplementedError()
