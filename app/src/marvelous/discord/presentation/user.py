import logging
from typing import List, Optional
import discord
from marvelous.domain import models, services
import marvelous.discord.bot as bot
import marvelous.settings as settings
import marvelous.helpers as helpers
from marvelous.discord.cahce import user_cache, UserContext
from .ranking import get_ranking


logger = logging.getLogger(__name__)


def get_initial_user(user: discord.Member):
    return models.User(
        discord_id=user.id,
        display_name=user.display_name,
        marvelous_bonus=models.DailyBonus(step=0, today=0),
        booing_penalty=models.DailyBonus(step=0, today=0),
        super_marvelous_left=settings.super_marvelous.initial_left_count,
        survival_bonus_given=False,
        point=0,
    )


def is_user_exist(user_id: int) -> bool:
    state: Optional[UserContext] = user_cache.get_state(user_id)
    if state is not None:
        return state.registered
    state = update_user_cache(user_id)
    return state.registered


def update_user_cache(user_id: int) -> UserContext:
    user = services.get_user_by_id(user_id)
    if user is None:
        state = UserContext(registered=False, survival_bonus_given=False)
    else:
        state = UserContext(registered=True, survival_bonus_given=user.survival_bonus_given)
    user_cache.set_state(user_id, state)
    return state


def clear_user_cache() -> None:
    user_cache.clear()


def get_status_message(user: models.User) -> str:
    marvelous_bonus_left = settings.marvelous.send_bonus.step_interval - user.marvelous_bonus.step
    booing_penalty_left = settings.booing.send_penalty.step_interval - user.booing_penalty.step
    today_marvelous_count = min(settings.marvelous.send_bonus.daily_step_limit, user.marvelous_bonus.today)
    today_booing_count = min(settings.booing.send_penalty.daily_step_limit, user.booing_penalty.today)
    return "\n".join([
        f"```",
        f"【{user.display_name}】",
        "累計 👏" + str(user.point),
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


async def show_status(user: discord.Member, channel: discord.TextChannel):
    await register_user_implicit(user)

    try:
        result_user = services.get_user_by_id(user.id)
    except models.ModelError:
        logger.exception("An unknown exception raised while getting user.")
        return

    message = get_status_message(result_user)
    await bot.message_gateway.send(channel, content=message)


async def register_user_implicit(author: discord.Member):
    if is_user_exist(author.id):
        return
    try:
        user: models.User = get_initial_user(author)
        services.register_user(user)
        update_user_cache(user.discord_id)
    except models.ModelError:
        logger.exception("An unknown exception raised while registering user.")


async def check_reset_marvelous_point():
    reset_time = settings.user.reset_marvelous_point_time
    reset_weekday = settings.user.reset_marvelous_point_weekday
    if not (helpers.is_now_time(reset_time) and helpers.is_now_weekday(reset_weekday)):
        return
    await run_reset_marvelous_point()


def get_weekly_message(ranking: List[models.User]) -> str:
    def get_user_column(index: int, user: models.User) -> str:
        return f"#{str(index + 1).zfill(2)} - {f'👏{user.point}'.rjust(4)}  {user.display_name}"

    if len(ranking) == 0:
        return ""

    ranking_text = "\n".join(map(lambda x: get_user_column(x[0], x[1]), enumerate(ranking[:5])))

    return (
        f"👑今週、一番えらかったのは...  **{str(ranking[0].display_name)}**\n"
        "\n"
        "```\n"
        "【ランキング上位】\n"
        f"{ranking_text}"
        "```\n"
        "今週もよく頑張ったね。みんなえらい！\n"
        "\n"
        f"「{settings.super_marvelous.reaction} めっちゃえらい！」の使用回数をリセットしました。\n"
        f"えらいポイントをリセットしました。今週も頑張ろう！"
    )


async def send_weekly_message():
    users = get_ranking()
    message = get_weekly_message(list(users))
    embed = discord.Embed(title="今週のえらい", description=message, color=0xe8b77b)
    await bot.message_gateway.send_to_default_channel(embed=embed, force=True)


async def run_reset_marvelous_point():
    await send_weekly_message()
    try:
        services.reset_marvelous_point()
    except models.ModelError:
        logger.exception("An unknown exception raised while resetting marvelous point.")
        return


async def register_github(user: discord.Member, channel: discord.TextChannel, github_id: str):
    await register_user_implicit(user)

    try:
        services.register_github(user.id, github_id)
    except models.GitHubIDTooLongError as err:
        message = f":no_entry: GitHub IDが長すぎます。{err.max_length}文字以下の文字列を指定してください。"
        await bot.message_gateway.send(channel, content=message, force=True)
        return
    except models.GitHubUserNotFoundError as err:
        message = f":no_entry: GitHub ID({err.user_id})が存在しません。"
        await bot.message_gateway.send(channel, content=message, force=True)
        return
    except models.ModelError:
        logger.exception("An unknown exception raised while registering github id.")
        message = f":no_entry: GitHub ID({github_id})の登録に失敗しました。"
        await bot.message_gateway.send(channel, content=message, force=True)
        return

    message = f":white_check_mark: GitHub ID({github_id})を更新しました。"
    await bot.message_gateway.send(channel, content=message, force=True)


async def unregister_github(user: discord.Member, channel: discord.TextChannel):
    await register_user_implicit(user)

    try:
        services.unregister_github(user.id)
    except models.GitHubNotRegisteredError:
        message = f":no_entry: GitHub IDは登録されていません。"
        await bot.message_gateway.send(channel, content=message, force=True)
        return
    except models.ModelError:
        logger.exception("An unknown exception raised while unregistering github id.")
        message = f":no_entry: GitHub IDの登録解除に失敗しました。"
        await bot.message_gateway.send(channel, content=message, force=True)
        return

    message = f":white_check_mark: GitHub IDの登録を解除しました。"
    await bot.message_gateway.send(channel, content=message)
