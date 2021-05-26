from marvelous import models, github, db, services


def register(discord_id: int, github_id: str) -> None:
    """ユーザーのGitHub IDを登録する"""
    max_github_id_length = 39
    user: models.User = services.user.get_by_id(discord_id)
    if user is None:
        raise models.UserNotFoundError(discord_id)

    if len(github_id) > max_github_id_length:
        raise models.GitHubIDTooLongError(max_github_id_length, len(github_id))
    if not github.account.is_exist(github_id):
        raise models.GitHubUserNotFoundError(github_id)

    user.github_id = github_id

    try:
        db.users.update(user)
    except Exception as err:
        raise models.DataUpdateError from err


def unregister(discord_id: int) -> None:
    """ユーザーのGitHub IDの登録を解除する"""
    user: models.User = services.user.get_by_id(discord_id)
    if user is None:
        raise models.UserNotFoundError(discord_id)
    if user.github_id is None:
        raise models.GitHubNotRegisteredError(discord_id)

    user.github_id = None

    try:
        db.users.update(user)
    except Exception as err:
        raise models.DataUpdateError from err
