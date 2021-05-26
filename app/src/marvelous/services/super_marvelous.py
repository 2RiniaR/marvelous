from marvelous import db, models


def reset_left_count(count: int) -> None:
    """「めっちゃえらい」の残り使用可能回数をリセットする"""
    try:
        db.users.reset_super_marvelous_left(count)
    except Exception as err:
        raise models.DataUpdateError from err
