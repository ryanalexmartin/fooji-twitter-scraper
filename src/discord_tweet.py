import tweepy
from modules.csv_handler import CsvHandler
import pandas as p
import json



auth = tweepy.OAuthHandler('eHtXXHzhyXH7s8AJpLr1c08bf', 'MByI3bcuHR8bWc9Dh18e5ojKOtzjRp6zKCGEyq6CdmoKVUcO4L')
auth.set_access_token('1348767110441414663-AF1drc9dE0JR9LTfk0oSBeF8lO3Mu2', 'UhgS6VkPbhGFgSuw6fq8kvlRUX1faD40VaK1J5GO0wr9D')
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

api = tweepy.API(auth)
# api.update_status('tweepy + oauth!')

csv_handler = CsvHandler()

existing_tweets = csv_handler.read_csv_file()

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        
        hashtags = status.entities['hashtags']
        hashtags_values = [d['text'] for d in hashtags]

        urls = status.entities['urls']
        urls_values = [d['display_url'] for d in urls]
        
        tweet_info = [status.user.screen_name, status.user.name, status.created_at, \
            status.text, f'https://twitter.com/{status.user.screen_name}/status/{status.id}', \
            hashtags_values, urls_values]

        if status.text not in existing_tweets:
            print('\n')
            print(tweet_info)
            print('\n')
            print('\n')
            # csv_handler.add_tweet_to_csv(status)thum

    def on_error(self, status_code):
        if status_code == 420:
            return False
        

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["fooji.info"])