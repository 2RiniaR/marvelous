from marvelous import models, services, db


def check_self_user(sender_id: int, receiver_id: int):
    if sender_id == receiver_id:
        raise models.SelfUserReactionError(sender_id)


def update(sender_id: int, receiver_id: int, reaction: models.Reaction, forward: bool):
    check_self_user(sender_id, receiver_id)

    try:
        sender = services.user.get_by_id(sender_id)
        receiver = services.user.get_by_id(receiver_id)
    except Exception as err:
        raise models.DataFetchError from err

    if sender is None:
        raise models.UserNotFoundError(sender_id)
    if receiver is None:
        raise models.UserNotFoundError(receiver_id)

    try:
        if forward:
            reaction.send(sender, receiver)
        else:
            reaction.cancel(sender, receiver)
    except Exception as err:
        raise models.CalculateError from err

    services.user.update(sender)
    services.user.update(receiver)


def send(sender_id: int, receiver_id: int, reaction: models.Reaction):
    """リアクションを送信する"""
    update(sender_id, receiver_id, reaction, True)


def cancel(sender_id: int, receiver_id: int, reaction: models.Reaction):
    """リアクションの送信をキャンセルする"""
    update(sender_id, receiver_id, reaction, False)
