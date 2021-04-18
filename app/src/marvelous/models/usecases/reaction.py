import marvelous.data_store as data_store
from .user import get_user
from ..events.reaction import Reaction
from ..errors import SelfUserReactionError


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
