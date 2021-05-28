import logging
from typing import Optional
import discord
from marvelous import services, models, settings
from marvelous.discord import cache, bot


logger = logging.getLogger(__name__)


def get_initial_model(user: discord.Member):
    return models.User(
        discord_id=user.id,
        display_name=user.display_name,
        marvelous_bonus=models.DailyBonus(step=0, today=0),
        booing_penalty=models.DailyBonus(step=0, today=0),
        super_marvelous_left=settings.super_marvelous.initial_left_count,
        survival_bonus_given=False,
        point=0,
    )


def is_exist(user_id: int) -> bool:
    state: Optional[cache.user.UserContext] = cache.user.memory.get_state(user_id)
    if state is not None:
        return state.registered
    state = update_cache(user_id)
    return state.registered


def update_cache(user_id: int) -> cache.user.UserContext:
    user = services.user.get_by_id(user_id)
    if user is None:
        state = cache.user.UserContext(registered=False)
    else:
        state = cache.user.UserContext(
            registered=True,
            survival_bonus_given=user.survival_bonus_given,
            sleeping=user.slept_at is not None
        )
    cache.user.memory.set_state(user_id, state)
    return state


def clear_cache() -> None:
    cache.user.memory.clear()


def get_status_message(user: models.User) -> str:
    marvelous_bonus_left = settings.marvelous.send_bonus.step_interval - user.marvelous_bonus.step
    booing_penalty_left = settings.booing.send_penalty.step_interval - user.booing_penalty.step
    today_marvelous_count = min(settings.marvelous.send_bonus.daily_step_limit, user.marvelous_bonus.today)
    today_booing_count = min(settings.booing.send_penalty.daily_step_limit, user.booing_penalty.today)
    return "\n".join([
        f"```",
        f"【{user.display_name}】",
        "累計 " + settings.message.marvelous_point_symbol + str(user.point),
        f"使用可能 {settings.super_marvelous.reaction}" + str(max(0, user.super_marvelous_left)),
        f"",
        (
            f":   {settings.marvelous.reaction}ボーナスまであと {settings.marvelous.reaction}{marvelous_bonus_left}  "
            f"（本日分カウント {today_marvelous_count}/{settings.marvelous.send_bonus.daily_step_limit}）"
        ),
        (
            f":   {settings.booing.reaction}ペナルティまであと {settings.booing.reaction}{booing_penalty_left}  "
            f"（本日分カウント {today_booing_count}/{settings.booing.send_penalty.daily_step_limit}）"
        ),
        f"",
        f"GitHub ID: {user.github_id if user.github_id is not None else '(未登録)'}"
        f"```"
    ])


def show_status(user: discord.Member, channel: discord.TextChannel):
    register_if_not_exist(user)

    try:
        result_user = services.user.get_by_id(user.id)
    except models.ModelError:
        logger.exception("An unknown exception raised while getting user.")
        return

    message = get_status_message(result_user)
    bot.message.sender.send(channel, content=message)


def register_if_not_exist(author: discord.Member):
    if is_exist(author.id):
        return
    try:
        user: models.User = get_initial_model(author)
        services.user.register(user)
        update_cache(user.discord_id)
    except models.ModelError:
        logger.exception("An unknown exception raised while registering user.")


def register_github(user: discord.Member, channel: discord.TextChannel, github_id: str):
    register_if_not_exist(user)

    try:
        services.github.register(user.id, github_id)
    except models.GitHubIDTooLongError as err:
        message = f":no_entry: GitHub IDが長すぎます。{err.max_length}文字以下の文字列を指定してください。"
        bot.message.sender.send(channel, content=message, force=True)
        return
    except models.GitHubUserNotFoundError as err:
        message = f":no_entry: GitHub ID({err.user_id})が存在しません。"
        bot.message.sender.send(channel, content=message, force=True)
        return
    except models.ModelError:
        logger.exception("An unknown exception raised while registering github id.")
        message = f":no_entry: GitHub ID({github_id})の登録に失敗しました。"
        bot.message.sender.send(channel, content=message, force=True)
        return

    message = f":white_check_mark: GitHub ID({github_id})を更新しました。"
    bot.message.sender.send(channel, content=message, force=True)


def unregister_github(user: discord.Member, channel: discord.TextChannel):
    register_if_not_exist(user)

    try:
        services.github.unregister(user.id)
    except models.GitHubNotRegisteredError:
        message = f":no_entry: GitHub IDは登録されていません。"
        bot.message.sender.send(channel, content=message, force=True)
        return
    except models.ModelError:
        logger.exception("An unknown exception raised while unregistering github id.")
        message = f":no_entry: GitHub IDの登録解除に失敗しました。"
        bot.message.sender.send(channel, content=message, force=True)
        return

    message = f":white_check_mark: GitHub IDの登録を解除しました。"
    bot.message.sender.send(channel, content=message)
