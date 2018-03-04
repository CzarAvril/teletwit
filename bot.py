import teletwit_bot.main as main
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
import pandas as pd
import numpy as np
from bittrex.bittrex import Bittrex, API_V2_0
import time
from binance.client import Client

# ******** dont forget to add keys!!!! ***************
#Client = Client(main.binance_api_key, main.binance_api_secret)



# connect the binace API
binance_market_summary = Client.get_ticker()
#binance_data = pd.DataFrame(binance_market_summary)










# this was in the bot main towards the bottom of this page
updater = Updater(token="474430462:AAEfUyEsazaBoGE30jcYBa03kPFnShrFQ68")
jobber = updater.job_queue





def subscribe(bot, update):
    # pull basic user info
    usr_id = update.effective_user.id  # user id
    usr_fname = update.effective_user.first_name  # user first name
    usr_lname = update.effective_user.last_name  # user last name

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

    # Add follow specific coin funtions later??? refer to programming notes
    # Coin Follow Functions ( **** Figure out how to automate )


def price_updater(bot, job):
    # use endpoint to extract the json object then put into Pandas Dataframe for further processing
    r = requests.get("https://bittrex.com/api/v1.1/public/getmarketsummaries")
    bittrex_data = r.json()

    # CMC api initialization
    coinmarketcap = Market()
    market_summary = coinmarketcap.ticker(limit=200)

    # add cmc to a dataframe
    cmc_df = pd.DataFrame(market_summary)

    ticker_list = {"ETH": "ethereum", "LTC": "litecoin", "XRP": "ripple", "CTR": "centra", "MOD": "modum",
                   "WTC": "walton", "ETC": "ethereum-classic"
                   }

    # set up Bittrex API
    # my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)

    # Constants used to do Calculations
    # BTC_summary = my_bittrex.get_marketsummary(market="USDT-BTC")  # Access BTC Market info
    # btc_price = BTC_summary["result"][0]["Last"]

    # price_list = {}
    price_list2 = ""
    for ticker in ticker_list.keys():
        if binance_price_checker(ticker_list, ticker,binance_market_summary) != "NP":
            price_list2 = binance_price_checker(ticker_list,ticker,binance_market_summary)
        elif bittrex_price_checker(ticker_list, ticker, bittrex_data) != "NP":
            price_list2 = bittrex_price_checker(ticker_list, ticker, bittrex_data)
        elif cmc_price_checker(ticker_list, ticker, cmc_df) != "NP":
            price_list2 = cmc_price_checker(ticker_list, ticker, cmc_df)

        bot.send_message(chat_id='275079674', text=price_list2, parse_mode="Markdown")


jobber.run_repeating(price_updater, interval=300, first=0)


def bittrex_price_checker(ticker_list, ticker, bittrex_data):
    # add Bittrex data to a Dataframe
    bittrex_df = pd.DataFrame(bittrex_data['result'])

    # refine data for relevant columns and btc price
    slim_bittrex_df = bittrex_df[["MarketName", "Last", 'Volume', 'PrevDay']]
    slim_bit_df = slim_bittrex_df.set_index('MarketName', drop=False)
    btc_price = slim_bit_df['Last']['USDT-BTC']

    # rudimentary way for gathering info, should make a column for each "change" and do computation in there
    ticker_pair = "BTC-" + ticker  # reformat for the Bittrex Api
    if ticker_pair not in set(slim_bit_df.MarketName):
        return "NP"
    coin_name = ticker_list[ticker]
    last = slim_bit_df['Last'][ticker_pair]
    volume = slim_bit_df['Volume'][ticker_pair]
    prevday = slim_bit_df['PrevDay'][ticker_pair]
    price_usd = last * btc_price
    price_RO = "%.2f" % price_usd
    vol = volume * btc_price
    vol_RO = "%.2f" % vol
    change = ((last - prevday) / prevday) * 100
    change_RO = "%.2f" % change
    coin_display_format = coin_name + "/" + ticker + "\n"

    # check for 24hr pump and change emoji
    chart_icon = pump_24hr(change)

    price_list = "💵*{coin}*\n _price💰:_ *${price}*\n _Vol:_💲*{vol}*\n _24hr{chart}:_ *{change}%* " \
                 "\n [{coin_name} on Bittrex](Bittrex_price_ETH)\n\n".format(coin=coin_display_format, price=price_RO,
                                                                             vol=vol_RO, change=change_RO,
                                                                             chart=chart_icon, coin_name=coin_name)
    return price_list


