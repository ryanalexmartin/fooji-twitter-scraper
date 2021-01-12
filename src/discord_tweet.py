import tweepy


auth = tweepy.OAuthHandler('eHtXXHzhyXH7s8AJpLr1c08bf', 'MByI3bcuHR8bWc9Dh18e5ojKOtzjRp6zKCGEyq6CdmoKVUcO4L')
auth.set_access_token('1348767110441414663-AF1drc9dE0JR9LTfk0oSBeF8lO3Mu2', 'UhgS6VkPbhGFgSuw6fq8kvlRUX1faD40VaK1J5GO0wr9D')
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')

api = tweepy.API(auth)
# api.update_status('tweepy + oauth!')

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
    def on_error(self, status_code):
        if status_code == 420:
            return False
        

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["fooji.info/theoffice"], follow="Ironically_Jo")