from discord.ext import tasks, commands

class ScrapeCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.printer()

    async def printfunc(self):
        print("coroutine just ran") #This never runs.

    @tasks.loop(seconds=10.0)
    async def printer(self):
        print('import scrape_fooji or something yo')
        #await scrape_fooji()