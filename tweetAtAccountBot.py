import tweepy
from os import path
from datetime import datetime
import time

ACCOUNTS_PER_DAY = 395  # Easy to change to 400 if you really wanna push it to the limit

with open("secrets.txt", "r") as keys:
    keys = keys.readlines()[0].split(",")
    consumer_key = keys[0]
    consumer_secret = keys[1]
    # Add your access token and secret here...
    access_token = keys[2]
    access_token_secret = keys[3]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Change this name to customize who the script is following!
target_account = keys[4][:-1]
msg = "@%s testing a bot, test test, mic check 1 2" % target_account
print(target_account)

error_log = "error_log_from_bot.txt"


def reply_to_tweet(tweet_id):
    try:
        print("FOO")
        # FIXME: this is supposed to reply to the tweet, and it does not
        api.update_status(msg, in_reply_to_status_id_str=str(tweet_id))
        return True
    except Exception as e:
        return str(e)


most_recent_tweet = api.user_timeline(screen_name=target_account, count=1)[0].id
time.sleep(2)
while True:
    newly_fetched_tweet = api.user_timeline(screen_name=target_account, count=1)[0].id
    if newly_fetched_tweet != most_recent_tweet:
        most_recent_tweet = newly_fetched_tweet
        success_message = reply_to_tweet(newly_fetched_tweet)
        if success_message is True:
            pass
        else:
            # log error to error log
            with open(error_log, "a") as log:
                log.write(success_message)
                log.write("\n")
    time.sleep(2)

