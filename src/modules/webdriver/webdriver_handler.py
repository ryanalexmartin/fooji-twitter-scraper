from .webdriver_utils import init_driver, get_tweet_data
import pandas as pd
import csv
from time import sleep
import requests
import asyncio


def send_tweet_to_discord_as_webhook(tweet):
    url = "https://discord.com/api/webhooks/798297681289150546/pkIV_Y7XyO6oUX4Y_Baa9xPNyAuXVsxXLf8BsSgQZIWyl5OGkxXEgwEUrSD7t_RW5Clv" #webhook url, from here: https://i.imgur.com/f9XnAew.png

    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data = {
        "content" : "New fooji detected!",
        "username" : "Fooji Tracker"
    }

    #leave this out if you dont want an embed
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description" : tweet[3],
            "title" : tweet[0]
        }
    ]

    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


class WebdriverHandler:
    path = "outputs/output.csv"


    def __init__(self, discord_bot, csv_handler, headless, loop):
        self.driver = init_driver(headless=headless)                  #Unique to each instance of WebdriverHandler() (should not be more than one instance)  
        self.csv_tweets_df = self.read_csv_file()
        self.csv_handler = csv_handler
        self.data = []
        self.tweet_ids = set()
        self.write_mode = 'a'
        self.path = "outputs/output.csv"
        self.is_scrolling = False
        self.discord_bot = discord_bot
        self.loop = loop
            # Read CSV file and add all rows to a DataFrame

    def read_csv_file(self):
        return pd.read_csv(self.path, header=[0])
        

    def get_all_tweet_cards_on_page(self):
        return self.driver.find_elements_by_xpath('//div[@data-testid="tweet"]')


    def get_csv_fooji_links(self):
        return self.csv_tweets_df[self.csv_tweets_df.columns[-1]].values

    # async def post_tweet_to_discord(self, tweet):
    #     channel = self.discord_bot.get_channel(796601973897035806)
    #     await channel.send('A new fooji link was discovered: ' + tweet[-1])

    def scrape(self, words=None, to_account=None, from_account=None, interval=5, navig="chrome", lang="en", \
                    headless=True, limit=float("inf"), display_type="Top", resume=False, proxy=None, hashtag=None):
        num_logged_pages = 0

        #with open(self.path, self.write_mode, newline='', encoding='utf-8') as f: 
        self.is_scrolling = True
        while self.is_scrolling and num_logged_pages <= limit:
            scroll_count = 0

            self.get_search_page(words=words, to_account=to_account, \
                from_account=from_account, lang=lang, display_type=display_type, hashtag=None)

            num_logged_pages += 1
            
            last_position = self.driver.execute_script("return window.pageYOffset;")
            self.is_scrolling = True

            print("Scraping for tweets...")

            tweets_parsed = 0

            # self.driver, self.data, writer, self.tweet_ids, self.is_scrolling, tweets_parsed, scroll_count, last_position = \  #This syntax is very unclear, so I'd rather just call the method.
            self.scroll_through_twitter_feed(self.data, self.csv_handler, self.tweet_ids, self.is_scrolling, tweets_parsed, limit, scroll_count, last_position)    

        self.driver.close()
        return self.data
    
    def scroll_through_twitter_feed(self, data, writer, tweet_urls, scrolling, tweets_parsed, limit, scroll_count, last_position):
        while tweets_parsed < limit:

            tweet_cards = self.get_all_tweet_cards_on_page()

            for card in tweet_cards:
                tweet = get_tweet_data(card)
                if tweet:                    
                    tweet_url = ''.join(tweet[len(tweet) - 2]) # grab URL from tweet's array, which is our unique identifier
                    
                    if tweet_url not in tweet_urls:
                        tweet_urls.add(tweet_url)
                        data.append(tweet)

                        fooji_link = tweet[-1]
                        csv_fooji_links = self.get_csv_fooji_links()
                        
                        if(fooji_link not in csv_fooji_links): #If the link has not yet been found
                            send_tweet_to_discord_as_webhook(tweet)
                            print("Writing new entry to output.csv and attempted to send Discord message to server...")
                            print("Tweet that was found: \n")
                            print(tweet)
                            print("\n")
                            self.csv_handler.add_tweet_to_csv(tweet)
                            self.csv_tweets_df = self.read_csv_file()


                        tweets_parsed += 1
                        if tweets_parsed >= limit:
                            break
                        
            scroll_attempt = 0

            while True and tweets_parsed < limit:
                # check scroll position
                print("scroll", scroll_count)
                # sleep(1)
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                scroll_count += 1

                sleep(1) # TODO: make this be less than one second.

                current_position = self.driver.execute_script("return window.pageYOffset;")

                if last_position == current_position:
                    scroll_attempt += 1

                    # end of scroll region
                    if scroll_attempt >= 2:
                        scrolling = False
                        break
                    else:
                        sleep(1)  # attempt another scroll
                else:
                    last_position = current_position
                    break

        return self.driver, data, writer, tweet_urls, scrolling, tweets_parsed, scroll_count, last_position


    def get_search_page(self, lang, display_type, words, to_account, from_account, hashtag):
        """ Search Twitter for this query between start_date and end_date"""

        # req='%20OR%20'.join(words)
        from_account = "(from%3A" + from_account + ")%20" if from_account is not None else ""
        to_account = "(to%3A" + to_account + ")%20" if to_account is not None else ""
        hash_tags = "(%23"+hashtag+")%20" if hashtag is not None else ""

        if words is not None:
            words = str(words).split("//")
            words = "(" + str('%20OR%20'.join(words)) + ")%20"
        else:
            words = ""

        if lang is not None:
            lang = 'lang%3A' + lang
        else:
            lang = ""

        #DISUSED
        # end_date = "until%3A" + end_date + "%20"
        # start_date = "since%3A" + start_date + "%20"
        # to_from = str('%20'.join([from_account,to_account]))+"%20"

        self.driver.get(
            'https://twitter.com/search?q=' + words + from_account + to_account + hash_tags + lang + '&src=typed_query')

        sleep(1) #wait for page to load (Not ideal to wait for 1 second, should instead verify that something exists on the page)

        # navigate to historical 'Top' or 'Latest' tab
        try:
            self.driver.find_element_by_link_text(display_type).click()
        except:
            print("\'Latest\' button could not be found.")
        


