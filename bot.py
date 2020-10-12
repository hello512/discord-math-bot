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



class GuildHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.run.start()

	def load_valid_guild_ids(self):
		#works
		with open("guild_ids.yml", "r") as guild_file:
			content = yaml.safe_load(guild_file)
			return content["valid_ids"] if content["valid_ids"] != None else []

	def add_valid_guild_id(self, id):
		##	works!
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		if id in self.load_baned_guild_ids():
			return "baned"
		with open("guild_ids.yml", "r") as guild_file:
			content = yaml.safe_load(guild_file)
		with open("guild_ids.yml", "w") as guild_file:
			content["valid_ids"].append(id)
			yaml.safe_dump(content, guild_file)
		return True

	def delete_valid_guild_id(self, id):
		#works
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		with open("guild_ids.yml", "r") as guild_file:
			content = yaml.safe_load(guild_file)
			try:
				content["valid_ids"].remove(id)
			except Exception as e:
				return
		with open("guild_ids.yml", "w") as guild_file:
			yaml.safe_dump(content, guild_file)

	def load_baned_guild_ids(self):
		#works
		with open("guild_ids.yml", "r") as guild_file:
			content = yaml.safe_load(guild_file)
			return content["baned_ids"] if content["baned_ids"] != None else []
		return

	def ban_guild_id(self, id):
		#works
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		with open("guild_ids.yml", "r") as guild_file:
			content = yaml.safe_load(guild_file)
			try:
				content["valid_ids"].remove(id)
			except:
				pass
			content["baned_ids"].append(id)
		with open("guild_ids.yml", "w") as guild_file:
			yaml.safe_dump(content, guild_file)


	def unban_guild_id(self, id):
		#works
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		with open("guild_ids.yml", "r") as guild_file:
			content = yaml.safe_load(guild_file)#
			try:
				content["baned_ids"].remove(id)
			except:
				return
		with open("guild_ids.yml", "w") as guild_file:
			yaml.safe_dump(content, guild_file)


	@tasks.loop(seconds = 0.5, count = None)
	async def run(self):
		##	loops through the guilds the bot is in and leaves the guilds that are not in the valid guild list
		for guild in self.bot.guilds:
			if guild.id not in self.load_valid_guild_ids() or guild.id in self.load_baned_guild_ids():
				print("leaving guild with id: ", guild.id)
				await guild.leave()



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
BOT.add_cog(GuildHandler(BOT))
BOT.load_extension("cogs.math")
BOT.load_extension("cogs.help")

if __name__ == "__main__":
	with open("token.dat", "r") as token_file:
		BOT.run(token_file.read())
