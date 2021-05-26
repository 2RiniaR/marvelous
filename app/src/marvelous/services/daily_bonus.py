from marvelous import db


def reset() -> None:
    """デイリーボーナスをリセットする"""
    db.users.reset_daily_steps()
