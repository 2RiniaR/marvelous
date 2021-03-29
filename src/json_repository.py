from user import User
import json
from repository import Repository

KEY_DISCORD_ID = "discord_id"
KEY_TWITTER_ID = "twitter_id"
KEY_GITHUB_ID = "github_id"
KEY_MARVELOUS = "marvelous"
KEY_SENT_MARVELOUS_COUNT = "sent_marvelous_count"
KEY_TODAY_SENT_MARVELOUS_BONUS_COUNT = "today_sent_marvelous_bonus_count"
KEY_SENT_BOO_COUNT = "sent_boo_count"
KEY_TODAY_SENT_BOO_BONUS_COUNT = "today_sent_boo_bonus_count"
KEY_SLEEPING = "sleeping"
KEY_SUPER_MARVELOUS_LEFT_COUNT = "super_marvelous_left_count"


def get_user_index(discord_id: str, users):
    target_user_indices = [i for i, u in enumerate(users) if u[KEY_DISCORD_ID] == discord_id]
    return target_user_indices[0] if len(target_user_indices) > 0 else -1


def user_to_dict(user: User):
    return {
        KEY_DISCORD_ID: user.discord_id,
        KEY_TWITTER_ID: user.twitter_id,
        KEY_GITHUB_ID: user.github_id,
        KEY_MARVELOUS: user.marvelous,
        KEY_SENT_MARVELOUS_COUNT: user.sent_marvelous_count,
        KEY_TODAY_SENT_MARVELOUS_BONUS_COUNT: user.today_sent_marvelous_bonus_count,
        KEY_SENT_BOO_COUNT: user.sent_boo_count,
        KEY_TODAY_SENT_BOO_BONUS_COUNT: user.today_sent_boo_bonus_count,
        KEY_SLEEPING: user.sleeping,
        KEY_SUPER_MARVELOUS_LEFT_COUNT: user.super_marvelous_left_count,
    }


def dict_to_user(dictionary) -> User:
    return User(
        discord_id=dictionary[KEY_DISCORD_ID],
        twitter_id=dictionary[KEY_TWITTER_ID],
        github_id=dictionary[KEY_GITHUB_ID],
        marvelous=dictionary[KEY_MARVELOUS],
        sent_marvelous_count=dictionary[KEY_SENT_MARVELOUS_COUNT],
        today_sent_marvelous_bonus_count=dictionary[KEY_TODAY_SENT_MARVELOUS_BONUS_COUNT],
        sent_boo_count=dictionary[KEY_SENT_BOO_COUNT],
        today_sent_boo_bonus_count=dictionary[KEY_TODAY_SENT_BOO_BONUS_COUNT],
        sleeping=dictionary[KEY_SLEEPING],
        super_marvelous_left_count=dictionary[KEY_SUPER_MARVELOUS_LEFT_COUNT]
    )


class JsonRepository(Repository):
    filepath: str

    def __init__(self, filepath: str):
        self.filepath = filepath

    def get_user(self, discord_id: str):
        with open(self.filepath, 'r') as f:
            users = json.load(f)

        target_user = next((user for user in users if user[KEY_DISCORD_ID] == discord_id), None)
        if target_user is None:
            return None

        return dict_to_user(target_user)

    def create_user(self, discord_id: str):
        with open(self.filepath, 'r') as f:
            users = json.load(f)

        target_user = next((user for user in users if user[KEY_DISCORD_ID] == discord_id), None)
        if target_user is not None:
            return None

        new_user = User(discord_id=discord_id)
        users.append(user_to_dict(new_user))

        with open(self.filepath, 'w') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

    def update_user(self, user: User):
        with open(self.filepath, 'r') as f:
            users = json.load(f)

        target_user_index = get_user_index(user.discord_id, users)
        if target_user_index < 0:
            return

        users[target_user_index] = user_to_dict(user)

        with open(self.filepath, 'w') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

    def delete_user(self, discord_id: str):
        with open(self.filepath, 'r') as f:
            users = json.load(f)

        target_user_index = get_user_index(discord_id, users)
        if target_user_index < 0:
            return

        users.pop(target_user_index)
        with open(self.filepath, 'w') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
