from discord.ext import commands, tasks

class GuildHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print("init")
		self.handler.start()

	def load_valid_guild_ids(self):
		#works
		with open("guild_ids.yml", "r") as guild_file:
			content = yaml.safe_load(guild_file)
			return content["valid_ids"]

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
			return content["baned_ids"]
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
	async def handler(self):
		##	loops through the guilds the bot is in and leaves the guilds that are not in the valid guild list
		for guild in self.bot.guilds:
			print(guild.id, "valid: ", self.load_valid_guild_ids(), " baned:", self.load_baned_guild_ids())
			if guild.id not in self.load_valid_guild_ids() or guild.id in load_baned_guild_ids():
				print("leaving guild with id: ", guild.id)
				await guild.leave()

    ## commands:

def setup(bot):
    pass
