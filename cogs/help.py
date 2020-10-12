import sys

from discord.ext import commands

sys.path.append("../")
from messages import MATHBOTINFOEMBED
from messages import GENERALINFOEMBED


##  contains anything to help the user
class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "?")
    async def _questionmark(self, ctx):
        await self.help(ctx)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed = GENERALINFOEMBED)



def setup(bot):
    bot.add_cog(Helper(bot))
