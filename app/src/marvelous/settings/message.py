from dataclasses import dataclass
from typing import List


@dataclass()
class PhrasesSettings:
    praise_something: List[str]
    comfort: List[str]
    praise_survival: List[str]


@dataclass()
class MessageSettings:
    strict_time: float
    ranking_limit: int
    phrases: PhrasesSettings


values = MessageSettings(
    strict_time=1.0,
    ranking_limit=8,
    phrases=PhrasesSettings(
        praise_something=[
            "えらいね、{name}！",
            "お疲れ様、{name}！よく頑張ったね！",
            "わたし、{name}みたいに頑張れる人ってすごいと思う！",
        ],
        comfort=[
            "よしよし、{name}。そんなこともあるよ。",
            "{name}、大丈夫。そうやって人は強くなるから。",
        ],
        praise_survival=[
            "{name}、今日も生きててえらい！",
            "{name}、今日も頑張ろうね！",
            "おはよう、{name}！ 今日はなにするの？",
            "今日も来てくれてありがとう、{name}！"
        ]
    )
)
