from discord.ext import tasks, commands

class ScrapeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.printer()

    # @tasks.loop(seconds=10.0)
    # async def printer(self):
    #     print('do a thing')