def cmc_price_checker(ticker_list, ticker, cmc_df):
    slim_cmcap_df = cmc_df[["id", "symbol", "price_usd", "price_btc", "percent_change_24h", "24h_volume_usd"]]
    slim_cmc_df = slim_cmcap_df.set_index('symbol', drop=False)

    if ticker not in slim_cmc_df.symbol:
        # print(slim_cmc_df)
        return "NP"
    coin_name = ticker_list[ticker]
    price_usd = float(slim_cmc_df["price_usd"][ticker])
    price_RO = round(price_usd, 2)
    vol = float(slim_cmc_df["24h_volume_usd"][ticker])
    vol_RO = round(vol, 2)
    change = float(slim_cmc_df["percent_change_24h"][ticker])
    change_RO = round(change, 2)
    coin_display_format = coin_name + "/" + ticker + "\n"

    # check for 24hr pump and change emoji
    chart_icon = pump_24hr(change)

    price_list = "💵*{coin}*\n _price💰:_ *${price}*\n _Vol:_💲*{vol}*\n _24hr{chart}:_ *{change}%* " \
                 "\n [{coin_name} on CoinMarketCap](Bittrex_price_ETH)\n\n".format(coin=coin_display_format,
                                                                                   price=price_RO, vol=vol_RO,
                                                                                   change=change_RO, chart=chart_icon,
                                                                                   coin_name=coin_name)
    return price_list


def binance_price_checker(ticker_list, ticker, binance_market_summary):
    binance_data = pd.DataFrame(binance_market_summary)

    ticker_pair2 = ticker + "BTC"
    slim_binance_data = binance_data[['symbol', "lastPrice", "priceChangePercent", "volume"]]
    slim_binance_df = slim_binance_data.set_index('symbol', drop=False)
    btc_price_bin = float(slim_binance_df["lastPrice"]["BTCUSDT"])

    if ticker_pair2 not in slim_binance_df.symbol:
        return "NP"
    coin_name = ticker_list[ticker]
    #last = float(slim_binance_df["lastPrice"][ticker_pair2])
    volume = float(slim_binance_df["volume"][ticker_pair2])
    #price_usd = last * btc_price_bin
    #price_RO = round(price_usd , 2)
    price_RO = round((float(slim_binance_df["lastPrice"][ticker_pair2]) * btc_price_bin), 2)
    vol = volume * btc_price_bin
    vol_RO = "%.2f" % vol
    change = float(slim_binance_df["priceChangePercent"][ticker_pair2])
    change_RO = "%.2f" % change
    coin_display_format = coin_name + "/" + ticker + "\n"

    # check for 24hr pump and change emoji
    chart_icon = pump_24hr(change)

    price_list = "💵*{coin}* _price💰:_ *${price}*\n _Vol:_💲*{vol}*\n _24hr{chart}:_ *{change}%* " \
                 "\n [{coin_name} on Binance](Bittrex_price_ETH)\n\n".format(coin=coin_display_format, price=price_RO,
                                                                             vol=vol_RO, change=change_RO,
                                                                             chart=chart_icon, coin_name=coin_name)
    return price_list


def pump_24hr(change):
    icon = "📈"
    if change < 0:
        icon = "📉"
    elif change >= 40:
        icon = "🤑"
    else:
        icon = "📈"
    return icon


