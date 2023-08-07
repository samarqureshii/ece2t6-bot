import discord
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)


class ECE2T6Bot(commands.Bot):
    COG_MODULE_PREFIX = 'ece2t6_bot.cogs'

    def __init__(self, initial_cogs: list[str], sync_password: str) -> None:
        super().__init__(
            command_prefix='ece2t6!', 
            intents=discord.Intents.all(),  # for simplicity
            help_command=None
        )

        self.initial_cogs = initial_cogs
        self.sync_password = sync_password

    async def on_ready(self):
        logger.info(f'We\'re ready and logged in as {self.user}!')

    async def setup_hook(self) -> None:
        logger.info(f'Loading cogs...')

        for cog in self.initial_cogs:
            cog = f'{self.COG_MODULE_PREFIX}.{cog}'
            try:
                await self.load_extension(cog)
            except Exception as e:
                logger.error(f'Failed to load extension {cog}: {e}')
            else:
                logger.info(f'Loaded extension {cog}.')


def run_bot(token: str, _guild_id: int, sync_password: str, initial_cogs: list[str]):
    '''Entrypoint to actually run the bot'''
    global bot, guild_id
    bot = ECE2T6Bot(initial_cogs=initial_cogs, sync_password=sync_password)
    guild_id = _guild_id

    bot.run(token, log_handler=None)
