import marvelous.data_store as data_store
import marvelous.github as github
from .user import User, get_all_users
from .errors import DataFetchError, DataUpdateError
import datetime
from logging import getLogger
from typing import Optional, List, Tuple


logger = getLogger(__name__)


def get_requests_id(users: List[User]) -> Tuple[List[str], List[Optional[int]]]:
    a = 0
    indices: List[Optional[int]] = []  # 各Userに対して、github_idが存在しないときはNone, するときは
    requests_id: List[str] = []  # github_idが存在するユーザーの、github_idの一覧
    for user in users:
        p: Optional[int] = None
        if user.github_id is not None:
            requests_id.append(user.github_id)
            p = a
            a += 1
        indices.append(p)
    return requests_id, indices


def check_bonuses(users: List[User], date: datetime.date) -> List[bool]:
    requests_id, indices = get_requests_id(users)
    try:
        counts = list(github.get_contribution_count(requests_id, date.year, date.month, date.day))
    except Exception as err:
        raise DataFetchError from err
    return [indices[i] is not None and counts[indices[i]] for i, _ in enumerate(users)]


def apply_bonus(user: User, give_point: int) -> None:
    user.point += give_point


def check_github_bonus(give_point: int, date: datetime.date) -> None:
    """全ユーザーのGitHub Contributionボーナスをチェックする"""
    users = list(get_all_users())
    bonuses = list(check_bonuses(users, date))

    for i in range(len(users)):
        if bonuses[i]:
            apply_bonus(users[i], give_point)

    try:
        data_store.users.update_marvelous_point_all(users)
    except Exception as err:
        raise DataUpdateError from err
