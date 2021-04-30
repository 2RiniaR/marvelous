from .execute import commit


def delete_user_by_id(discord_id: str) -> None:
    query = "DELETE FROM users WHERE discord_id = %(discord_id)s"
    params = {"discord_id": discord_id}
    commit(query, params)
