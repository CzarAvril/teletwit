import teletwit_bot.common as common
# import teletwit_bot.main as main
import tweepy


class TweetsStreamListener(tweepy.StreamListener):
    def on_connect(self):
        print("Connected to stream")

    def on_status(self, status):
        print("waiting for tweets....")
        if not status.entities["user_mentions"]:
            print("testing")
            for chat_id in common.subscribers:
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
