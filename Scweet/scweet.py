import csv
import os
import datetime
import argparse
import pandas as pd

from utils import init_driver, get_last_date_from_csv, log_search_page, keep_scrolling

def write_header_to_csv(path, write_mode):
    header = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets',
                  'Image link', 'Tweet URL', 'Hashtags', 'Fooji link']
    with open(path, write_mode, newline='', encoding='utf-8') as f: 
        writer = csv.writer(f)
        writer.writerow(header)

def scrape(words=None, to_account=None, from_account=None, interval=5, navig="chrome", lang="en",
          headless=True, limit=float("inf"), display_type="Top", resume=False, proxy=None, hashtag=None):

    driver = init_driver(navig, headless, proxy)
    data = []

    tweet_ids = set()
    save_dir = "outputs"
    write_mode = 'a'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)




    path = save_dir + "/output.csv" #Because we are checking against the existing .csv file to see if a fooji tweet has been shared, it's better to keep only one CSV file.

    #write_header_to_csv(path, write_mode) #uncomment to write header (first line of .csv should be the header... TODO:  Make this not shitty)

    num_logged_pages = 0


    with open(path, write_mode, newline='', encoding='utf-8') as f: 
        while num_logged_pages <= limit:
            scrolls = 0
            writer = csv.writer(f)


            log_search_page(driver=driver, words=words,
                                # start_date=datetime.datetime.strftime(start_date, '%Y-%m-%d'),
                                # end_date=datetime.datetime.strftime(end_date, '%Y-%m-%d'), 
                                to_account=to_account,
                                from_account=from_account, lang=lang, display_type=display_type, hashtag=None)


            num_logged_pages += 1
            last_position = driver.execute_script("return window.pageYOffset;")
            scrolling = True

            print("Scraping for tweets...")

            # start scrolling and get tweets
            tweets_parsed = 0

            driver, data, writer, tweet_ids, scrolling, tweets_parsed, scrolls, last_position = \
                keep_scrolling(driver, data, writer, tweet_ids, scrolling, tweets_parsed, limit, scrolls, last_position)


    

    driver.close()
    return data

    # # run another loop
    # data = scrape(words, to_account, from_account, interval, navig, lang, headless, limit,
    #              display_type, resume, proxy)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrap tweets.')

    parser.add_argument('--words', type=str,
                        help='Queries. they should be devided by "//" : Cat//Dog.', default=None)
    parser.add_argument('--from_account', type=str,
                        help='Tweets from this account (axample : @Tesla).', default=None)
    parser.add_argument('--to_account', type=str,
                        help='Tweets replyed to this account (axample : @Tesla).', default=None)
    parser.add_argument('--interval', type=int,
                        help='Interval days between each start date and end date for search queries. example : 5.',
                        default=1)
    parser.add_argument('--navig', type=str,
                        help='Navigator to use : chrome or edge.', default="chrome")
    parser.add_argument('--lang', type=str,
                        help='Tweets language. example : "en" for english and "fr" for french.', default=None)
    parser.add_argument('--headless', type=bool,
                        help='Headless webdrives or not. True or False', default=False)
    parser.add_argument('--limit', type=int,
                        help='Limit tweets per <interval>', default=float("inf"))
    parser.add_argument('--display_type', type=str,
                        help='Display type of twitter page : Latest or Top', default="Top")
    parser.add_argument('--resume', type=bool,
                        help='Resume the last scraping. specify the csv file path.', default=False)
    parser.add_argument('--proxy', type=str,
                        help='Proxy server', default=None)

    args = parser.parse_args()

    words = args.words
    interval = args.interval
    navig = args.navig
    lang = args.lang
    headless = args.headless
    limit = args.limit
    display_type = args.display_type
    from_account = args.from_account
    to_account = args.to_account
    resume = args.resume
    proxy = args.proxy

    # data = scrape(words, to_account, from_account, interval, navig, lang, headless, limit,
    #              display_type, resume, proxy)


    data = scrape(words, to_account, from_account, interval, navig, lang, headless, limit,
                 display_type, resume, proxy)


    
