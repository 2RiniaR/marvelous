import os
from dataclasses import dataclass


DEVELOPMENT_VALUE = "development"


@dataclass()
class EnvironmentSettings:
    is_development: bool


values = EnvironmentSettings(
    is_development=os.environ.get("RUN_ENVIRONMENT") == DEVELOPMENT_VALUE
)
