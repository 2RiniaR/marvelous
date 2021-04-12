import marvelous.data_store as data_store


def reset_super_marvelous_left(count: int) -> None:
    """「めっちゃえらい」の残り使用可能回数をリセットする"""
    data_store.users.reset_super_marvelous_left(count)
