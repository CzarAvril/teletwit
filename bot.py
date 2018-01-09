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
import requests
from coinmarketcap import Market
from bs4 import BeautifulSoup
from bittrex.bittrex import Bittrex, API_V2_0
import time



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


# Coin Follow Functions ( **** Figure out how to automate )


def BTC(bot, update):
    coin_list2 = {"BTC": ["Bitcoin", "357312062"], "ETH": "Ethereum", "LTC": "Litecoin", "XRP": "Ripple",
                  "ETC": "Ethereum Classic",
                  "WTC": " Walton Chain", "ICX": "Icon", "CTR": "Centra", "MOD": "Modum", "SNT": "Status"
                  }
    usr_id = update.effective_user.id
    if "BTC" not in common.subscribers[usr_id]['coins']:
        print("tall trees")
        common.subscribers[usr_id]['coins'].append(coin_list2["BTC"][1])
        print("under the if statement1")
        bot.sendMessage(update.message.chat_id, text='You are now following Bitcoin')
        common.saveSubscribers(common.subscribers)


def ETH(bot, update):
    usr_id = update.effective_user.id
    if "ETH" not in common.subscribers[usr_id]['coins']:
        print("tall trees")
        common.subscribers[usr_id]['coins'].append("ETH")
        print("under the if statement1")
        bot.sendMessage(update.message.chat_id, text='You are now following Ethereum')
        common.saveSubscribers(common.subscribers)


# lets try to automate the price function
def price(bot, update):


    ticker_list = {"BTC": ["bitcoin", "357312062"], "ETH": "ethereum", "LTC": "litecoin", "XRP": "ripple",
                  "ETC": "ethereum classic", "WTC": " walton", "ICX": "icon", "CTR": "centra", "MOD": "modum",
                   "SNT": "status", "BCH": "bitcoin cash", "ADA": "cardano", "XEM": "nem", "XLM":"stellar",
                   "IOTA": "miota", "DASH": "dash", "NEO":"neo", "XMR":"monero", "QTUM": "qtum", "BTG": "bitcoin gold",
                   "LSK" : "lisk" , "XRB": "raiblocks", "XVG": "verge" , "SC": "siacoin", "BCN":"bytecoin", "BCC" : "bitconnect",
                   "ZEC": "zcash", "STRAT": "stratis"

                  }
    # get the users text and format it for the Bittrex API
    price_coin_ticker = update.message.text
    coin_ticker = price_coin_ticker[7:]
    ticker_pair = "BTC-"+coin_ticker
    print(coin_ticker, ticker_pair)
    #update.message.reply_text(coin_ticker)
    #update.message.reply_text(ticker_pair)


# CMC api initialization
    coinmarketcap = Market()

# set up Bittrex API
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)

# Constants used to do Calculations
    BTC_summary = my_bittrex.get_marketsummary(market="USDT-BTC") # Access BTC Market info
    btc_price = BTC_summary["result"][0]["Last"]

    #print("before cmc")
    #cmc_summary = coinmarketcap.ticker(coin_ticker)
    #print(cmc_summary)
    #print("passed intiliazation")


# getting Market info from Bittrex API
    summary = my_bittrex.get_marketsummary(market=ticker_pair)
    print(summary)
    if summary['success'] != True :
        coin_ticker2 = ticker_list[coin_ticker]
        print("here cmc")
        cmc_summary = coinmarketcap.ticker(coin_ticker2)
        print("passed intiliazation")
        print(cmc_summary)
        bit_price = cmc_summary[0]['price_usd']
        vol_RO = cmc_summary[0]['24h_volume_usd']
        #vol_RO = "%.2f" % vol
        change_RO = cmc_summary[0]['percent_change_24h']
        price_RO = cmc_summary[0]['price_usd']
        print("CMC price")
        print(btc_price, bit_price, price_RO )
        # update.message.reply_text("Sorry! Coin is not supported by the Hustler Team")

    else:
        bit_price = summary["result"][0]["Last"] # price in BTC
        vol = (summary["result"][0]["Volume"]) * btc_price # Volume in BTC
        prevDay = summary["result"][0]["PrevDay"]
        change = ((bit_price - prevDay) /prevDay) * 100
        change_RO = "%.2f" % change
        price = bit_price * btc_price
        price_RO = "%.2f" % price
        vol_RO = "%.2f" % vol
        print(btc_price, bit_price, price_RO, price, vol)

    # Send info to the bot/user | using Reply or send
    # Reply
    update.message.reply_text("💵*{coin}*💵 \n _price💰:_ *${price}* \n _Vol:_$*{vol}* \n "
                              "_24hr📈:_ *{change}%*  \n [{coin} on Bittrex](Bittrex_price_ETH) ".format(
        coin=coin_ticker,
        price=price_RO, vol=vol_RO, change=change_RO), parse_mode="Markdown")

    # Send
    bot.sendMessage(update.message.chat_id, "💵*{coin}*💵 \n _price💰:_ *${price}* \n _Vol:_$*{vol}* \n "
                                            "_24hr📈:_ *{change}%*  \n [{coin} on Bittrex](Bittrex_price_ETH) ".format(
       coin=coin_ticker,
       price=price_RO, vol=vol_RO, change=change_RO), parse_mode="Markdown")


