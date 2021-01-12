import requests
import urllib

tweet = ['IphonesRock', '@rosegold098765', '2020-11-13T22:42:20.000Z', '@strongblacklead\n Tweet #jinglejangle  + #promo to enter our special treat giveaway. No Purchase Necessary. Must be 18+. Void Where Prohibited. For official rules@ http://fooji.info/JingleJangle ', '', '1', '', '', '', 'https://twitter.com/rosegold098765/status/1327381310990548992', ['jinglejangle', 'promo'], 'http://fooji.info/JingleJangle']

space_replace = "%20"
hashtag_replace = "%23"

def send_tweet_to_discord_as_webhook(tweet):
    url = "https://discord.com/api/webhooks/798297681289150546/pkIV_Y7XyO6oUX4Y_Baa9xPNyAuXVsxXLf8BsSgQZIWyl5OGkxXEgwEUrSD7t_RW5Clv" #webhook url, from here: https://i.imgur.com/f9XnAew.png

    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook

    r = requests.get(tweet[-1]) #should only run this if fooji link is .info
    fooji_redirected_url = r.url.strip('/#rules')
    original_tweet_url = tweet[len(tweet) -3]
    generated_tweet = '#' + ' #'.join(tweet[len(tweet) -2])
    generated_tweet_encoded = f'https://twitter.com/intent/tweet?text={urllib.parse.quote_plus(generated_tweet)}'

    data = {
        "content" : f"New fooji detected!  [Click here to tweet.]({generated_tweet_encoded})\
        \nLink of original tweet: {original_tweet_url}\
        \nLink to rules: {fooji_redirected_url}/#rules\
        \nLink to Fooji Site: {fooji_redirected_url}\
        \nBypass Link Bypass Link (just click before ven getting reply, does not work for all foojis): {fooji_redirected_url}/#start\
        \nSkip Questions Bypass link (using this link will let you skip all the questions when re-entering the contest Foojis): {fooji_redirected_url}/#activate-workflow-1",
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

send_tweet_to_discord_as_webhook(tweet)