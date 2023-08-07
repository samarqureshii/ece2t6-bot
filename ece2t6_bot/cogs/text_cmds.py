import logging
from discord.ext import commands

logger = logging.getLogger(__name__)


class TextCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def sync(self, ctx: commands.Context, password: str = None):
        if password is None or password != self.bot.sync_password:
            await ctx.send('Nothing to see here.')
            return
        
        synced = await self.bot.tree.sync()
        info_str = 'Synced commands: ' + ', '.join([f'/{cmd.name}' for cmd in synced])
        
        logger.info(info_str)
        await ctx.send(info_str)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TextCommandCog(bot))
