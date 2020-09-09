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

api = tweepy.API(auth)

# Change this name to customize who the script is following!
target_account = ""

database_name = "people_who_retweeted_{}_database.txt".format(target_account)

