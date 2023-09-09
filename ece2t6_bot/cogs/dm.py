from __future__ import annotations

import discord
from discord.ext import commands
import logging

from ..bot import dm_reflection_channel_id

logger = logging.getLogger(__name__)


class DMCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        if not (passed := isinstance(ctx.channel, discord.DMChannel)):
            await ctx.send('Please DM me to use this command.')

        return passed

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if not (passed := isinstance(interaction.channel, discord.DMChannel)):
            await interaction.response.send_message('Please DM me to use this command.')

        return passed

    # -- EXAMPLE TEMPLATE --
    # @app_commands.command()
    # async def pang(self, interaction: discord.Interaction):
    #     await interaction.response.send_message('Ping-pong!')

    @commands.Cog.listener('on_message')
    async def reflect_dms(self, msg: discord.Message):
        if isinstance(msg.channel, discord.DMChannel):
            output_chan = self.bot.get_channel(dm_reflection_channel_id)    # needs error handler later:tm:

            embed = discord.Embed(description=msg.content)
            embed.set_author(name=msg.author.name, icon_url=msg.author.avatar.url)

            await output_chan.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DMCommandCog(bot))
