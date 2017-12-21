import teletwit_bot.common as common
from telegram.ext import Updater
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
import datetime


# from telegram import Updater

# command handlers
# rough draft of coin list(buttons) that users will be able to choose from
# updates*** create dynamic button creation or even better checklist
def follow(bot, update):
    keyboard = [[InlineKeyboardButton("Walton (WTC)", callback_data='Walton'),
                 InlineKeyboardButton("Ether (ETH)", callback_data='Ether')],

                [InlineKeyboardButton("Bitcoin (BTC)", callback_data='Bitcoin'),
                 InlineKeyboardButton("Centra (CTR)", callback_data='Centra')],

                [InlineKeyboardButton("Ethos (BQX)", callback_data='Ethos'),
                 InlineKeyboardButton("MIOTA (IOTA)", callback_data='MIOTA')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please Select the coins you would like to be updated on :', reply_markup=reply_markup)


def button(bot, update):

    query = update.callback_query

    bot.edit_message_text(text="You are now following: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    answer = "{}".format(query.data)
    answers = {"Walton":"903434091650883586", "Ether":2312333412, "Bitcoin":357312062, "Centra":884936655437791232,
              "Ethos":"862007728956485632", "MIOTA":3992601857}

# ****** this is the place where i think the error is , i want the dictionary to function like a data frame
 # yes, atom doesnt have input either, for the elif statement if the coloumn is there then it adds the value to the last postion
    # kinna like pop and push, you following ?
    # right now
    # that will change later, just trying to get the basic function down
    # you can run it , on terminal
    # welllll, since the bot is in different files am not sure
    # if it was one file, but the directory should run on terminal right ?
    # run the main
    # watch what happens when i run the bot and try to follow
    # am going to to unssubscribe, then subscribe,then follow a coin or two
     # watch what happens to the subscriber.json file
    # i deliberatly deleted the other coin coloumns from the json file
    # so i was able to subscribe
    # you can see my info, cause i printed it out from the subscribe function
    # you deh ?
    # watch the json file
    # i followed walton but nothing happened
    # strange, it should work, but now am going to follow coins that are not in the dictionary coloumns
    # it will add the coloumns and populte it, i want that behaviour, but i dont want it to keep adding the same coin if i already changed the value
    # you get what am saying ?
    # i followed ether, and you can see
    # it added the colomn am goin to follow again, it will add it again not the colomn but the value ---- i dont want that
    # i want multple values, but not for the same person, not for the same user id or name, you check, i want each coin to be a tru or false
    # yep that will make it easy for later, when we doing the machine learning, its called hotspotting the data
    # you still seeing my screen ?
    # you have headphones? can i talk?

    def create_Hustler(bot, update):
        for id in range(len(common.subscribers['chat_id'])):
            if answers[answer] not in common.subscribers.keys():
                common.subscribers[answers[answer]] = [1]
                common.saveSubscribers(common.subscribers)
                print("testing bitches")
            elif common.subscribers[answers[answer]][-1] != 0:
                print("else bitches")
                common.subscribers[answers[answer]].append(1)
                common.saveSubscribers(common.subscribers)
                print(" working bitch?")
            else:
                common.subscribers[answers[answer]].append(1)
                common.saveSubscribers(common.subscribers)
                print("are we working bitch?")

                # common.subscribers['chat_id'][id]

    create_Hustler(bot, update)


def subscribe(bot, update):
    if update.message.chat_id not in common.subscribers["chat_id"]:
        common.subscribers["chat_id"].append(update.message.chat_id)
        common.subscribers["first_name"].append(update.message.from_user.first_name)
        common.subscribers["last_name"].append(update.message.from_user.last_name)
        #common.subscribers["username"].append(str(update.message.from_user.username))
        #common.subscribers["user_id"].append(update.message.from_user.id)
        print(str(update.message.from_user.first_name))
        print(str(update.message.from_user.id))
        bot.sendMessage(update.message.chat_id, text='Subscribed!')
        common.saveSubscribers(common.subscribers)

    else:
        bot.sendMessage(update.message.chat_id, text='Already Subscribed!')


def unsubscribe(bot, update):
    if update.message.chat_id in common.subscribers["chat_id"]:
        common.subscribers["chat_id"].remove(update.message.chat_id)
        #common.subscribers["sub_date"].remove(str(update.message.date))
        common.subscribers["first_name"].remove(update.message.from_user.first_name)
        common.subscribers["last_name"].remove(update.message.from_user.last_name)
        #common.subscribers["username"].remove(update.message.from_user.username)
        #common.subscribers["user_id"].remove(update.message.from_user.id)
        bot.sendMessage(update.message.chat_id, text='Unsubscribed!')
        common.saveSubscribers(common.subscribers)
    else:
        bot.sendMessage(update.message.chat_id, text='You need to subscribe first!')


def bot_main(bot_token=""):
    # Create the EventHandler and pass it your bot's token.
   # updater = Updater(token=bot_token)
    updater = Updater(token="474430462:AAEfUyEsazaBoGE30jcYBa03kPFnShrFQ68")


    common.bot = updater.bot
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('follow', follow))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))
    dp.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling(timeout=5)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
