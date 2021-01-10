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
from signal import signal, SIGINT
from sys import exit


class DiscordBotContainer:
    path = "outputs/output.csv"
    def __init__(self):
        self.csv_handler = CsvHandler()
        self.bot = commands.Bot(command_prefix='!')
        self.bot.add_cog(ScrapeCog(self))
        self.bot.run(auth_token)
        self.driver = WebdriverHandler(discord_bot=self.bot, csv_handler=self.csv_handler)
        self.tweet_ids = set()
        self.data = []

    def start(self):
        print("Started discord bot: ", self.bot)
        self.scrape()

    async def scrape(self, words=None, to_account=None, from_account=None, interval=5, navig="chrome", lang="en", \
                    headless=True, limit=float("inf"), display_type="Top", resume=False, proxy=None, hashtag=None):
        if not os.path.exists("outputs"):
            os.makedirs("outputs")
        
        write_mode = 'a'
        num_logged_pages = 0

        with open(self.path, write_mode, newline='', encoding='utf-8') as f: 
            while num_logged_pages <= limit:
                scrolls = 0
                writer = csv.writer(f)

                self.driver.get_search_page(driver=self.driver, words=words, to_account=to_account, \
                    from_account=from_account, lang=lang, display_type=display_type, hashtag=None)

                num_logged_pages += 1
                
                last_position = self.driver.execute_script("return window.pageYOffset;")
                scrolling = True

                print("Scraping for tweets...")

                tweets_parsed = 0
                self.driver, self.data, writer, self.tweet_ids, scrolling, tweets_parsed, scrolls, last_position = \
                    await self.driver.scroll_through_twitter_feed(self.driver, self.data, writer, self.tweet_ids, scrolling, tweets_parsed, limit, scrolls, last_position)    
        self.driver.close()
        return self.data
    
def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    # Should take reference to driver from utils here.
    exit(0)

    

