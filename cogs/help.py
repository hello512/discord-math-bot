from discord.ctx import commands


##  contains anything to help the user
class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def questionmark(self):
        return

    @commands.command()
    async def help(self):
        return
