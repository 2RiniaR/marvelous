import marvelous.data_store as data_store


def reset_survival_bonus() -> None:
    """「生きててえらいボーナス」をリセットする"""
    data_store.users.reset_survival_bonus()
