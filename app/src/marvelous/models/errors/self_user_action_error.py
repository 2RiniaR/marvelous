class SelfUserReactionError(Exception):
    user_id: int

    def __init__(self, user_id: int):
        self.user_id = user_id

    def __str__(self):
        return f"The user(id={self.user_id}) tried to reaction to self. Skipped to update."
