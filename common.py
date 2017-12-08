import os
import telegram.ext
import json

#global_var = None


def init():
    global subscribers
    global followers
    if os.path.isfile('subscribers.json'):
        subscribers = loadSubscribers()
    else:
        subscribers = []

    if os.path.isfile('follow_list.json'):
        followers = loadFollowers()
    else:
        followers = []


global bot
bot = ""
# print(bot.get_me())


def saveSubscribers(subscribers_list):
    with open('subscribers.json', 'w') as subscribers_list_file:
        save_data = {'subscribers': subscribers_list}
        json.dump(save_data, subscribers_list_file)


def loadSubscribers():
    with open('subscribers.json') as subscribers_list_file:
        load_data = json.load(subscribers_list_file)
        return load_data['subscribers']


def loadFollowers():
    with open('follow_list.json') as follow_list_file:
        follow_data = json.load(follow_list_file)
        return follow_data['follow_list']