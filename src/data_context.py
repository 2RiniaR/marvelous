from repository import Repository
from logger import Logger
from user import User


class DataContext:
    repository: Repository
    logger: Logger

    def __init__(self, repository: Repository, logger: Logger):
        self.repository = repository
        self.logger = logger

    def create_user(self, discord_id: str):
        self.repository.create_user(discord_id)

    def send_marvelous(self, sender_id: str, target_id: str):
        sender: User = self.repository.get_user(sender_id)
        target: User = self.repository.get_user(target_id)
        sender.send_marvelous()
        target.receive_marvelous()
        self.repository.update_user(sender)
        self.repository.update_user(target)

    def send_boo(self, sender_id: str, target_id: str):
        sender: User = self.repository.get_user(sender_id)
        target: User = self.repository.get_user(target_id)
        sender.send_boo()
        target.receive_boo()
        self.repository.update_user(sender)
        self.repository.update_user(target)

    def send_super_marvelous(self, sender_id: str, target_id: str):
        sender: User = self.repository.get_user(sender_id)
        target: User = self.repository.get_user(target_id)
        succeed, error = sender.send_marvelous()
        if succeed:
            target.receive_marvelous()
        self.repository.update_user(sender)
        self.repository.update_user(target)
