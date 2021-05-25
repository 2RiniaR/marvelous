import os
from dataclasses import dataclass


@dataclass()
class GitHubSettings:
    token: str


values = GitHubSettings(
    token=os.environ.get("GITHUB_BEARER_TOKEN")
)
