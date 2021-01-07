# A bot that scrapes twitter for Fooji links and posts them to Discord
# by insom#4211

In the last days, Twitter banned every twitter scrapers. This repository represent an alternative legal tool (depending on how many seconds we wait between each scrolling) to scrap tweets between two given dates (start_date and max_date), for a given language and list of words or account name, and saves a csv file containing scraped data. It is also possible to scrape user profile information, including following and followers.

Scweet uses only selenium to scrape data. Authentification is required in the case of followers/following scraping. It is recommended to log in with a new account (if the list of followers is very long, it is possible that your account will be banned). To log in to your account, you need to enter your ``username`` and ``password`` in [env](https://github.com/Altimis/Scweet/blob/master/.env) file. You can controle the ``wait`` parameter in the ``get_followers`` and ``get_following`` functions. 

The [user](https://github.com/Altimis/Scweet/blob/master/Scweet/user.py) code allows you to get all user information, including location, join date and lists of **followers and following**. Check [this example](https://github.com/Altimis/Scweet/blob/master/Scweet/Example.ipynb).

**Note that all these functionalities will be added in the final version of the library**.

## Requierments : 

```pip install -r requirements.txt```

## Results :

### Tweets :

The CSV file contains the following features (for each tweet) :

- 'UserScreenName' : 
- 'UserName' : UserName 
- 'Timestamp' : timestamp of the tweet
- 'Text' : tweet text
- 'Emojis' : emojis existing in tweet
- 'Comments' : number of comments
- 'Likes' : number of likes
- 'Retweets' : number of retweets
- 'Image link' : Link of the image in the tweet (it will be an option to download images soon).
- 'Tweet URL' : Tweet URL.

### Following / Followers :

The ``get_following`` and ``get_followers`` in [user](https://github.com/Altimis/Scweet/blob/master/Scweet/user.py) give a list of following and followers fo a given user. Note that the ``user`` should start with an uppercase letter. 

**More features will be added soon, such as "all reaplies of each tweet for a specific twitter account"**

## Usage :

### Notebook example : 

**You can check the example [here](https://github.com/Altimis/Scweet/blob/master/Scweet/Example.ipynb).**

### Terminal :

```Scrap tweets.

optional arguments:
  -h, --help            show this help message and exit
  --words WORDS         Words to search. they should be separated by "//" : Cat//Dog.
  --from_account FROM_ACCOUNT
                        Tweets posted by "from_account" account.
  --to_account TO_ACCOUNT
                        Tweets posted in response to "to_account" account.
  --max_date MAX_DATE   max date for search query. example : %Y-%m-%d.
  --start_date START_DATE
                        Start date for search query. example : %Y-%m-%d.
  --interval INTERVAL   Interval days between each start date and end date for
                        search queries. example : 5.
  --navig NAVIG         Navigator to use : chrome or edge.
  --lang LANG           tweets language. Example : "en" for english and "fr"
                        for french.
  --headless HEADLESS   Headless webdrives or not. True or False
  --limit LIMIT         Limit tweets per <interval>
  --display_type DISPLAY_TYPE
                        Display type of twitter page : Latest or Top tweets (
  --resume RESUME       Resume the last scraping work. You need to pass the same arguments (<words>, <start_date>, <max_date>...)```

### To execute the script : 

todo: autorun on loop
todo: discord web hook

python scweet.py --words "fooji.info" --limit 5 --navig chrome --display_type Latest

optional:  --headless True
```
