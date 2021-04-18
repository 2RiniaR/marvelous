from dataclasses import dataclass
from ...entities import User
from .reaction import Reaction


def left_count_is_enough(user: User) -> bool:
    return user.super_marvelous_left > 0


@dataclass()
class SuperMarvelousSettings:
    sender_point: int
    receiver_point: int


@dataclass()
class SuperMarvelousResult:
    no_left_count: bool
    sender_point_diff: int
    receiver_point_diff: int


class SuperMarvelousReaction(Reaction):
    settings: SuperMarvelousSettings
    result: SuperMarvelousResult

    def __init__(self, settings: SuperMarvelousSettings):
        self.settings = settings

    def send(self, sender: User, receiver: User):
        if not left_count_is_enough(sender):
            sender.super_marvelous_left -= 1
            self.result = SuperMarvelousResult(no_left_count=True, sender_point_diff=0, receiver_point_diff=0)
            return

        sender.super_marvelous_left -= 1
        sender.point += self.settings.sender_point
        receiver.point += self.settings.receiver_point
        self.result = SuperMarvelousResult(
            no_left_count=False,
            sender_point_diff=self.settings.sender_point,
            receiver_point_diff=self.settings.receiver_point
        )

    def cancel(self, sender: User, receiver: User):
        sender.super_marvelous_left += 1
        if not left_count_is_enough(sender):
            self.result = SuperMarvelousResult(no_left_count=True, sender_point_diff=0, receiver_point_diff=0)
            return

        sender.point -= self.settings.sender_point
        receiver.point -= self.settings.receiver_point
        self.result = SuperMarvelousResult(
            no_left_count=False,
            sender_point_diff=-self.settings.sender_point,
            receiver_point_diff=-self.settings.receiver_point
        )
