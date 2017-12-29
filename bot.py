import teletwit_bot.common as common
from telegram.ext import Updater
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
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

    usr_id = update.effective_user.id  # user id
    usr_fname = update.effective_user.first_name  # user first name
    usr_lname = update.effective_user.last_name   # user last name

    if usr_id not in common.subscribers.keys():
        common.subscribers[usr_id] = {"user_id": usr_id,
                                      "first_name": usr_fname,
                                      "user_name": usr_lname,
                                      "coins": []
                                      }
        bot.sendMessage(update.message.chat_id, text='Subscribed!')
        bot.sendMessage(update.message.chat_id, text='Thank you for subscribing!'
                                                     'To see a current list of coins that you can now follow and how '
                                                     'you can do so please use the /coinlist command ')

    else:
        bot.sendMessage(update.message.chat_id, text='Already Subscribed!')
        bot.sendMessage(update.message.chat_id, text='If you would like to follow a new coin use the "/follow" command')


def jump():
    print('tall cats')

def follow_coin(bot, update, query):
    print("here")
    usr_id = update.effective_user.id
    user_chat_id = update.inline_query.id
    print("here2")
    coin_list = {"BTC": "Bitcoin", "ETH": "Ethereum", "LTC": "Litecoin", "XRP": "Ripple", "ETC": "Ethereum Classic",
                 "WTC": " Walton Chain", "ICX": "Icon", "CTR": "Centra", "MOD": "Modum", "SNT": "Status"
                 }
    #if query in coin_list and not common.subscribers[user_chat_id]["coins"]:
    if query in coin_list.keys():
        print("under the for loop")
        print(common.subscribers[usr_id])
        print(usr_id)
        #if query == ticker and query not in common.subscribers[usr_id]['coins']":
        if query not in common.subscribers[usr_id]['coins']:
                print("tall trees")
                common.subscribers[usr_id]['coins'].append(coin_list[query])
                print("under the if statement1")
           # should send message saying the ticker used isnt correct
        else:
            #common.subscribers[usr_id]['coins'].append(coin_list[query])
            print("under the if statement")
            #common.subscribers[usr_id]['coins'].append(coin_list[query])
            print("here3")
            print(user_chat_id)
            print(usr_id)
            #common.saveSubscribers(common.subscribers)


def coinlist(bot, update,):
    coin_list = {"BTC": "Bitcoin", "ETH": "Ethereum", "LTC": "Litecoin", "XRP": "Ripple", "ETC": "Ethereum Classic",
                 "WTC": " Walton Chain", "ICX": "Icon", "CTR": "Centra", "MOD": "Modum", "SNT": "Status"
                 }
    print("here we go")
    stuff = '\t' + str(["%s = %s " %(ticker, name) for ticker, name in coin_list.items()])
    coin_list2 = " To Follow a coin, please type @CryptoHuslter_bot + the coin's Ticker from the list\n "

    bot.sendMessage(update.message.chat_id, text=coin_list2 + stuff)



def inline_caps(bot, update):
    query = update.inline_query.query
    btc = "https://www.google.com/search?q=btc+logo&hl=en&site=imghp&tbm=isch&source=lnt&tbs=isz:m&sa=X&ved=0ahUKEwj92M7h76zYAhUHzIMKHdRPAgsQpwUIIA&biw=1259&bih=676&dpr=1#imgrc=Jef9qHkdlhE2QM:"
    if not query:
        return
    results = list()
    print("did it pass")
    results.append(InlineQueryResultArticle(id = query.upper(),title = 'Caps', thumb_url= btc,
                                            input_message_content = InputTextMessageContent(query.upper())))
    print("there1")
    results.append(InlineQueryResultArticle(id= "follow" , title='follow',
                                            input_message_content=InputTextMessageContent( message_text= " you are now following:" + query)))
    print("are we here")

    bot.answer_inline_query(update.inline_query.id, results)

    print("passed")







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
    chat_id2 = query.message.chat_id
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
        "Ether(ETH)": 2312333412, "Bitcoin(BTC)": 357312062,"WanChain": 883984505119297536,
        "Centra(CTR)": 884936655437791232, "Ethos(BQX)": 862007728956485632, "MIOTA(IOTA)": 3992601857,
        "Icon(ICX)": 889691121000996864,  "Walton(WTC)": 903434091650883586, "UnikoinGold": 2946825834,
        "Status(SNT)": 774689518767181828

    }
    print("here")
    #keyboard = [KeyboardButton(s) for s in answers.keys()]

    #for coin, id in answers.items():
       # print('tere')
       # keyboard2 = [[InlineKeyboardButton(coin, callback_data=id)]]

    keyboard2 = [[InlineKeyboardButton(coin, callback_data=id), ] for coin, id in answers.items()]


    keyboard = [[InlineKeyboardButton("Walton (WTC)", callback_data='Walton'),
                InlineKeyboardButton("Ether (ETH)", callback_data='Ether')],

              [InlineKeyboardButton("Bitcoin (BTC)", callback_data='Bitcoin'),
               InlineKeyboardButton("Centra (CTR)", callback_data='Centra')],

               [InlineKeyboardButton("Ethos (BQX)", callback_data='Ethos'),
                InlineKeyboardButton("MIOTA (IOTA)", callback_data='MIOTA')]


                ]

    keyboard3 = [[InlineKeyboardButton(coin, callback_data=id),
                 InlineKeyboardButton(coin, callback_data=id)]


                for coin, id in answers.items()]

    reply_markup = InlineKeyboardMarkup(keyboard2)
    #reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True, resize_keyboard=True)
    #reply_markup = ReplyKeyboardRemove()

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
    inline_caps_handler = InlineQueryHandler(inline_caps)
    dp.add_handler(inline_caps_handler)
    dp.add_handler(CommandHandler('coinlist', coinlist))
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
