import logging
from discord.ext import commands

from ..bot import guild_id

logger = logging.getLogger(__name__)


class TextCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def sync(self, ctx: commands.Context, password: str = None):
        if password is None or password != self.bot.sync_password:
            await ctx.send('Nothing to see here.')
            return
        
        # Sync global commands
        synced_global = await self.bot.tree.sync()
        info_str = 'Synced global commands: ' + ', '.join([f'/{cmd.name}' for cmd in synced_global])
        logger.info(info_str)
        await ctx.send(info_str)

        # Sync our guild specific commands
        synced_guild = await self.bot.tree.sync(guild=self.bot.get_guild(guild_id))     # this one requires Guild, not just int for some reason
        info_str = f'Synced guild ({guild_id}) commands: ' + ', '.join([f'/{cmd.name}' for cmd in synced_guild])
        logger.info(info_str)
        await ctx.send(info_str)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TextCommandCog(bot))
