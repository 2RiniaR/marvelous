from marvelous.models.user import User
from marvelous.models.reaction.reaction import Reaction
from dataclasses import dataclass


@dataclass()
class MarvelousSettings:
    daily_step_limit: int
    steps_per_bonus: int
    sender_bonus_point: int
    receiver_point: int


@dataclass()
class MarvelousResult:
    sender_bonus_diff: int
    sender_point_diff: int
    receiver_point_diff: int


class MarvelousReaction(Reaction):
    settings: MarvelousSettings
    result: MarvelousResult

    def __init__(self, settings: MarvelousSettings):
        self.settings = settings

    def send(self, sender: User, receiver: User):
        sender_point_before = sender.point
        receiver_point_before = receiver.point

        bonus = sender.marvelous_bonus.add_step(
            step=1,
            today_limit=self.settings.daily_step_limit,
            step_interval=self.settings.steps_per_bonus
        )
        sender.point += self.settings.sender_bonus_point * bonus
        receiver.point += self.settings.receiver_point

        self.result = MarvelousResult(
            sender_bonus_diff=bonus,
            sender_point_diff=sender.point - sender_point_before,
            receiver_point_diff=receiver.point - receiver_point_before
        )

    def cancel(self, sender: User, receiver: User):
        sender_point_before = sender.point
        receiver_point_before = receiver.point

        bonus = sender.marvelous_bonus.add_step(
            step=-1,
            today_limit=self.settings.daily_step_limit,
            step_interval=self.settings.steps_per_bonus
        )
        sender.point += self.settings.sender_bonus_point * bonus
        receiver.point -= self.settings.receiver_point

        self.result = MarvelousResult(
            sender_bonus_diff=bonus,
            sender_point_diff=sender.point - sender_point_before,
            receiver_point_diff=receiver.point - receiver_point_before
        )
