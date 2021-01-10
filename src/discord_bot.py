# This bot handles Discord logins and config issues, and runs in the background while the scraper runs in a loop.

from modules.csv_handler import CsvHandler
from modules.webdriver.webdriver_handler import WebdriverHandler
from modules.webdriver.webdriver_utils import init_driver
from modules.cogs.scrape_cog import ScrapeCog
import asyncio
import discord
import os
from modules.config import auth_token

from discord.ext import tasks, commands

import csv
import os
import datetime
import argparse
import threading
import asyncio
from time import sleep
import csv

bot = commands.Bot(command_prefix='!')
bot.add_cog(ScrapeCog(bot))

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


bot.run(auth_token) # Nothing after bot.run('my-token') will run since it is fully blocking.