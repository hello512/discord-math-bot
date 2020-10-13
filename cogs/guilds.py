from discord.ext import commands, tasks
import yaml


def channel_type(ctx):
	print(str(ctx.channel.type))
	return str(ctx.channel.type) == "private"

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


	def make_str(self, content):
		finished_str = "\n".join(content)
		return "```" + finished_str + "```"

	##	commands:

	@commands.command(name = "ban-guild")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _ban_guild(self, ctx, *args):
		returncontent = []
		for id in args:
			res = self.ban_guild_id(id)
			returncontent.append(f"{id}: invalid format" if not res else f"{id}: baned")
		await ctx.send(self.make_str(returncontent))

	@commands.command(name = "unban-guild")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _unban_guild(self, ctx, *args):
		returncontent = []
		for id in args:
			res = self.unban_guild_id(id)
			returncontent.append(f"{id}: invalid format" if not res else f"{id}: unbaned")
		await ctx.send(self.make_str(returncontent))

	@commands.command(name = "add-guild")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _add_guild(self, ctx, *args):
		async def _unban_guild(self, ctx, *args):
			returncontent = []
			for id in args:
				res = self.add_valid_guild_id(id)
				returncontent.append(f"{id}: invalid format" if not res else f"{id}: added to valid guild ids")
			await ctx.send(self.make_str(returncontent))

	@commands.command(name = "add-guild")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _remove_guild(self, ctx, *args):
		async def _unban_guild(self, ctx, *args):
			returncontent = []
			for id in args:
				res = self.delete_valid_guild_id(id)
				returncontent.append(f"{id}: invalid format" if not res else f"{id}: removed from valid guild ids")
			await ctx.send(self.make_str(returncontent))

	@commands.command(name = "guild-status")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _guild_status(self, ctx, *args):
		pass


def setup(bot):
    bot.add_cog(GuildHandler(bot))
