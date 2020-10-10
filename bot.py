from discord.ext import commands
import discord
import logging
import string
import time
import sys


from discord.ext import commands

BOT = commands.Bot(command_prefix = ".", help_command = None)
#BOT.remove_command("help")


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