# ******* Now we define the price function
def priceBTC(bot, update):
    #r = requests.get('https://coins.live/')
    #soup = BeautifulSoup(r.text,'html.parser')
    #results = soup.find_all('td', attrs={"class" : "right-align green-text text-darken-1"})
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
    my_bittrex.get_markets()
    #print(my_bittrex.get_markets())
    #print(my_bittrex.get_ticker(market="BTC-ETH"))
    LTC_summary = my_bittrex.get_marketsummary(market="BTC-ETH")
    BTC_summary = my_bittrex.get_marketsummary(market="USDT-BTC")
    ETH_summary = my_bittrex.get_marketsummary(market="USDT-ETH")
    print(LTC_summary)
    print(BTC_summary)
    bit_price = LTC_summary["result"][0]["Last"]
    high= LTC_summary["result"][0]["High"]
    low = LTC_summary["result"][0]["Low"]
    vol = LTC_summary["result"][0]["Volume"]
    coin = LTC_summary["result"][0]["MarketName"][4:]
    created = LTC_summary["result"][0]["TimeStamp"]
    btc_price = BTC_summary["result"][0]["Last"]
    prevDay = LTC_summary["result"][0]["PrevDay"]
    change = (prevDay - bit_price) / 100
    change_RO = "%.2f" % change
    price = bit_price * btc_price
    price_RO = "%.2f" % price
    vol_RO = "%.2f" % vol
    print(btc_price, bit_price, price_RO, price, high,low,vol)
    print(LTC_summary)
    Bittrex_price_ETH = "https://bittrex.com/Market/Index?MarketName=USDT-ETH"




    #len(results)
    #print(len(results))
    #print(results)
    #print(results[0:500])
    #print(results[0:500])
    # bot.sendMessage(update.message.chat_id, text='*BITCOIN* '
                                                # '\t\n_Price:_' + price +
                                                # '\n_24hr Change:_ ' + high +
                                                # '\n_24hr Volume:_' + vol ,
                    #parse_mode='Markdown')
   # bot.sendMessage(update.message.chat_id, text= coin + price)

    bot.sendMessage(update.message.chat_id, "💵*{coin}*💵 \n _price💰:_ *${price}* \n _Vol:_*{vol}* \n "
                                            "_24hr📈:_ *{change}%*  \n [ETH on Bittrex](Bittrex_price_ETH) ".format(coin = coin,
                                            price=price_RO, vol=vol_RO, change=change_RO, low=low ), parse_mode= "Markdown")








def jump(bot, update):
    print('tall cats')

def follow_coin(bot, update, query):
    print("here")
    usr_id = update.effective_user.id
    user_chat_id = update.inline_query.id
    print("here2")
    coin_list2 = {"BTC": ["Bitcoin", "357312062" ], "ETH": "Ethereum", "LTC": "Litecoin", "XRP": "Ripple", "ETC": "Ethereum Classic",
                 "WTC": " Walton Chain", "ICX": "Icon", "CTR": "Centra", "MOD": "Modum", "SNT": "Status"
                 }
    #if query in coin_list and not common.subscribers[user_chat_id]["coins"]:
    if query in coin_list2.keys():
        print("under the for loop")
        print(common.subscribers[usr_id])
        print(usr_id)
        #if query == ticker and query not in common.subscribers[usr_id]['coins']":
        if query not in common.subscribers[usr_id]['coins']:
                print("tall trees")
                common.subscribers[usr_id]['coins'].append(coin_list2[query][1])
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
    coin_list = {"/BTC": ["Bitcoin"], "/ETH": "Ethereum", "LTC": "Litecoin", "XRP": "Ripple", "ETC": "Ethereum Classic",
                 "WTC": " Walton Chain", "ICX": "Icon", "CTR": "Centra", "MOD": "Modum", "SNT": "Status"
                 }
    print("here we go")
    stuff = '\t' + str(["%s = %s " %(ticker, name) for ticker, name in coin_list.items()])
    coin_list2 = " To Follow a coin, please tap on the coin's Ticker from the list\n "



def inline_caps(bot, update):
    query = update.inline_query.query
    btc = "https://www.google.com/search?q=btc+logo&hl=en&site=imghp&tbm=isch&source=lnt&tbs=isz:m&sa=X&ved=0ahUKEwj92M7h76zYAhUHzIMKHdRPAgsQpwUIIA&biw=1259&bih=676&dpr=1#imgrc=Jef9qHkdlhE2QM:"
    if not query:
        return
    results = list()
    print("did it pass")
    results.append(InlineQueryResultArticle(id = query.upper(),title = 'Cap', thumb_url= btc,
                                            input_message_content = InputTextMessageContent(query.upper())))

    results.append(InlineQueryResultArticle(id= "Bitcoin" , title='Price :$14,5467', url="https://coinmarketcap.com/currencies/bitcoin/", hide_url=True,
                                            input_message_content=InputTextMessageContent( " you are now following:"),
                                             thumb_url="https://faucethub.io/assets/img/coins/BTC.png", description= "24hr Change: 24.45 %" ))

    results.append(InlineQueryResultArticle(id="Ethereum", title='Price :$740.47',
                                            url="https://coinmarketcap.com/currencies/ethereum/", hide_url=True,
                                            input_message_content=InputTextMessageContent(" you are now following:"),
                                            thumb_url="https://eth-price.com/images/coins/ethereum.png",
                                            description="24hr Change: 15.45 %"))
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
    dp.add_handler(CommandHandler("priceBTC", priceBTC))
    dp.add_handler(CommandHandler("price", price))
   # dp.add_handler(CommandHandler("hustlers", hustlers))
    dp.add_handler(CallbackQueryHandler(button))

    # Coin Follow Functions ( NEEEEDs To Be automated)
    dp.add_handler(CommandHandler('BTC', BTC))
    dp.add_handler(CommandHandler('ETH', ETH))


    # Start the Bot
    updater.start_polling(timeout=5)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
