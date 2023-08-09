import discord
from discord import app_commands
from discord.ext import commands


class PublicCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guild_only()
    @app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message('Pong!')

    @app_commands.guild_only()
    @app_commands.command()
    async def fearfoursome(self, interaction: discord.Interaction):
        await interaction.response.send_message("real ones know.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PublicCommandCog(bot))
