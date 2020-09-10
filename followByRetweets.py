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

# TODO: Ask DK and OF if they want to run the script using python, or would prefer it as an .exe with userInput funcs

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# Change this name to customize who the script is following!
target_account = keys[4][:-1]
print(target_account)

database_name = "people_who_retweeted_{}_database.txt".format(target_account)

tweets = api.user_timeline(target_account)
daily_scrape_of_retweeters = []
for tweet in tweets:
    print(tweet.text)
    retweets_of_original_tweet = api.retweets(tweet.id, 100)  # retrieves ONLY 100 people who retweeted the tweet
    # print(len(retweets_of_original_tweet))

    # For each retweet...
    for retweet in retweets_of_original_tweet:
        daily_scrape_of_retweeters.append({"id": retweet.user.id, "follower_count": retweet.user.followers_count})

    if len(daily_scrape_of_retweeters) > 995:
        break

# sort retweeters list in place, ordered by most followers to least followers
sorted_retweeters = sorted(daily_scrape_of_retweeters, key=lambda x: x["follower_count"], reverse=True)

if path.exists(database_name):
    # Extract the db from the txt file
    with open(database_name, "r") as db:
        with_semicolons = db.read().split(",")
        users = []
        for entry in with_semicolons:
            try:
                split = entry.split(";")
                users.append({"id": split[0], "follower_count": split[1]})
            except Exception as e:
                print(str(e), split, ";")

    # Add the top 400 of the new accounts to the list from the database so they can compete for spots
    for follower in range(0, ACCOUNTS_PER_DAY):
        users.append(sorted_retweeters[follower])

    # Sort them by follower count, again
    users_sorted = sorted(users, key=lambda x: int(x["follower_count"]), reverse=True)

    # Follow the top 395, picked from both the options stored in the db and the new ones from today
    follows = 0
    accounts_followed_today = 0
    for follower in range(0, len(users_sorted)):
        follows = follows + int(users_sorted[follower]["follower_count"])
        # api.create_friendship(id=old_and_new_users_sorted[follower]["id"])  # TODO: enable this code for live ver
        accounts_followed_today += 1
        if accounts_followed_today > 394:
            break
    follows_per_account = follows / ACCOUNTS_PER_DAY

    # Remove the followed accounts, simplifying the list
    remaining_accounts = users_sorted[accounts_followed_today:]

    # Put the remaining users into the database
    x = 0
    with open(database_name, "w") as db:
        # print("yayayayayay:", len(remaining_accounts))
        # time.sleep(10)
        for follower in range(0, len(remaining_accounts)):
            # FIXME: IndexError: list index out of range
            # print(follower)
            x += 1
            try:
                db.write(str(remaining_accounts[follower]["id"]) + ";" +
                         str(remaining_accounts[follower]["follower_count"]))
                db.write(",")
            except Exception as e:
                print("error:", e)
                time.sleep(5)
    # print("look here is x {}, predictably it is the value of {} or smaller".format(x, len(remaining_accounts)))

else:
    # Follow the top 395 accounts
    follows = 0
    for follower in range(0, ACCOUNTS_PER_DAY):
        follows = follows + sorted_retweeters[follower]["follower_count"]
        # api.create_friendship(id=follower.id)  # TODO: enable this code for live ver
    follows_per_account = follows / ACCOUNTS_PER_DAY

    # Save the next 395 accounts into the database. Discard the rest!
    with open(database_name, "w") as db:
        for follower in range(ACCOUNTS_PER_DAY, ACCOUNTS_PER_DAY * 2):
            # Format of an entry in the db is "id;follower_count". Entries are comma separated.
            line = str(sorted_retweeters[follower]["id"]) + ";" + \
                   str(sorted_retweeters[follower]["follower_count"])
            db.write(line)
            db.write(",")

print("Done! Followed accounts with a total of {} followers, an average of {} followers per account."
      .format(str(follows), str(round(follows_per_account, 3))))
print("Closing in 5...")
time.sleep(5)
exit()

# FIXME: what happens when that sicknasty list comprehension runs into the "" after the last "," in the txt db?
