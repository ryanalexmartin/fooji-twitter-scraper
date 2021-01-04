import csv
import os
import datetime
import argparse

from utils import init_driver, get_last_date_from_csv, log_search_page, keep_scroling

def scrape(words=None, to_account=None, from_account=None, interval=5, navig="chrome", lang="en",
          headless=True, limit=float("inf"), display_type="Top", resume=False, proxy=None):

    global driver
    data = []

    tweet_ids = set()
    save_dir = "outputs"
    write_mode = 'w'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)


    path = save_dir + "/output.csv" #Because we are checking against the existing .csv file to see if a fooji tweet has been shared, it's better to keep only one CSV file.

    start_date = datetime.date.today() - datetime.timedelta(1) #search from yesterday (TODO: might be more efficient to search from last hour)
    max_date = datetime.date.today()

    if resume:
        start_date = str(get_last_date_from_csv(path))[:10]
        write_mode = 'a'
    end_date = start_date + datetime.timedelta(days=interval)

    num_logged_pages = 0


    with open(path, write_mode, newline='', encoding='utf-8') as f: 
        header = ['UserScreenName', 'UserName', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets',
                  'Image link', 'Tweet URL']
        writer = csv.writer(f)
        if write_mode == 'w':
            writer.writerow(header)
        while end_date <= max_date:
            scrolls = 0

            # log search page between start_date and end_date
            if type(start_date) != str:
                log_search_page(driver=driver, words=words,
                                start_date=datetime.datetime.strftime(start_date, '%Y-%m-%d'),
                                end_date=datetime.datetime.strftime(end_date, '%Y-%m-%d'), to_account=to_account,
                                from_account=from_account, lang=lang, display_type=display_type)
            else:
                log_search_page(driver=driver, words=words, start_date=start_date,
                                end_date=datetime.datetime.strftime(end_date, '%Y-%m-%d'), to_account=to_account,
                                from_account=from_account, lang=lang, display_type=display_type)

            num_logged_pages += 1
            #TODO:  remove "interval"

            # last position of the page : the purpose for this is to know if we reached the end of the page of not so
            # that we refresh for another <start_date> and <end_date>
            last_position = driver.execute_script("return window.pageYOffset;")
            # should we keep scrolling ?
            scrolling = True

            print("looking for tweets between " + str(start_date) + " and " + str(end_date) + " ...")

            # start scrolling and get tweets
            tweet_parsed = 0

            driver, data, writer, tweet_ids, scrolling, tweet_parsed, scrolls, last_position = \
                keep_scroling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scrolls, last_position)

            # keep updating <start date> and <end date> for every search
            if type(start_date) == str:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(days=interval)
            else:
                start_date = start_date + datetime.timedelta(days=interval)
            end_date = end_date + datetime.timedelta(days=interval)

    # close the web driver
    data = scrape(words, to_account, from_account, interval, navig, lang, headless, limit,
                 display_type, resume, proxy)


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

    global driver
    driver = init_driver(navig, headless, proxy)

    scrape(words, to_account, from_account, interval, navig, lang, headless, limit,
                 display_type, resume, proxy)


    