# lets try to automate the price function
def price(bot, update):
    # this list is used to cross reference the "symbol" to the coins name,
    # it should be replaced by a more efficicent way, maybe the CMC dataframe????
    ticker_list = {"BTC": ["bitcoin", "357312062"], "ETH": "ethereum", "LTC": "litecoin", "XRP": "ripple",
                   "ETC": "ethereum classic", "WTC": " walton", "ICX": "icon", "CTR": "centra", "MOD": "modum",
                   "SNT": "status", "BCH": "bitcoin cash", "ADA": "cardano", "XEM": "nem", "XLM": "stellar",
                   "IOTA": "miota", "DASH": "dash", "NEO": "neo", "XMR": "monero", "QTUM": "qtum",
                   "BTG": "bitcoin gold",
                   "LSK": "lisk", "XRB": "raiblocks", "XVG": "verge", "SC": "siacoin", "BCN": "bytecoin",
                   "BCC": "bitconnect", "ZEC": "zcash", "STRAT": "stratis"
                   }

    # get the users text and format it for the Bittrex API
    price_coin_ticker = update.message.text  # what the user enters, with the /price
    coin_ticker = price_coin_ticker[7:]  # we slice the coins ticker/symbol
    ticker_pair = "BTC-" + coin_ticker  # reformat for the Bittrex Api
    print("Fetching %s, for the coin %s " % (coin_ticker, ticker_pair))

    # set up Bittrex API
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)

    # CMC api initialization
    coinmarketcap = Market()

    # Constants used to do Calculations
    BTC_summary = my_bittrex.get_marketsummary(market="USDT-BTC")  # Access BTC Market info
    btc_price = BTC_summary["result"][0]["Last"]

    # print("before cmc")
    # cmc_summary = coinmarketcap.ticker(coin_ticker)
    # print(cmc_summary)
    # print("passed intiliazation")

    # getting Market info from Bittrex API
    summary = my_bittrex.get_marketsummary(market=ticker_pair)
    print(summary)
    if summary['success'] != True:
        coin_ticker2 = ticker_list[coin_ticker]
        print("here cmc")
        cmc_summary = coinmarketcap.ticker(coin_ticker2)
        print("passed intiliazation")
        print(cmc_summary)
        bit_price = cmc_summary[0]['price_usd']
        vol_RO = cmc_summary[0]['24h_volume_usd']
        # vol_RO = "%.2f" % vol
        change_RO = cmc_summary[0]['percent_change_24h']
        price_RO = cmc_summary[0]['price_usd']
        print("CMC price")
        print(btc_price, bit_price, price_RO)
        # update.message.reply_text("Sorry! Coin is not supported by the Hustler Team")

    else:
        bit_price = summary["result"][0]["Last"]  # price in BTC
        vol = (summary["result"][0]["Volume"]) * btc_price  # Volume in BTC
        prevDay = summary["result"][0]["PrevDay"]
        change = ((bit_price - prevDay) / prevDay) * 100
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
    # r = requests.get('https://coins.live/')
    # soup = BeautifulSoup(r.text,'html.parser')
    # results = soup.find_all('td', attrs={"class" : "right-align green-text text-darken-1"})
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
    my_bittrex.get_markets()
    # print(my_bittrex.get_markets())
    # print(my_bittrex.get_ticker(market="BTC-ETH"))
    LTC_summary = my_bittrex.get_marketsummary(market="BTC-ETH")
    BTC_summary = my_bittrex.get_marketsummary(market="USDT-BTC")
    ETH_summary = my_bittrex.get_marketsummary(market="USDT-ETH")
    print(LTC_summary)
    print(BTC_summary)
    bit_price = LTC_summary["result"][0]["Last"]
    high = LTC_summary["result"][0]["High"]
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
    print(btc_price, bit_price, price_RO, price, high, low, vol)
    print(LTC_summary)
    Bittrex_price_ETH = "https://bittrex.com/Market/Index?MarketName=USDT-ETH"

    # len(results)
    # print(len(results))
    # print(results)
    # print(results[0:500])
    # print(results[0:500])
    # bot.sendMessage(update.message.chat_id, text='*BITCOIN* '
    # '\t\n_Price:_' + price +
    # '\n_24hr Change:_ ' + high +
    # '\n_24hr Volume:_' + vol ,
    # parse_mode='Markdown')
    # bot.sendMessage(update.message.chat_id, text= coin + price)

    bot.sendMessage(update.message.chat_id, "💵*{coin}*💵 \n _price💰:_ *${price}* \n _Vol:_*{vol}* \n "
                                            "_24hr📈:_ *{change}%*  \n [ETH on Bittrex](Bittrex_price_ETH) ".format(
        coin=coin,
        price=price_RO, vol=vol_RO, change=change_RO, low=low), parse_mode="Markdown")


def jump(bot, update):
    print('tall cats')


