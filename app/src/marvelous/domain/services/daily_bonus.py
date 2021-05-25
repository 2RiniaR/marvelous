import marvelous.db as db


def reset() -> None:
    """デイリーボーナスをリセットする"""
    db.users.reset_daily_steps()
