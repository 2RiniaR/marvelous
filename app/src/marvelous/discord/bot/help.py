from discord.ext import commands
import discord
import logging
from marvelous import settings


WEEKDAY_DISPLAY = ["月", "火", "水", "木", "金", "土", "日"]
logger = logging.getLogger(__name__)
help_text = f"""
各ユーザーの 👏えらいポイント を管理するbotです。

👏えらいポイント は、毎週{WEEKDAY_DISPLAY[settings.user.reset_marvelous_point_weekday]}曜{settings.user.reset_marvelous_point_time.strftime('%H:%M')}にリセットされます。
このとき、ポイントを多く集めた人を表彰します。たくさんポイントを集められるようにがんばりましょう！

他のユーザーのメッセージに以下のリアクションを付けると、アクションが可能です。
```md
{settings.marvelous.reaction} 「えらい！」を送る
    - 相手に👏{'{:+}'.format(settings.marvelous.receive_point)}
    - 同じメッセージに何個か{settings.marvelous.reaction}が付くと...？
{settings.booing.reaction} 「カス！」を送る
    - 相手に👏{'{:+}'.format(settings.booing.receive_point)}
    - 同じメッセージに何個か{settings.booing.reaction}が付くと...？
{settings.super_marvelous.reaction} 「めっちゃえらい！」を送る
    - 相手に👏{'{:+}'.format(settings.super_marvelous.receive_point)}
    - 自分に👏{'{:+}'.format(settings.super_marvelous.send_point)}
    - 各ユーザー、1週間に{settings.super_marvelous.initial_left_count}回まで（毎週{WEEKDAY_DISPLAY[settings.super_marvelous.reset_weekday]}曜{settings.super_marvelous.reset_time.strftime('%H:%M')}に回数リセット、残り回数は !erai me で確認可能）
```

その他、以下のアクションによって 👏えらいポイント が変動します。
```md
その日最初のメッセージを送る
    - 自分に👏{'{:+}'.format(settings.survival_bonus.point)}
「えらい！」を{settings.marvelous.send_bonus.step_interval}回送る（{settings.marvelous.send_bonus.daily_step_limit}カウント/日）
    - 自分に👏{'{:+}'.format(settings.marvelous.send_bonus.point)}
「カス！」を{settings.booing.send_penalty.step_interval}回送る（{settings.booing.send_penalty.daily_step_limit}カウント/日）
    - 自分に👏{'{:+}'.format(settings.booing.send_penalty.point)}
1日1回以上、GitHubにContributionする
    - 自分に👏{'{:+}'.format(settings.contribution_bonus.point)} (翌日{settings.contribution_bonus.given_time}時点で集計)
    - 使用するためには !erai github register コマンドでGitHub IDを登録する必要があります
    - 集計時までにContributionとしてカウントされていないと反映されないため、pushやmergeのし忘れに注意！
```

【コマンド一覧】
`!erai me`      : 自分のステータスを表示する
`!erai ranking` : えらいポイントのランキングを表示する
`!erai help`    : ヘルプを表示する

`!erai github register [GitHub ID]` : GitHub IDを登録する
`!erai github unregister`           : GitHub IDの登録を解除する

【開発者】
Rinia
【開発ソース】
https://github.com/watano1168/marvelous
【問題点・改善案は、こちらから報告をお願いします】
https://github.com/watano1168/marvelous/issues
"""


def get_embed() -> discord.Embed:
    return discord.Embed(title="ヘルプ", description=help_text, color=0x00ff00)


async def show(message: discord.Message):
    author: discord.User = message.author
    if author is None:
        return
    try:
        await author.send(embed=get_embed())
    except discord.Forbidden:
        channel: discord.TextChannel = message.channel
        if channel is None or not isinstance(channel, discord.TextChannel):
            return
        await channel.send(embed=get_embed())
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
        await show(ctx.message)

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"
