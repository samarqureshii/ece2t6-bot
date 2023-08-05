import discord
from discord import app_commands
import logging

logger = logging.getLogger(__name__)

# setting which events the bot should listen for
intents = discord.Intents.default()

# creating a bot client with intents
client = discord.Client(intents=intents)

# a container that holds a list of all of the bots commands
tree = app_commands.CommandTree(client)


@tree.command(name="ping", description="test")
async def ping(interaction):
    await interaction.response.send_message("pong")


@client.event
async def on_ready():
    """
    On startup, the bot collects all of the coded commands.
    It then syncs it to discord for users to use.
    """

    logger.info(f"We have logged in as {client.user}.")

    synced = await tree.sync()

    logger.info(
        "Synced commands: " + ", ".join([f"/{command.name}" for command in synced])
    )


def run_bot(token: str):
    """
    Runs the client.
    """
    client.run(token, log_handler=None)
