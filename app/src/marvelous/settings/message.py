from dataclasses import dataclass
from typing import List


@dataclass
class PhrasesSettings:
    on_receive_many_marvelous: List[str]
    on_receive_super_marvelous: List[str]
    on_receive_many_booing: List[str]
    on_make_sure_survival: List[str]
    on_sleep_better: List[str]
    on_stay_up_late: List[str]
    on_wake_up_late: List[str]


@dataclass
class MessageSettings:
    strict_time: float
    ranking_limit: int
    phrases: PhrasesSettings


values = MessageSettings(
    strict_time=1.0,
    ranking_limit=8,
    phrases=PhrasesSettings(
        on_receive_many_marvelous=[
            "えらいね、{name}！",
            "お疲れ様、{name}！よく頑張ったね！",
            "わたし、{name}みたいに頑張れる人ってすごいと思う！",
        ],
        on_receive_super_marvelous=[
            "えらいね、{name}！",
            "お疲れ様、{name}！よく頑張ったね！",
            "わたし、{name}みたいに頑張れる人ってすごいと思う！",
        ],
        on_receive_many_booing=[
            "よしよし、{name}。そんなこともあるよ。",
            "{name}、大丈夫。そうやって人は強くなるから。",
        ],
        on_make_sure_survival=[
            "{name}、今日も生きててえらい！",
            "{name}、今日も頑張ろうね！",
            "おはよう、{name}！ 今日はなにするの？",
            "今日も来てくれてありがとう、{name}！"
        ],
        on_sleep_better=[
            "おはよう、{name}！よく眠れたね！",
            "すごい！{name}って、健康にも気を使ってるんだね！",
            "早寝早起きは健康の証！今日はきっといいことあるよ、{name}！"
        ],
        on_stay_up_late=[
            "まだ起きてたんだね。こんな時間までお疲れさま、{name}。",
            "夜も遅いから、あんまり無理しないでね。{name}。",
            "真夜中はちょっと特別な気分になるね、{name}。"
        ],
        on_wake_up_late=[
            "おはよう、{name}！調子はどう？結構よく眠れたんじゃない？",
            "時間は遅くても、{name}の一日はこれからだよ！頑張ろうね！",
        ]
    )
)
