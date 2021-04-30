class ModelError(Exception):
    pass


class DataUpdateError(ModelError):
    pass


class DataFetchError(ModelError):
    pass


class CalculateError(ModelError):
    pass


class UserNotFoundError(ModelError):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"The user(id={self.user_id}) was not found."


class SelfUserReactionError(ModelError):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"The user(id={self.user_id}) tried to reaction to self. Skipped to update."


class AlreadyExistError(ModelError):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"The user(id={self.user_id}) already exist. Skipped to register."