def follow_coin(bot, update, query):
    print("here")
    usr_id = update.effective_user.id
    user_chat_id = update.inline_query.id
    print("here2")
    coin_list2 = {"BTC": ["Bitcoin", "357312062"], "ETH": "Ethereum", "LTC": "Litecoin", "XRP": "Ripple",
                  "ETC": "Ethereum Classic",
                  "WTC": " Walton Chain", "ICX": "Icon", "CTR": "Centra", "MOD": "Modum", "SNT": "Status"
                  }
    # if query in coin_list and not common.subscribers[user_chat_id]["coins"]:
    if query in coin_list2.keys():
        print("under the for loop")
        print(common.subscribers[usr_id])
        print(usr_id)
        # if query == ticker and query not in common.subscribers[usr_id]['coins']":
        if query not in common.subscribers[usr_id]['coins']:
            print("tall trees")
            common.subscribers[usr_id]['coins'].append(coin_list2[query][1])
            print("under the if statement1")
        # should send message saying the ticker used isnt correct
        else:
            # common.subscribers[usr_id]['coins'].append(coin_list[query])
            print("under the if statement")
            # common.subscribers[usr_id]['coins'].append(coin_list[query])
            print("here3")
            print(user_chat_id)
            print(usr_id)
            # common.saveSubscribers(common.subscribers)


def coinlist(bot, update, ):
    coin_list = {"/BTC": ["Bitcoin"], "/ETH": "Ethereum", "LTC": "Litecoin", "XRP": "Ripple", "ETC": "Ethereum Classic",
                 "WTC": " Walton Chain", "ICX": "Icon", "CTR": "Centra", "MOD": "Modum", "SNT": "Status"
                 }
    print("here we go")
    stuff = '\t' + str(["%s = %s " % (ticker, name) for ticker, name in coin_list.items()])
    coin_list2 = " To Follow a coin, please tap on the coin's Ticker from the list\n "


