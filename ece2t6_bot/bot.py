import discord
from discord.ext import commands

TOKEN = 'your-bot-token' 

bot = commands.Bot(command_prefix='$')  

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(TOKEN)
