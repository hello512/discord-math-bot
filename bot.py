from discord.ext import commands
from discord.ext import tasks
#import discord
#import logging
#import string
import asyncio
import yaml
import time
import sys


sys.path.append("../")
from messages import COMMAND_NOT_AVAILABLE_MESSAGE

BOT = commands.Bot(command_prefix = ".", help_command = None)


async def on_connect():
	print("connected")

async def on_ready():
    print("math-bot is now online!")

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
	with open("token.dat", "r") as token_file:
		BOT.run(token_file.read())
