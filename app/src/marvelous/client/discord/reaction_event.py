from dataclasses import dataclass
import discord
from typing import Optional


@dataclass()
class ReactionEvent:
    sender: discord.Member
    receiver: discord.Member
    channel: discord.TextChannel
    emoji: discord.PartialEmoji
    reaction: Optional[discord.Reaction]
