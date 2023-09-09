import discord
from discord import app_commands
from discord.ext import commands
import logging
import git
from pathlib import Path
import inspect

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

    def _cogs_available(self) -> list[str]:
        cogs_dir = Path(__file__).parent
        files = [p for p in cogs_dir.iterdir() if p.is_file()]
        cog_names = [f.name.replace('.py', '') for f in files if '.py' in f.name and '__init__' not in f.name]

        return cog_names

    def _cogs_enabled(self) -> list[str]:
        # This is a pretty hacky solution
        cog_names = []
        for cog in self.bot.cogs.values():
            path = Path(inspect.getfile(cog.__class__))
            cog_names.append(path.name.replace('.py', ''))

        return cog_names

    def _cogs_disabled(self) -> list[str]:
        available = self._cogs_available()
        enabled = self._cogs_enabled()

        return filter(lambda c: c not in enabled, available)

    # severely disobeys DRY starting here :(

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

    @unload_cog.autocomplete('cog')
    @reload_cog.autocomplete('cog')
    async def cogs_enabled_autocomplete(self, _, current: str):
        enabled = self._cogs_enabled()
        return [app_commands.Choice(name=cog, value=cog) for cog in enabled if current in cog]

    @load_cog.autocomplete('cog')
    async def cogs_disabled_autocomplete(self, _, current: str):
        disabled = self._cogs_disabled()
        return [app_commands.Choice(name=cog, value=cog) for cog in disabled if current in cog]

    # -- Git commands --

    @app_commands.default_permissions(administrator=True)
    @app_commands.guilds(guild_id)
    @app_commands.command(name='selfupdate', description='Self-updates from Git repo')
    async def git_pull(self, interaction: discord.Interaction):
        try:
            g = git.cmd.Git(str(Path(__file__).resolve().parents[2]))
            msg = g.pull()
        except git.exc.GitCommandError as e:
            embed = discord.Embed(title='Failed to run `git pull`, got error:', description=f'```{e}```', colour=discord.Colour(0xd0021b))
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title='Ran `git pull`:', description=f'```{msg}```', colour=discord.Colour(0x7ed321))
            await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PrivateCommandCog(bot))
