import random
from typing import List


random.seed()


def get_random_phrase(group: List[str], name: str) -> str:
    return random.choice(group).format(name=name)
