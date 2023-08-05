import discord
from discord.ext import commands
import logging

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())  
logger = logging.getLogger(__name__)


@bot.event
async def on_ready():
    logger.info(f'We have logged in as {bot.user}!')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


def run_bot(token: str):
    bot.run(token, log_handler=None)
