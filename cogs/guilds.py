from discord.ext import commands, tasks
from discord import AppInfo
import asyncio
import yaml
import time


GUILDFILE_PATH = "permanent_storage/guild_ids.yml"


def channel_type(ctx):
	return str(ctx.channel.type) == "private"


class GuildHandler(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.run.start()

	def load_valid_guild_ids(self):
		#works
		with open(GUILDFILE_PATH, "r") as guild_file:
			content = yaml.safe_load(guild_file)
			return content["valid_ids"] if content["valid_ids"] != None else []

	def add_valid_guild_id(self, id):
		##	works!
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		if id in self.load_baned_guild_ids():
			return "baned"
		with open(GUILDFILE_PATH, "r") as guild_file:
			content = yaml.safe_load(guild_file)
		if content["valid_ids"] != None and id not in content["valid_ids"]:
			content["valid_ids"].append(id)
		elif id not in content["valid_ids"]:
			content["valid_ids"] = [id]
		with open(GUILDFILE_PATH, "w") as guild_file:
			yaml.safe_dump(content, guild_file)
		return True

	def delete_valid_guild_id(self, id) -> bool:
		#works
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		with open(GUILDFILE_PATH, "r") as guild_file:
			content = yaml.safe_load(guild_file)
			try:
				content["valid_ids"].remove(id)
			except:
				return True
		with open(GUILDFILE_PATH, "w") as guild_file:
			yaml.safe_dump(content, guild_file)
		return True

	def load_baned_guild_ids(self) -> dict:
		# loads baned guild ids and ban reasons and returns them as a dict
		with open(GUILDFILE_PATH, "r") as guild_file:
			content = yaml.safe_load(guild_file)
			return content["baned_ids"] if content["baned_ids"] != None else {}
		return

	def ban_guild_id(self, id : int, reason : str = False) -> bool:
		#works
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		with open(GUILDFILE_PATH, "r") as guild_file:
			content = yaml.safe_load(guild_file)
			self.delete_valid_guild_id(id)
			if content["baned_ids"] == None:
				content["baned_ids"] = {}
			content["baned_ids"][id] = {}
			content["baned_ids"][id]["reason"] = reason if reason != False else "no reason was mentioned"
		with open(GUILDFILE_PATH, "w") as guild_file:
			yaml.safe_dump(content, guild_file)
		return True


	def unban_guild_id(self, id : int) -> bool:
		#works
		if len(str(id)) != 18 or type(id).__name__ != "int":
			return False
		with open(GUILDFILE_PATH, "r") as guild_file:
			content = yaml.safe_load(guild_file)#
			try:
				content["baned_ids"].pop(id)
			except Exception as e:
				return True
		with open(GUILDFILE_PATH, "w") as guild_file:
			yaml.safe_dump(content, guild_file)
		return True

	def get_bot_guilds(self):
		return self.bot.guilds


	@tasks.loop(seconds = 0.5, count = None)
	async def run(self):
		##	loops through the guilds the bot is in and leaves the guilds that are not in the valid guild list
		for guild in self.bot.guilds:
			if guild.id not in self.load_valid_guild_ids() or guild.id in self.load_baned_guild_ids():
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
		for index, id in enumerate(args):
			reason = False
			if len(args) > index + 1:
				if len(args[index + 1]) != 18 or args[index + 1].isnumeric() == False:
					reason = " ".join(args[-index + 1:])
			try:
				res = self.ban_guild_id(int(id), reason)
			except Exception as e:
				res = False
			returncontent.append(f"{id}: invalid format" if not res else f"{id}: baned")
			if reason != False:
				break
		await ctx.send(self.make_str(returncontent))

	@commands.command(name = "unban-guild")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _unban_guild(self, ctx, *args):

		def check(reaction, user):
			return ctx.author == user and str(reaction.emoji) == "✅"

		emote = "✅" ##	white checkmark emoji
		returncontent = []
		for id in args:
			baned_ids = self.load_baned_guild_ids()
			if id.isnumeric():
				if int(id) in baned_ids:
					reason = baned_ids[int(id)].get("reason")
					message = await ctx.send(f"Are you sure you want to unban guild id {id}?\nban reason: `%s`\nIf you are sure, please click on the ✅!" % reason)
					await message.add_reaction(emote)

					try:
						reaction, user = await self.bot.wait_for("reaction_add", timeout = 20, check = check)
					except asyncio.TimeoutError:
						returncontent.append(f"{id}: still baned!")
					else:
						try:
							res = self.unban_guild_id(int(id))
						except:
							res = False
						returncontent.append(f"{id}: invalid format" if not res else f"{id}: unbaned")
		await ctx.send(self.make_str(returncontent))

	@commands.command(name = "add-guild")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _add_guild(self, ctx, *args):
		returncontent = []
		for id in args:
			try:
				res = self.add_valid_guild_id(int(id))
			except:
				res = False
			returncontent.append(f"{id}: invalid format" if not res else f"{id}: added to valid guild ids")
		await ctx.send(self.make_str(returncontent))

	@commands.command(name = "remove-guild")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _remove_guild(self, ctx, *args):
		returncontent = []
		for id in args:
			try:
				res = self.delete_valid_guild_id(int(id))
			except:
				res = False
			returncontent.append(f"{id}: invalid format" if not res else f"{id}: removed from valid guild ids")
		await ctx.send(self.make_str(returncontent))

	@commands.command(name = "guild-status")
	@commands.is_owner()
	@commands.check(channel_type)
	async def _guild_status(self, ctx, *args):
		baned_guild_ids = []
		for id, id_info in self.load_baned_guild_ids().items():
			baned_guild_ids.append(f"{id} : %s" % id_info.get("reason"))

		await ctx.send(self.make_str(["bot is currently in guilds:"] + [str(i.id) + " " + str(i) for i in self.get_bot_guilds()] + ["valid guild ids:"] + [str(i) for i in self.load_valid_guild_ids()] + ["baned guild ids:"] + [str(i) for i in baned_guild_ids]))



def setup(bot):
    bot.add_cog(GuildHandler(bot))
