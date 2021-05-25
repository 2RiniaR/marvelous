import datetime
import logging
from typing import Optional, List, Tuple
import marvelous.github as github
import marvelous.domain.models as models
import marvelous.db as db
from .user import get_all as get_all_users


logger = logging.getLogger(__name__)


def get_requests_id(users: List[models.User]) -> Tuple[List[str], List[Optional[int]]]:
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


def check(users: List[models.User], date: datetime.date) -> List[bool]:
    requests_id, indices = get_requests_id(users)
    try:
        counts = github.get_contribution_count(requests_id, date.year, date.month, date.day)
    except Exception as err:
        raise models.DataFetchError from err
    return [indices[i] is not None and counts[indices[i]] for i, _ in enumerate(users)]


def apply(user: models.User, give_point: int) -> None:
    user.point += give_point


def give(give_point: int, date: datetime.date) -> None:
    """全ユーザーのGitHub Contributionボーナスをチェックする"""
    users = get_all_users()
    bonuses = check(users, date)

    for i in range(len(users)):
        if bonuses[i]:
            apply(users[i], give_point)

    try:
        db.users.update_marvelous_point_all(users)
    except Exception as err:
        raise models.DataUpdateError from err
