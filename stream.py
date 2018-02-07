import teletwit_bot.common as common
from teletwit_bot import common, bot
# import teletwit_bot.main as main
import tweepy


class TweetsStreamListener(tweepy.StreamListener):
    #usr_id = bot.subscribe.usr_id  # Need to link the user id from the bot class to this class for the dictionary
    def on_connect(self):
        print("Connected to stream")

    def on_status(self, status):
        #usr_id = bot.subscribe.usr_id
        print("waiting for tweets....")
        if not status.entities["user_mentions"]:
            print("testing")
            for chat_id in common.subscribers:
                if status.user.id_str in common.subscribers.items(): # this .item is temporary, shoukd be repplaced by [usr_id][coins] for the bot class
                    print("it passed the dictionary test")
                    common.bot.sendMessage(chat_id, "@{screen_name}: {text} {url}".format(
                        screen_name=status.user.screen_name, text=status.text, url="https://twitter.com/%s/status/%s"
                        % (status.user.screen_name, status.id_str)))

            try:
                print("{screen_name}: {text} {url}".format(screen_name=status.user.screen_name, text=status.text,
                                                           url="https://twitter.com/%s/status/%s"
                                                               % (status.user.screen_name, status.id_str)))
            except UnicodeEncodeError:
                pass

    def on_error(self, status_code):
        if status_code == 420:
            print("Reached connection threshold to twitter server. disconnecting")
            return False

        print("error status: {status_code}".format(status_code=status_code))
