import requests
from marvelous.settings.env import github_bearer_token
from typing import Tuple, Dict
from logging import getLogger


logger = getLogger(__name__)


def escape(value: str) -> str:
    return value.replace('"', '')


def get_request_params(user_id: str) -> Tuple[str, Dict[str, str], Dict[str, str]]:
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": "bearer " + github_bearer_token,
        "Content-Type": "application/json",
    }
    query = "\n".join([
        "query($user: String!) {",
        "  user(login: $user) { id }",
        "}",
    ])
    variables = f"{{ \"user\": \"{escape(user_id)}\" }}"
    body = {"query": query, "variables": variables}

    return url, headers, body


def interpret_response(res: any) -> bool:
    try:
        if "data" not in res.keys():
            return False
        user_res = res["data"]["user"]
        return user_res is not None
    except Exception as err:
        raise ValueError("Data structure isn't correct.") from err


def is_account_exist(user_id: str) -> bool:
    url, headers, query = get_request_params(user_id)
    response = requests.post(url, json=query, headers=headers)
    if response.status_code != 200:
        raise RuntimeError("Request failed: {}".format(response.status_code))
    return interpret_response(response.json())
