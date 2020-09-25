#!/usr/bin/env python
import os

from src.bot import MathBot



if __name__ == "__main__":
	bot = MathBot()
	with open("test_token.dat", "r") as token_file:
		token = token_file.read()
	bot.run(token)
	#bot.run(os.getenv('MathBotToken'))