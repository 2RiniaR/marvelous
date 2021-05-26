import os
from dataclasses import dataclass


@dataclass()
class NetworkSettings:
    proxy: str


values = NetworkSettings(
    proxy=os.environ.get("HTTP_PROXY")
)
