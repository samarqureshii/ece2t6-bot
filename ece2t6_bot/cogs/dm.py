from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands


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


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DMCommandCog(bot))
