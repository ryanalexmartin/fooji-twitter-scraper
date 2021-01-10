from .webdriver_utils import init_driver, get_tweet_data
import pandas as pd
from time import sleep


class WebdriverHandler:
    path = "outputs/output.csv"

    def __init__(self, discord_bot, csv_handler):
        self.driver = init_driver()                  #Unique to each instance of WebdriverHandler() (should not be more than one instance)  
        self.csv_tweets_df = self.read_csv_file()
        self.csv_handler = csv_handler

        self.discord_bot = discord_bot
            # Read CSV file and add all rows to a DataFrame

    def read_csv_file(self):
        return pd.read_csv(self.path, header=[0])
        

    def get_all_tweet_cards_on_page(self):
        return self.driver.find_elements_by_xpath('//div[@data-testid="tweet"]')


    def get_csv_fooji_links(self):
        return self.csv_tweets_df[self.csv_tweets_df.columns[-1]].values

    async def post_tweet_to_discord(self, tweet):
        await self.discord_bot.wait_until_ready()
        channel = self.discord_bot.get_channel(796601973897035806)
        await channel.send('A new fooji link was discovered: ' + tweet[-1])
    
    async def scroll_through_twitter_feed(self, data, writer, tweet_urls, scrolling, tweets_parsed, limit, scroll_count, last_position):
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
                            self.post_tweet_to_discord(tweet)
                            print("Writing new entry to output.csv and attempted to send Discord message to server...")
                            writer.writerow(tweet)

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
        


