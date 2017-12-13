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

     # create a function that checks if the user is in the list already
    def create_Hustler(bot, update):
        for id in common.subscribers['chat_id']:
            if answer in answers.keys():
                common.subscribers[answers[answer]] = []
                if common.subscribers[answers[answer]] != 1:
                    common.subscribers[answers[answer]].append(1)
                common.saveSubscribers(common.subscribers)
                print("presnet")
                #common.subscribers[answers[answer]].append("1")
                common.saveSubscribers(common.subscribers)
                print(" value added")
    create_Hustler(bot, update)

    # list of numbers and Names: Walton = 903434091650883586, Ethereum = 2312333412, Bitcoin = 357312062,
    # Centra = 884936655437791232, Ethos = 862007728956485632, MIOTA = 3992601857


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
