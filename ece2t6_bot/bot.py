import discord
from discord.ext import commands
import logging

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())  
logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}!')

    synced = await bot.tree.sync()
    logger.info('Synced commands: ' + ', '.join([f'/{cmd.name}' for cmd in synced]))


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


def run_bot(token: str):
    bot.run(token, log_handler=None)
