from discord.ext import commands
from threading import Thread
#import discord
#import logging
#import string
import pickle
import time
import sys


sys.path.append("../")
from messages import COMMAND_NOT_AVAILABLE_MESSAGE

BOT = commands.Bot(command_prefix = ".", help_command = None)

class GuildHandler(Thread):
	def __init__(self, bot):
		self.bot = bot
		self.guilds = bot.guilds

	def load_valid_guild_ids(self):
		pass

	def add_valid_guild_id(self, id):
		pass

	def delete_guild_id(self, id):
		pass

	def run(self):
		while True:
			for guild in self.guilds:
				if guild.id not in self.load_valid_guild_ids:
					guild.leave()
			time.sleep(0.5)






async def on_connect():
	print("connected")

async def on_ready():
    print("math-bot is now online!")

async def on_command(ctx):
	print(ctx.guild, "id: ", ctx.guild.id)
	print(ctx.channel)
	print(ctx.author, "id: ", ctx.author.id)
	#if ctx.guild.id != 3:
	#	await ctx.guild.leave()

async def on_guild_join(guild):
	pass

async def on_command_error(ctx, error):
	await ctx.send(COMMAND_NOT_AVAILABLE_MESSAGE)

def leave_guild(guild):
	guild.leave()

@commands.command()
async def ping(ctx):
	await ctx.send("pong")

BOT.add_listener(on_connect)
BOT.add_listener(on_ready)
BOT.add_listener(on_command_error)
BOT.add_listener(on_command)
BOT.add_command(ping)
BOT.load_extension("cogs.math")
BOT.load_extension("cogs.help")

if __name__ == "__main__":
	with open("test_token.dat", "r") as token_file:
		BOT.run(token_file.read())
