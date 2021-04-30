import random


random.seed()
message_groups = {
    "praise_something": [
        "えらいね、{name}！",
        "お疲れ様、{name}！よく頑張ったね！",
        "わたし、{name}みたいに頑張れる人ってすごいと思う！",
    ],
    "comfort": [
        "よしよし、{name}。そんなこともあるよ。",
        "{name}、大丈夫。そうやって人は強くなるから。",
    ],
    "praise_survival": [
        "{name}、今日も生きててえらい！",
        "{name}、今日も頑張ろうね！",
        "おはよう、{name}！ 今日はなにするの？",
        "今日も来てくれてありがとう、{name}！"
    ]
}


def get_message(group: str, name: str) -> str:
    message_group = message_groups[group]
    if message_group is None:
        raise ValueError(f"Group {group} was not found.")
    return random.choice(message_group).format(name=name)
