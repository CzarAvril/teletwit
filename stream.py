import teletwit_bot.common as common
import tweepy


class TweetsStreamListener(tweepy.StreamListener):
    def on_connect(self):
        print("Connected to stream")

    def on_status(self, status):
        if status.mention in common.followers:
            print("mentioned")
        elif not status.retweeted and 'RT @'not in status.text and status.in_reply_to_status_id \
                and status.in_reply_to_screen_name and status.in_reply_to_user_id \
                and status.in_reply_to_user_id_str and status.in_reply_to_status_id_str and status.retweet \
                and status.entities:
                # if not hasattr(status, 'retweeted_status'):
                for chat_id in common.subscribers:
                    common.bot.sendMessage(chat_id, "@{screen_name}: {text}".format(screen_name=status.user.screen_name,
                                                                                    text=status.text))

        try:
            print("{screen_name}: {text}".format(screen_name=status.user.screen_name, text=status.text))
        except UnicodeEncodeError:
            pass

    def on_error(self, status_code):
        if status_code == 420:
            print("Reached connection threshold to twitter server. disconnecting")
            return False

        print("error status: {status_code}".format(status_code=status_code))
