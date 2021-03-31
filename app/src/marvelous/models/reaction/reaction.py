from marvelous.models.user import User


class Reaction:
    def send(self, sender: User, receiver: User):
        pass

    def cancel(self, sender: User, receiver: User):
        pass
