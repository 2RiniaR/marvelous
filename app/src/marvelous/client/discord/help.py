from discord.ext import commands
import discord
from logging import getLogger


logger = getLogger(__name__)


class MarvelousHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = ""
        self.command_attrs["help"] = "コマンド一覧とヘルプを表示する"
        self.content = (
            "各ユーザーの 👏えらいポイント を管理するbotです。\n"
            "\n"
            "他のユーザーのメッセージに以下のリアクションを付けると、アクションが可能です。\n"
            "```md\n"
            "👏 「えらい！」を送る\n"
            "    - 相手に👏+1\n"
            "🖕 「カス！」を送る\n"
            "    - 相手に👏-1\n"
            "🙌 「めっちゃえらい！」を送る\n"
            "    - 相手に👏+10\n"
            "    - 自分に👏+1\n"
            "    - 各ユーザー、1週間に3回まで（毎週日曜4:00に回数リセット）\n"
            "```\n"
            "\n"
            "その他、以下のアクションによって 👏えらいポイント が変動します。\n"
            "```md\n"
            "その日最初のメッセージを送る\n"
            "    - 自分に👏+1\n"
            "「えらい！」を5回送る（10カウント/日）\n"
            "    - 自分に👏+1\n"
            "「カス！」を5回送る（10カウント/日）\n"
            "    - 自分に👏-1\n"
            "```\n"
            "\n"
            "【コマンド一覧】\n"
            "`!erai me`      : 自分のステータスを表示する\n"
            "`!erai ranking` : えらいポイントのランキングを表示する\n"
            "`!erai help`    : ヘルプを表示する\n"
        )

    def get_ending_note(self):
        return ""

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="エライさんbot - ヘルプ", description=self.content, color=0x00ff00)
        try:
            await self.get_destination().send(embed=embed)
        except Exception as err:
            logger.error(str(err))

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


