import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())  


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


def run_bot(token: str):
    bot.run(token)
