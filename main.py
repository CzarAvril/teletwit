#import twitter_telegram_bot2.common as common

import os
import sys
#import bot
import json
# import twitter_telegram_bot2.bot as bot
import tweepy
# import twitter_telegram_bot2.stream as stream
from teletwit_bot import common, bot
from teletwit_bot.stream import TweetsStreamListener


def main():
    print("Booting")

    common.init()

    telegram_bot_token = ""
    twitter_consumer_key = ""
    twitter_consumer_secret = ""
    twitter_access_token = ""
    twitter_access_secret = ""

    # READ API TOKENS FROM FILE
    with open('tokens.json') as token_file:
        token_data = json.load(token_file)
        telegram_bot_token = token_data['telegram_bot_token']
        twitter_consumer_key = token_data['consumer_key']
        twitter_consumer_secret = token_data['consumer_secret']
        twitter_access_token = token_data['access_token']
        twitter_access_secret = token_data['access_token_secret']

    follow_list = []
    with open('follow_list.json') as follow_list_file:
        follow_data = json.load(follow_list_file)
        follow_list = follow_data['follow_list']

    # AUTH
    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_secret)

    api = tweepy.API(auth)

    follow_list_ids = []
    for item in follow_list:
        user = api.get_user(item)
        follow_list_ids.append(str(user.id))

    stream = ""
    try:
        # SET UP STREAM
        streamListener = TweetsStreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=streamListener)
        stream.filter(follow=follow_list_ids, async=True)
        bot.bot_main(telegram_bot_token)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        stream.disconnect()
        print("Disconnected from stream")
    # sys.exit(0)


if __name__ == "__main__":
    main()
