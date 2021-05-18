from discord.ext import commands
import discord
from logging import getLogger
from . import client
from marvelous.settings import app_settings

WEEKDAY_DISPLAY = ["月", "火", "水", "木", "金", "土", "日"]

logger = getLogger(__name__)
help_text = (
    "各ユーザーの 👏えらいポイント を管理するbotです。\n"
    "\n"
    f"👏えらいポイント は、毎週{WEEKDAY_DISPLAY[app_settings.user.reset_marvelous_point_weekday]}曜"
    f"{app_settings.user.reset_marvelous_point_time.strftime('%H:%M')}にリセットされます。\n"
    "このとき、ポイントを多く集めた人を表彰します。たくさんポイントを集められるようにがんばりましょう！\n"
    "\n"
    "他のユーザーのメッセージに以下のリアクションを付けると、アクションが可能です。\n"
    "```md\n"
    f"{app_settings.marvelous.reaction} 「えらい！」を送る\n"
    f"    - 相手に👏{'{:+}'.format(app_settings.marvelous.receive_point)}\n"
    f"    - 同じメッセージに何個か{app_settings.marvelous.reaction}が付くと...？\n"
    f"{app_settings.booing.reaction} 「カス！」を送る\n"
    f"    - 相手に👏{'{:+}'.format(app_settings.booing.receive_point)}\n"
    f"    - 同じメッセージに何個か{app_settings.booing.reaction}が付くと...？\n"
    f"{app_settings.super_marvelous.reaction} 「めっちゃえらい！」を送る\n"
    f"    - 相手に👏{'{:+}'.format(app_settings.super_marvelous.receive_point)}\n"
    f"    - 自分に👏{'{:+}'.format(app_settings.super_marvelous.send_point)}\n"
    f"    - 各ユーザー、1週間に{app_settings.super_marvelous.initial_left_count}回まで"
    f"（毎週{WEEKDAY_DISPLAY[app_settings.super_marvelous.reset_weekday]}曜"
    f"{app_settings.super_marvelous.reset_time.strftime('%H:%M')}に回数リセット、残り回数は !erai me で確認可能）\n"
    "```\n"
    "\n"
    "その他、以下のアクションによって 👏えらいポイント が変動します。\n"
    "```md\n"
    "その日最初のメッセージを送る\n"
    f"    - 自分に👏{'{:+}'.format(app_settings.survival.point)}\n"
    f"「えらい！」を{app_settings.marvelous.send_bonus.step_interval}回送る"
    f"（{app_settings.marvelous.send_bonus.daily_step_limit}カウント/日）\n"
    f"    - 自分に👏{'{:+}'.format(app_settings.marvelous.send_bonus.point)}\n"
    f"「カス！」を{app_settings.booing.send_penalty.step_interval}回送る"
    f"（{app_settings.booing.send_penalty.daily_step_limit}カウント/日）\n"
    f"    - 自分に👏{'{:+}'.format(app_settings.booing.send_penalty.point)}\n"
    "```\n"
    "\n"
    "【コマンド一覧】\n"
    "`!erai me`      : 自分のステータスを表示する\n"
    "`!erai ranking` : えらいポイントのランキングを表示する\n"
    "`!erai help`    : ヘルプを表示する\n"
    "\n"
    "【開発者】\n"
    "Rinia\n"
    "【開発ソース】\n"
    "https://github.com/watano1168/marvelous\n"
    "【問題点・改善案は、こちらから報告をお願いします】\n"
    "https://github.com/watano1168/marvelous/issues"
)


def get_help_embed() -> discord.Embed:
    return discord.Embed(title="ヘルプ", description=help_text, color=0x00ff00)


async def show_help_on_mention(message: discord.Message):
    if client.bot.user not in message.mentions:
        return
    await show_help(message)


async def show_help(message: discord.Message):
    author: discord.User = message.author
    if author is None:
        return
    try:
        await author.send(embed=get_help_embed())
    except discord.Forbidden:
        channel: discord.TextChannel = message.channel
        if channel is None or not isinstance(channel, discord.TextChannel):
            return
        await channel.send(embed=get_help_embed())
    except Exception as err:
        logger.error(str(err))


class MarvelousHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = ""
        self.command_attrs["help"] = "コマンド一覧とヘルプを表示する"
        self.dm_help = True

    def get_ending_note(self):
        return ""

    async def send_bot_help(self, mapping):
        ctx: commands.Context = self.context
        if ctx is None:
            return
        await show_help(ctx.message)

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


