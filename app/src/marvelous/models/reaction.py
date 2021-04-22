from .user import User, get_user
import marvelous.data_store as data_store
from .errors import SelfUserReactionError


class Reaction:
    def send(self, sender: User, receiver: User):
        pass

    def cancel(self, sender: User, receiver: User):
        pass


def check_self_user(sender_id: int, receiver_id: int):
    if sender_id == receiver_id:
        raise SelfUserReactionError(sender_id)


def update_reaction(sender_id: int, receiver_id: int, reaction: Reaction, forward: bool):
    check_self_user(sender_id, receiver_id)
    sender = get_user(sender_id)
    receiver = get_user(receiver_id)

    if forward:
        reaction.send(sender, receiver)
    else:
        reaction.cancel(sender, receiver)

    data_store.users.update_user(sender)
    data_store.users.update_user(receiver)


def send_reaction(sender_id: int, receiver_id: int, reaction: Reaction):
    """リアクションを送信する"""
    update_reaction(sender_id, receiver_id, reaction, True)


def cancel_reaction(sender_id: int, receiver_id: int, reaction: Reaction):
    """リアクションの送信をキャンセルする"""
    update_reaction(sender_id, receiver_id, reaction, False)
