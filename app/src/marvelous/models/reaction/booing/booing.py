from marvelous.models.user import User
from marvelous.models.reaction.reaction import Reaction
from dataclasses import dataclass


@dataclass()
class BooingSettings:
    daily_step_limit: int
    steps_per_bonus: int
    sender_bonus_point: int
    receiver_point: int


@dataclass()
class BooingResult:
    sender_penalty_diff: int
    sender_point_diff: int
    receiver_point_diff: int


class BooingReaction(Reaction):
    settings: BooingSettings
    result: BooingResult

    def __init__(self, settings: BooingSettings):
        self.settings = settings

    def send(self, sender: User, receiver: User):
        sender_point_before = sender.point
        receiver_point_before = receiver.point

        penalty = sender.booing_penalty.add_step(
            step=1,
            today_limit=self.settings.daily_step_limit,
            step_interval=self.settings.steps_per_bonus
        )
        sender.point += self.settings.sender_bonus_point * penalty
        receiver.point += self.settings.receiver_point

        self.result = BooingResult(
            sender_penalty_diff=penalty,
            sender_point_diff=sender.point - sender_point_before,
            receiver_point_diff=receiver.point - receiver_point_before
        )

    def cancel(self, sender: User, receiver: User):
        sender_point_before = sender.point
        receiver_point_before = receiver.point

        penalty = sender.booing_penalty.add_step(
            step=-1,
            today_limit=self.settings.daily_step_limit,
            step_interval=self.settings.steps_per_bonus
        )
        receiver.point -= self.settings.receiver_point
        sender.point += self.settings.sender_bonus_point * penalty

        self.result = BooingResult(
            sender_penalty_diff=penalty,
            sender_point_diff=sender.point - sender_point_before,
            receiver_point_diff=receiver.point - receiver_point_before
        )
