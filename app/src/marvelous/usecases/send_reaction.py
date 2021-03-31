import marvelous.data_store as data_store
from marvelous.usecases.get_user import get_user
from marvelous.models.reaction import Reaction


class SelfUserActionError(Exception):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"同一のユーザー間でアクションを送受信しました。(ID: {self.user_id})"


def check_self_user(sender_id: int, receiver_id: int):
    if sender_id == receiver_id:
        raise SelfUserActionError(sender_id)


def update_reaction(sender_id: int, receiver_id: int, reaction: Reaction, forward: bool):
    """リアクションを送信する"""
    check_self_user(sender_id, receiver_id)
    sender = get_user(sender_id)
    receiver = get_user(receiver_id)

    if forward:
        reaction.send(sender, receiver)
    else:
        reaction.cancel(sender, receiver)

    data_store.users.update(sender)
    data_store.users.update(receiver)


def send_reaction(sender_id: int, receiver_id: int, reaction: Reaction):
    update_reaction(sender_id, receiver_id, reaction, True)


def cancel_reaction(sender_id: int, receiver_id: int, reaction: Reaction):
    update_reaction(sender_id, receiver_id, reaction, False)
