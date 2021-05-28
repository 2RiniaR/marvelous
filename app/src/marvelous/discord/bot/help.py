import datetime
from discord.ext import commands
import discord
import logging
from marvelous import settings, helpers
from marvelous.discord import bot


WEEKDAY_DISPLAY = ["月", "火", "水", "木", "金", "土", "日"]
logger = logging.getLogger(__name__)
help_text = f"""
あなたの {settings.message.marvelous_point_symbol}えらい を見ているbotです。

↓詳しい仕様↓
https://github.com/watano1168/marvelous

***(1) {settings.message.marvelous_point_symbol} えらいポイント***
```md
　エライさんによって集計される、あなたの行動のえらさを表すポイントです。
　毎週{WEEKDAY_DISPLAY[settings.user.reset_marvelous_point_weekday]}曜{settings.user.reset_marvelous_point_time.strftime('%H:%M')}にリセットされます。
　このとき、エライさんはポイントを多く集めた人を表彰します。たくさんポイントを集められるようにがんばりましょう！
```

***(2) {settings.marvelous.reaction} 人を褒める***
```md
　人のメッセージに {settings.marvelous.reaction} のリアクションを付けると、相手を褒めることができます。
　このとき、エライさんから相手に {settings.message.marvelous_point_symbol}{'{:+}'.format(settings.marvelous.receive_point)} がプレゼントされます。
　何回でも使えるので、気軽に周りの人を褒めましょう！いっぱい人を褒めると良いことがあるかも...？
```

***(3) {settings.super_marvelous.reaction} めっちゃ褒める***
```md
　とてもえらいことを成し遂げた人がいるときは、その人のメッセージに {settings.super_marvelous.reaction} のリアクションを付けてあげましょう。
　このリアクションは1週間に{settings.super_marvelous.initial_left_count}回までしか使えませんが、エライさんから相手に {settings.message.marvelous_point_symbol}{'{:+}'.format(settings.super_marvelous.receive_point)} がプレゼントされます。
　それと同時に、あなたにも {settings.message.marvelous_point_symbol}{'{:+}'.format(settings.super_marvelous.send_point)} がプレゼントされます。

　残り使用回数は{WEEKDAY_DISPLAY[settings.super_marvelous.reset_weekday]}曜{settings.super_marvelous.reset_time.strftime('%H:%M')}にリセットされます。
　残り回数は !erai me コマンドで確認可能です。
```

***(4) {settings.booing.reaction} 人を咎める***
```md
　人のメッセージに {settings.booing.reaction} のリアクションを付けると、相手を咎めることができます。
　このとき、エライさんは相手から {settings.message.marvelous_point_symbol}{'{}'.format(-settings.marvelous.receive_point)} を没収します。
　やりすぎはやめましょう。いっぱい人を咎めても良いことはありません。
```

***(5) 😎 毎日、元気に顔を見せる***
```md
　あなたがその日最初のメッセージを送信したとき、エライさんはあなたに {settings.message.marvelous_point_symbol}{'{:+}'.format(settings.survival_bonus.point)} をプレゼントします。
```

***(6) 🥰 人をいっぱい褒める***
```
　あなたが人を{settings.marvelous.send_bonus.step_interval}回褒めるにつき、エライさんはその優しさに {'{:+}'.format(settings.marvelous.send_bonus.point)} をプレゼントします。

　ただし、手当り次第褒めればいいものではありません。褒めた回数のカウントは、一日{settings.marvelous.send_bonus.daily_step_limit}カウントまでです。

　逆に、人を咎めすぎることはあまり良くありません。
　あなたが人を{settings.booing.send_penalty.step_interval}回咎めるにつき、エライさんは相手に同情してあなたに {settings.message.marvelous_point_symbol}{'{:+}'.format(settings.booing.send_penalty.point)} のペナルティを与えます。

　しかし、エライさんもあまりあなたにバツを与えたくありません。咎めた回数のカウントは、一日{settings.booing.send_penalty.daily_step_limit}カウントまでで許します。
```
    
***(7) 💦 毎日、ちょっとずつ進歩する***
```md
※使用するためには !erai github register コマンドでGitHub IDを登録する必要があります

　あなたがちょっとずつでも前に進もうとして、その日のうちに1回でもGitHubにContributionをした場合、エライさんはその頑張りに {'{:+}'.format(settings.contribution_bonus.point)} をプレゼントします。

　エライさんはあなたのGitHubでの活動を、翌日{settings.contribution_bonus.given_time}にチェックしに行きます。
　集計時までにContributionとしてカウントされていないと反映されないため、pushやmergeのし忘れに注意しましょう。
```
    
***(8) 💤 健康な睡眠を取る***
```md
　あなたが夜ふかしをせずに、「おやすみ」の挨拶を決まった時間（{(datetime.datetime.min + settings.sleeping_bonus.accept_sleep_start_time).strftime('%H:%M')}〜{(datetime.datetime.min + settings.sleeping_bonus.accept_sleep_end_time).strftime('%H:%M')}）にすると、エライさんは 😴 のリアクションを付けてくれます。

　次の朝、遅くまで寝ずに決まった時間（{(datetime.datetime.min + settings.sleeping_bonus.accept_wake_up_start_time).strftime('%H:%M')}〜{(datetime.datetime.min + settings.sleeping_bonus.accept_wake_up_end_time).strftime('%H:%M')}）に挨拶をすると、エライさんはあなたが早寝早起きをしたとして {settings.message.marvelous_point_symbol}{'{:+}'.format(settings.sleeping_bonus.point)} をプレゼントします。挨拶はなんでも構いません。健康な時間に目覚めましょう。

　ただし、エライさんはあなたをちゃんと見ています。「おやすみ」の挨拶をした後、夜遅く（{(datetime.datetime.min + settings.sleeping_bonus.accept_sleep_end_time).strftime('%H:%M')}〜{(datetime.datetime.min + settings.sleeping_bonus.accept_wake_up_start_time).strftime('%H:%M')}）に喋っていると、エライさんはあなたが早く寝ていないため、ポイントをあげません。
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


def show(message: discord.Message):
    author: discord.User = message.author
    if author is None:
        return
    embed = get_embed()
    try:
        bot.message.sender.send(message.author, embed=embed, force=True)
    except discord.Forbidden:
        channel: discord.TextChannel = message.channel
        if channel is None or not isinstance(channel, discord.TextChannel):
            return
        bot.message.sender.send(channel, embed=embed, force=True)
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
        show(ctx.message)

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"
