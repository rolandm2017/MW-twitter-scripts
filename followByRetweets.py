import tweepy
from os import path
import time
from datetime import date

with open("secrets.txt", "r") as keys:
    keys = keys.readlines()[0].split(",")
    consumer_key = keys[0]
    consumer_secret = keys[1]
    # Add your access token and secret here...
    access_token = keys[2]
    access_token_secret = keys[3]

# TODO: Ask DK and OF if they want to run the script using python, or would prefer it as an .exe with userInput funcs

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# Change this name to customize who the script is following!
target_account = keys[4]
print(keys[4])

database_name = "people_who_retweeted_{}_database.txt".format(target_account)

tweets = api.user_timeline(target_account)
retweeters = []
for tweet in tweets:
    print(tweet.text)
    retweets_of_original_tweet = api.retweets(tweet.id)
    # For each retweet...
    for retweet in retweets_of_original_tweet:
        # ...get the retweeter and...
        user_who_retweeted = api.get_user(retweet.user.id).screen_name
        retweeters.append([user_who_retweeted, retweet.user.followers_count])

for x in retweeters:
    print(x)
