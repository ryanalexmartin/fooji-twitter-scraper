# This bot handles Discord logins and config issues, and runs in the background while the scraper runs in a loop.

from utils import init_driver
import asyncio
import discord
import os
import scweet
import scweet

from discord.ext import tasks, commands

import csv
import os
import datetime
import argparse
import pandas as pd
import threading
import asyncio
from time import sleep


from signal import signal, SIGINT
from sys import exit





import config
import utils

client = commands.Bot('!')

def write_header_to_csv(path, write_mode):
    header = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets',
                  'Image link', 'Tweet URL', 'Hashtags', 'Fooji link']
    with open(path, write_mode, newline='', encoding='utf-8') as f: 
        writer = csv.writer(f)
        writer.writerow(header)

async def keep_scrolling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position):
    path = "outputs/output.csv"

    #read csv file and add all rows to a datafield
    df = pd.read_csv(path, header=[0])


    while scrolling and tweet_parsed < limit:
        # get the card of tweets
        page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
        for card in page_cards:
            tweet = utils.get_tweet_data(card)
            if tweet:
                # print(tweet)
                # check if the tweet is unique by grabbing URL
                tweet_id = ''.join(tweet[len(tweet) - 2])
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    data.append(tweet)
                    last_date = str(tweet[2])
                    print("Tweet made at: " + str(last_date) + " is found.")
                    print(tweet[-1])
                    if(tweet[-1] not in df[df.columns[-1]].values): #If the link has not yet been found
                        ##TODO:  send to DISCORD right here!
                        await client.wait_until_ready()
                        channel = client.get_channel(796601973897035806)
                        await channel.send('A new fooji link was discovered: ' + tweet[-1])
                        print("Writing new entry to output.csv and attempted to send Discord message to server...")
                        writer.writerow(tweet)
                    tweet_parsed += 1
                    if tweet_parsed >= limit:
                        break
        scroll_attempt = 0
        while True and tweet_parsed < limit:
            # check scroll position
            print("scroll", scroll)
            # sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            scroll += 1
            sleep(1)
            curr_position = driver.execute_script("return window.pageYOffset;")
            if last_position == curr_position:
                scroll_attempt += 1

                # end of scroll region
                if scroll_attempt >= 2:
                    scrolling = False
                    break
                else:
                    sleep(1)  # attempt another scroll
            else:
                last_position = curr_position
                break
    return driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position


        
async def scrape(words=None, to_account=None, from_account=None, interval=5, navig="chrome", lang="en",
          headless=True, limit=float("inf"), display_type="Top", resume=False, proxy=None, hashtag=None):

    driver = utils.init_driver(navig, headless, proxy)
    data = []

    tweet_ids = set()
    save_dir = "outputs"
    write_mode = 'a'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    path = save_dir + "/output.csv"

    num_logged_pages = 0

    with open(path, write_mode, newline='', encoding='utf-8') as f: 
        while num_logged_pages <= limit:
            scrolls = 0
            writer = csv.writer(f)

            utils.log_search_page(driver=driver, words=words,
                                to_account=to_account,
                                from_account=from_account, lang=lang, display_type=display_type, hashtag=None)


            num_logged_pages += 1
            last_position = driver.execute_script("return window.pageYOffset;")
            scrolling = True

            print("Scraping for tweets...")

            tweets_parsed = 0
            driver, data, writer, tweet_ids, scrolling, tweets_parsed, scrolls, last_position = \
                await keep_scrolling(driver, data, writer, tweet_ids, scrolling, tweets_parsed, limit, scrolls, last_position)    
    driver.close()
    return data


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

async def scrape_fooji():
    words = "fooji.info//fooji.com"
    interval = 5
    navig = "chrome"
    lang = "en"
    headless = False
    limit = default=float("inf")
    display_type = "Latest"
    from_account = None
    to_account = None
    resume = "False"
    proxy = None

    await scrape(words, to_account, from_account, interval, navig, lang, headless, limit,
                display_type, resume, proxy)

class ScrapeCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.printer.start()

    async def printfunc(self):
        print("coroutine just ran") #This never runs.

    @tasks.loop(seconds=10.0)
    async def printer(self):
        await scrape_fooji()



client.add_cog(ScrapeCog(client))
client.run(config.auth_token)

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    # Should take reference to driver from utils here.
    exit(0)

    
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT is recieved
    signal(SIGINT, handler)


