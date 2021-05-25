import os
from dataclasses import dataclass


@dataclass()
class DiscordSettings:
    token: str
    default_channel_id: int


values = DiscordSettings(
    token=os.environ.get("DISCORD_TOKEN"),
    default_channel_id=int(os.environ.get("DISCORD_DEFAULT_CHANNEL_ID"))
)
