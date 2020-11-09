from discord.ext import commands
from discord.ext import tasks
from discord import (
	Status,
	Game
)
#import discord
#import logging
#import string
import asyncio
import yaml
import time
import sys

sys.path.append("../")
from messages import COMMAND_NOT_AVAILABLE_MESSAGE


TOKEN_FILE_PATH = "permanent_storage/test_token.dat"

BOT = commands.Bot(command_prefix = ".", help_command = None)

BOT_GAME = Game("Vector math developed by: 0x5F_#3292 github.com/hello512/discord-math-bot")
BOT_STATUS = Status.online


async def on_connect():
	print("connected")

async def on_ready():
	print("math-bot is now online!")
	await BOT.change_presence(status = BOT_STATUS, activity = BOT_GAME)


async def on_command(ctx):
	pass

async def on_guild_join(guild):
	GH.check_joined_guild(guild)

async def on_command_error(ctx, error):
	await ctx.send(COMMAND_NOT_AVAILABLE_MESSAGE)

@commands.command()
async def ping(ctx):
	await ctx.send("pong")

BOT.add_listener(on_connect)
BOT.add_listener(on_ready)
BOT.add_listener(on_command_error)
BOT.add_listener(on_guild_join)
BOT.add_listener(on_command)
BOT.add_command(ping)
BOT.load_extension("cogs.guilds")
BOT.load_extension("cogs.math")
BOT.load_extension("cogs.help")

if __name__ == "__main__":
	with open(TOKEN_FILE_PATH, "r") as token_file:
		BOT.run(token_file.read())