def inline_caps(bot, update):
    # lets feed the inline bot the CMC Api data so user can quickly search for price and change without sending a message
    # in the group, we are going to use the same variables from the /price function, later we will refactor and add a class
    # lets just make it work first

    # Dict to cross reference users input and ge the correct coin name or ticker signal

    ticker_list = {"BTC": "bitcoin", "ETH": "ethereum", "LTC": "litecoin", "XRP": "ripple",
                   "ETC": "ethereum classic", "WTC": " walton", "ICX": "icon", "CTR": "centra", "MOD": "modum",
                   "SNT": "status", "BCH": "bitcoin cash", "ADA": "cardano", "XEM": "nem", "XLM": "stellar",
                   "IOTA": "miota", "DASH": "dash", "NEO": "neo", "XMR": "monero", "QTUM": "qtum",
                   "BTG": "bitcoin gold",
                   "LSK": "lisk", "XRB": "raiblocks", "XVG": "verge", "SC": "siacoin", "BCN": "bytecoin",
                   "BCC": "bitconnect",
                   "ZEC": "zcash", "STRAT": "stratis"

                   }

    ticker_list2 = {"BTC": "bitcoin", "ETH": "ethereum", "LTC": "litecoin", "XRP": "ripple", "WTC": "walton",
                    "ICX": "icon", "CTR": "centra", "MOD": "modum", "SNT": "status", "BCH": "bitcoin-cash",
                    "ADA": "cardano"
                    }

    # CMC api initialization
    coinmarketcap = Market()

    # ********* Using Pandas to easily manipulate the data

    # Create market summary object with a limit of 100 / or not
    market_summary = coinmarketcap.ticker(limit=100)
    cmc_df = pd.DataFrame(market_summary)

    # now we pull the relevant columns from the dataset , PS i Jupyter Notebook to help visualize this
    slim_cmc_df = cmc_df[
        ["percent_change_24h", "id", "24h_volume_usd", "price_usd", "price_btc", "symbol"]].sort_values(
        "percent_change_24h", ascending=False)

    # now that we have a new dataframe from our original with the data we need, we are now going to add a new index
    slim_cmc_df = slim_cmc_df.head(n=10)
    trending = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
    slim_cmc_df.index = trending
    # slim_cmc_df

    # now we iterate through the dataframe

    query = update.inline_query.query
    if not query:
        return
    results = list()
    print("did it pass")
    for index, row in slim_cmc_df.iterrows():
        coin_key = row['id']
        symbol = row['symbol']
        change_RO = row['percent_change_24h']
        price_RO = row['price_usd']
        vol_RO = row['24h_volume_usd']
        url = "https://coinmarketcap.com/currencies/"
        coin_url = url + coin_key + "/"
        icon_url = "https://files.coinmarketcap.com/static/img/coins/32x32/"
        thumb = icon_url + coin_key + ".png"
        title_price = coin_key.title() + "/" + symbol + ": $" + price_RO + "💵"
        desc_coin = "24hr📈:" + change_RO + "%" + "\n 24hr Vol:" + "$" + vol_RO
        results.append(InlineQueryResultArticle(id=coin_key, title=title_price, url=coin_url, hide_url=True,
                                                description=desc_coin, thumb_url=thumb,
                                                input_message_content=InputTextMessageContent(
                                                    " you are now following:")))

    # ********** Add search feature for CoinMArket cap based on users input query
    # save code at the bottom for that implementation

    # pulling data and adding it to DF for easy manipulation

    # market_summary = coinmarketcap.ticker()
    # cmc_df =pd.DataFrame(market_summary)

    # print(cmc_summary)

    # cmc_summary = coinmarketcap.ticker("bitcoin")
    # bit_price = cmc_summary[0]['price_usd']
    # vol_RO = cmc_summary[0]['24h_volume_usd']
    # vol_RO = "%.2f" % vol
    # change_RO = cmc_summary[0]['percent_change_24h']
    # price_RO = cmc_summary[0]['price_usd']

    # query = update.inline_query.query
    # btc = "https://www.google.com/search?q=btc+logo&hl=en&site=imghp&tbm=isch&source=lnt&tbs=isz:m&sa=X&ved=0ahUKEwj92M7h76zYAhUHzIMKHdRPAgsQpwUIIA&biw=1259&bih=676&dpr=1#imgrc=Jef9qHkdlhE2QM:"
    # if not query:
    #   return
    # results = list()
    # print("did it pass")
    # for coin_key in ticker_list2:
    #   cmc_summary = coinmarketcap.ticker(ticker_list2[coin_key])
    #  url = "https://coinmarketcap.com/currencies/"
    # coin_url = url+ticker_list2[coin_key]+"/"
    #  change_RO = cmc_summary[0]['percent_change_24h']
    # price_RO = cmc_summary[0]['price_usd']
    # vol_RO = cmc_summary[0]['24h_volume_usd']
    # icon_url = "https://files.coinmarketcap.com/static/img/coins/32x32/"
    # thumb = icon_url+ticker_list2[coin_key]+".png"
    # title_price = ticker_list2[coin_key].title()+": $"+price_RO+"💵"
    # desc_coin = "24hr📈:"+change_RO +"\n 24hr Vol:"+vol_RO
    # results.append(InlineQueryResultArticle(id=coin_key, title=title_price, url=coin_url, hide_url=True,
    #                           input_message_content=InputTextMessageContent(" you are now following:"),
    #                          description=desc_coin, thumb_url=thumb))

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
        "Ether(ETH)": 2312333412, "Bitcoin(BTC)": 357312062, "WanChain": 883984505119297536,
        "Centra(CTR)": 884936655437791232, "Ethos(BQX)": 862007728956485632, "MIOTA(IOTA)": 3992601857,
        "Icon(ICX)": 889691121000996864, "Walton(WTC)": 903434091650883586, "UnikoinGold": 2946825834,
        "Status(SNT)": 774689518767181828

    }
    print("here")
    # keyboard = [KeyboardButton(s) for s in answers.keys()]

    # for coin, id in answers.items():
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
    # reply_markup = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=True, resize_keyboard=True)
    # reply_markup = ReplyKeyboardRemove()

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
    # instantiate the job queue "jobber"
    # updater = Updater(token="474430462:AAEfUyEsazaBoGE30jcYBa03kPFnShrFQ68")
    # jobber = updater.job_queue

    common.bot = updater.bot
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    price_handler = CommandHandler(" price updater", price_updater)
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
    # dp.add_handler(CommandHandler('BTC', BTC))
    # dp.add_handler(CommandHandler('ETH', ETH))

    # Start the Bot
    updater.start_polling(timeout=5)

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
