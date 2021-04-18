import random


random.seed()
message_groups = {
    "praise_something": [
        "えらいね、{name}！",
        "お疲れ様、{name}！よく頑張ったね！",
        "わたし、{name}みたいに頑張れる人ってすごいと思う！"
    ],
    "praise_something_too_much": [

    ],
    "comfort": [

    ],
    "praise_survival": [
        "{name}、今日も生きててえらい！"
    ]
}


def get_message(group: str, name: str) -> str:
    message_group = message_groups[group]
    if message_group is None:
        raise ValueError(f"Group {group} was not found.")
    return random.choice(message_group).format(name=name)
