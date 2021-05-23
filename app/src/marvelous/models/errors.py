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


class GitHubIDTooLongError(ModelError):
    max_length: int
    actual_length: int

    def __init__(self, max_length: int, actual_length: int):
        self.max_length = max_length
        self.actual_length = actual_length

    def __str__(self):
        return f"Length of the GitHub user id was too long. ({self.actual_length} > {self.max_length})"


class GitHubUserNotFoundError(ModelError):
    user_id: str

    def __init__(self, user_id: str):
        self.user_id = user_id

    def __str__(self):
        return f"The GitHub user(id={self.user_id}) was not found."
