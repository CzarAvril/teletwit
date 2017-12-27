import teletwit_bot.common as common
from telegram.ext import Updater
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
import datetime


# from telegram import Updater

# command handlers
# rough draft of coin list(buttons) that users will be able to choose from
# updates*** create dynamic button creation or even better checklist

def subscribe(bot, update):
    last_name = update.message.from_user.last_name
    if update.message.chat_id not in common.subscribers.keys():
        common.subscribers[update.message.chat_id] = {"chat_id": update.message.chat_id,
                                                      "first_name": update.message.from_user.first_name,
                                                      "user_name": last_name,
                                                      "coins": []
                                                      }

        bot.sendMessage(update.message.chat_id, text='Subscribed!')
        follow(bot, update)

    else:
        bot.sendMessage(update.message.chat_id, text='Already Subscribed!')
        bot.sendMessage(update.message.chat_id, text='If you would like to follow a new coin use the "/follow" command')


def unsubscribe(bot, update, chat_id):
    print("here")
    if chat_id in common.subscribers.keys():
        print("there")
        common.subscribers.remove(update.message.chat_id)
        bot.sendMessage(update.message.chat_id, text='Unsubscribed!')
        common.saveSubscribers(common.subscribers)
    else:
        bot.sendMessage(update.message.chat_id, text='You need to subscribe first!')


def hustlers(bot, update, answer, query):
    chat_id = query.message.chat_id
    print(chat_id)
    bot.sendMessage(chat_id, text='hello!')
    if answer not in common.subscribers[chat_id].keys():
            print("did it pass")
            common.subscribers[chat_id]["coins"].append(answer)
            print("getting there")
            common.saveSubscribers(common.subscribers)


def follow(bot, update):
    answers = {
        "Walton(WTC)": 903434091650883586, "Ether(ETH)": 2312333412, "Bitcoin(BTC)": 357312062,
        "Centra(CTR)": 884936655437791232, "Ethos(BQX)": 862007728956485632, "MIOTA(IOTA)": 3992601857,
        "Icon(ICX)": 889691121000996864, "WanChain": 883984505119297536, "UnikoinGold": 2946825834,
        "Status(SNT)": 774689518767181828

    }

    answers2 = {
        "Ether(ETH)": 2312333412, "Bitcoin(BTC)": 357312062, "WanChain": 883984505119297536,
        "Centra(CTR)": 884936655437791232, "Ethos(BQX)": 862007728956485632, "MIOTA(IOTA)": 3992601857,
        "Icon(ICX)": 889691121000996864,  "Walton(WTC)": 903434091650883586, "UnikoinGold": 2946825834,
        "Status(SNT)": 774689518767181828

    }
    print("here")
    #keyboard = [KeyboardButton(s) for s in answers.keys()]

    #for coin, id in answers.items():
       # print('tere')
       # keyboard2 = [[InlineKeyboardButton(coin, callback_data=id)]]

    keyboard2 = [[KeyboardButton(coin, callback_data=id)] for coin, id in answers.items()]


    keyboard = [[InlineKeyboardButton("Walton (WTC)", callback_data='Walton'),
                InlineKeyboardButton("Ether (ETH)", callback_data='Ether')],

              [InlineKeyboardButton("Bitcoin (BTC)", callback_data='Bitcoin'),
               InlineKeyboardButton("Centra (CTR)", callback_data='Centra')],

               [InlineKeyboardButton("Ethos (BQX)", callback_data='Ethos'),
                InlineKeyboardButton("MIOTA (IOTA)", callback_data='MIOTA')]


                ]

    keyboard3 = [[InlineKeyboardButton(coin, callback_data=id), InlineKeyboardButton(coin2, callback_data=id2)] for coin, id in answers.items()
               and for coin2, id2 in answers2.items()]




    #reply_markup = InlineKeyboardMarkup(keyboard2)
    reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True, resize_keyboard=True)

    update.message.reply_text('Please Select the coins you would like to be updated on :', reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="You are now following: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)

    answer = "{}".format(query.data)


    print("cat")

    hustlers(bot, update, answer, query)


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
   # dp.add_handler(CommandHandler("hustlers", hustlers))
    dp.add_handler(CallbackQueryHandler(button))


    # Start the Bot
    updater.start_polling(timeout=5)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
