import marvelous.data_store as data_store


def reset_daily_steps() -> None:
    """デイリーボーナスをリセットする"""
    data_store.users.reset_daily_steps()
