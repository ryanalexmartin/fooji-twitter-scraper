# A bot that scrapes twitter for Fooji links and posts them to Discord
# by insom#4211 and Zoopzse#9800

## To do:
* Servlet should run in a loop (Look at how Discord bots use event loops)
* Add Discord hook functionality (and relevant config files for customers to modify)
* Update this readme to make it easier to onboard customers
* Figure out cloud instance strategy
* Update help message to match the below.
* Build out command line functionality to make it easier for the customer.
* Probably want to limit search dates to 2 days ago, max.

* Should handle links that look like: (These are not retweet giveaways, but actual straight-up giveaways)
      https://jordanwnz.fooji.com/



## Install python requirements prior to running: 
```pip install -r requirements.txt```

## Usage :
### Terminal :

The important  we need to create are:

```
  --discord             Bot will post to Discord.
  --words WORDS         Words to search. they should be separated by "//" : Cat//Dog.

```


```Scrap tweets.

optional arguments:
  -h, --help            show this help message and exit (must update help message in code)
  --words WORDS         Words to search. they should be separated by "//" : Cat//Dog.
  --from_account FROM_ACCOUNT
                        Tweets posted by "from_account" account.
  --interval INTERVAL   Interval days between each start date and end date for
                        search queries. example : 5.
  --navig NAVIG         Navigator to use : chrome or edge.
  --headless HEADLESS   Headless webdrives or not. True or False (Absolutely necessary on cloud instances)
  --limit LIMIT         Limit tweets per <interval> (still not totally sure what this does tbh)
  --display_type DISPLAY_TYPE
                        Display type of twitter page : Latest or Top tweets
  ### Deprecated, I believe... (must confirm) 
        --resume RESUME       Resume the last scraping work. You need to pass the same arguments (<words>, <start_date>, <max_date>...)```

### To execute the script : 

python scweet.py --words "fooji.info//fooji.com" --navig chrome --display_type Latest

optional:  --headless True
```
