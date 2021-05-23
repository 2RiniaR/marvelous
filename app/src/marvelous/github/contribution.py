import requests
from itertools import chain
from marvelous.settings.env import github_bearer_token
from typing import Tuple, Dict, Optional, List
from marvelous.helpers.iterable import first_match
import datetime


def escape(value: str) -> str:
    return value.replace('"', '')


def get_request_params(users_id: List[str], year: int, month: int, day: int) -> Tuple[str, Dict[str, str], Dict[str, str]]:
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": "bearer " + github_bearer_token,
        "Content-Type": "application/json",
    }
    from_time = datetime.datetime(year, month, day, 0, 0, 0, 0)
    to_time = datetime.datetime(year, month, day, 23, 59, 59, 999)
    query_fragment = "\n".join([
        f"fragment Contribution on User {{",
        f"  contributionsCollection(from: \"{from_time.isoformat()}\", to: \"{to_time.isoformat()}\") {{",
        f"    contributionCalendar {{",
        f"      weeks {{",
        f"        contributionDays {{",
        f"          contributionCount",
        f"          date",
        f"        }}",
        f"      }}",
        f"    }}",
        f"  }}",
        f"}}",
    ])

    arguments = ", ".join([f"$user_{i}: String!" for i in range(len(users_id))])
    fields = "\n".join([f"  user_{i}: user(login: $user_{i}){{ ...Contribution }}" for i in range(len(users_id))])
    query = "\n".join([
        query_fragment,
        f"query({arguments}) {{",
        fields,
        f"}}",
    ])
    variables = "{" + "\n".join([f"  \"user_{i}\": \"{escape(user_id)}\"" for i, user_id in enumerate(users_id)]) + "}"
    body = {"query": query, "variables": variables}
    return url, headers, body


def interpret_response(res: any, users_id: List[str], year: int, month: int, day: int) -> List[Optional[int]]:
    date_str = f"{year:04}-{month:02}-{day:02}"

    def get_user_count(user_res: any) -> Optional[int]:
        if user_res is None:
            return None
        weeks_res = user_res["contributionsCollection"]["contributionCalendar"]["weeks"]
        days_res = list(chain.from_iterable(map(lambda w: w["contributionDays"], weeks_res)))
        day_res = first_match(days_res, pred=lambda d: str(d["date"]).startswith(date_str))
        if day_res is None:
            return None
        count: int = int(day_res["contributionCount"])
        return count

    try:
        if "data" not in res.keys():
            return [None] * len(users_id)
        users_res = res["data"]
        return [get_user_count(users_res[f"user_{i}"]) for i in range(len(users_id))]
    except Exception as err:
        raise ValueError("Data structure isn't correct.") from err


def get_contribution_count(users_id: List[str], year: int, month: int, day: int) -> List[Optional[int]]:
    url, headers, query = get_request_params(users_id, year, month, day)
    response = requests.post(url, json=query, headers=headers)
    if response.status_code != 200:
        raise RuntimeError("Request failed: {}".format(response.status_code))
    return interpret_response(response.json(), users_id, year, month, day)
