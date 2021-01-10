# This bot handles Discord logins and config issues, and runs in the background while the scraper runs in a loop.

from .csv_handler import CsvHandler
from .webdriver.webdriver_handler import WebdriverHandler
from .webdriver.webdriver_utils import init_driver
from .cogs.scrape_cog import ScrapeCog
import asyncio
import discord
import os
from .config import auth_token

from discord.ext import tasks, commands

import csv
import os
import datetime
import argparse
import threading
import asyncio
from time import sleep
import csv

class DiscordBotContainer():
    path = "outputs/output.csv"
    def __init__(self):
        self.csv_handler = CsvHandler()
        self.driver = WebdriverHandler(discord_bot=self.bot, csv_handler=self.csv_handler)
        self.tweet_ids = set()
        self.data = []
        self.is_scrolling = False
        self.bot = commands.Bot(command_prefix='!')
        self.bot.add_cog(ScrapeCog(self.bot))
        self.bot.run(auth_token)
        print("Starting discord bot: ", self.bot)


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.bot))

    async def scrape(self, words=None, to_account=None, from_account=None, interval=5, navig="chrome", lang="en", \
                    headless=True, limit=float("inf"), display_type="Top", resume=False, proxy=None, hashtag=None):
                    
       
        write_mode = 'a'
        num_logged_pages = 0

        with open(self.path, write_mode, newline='', encoding='utf-8') as f: 
            self.is_scrolling = True
            while self.is_scrolling and num_logged_pages <= limit:
                scrolls = 0
                writer = csv.writer(f)

                self.driver.get_search_page(driver=self.driver, words=words, to_account=to_account, \
                    from_account=from_account, lang=lang, display_type=display_type, hashtag=None)

                num_logged_pages += 1
                
                last_position = self.driver.execute_script("return window.pageYOffset;")
                self.is_scrolling = True

                print("Scraping for tweets...")

                tweets_parsed = 0

                self.driver, self.data, writer, self.tweet_ids, self.is_scrolling, tweets_parsed, scrolls, last_position = \
                    await self.driver.scroll_through_twitter_feed(self.driver, self.data, writer, self.tweet_ids, self.is_scrolling, tweets_parsed, limit, scrolls, last_position)    

        self.driver.close()
        
        return self.data

