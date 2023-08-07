import discord
from discord import app_commands
from discord.ext import commands


class PrivateCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # -- EXAMPLE TEMPLATE --
    # @app_commands.default_permissions(administrator=True)
    # @app_commands.guild_only()
    # @app_commands.command()
    # async def pong(self, interaction: discord.Interaction):
    #     await interaction.response.send_message('Ping!')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PrivateCommandCog(bot))
