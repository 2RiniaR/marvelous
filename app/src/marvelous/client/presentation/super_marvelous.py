from marvelous.models.super_marvelous import reset_super_marvelous_left, SuperMarvelousReaction
from marvelous.settings import app_settings
from marvelous.helpers import is_now_time, is_now_weekday
from ..discord.reaction import ReactionEvent
from ..discord import message_gateway


async def response_super_marvelous(event: ReactionEvent, reaction: SuperMarvelousReaction):
    if reaction.result.no_left_count:
        message = f":no_entry: {event.sender.name}    <<<    「めっちゃえらい！」の残り使用回数が0です"
    else:
        message = (
            f"{event.sender.display_name}    >>>    "
            f"{':raised_hands:    ' * 3}"
            f"**{str(event.receiver.name)}**"
            f"{'    :raised_hands:' * 3}"
        )
    await message_gateway.send(message, event.channel)


def check_reset_super_marvelous_left():
    reset_time = app_settings.super_marvelous.reset_time
    reset_weekday = app_settings.super_marvelous.reset_weekday
    if is_now_time(reset_time) and is_now_weekday(reset_weekday):
        reset_super_marvelous_left(app_settings.super_marvelous.initial_left_count)
