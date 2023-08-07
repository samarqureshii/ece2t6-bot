import discord
from discord import app_commands
from discord.ext import commands
import logging

from ..bot import guild_id

logger = logging.getLogger(__name__)


class PrivateCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # -- EXAMPLE TEMPLATE --
    # @app_commands.default_permissions(administrator=True)
    # @app_commands.guilds(guild_id)
    # @app_commands.command()
    # async def pong(self, interaction: discord.Interaction):
    #     await interaction.response.send_message('Ping!')

    # -- Cog administration commands --
    # severely disobeys DRY here :(

    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(guild_id)
    @app_commands.command(name='load', description='Loads a cog')
    @app_commands.describe(cog='Module name of cog')
    async def load_cog(self, interaction: discord.Interaction, cog: str):
        cog = f'{self.bot.COG_MODULE_PREFIX}.{cog}'

        # Try to load the cog, outputting error message if it fails.
        try:
            await self.bot.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title=f'Failed to load cog {cog}. Error: {e}', colour=discord.Colour(0xd0021b))
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=f'Loaded cog {cog}.', colour=discord.Colour(0x7ed321))
            await interaction.response.send_message(embed=embed)

    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(guild_id)
    @app_commands.command(name='unload', description='Unloads a cog')
    @app_commands.describe(cog='Module name of cog')
    async def unload_cog(self, interaction: discord.Interaction, cog: str):
        cog = f'{self.bot.COG_MODULE_PREFIX}.{cog}'

        # Try to unload the cog, outputting error message if it fails.
        try:
            await self.bot.unload_extension(cog)
        except Exception as e:
            embed = discord.Embed(title=f'Failed to unload cog {cog}. Error: {e}', colour=discord.Colour(0xd0021b))
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=f'Unloaded cog {cog}.', colour=discord.Colour(0x7ed321))
            await interaction.response.send_message(embed=embed)

    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(guild_id)
    @app_commands.command(name='reload', description='Reloads a cog')
    @app_commands.describe(cog='Module name of cog')
    async def reload_cog(self, interaction: discord.Interaction, cog: str):
        cog = f'{self.bot.COG_MODULE_PREFIX}.{cog}'

        # Try to reload the cog, outputting error message if it fails.
        try:
            await self.bot.unload_extension(cog)
            await self.bot.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title=f'Failed to reload extension {cog}. Error: {e}', colour=discord.Colour(0xd0021b))
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=f'Reloaded extension {cog}.', colour=discord.Colour(0x7ed321))
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PrivateCommandCog(bot))
