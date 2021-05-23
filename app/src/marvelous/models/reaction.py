from .user import User, get_user
import marvelous.data_store as data_store
from .errors import SelfUserReactionError, DataFetchError, CalculateError, DataUpdateError, UserNotFoundError


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

    try:
        sender = get_user(sender_id)
        receiver = get_user(receiver_id)
    except Exception as err:
        raise DataFetchError from err

    if sender is None:
        raise UserNotFoundError(sender_id)
    if receiver is None:
        raise UserNotFoundError(receiver_id)

    try:
        if forward:
            reaction.send(sender, receiver)
        else:
            reaction.cancel(sender, receiver)
    except Exception as err:
        raise CalculateError from err

    try:
        data_store.users.update(sender)
        data_store.users.update(receiver)
    except Exception as err:
        raise DataUpdateError from err


def send_reaction(sender_id: int, receiver_id: int, reaction: Reaction):
    """リアクションを送信する"""
    update_reaction(sender_id, receiver_id, reaction, True)


def cancel_reaction(sender_id: int, receiver_id: int, reaction: Reaction):
    """リアクションの送信をキャンセルする"""
    update_reaction(sender_id, receiver_id, reaction, False)
