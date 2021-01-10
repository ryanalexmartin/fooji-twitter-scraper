from modules.csv_handler import CsvHandler
from modules.webdriver.webdriver_handler import WebdriverHandler
from discord.ext import tasks, commands
import asyncio

class ScrapeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.csv_handler = CsvHandler()
        self.scraper.start()
        self.driver = None
    
    def cog_unload(self):
        self.scraper.cancel()

    @tasks.loop(seconds=10.0) #scrape every 10 seconds.
    async def scraper(self):
        if self.driver:
            self.driver.driver.close()

        self.driver = WebdriverHandler(discord_bot=self.bot, csv_handler=self.csv_handler, headless=False)
        self.driver.scrape(words="fooji.info//fooji.com", display_type="Top") # TODO: set this back to "Latest" before actually scraping.


    @scraper.before_loop
    async def before_scraper(self):
        print('waiting for bot to be ready...')
        await self.bot.wait_until_ready()

    @scraper.after_loop
    async def after_scraper(self):
        if self.scraper.is_being_cancelled():
            self.driver.is_scrolling = False # Will cause driver to clean itself up
        # self.driver.driver.close()
