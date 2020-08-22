#!/usr/bin/env python

import os

from src.bot import MathBot



if __name__ == "__main__":

	bot = MathBot()
	bot.run(os.getenv('TestBotToken'))