import tweepy
from modules.csv_handler import CsvHandler
import pandas as pd
import csv
from webhook_send_tweet import send_tweet_to_discord_as_webhook


auth = tweepy.OAuthHandler('eHtXXHzhyXH7s8AJpLr1c08bf', 'MByI3bcuHR8bWc9Dh18e5ojKOtzjRp6zKCGEyq6CdmoKVUcO4L')
auth.set_access_token('1348767110441414663-AF1drc9dE0JR9LTfk0oSBeF8lO3Mu2', 'UhgS6VkPbhGFgSuw6fq8kvlRUX1faD40VaK1J5GO0wr9D')
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

api = tweepy.API(auth)
# api.update_status('tweepy + oauth!')

path = 'outputs/output.csv'


def read_csv_file():
        return pd.read_csv(path, header=[0])

def add_tweet_to_csv(tweet):
    mode_append = 'a'
    with open(path, mode_append, newline='', encoding='utf-8') as f: 
        writer = csv.writer(f)
        writer.writerow(tweet)

existing_tweets = read_csv_file() # a LOT of wasted compute cycles... should extend init method
print('contents of outputs/output.csv will be checked against before sending Discord messages.')
print(existing_tweets)


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        existing_tweets = read_csv_file() # a LOT of wasted compute cycles... should extend init method
        hashtags = status.entities['hashtags']
        hashtags_values = [d['text'] for d in hashtags]

        urls = status.entities['urls']
        urls_values = [d['display_url'] for d in urls]
        
        tweet_info = [status.user.screen_name, status.user.name, status.created_at, \
            status.text, f'https://twitter.com/{status.user.screen_name}/status/{status.id}', \
            hashtags_values, urls_values]

        #logic for our own filtering purposes

        print(urls_values)

        if urls_values:
            if urls_values[0]:
                if urls_values[0] not in existing_tweets:
                    print('\n')
                    print(tweet_info)
                    print('\n')
                    print('\n')
                    add_tweet_to_csv(tweet_info)
                    send_tweet_to_discord_as_webhook(tweet_info)
        else:
            print('Found tweet and ignored it as URL was found in .csv file.')

    def on_error(self, status_code):
        if status_code == 420:
            return False
        
filters = 'trump'

print('Listening for tweets containing: \"' + filters + '\"...')
stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=[filters], encoding='utf8')

