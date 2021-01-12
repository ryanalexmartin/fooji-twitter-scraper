import requests
import urllib

def send_tweet_to_discord_as_webhook(tweet):
    main_server_url = "https://discord.com/api/webhooks/798417075839565835/yQ4IBosSl_muATBGKrm4YQzSQIsS4nC7h_rTFSY5Sa-nhh-a1gMAdNFIw-pNmak3DMXH" #webhook url, from here: https://i.imgur.com/f9XnAew.png


    #for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook

    r = requests.get(format_url(tweet[-1][0])) #should only run this if fooji link is .info
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
    }

    #leave this out if you dont want an embed
    #for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"] = [
        {
            "description" : tweet[3],
            "title" : tweet[0] #author of the tweet
        }
    ]

    result = requests.post(main_server_url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

def format_url(url):
    url = url.lower()
    p = urllib.parse.urlparse(url, 'http')
    netloc = p.netloc or p.path
    path = p.path if p.netloc else ''
    if not netloc.startswith('www.'):
        netloc = 'www.' + netloc

    p = urllib.parse.ParseResult('http', netloc, path, *p[3:])
    return p.geturl()