from discord.ext import commands
import discord
import logging
import string
import time
import sys


"""

class MathBot(discord.Client):
	async def on_ready(self):
		print("logged in as bot")

	#if message posted
	async def on_message(self, message):
		if str(message.author) == "test_bot#3640":
			return

		if message.channel.name != "bot-commands":
			##	The bot only runs in this specified channels
			return

		if message.content.startswith(".math info") or message.content.startswith(".math help"):
			##	User requested an info sheet about the mathbot
			await message.channel.send(embed = embeds.MATHBOTINFOEMBED)
			return

		if message.content.startswith(".math"):
			##	The actual math bot is called
			botmessage = analysemathmsg(message.content)
			if type(botmessage).__name__ == "str":
				await message.channel.send(botmessage)
			if type(botmessage).__name__ == "Embed":
				await message.channel.send(embed = botmessage)
			print(type(botmessage).__name__)

		if message.content.startswith(".?") or message.content.startswith(".help"):
			##	sends an info embed back to the user
			await message.channel.send(embed = embeds.GENERALINFOEMBED)

"""
from discord.ext import commands

BOT = commands.Bot(command_prefix = ".", help_command = None)
BOT.remove_command("help")


@commands.command()
async def help(ctx, *arg):
    await ctx.send("help page: nothing")

async def on_ready():
    print("math-bot is now online!")

BOT.add_listener(on_ready)
BOT.load_extension("cogs.math")

if __name__ == "__main__":
	with open("test_token.dat", "r") as token_file:
		BOT.run(token_file.read())
