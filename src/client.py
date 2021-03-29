import discord
from logger import Logger
from data_context import DataContext


COMMAND_PREFIX = "!erai"


class MarvelousClient(discord.Client):
    context: DataContext
    logger: Logger

    def __init__(self, logger: Logger, context: DataContext, **options):
        super().__init__(**options)
        self.logger = logger
        self.context = context

    async def on_ready(self):
        self.logger.write_info("READY")

    async def on_message(self, message: discord.Message):
        content: str = message.content
        if message.author.bot or not content.startswith(COMMAND_PREFIX + " "):
            return

        command = content.split(" ")
        if len(command) == 2 and command[1] == "register":
            author: discord.User = message.author
            self.context.create_user(author.id)
            self.logger.write_info(f'CREATE NEW USER: {author.id}')

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        reaction_name = str(reaction)
        sender_id = user.id
        target_id = reaction.message.author.id

        if sender_id == target_id or user.bot:
            return

        if reaction_name == "💪":
            self.context.send_marvelous(sender_id, target_id)
            self.logger.write_info(f'SEND MARVELOUS: {user.name} --> {reaction.message.author.name}')
        elif reaction_name == "🦾":
            self.context.send_super_marvelous(sender_id, target_id)
            self.logger.write_info(f'SEND SUPER MARVELOUS: {user.name} --> {reaction.message.author.name}')
        elif reaction_name == "🖕":
            self.context.send_boo(sender_id, target_id)
            self.logger.write_info(f'SEND BOO: {user.name} --> {reaction.message.author.name}')

    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        pass
