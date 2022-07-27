from cgitb import reset
from genericpath import getsize
from pickle import FALSE, TRUE
import time
import os
import sys
import logging
from tokenize import String
# from tkinter.messagebox import NO
import traceback
###
# from matplotlib.pyplot import hist
import upbit_api
import pyupbit
import telegram
from datetime import datetime, timedelta
from datetime import date
import pandas as pd
import openpyxl
import bitget.mix.market_api as market
import bitget.mix.account_api as accounts
import bitget.mix.position_api as position
import bitget.mix.order_api as order
import bitget.mix.plan_api as plan
import bitget.mix.trace_api as trace
import datetime as pydatetime
import schedule
import math
import time
import pandas as pd
import requests
import pandas as pd
import time
import webbrowser
import numpy as np

access = "xwdEMciw0PeGRfpA8xMaVtnVGmFPFxTR6dkKCnUQ"
secret = "UOxwdGYVZflyTCbMwrlrzB0Ey44GGxSLl70xp8A4"
teleToken = "5175235797:AAFCLeiEULzRZBHt_9QFypaXtVq9w6LcYbQ"
chatId = "5046654369"

bot = telegram.Bot(token=teleToken)

# updates = bot.getUpdates()
# for u in updates:
#     if u is None:
#         continue
#     if u.message is None:
#         continue
#     if u.message['chat'] is None:
#         continue
#     print(u.message['chat']['id'])

# text = 'asdasdsd'
# bot.sendMessage(chat_id = chatId, text=text)

# #승훈이형꺼
# api_key = "bg_c2e86c21f1af686f340a9d7752275c70"
# secret_key = "556337e606fee895337b40bae2daed577c78ed7cd6f76b8bb0d1ff78181ec10e"
# passphrase = "lsh790308"
# myAvailable = 2000

#내꺼
api_key = "bg_d824038ea0c0f9a80ecc2b62b4e46e3a"
secret_key = "9cb1d21914debdda86deeb202af7b146954c28b85c80bdd22dc9850116b4810a"
passphrase = "larryapi1"


coin = 'USDT'
coinType = 'UMCBL'
leverage = 100


rateList = []
dateList = []
tickerList = []

bot = telegram.Bot(token=teleToken)

marketApi = market.MarketApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
accountApi = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
planApi = plan.PlanApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
positionApi = position.PositionApi(api_key, secret_key, passphrase, use_server_time=False, first=False)

contracts = marketApi.contracts(coinType)


tickers = []
tickerList = marketApi.tickers(coinType)
buysDict = {}
totalPer = 0
maxPer = 0
minPer = 0
maxMulti = 1
used = 0 #사용중인 금액
fixBuyPrice = 10 #코인당 투자금액

for t in tickerList['data']:
    symbol = t['symbol']
    # if 'BTC' in symbol:
    tickers.append(symbol)
    buysDict[symbol] = {'side':'open_short', 'multi':1, 'buy':False}

def getTime():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S")

def removeTailStr(s):
    return s.replace('_UMCBL','')

def testStart():    
    global totalPer
    global maxPer
    global minPer
    global maxMulti
    global used
    
    for i in range(len(tickers)):
        t = tickers[i]
        time.sleep(1)
        market = marketApi.market_price(t)
        if market is None:
            continue
        
        marketPrice = float(market['data']['markPrice'])
        
        if buysDict[t]['buy'] == False:
            buysDict[t]['buy'] = True
            buysDict[t]['buyPrice'] = marketPrice
            msg = getTime() + " " + removeTailStr(t) + " " + buysDict[t]['side'] + " " + 'buy' + " " + str(buysDict[t]['multi'])
            used += (fixBuyPrice * buysDict[t]['multi'])
            # print(msg)
            # if 'BTC' in t:
            #     bot.sendMessage(chat_id = chatId, text=msg)
        else:
            if bool(buysDict[t].get('buyPrice')) == True:
                buyPrice = buysDict[t]['buyPrice']
                multiply = 1
                if buysDict[t]['side'] == 'open_short':
                    multiply = -1
                orgPer = round((((marketPrice / buyPrice) * 100) - 100) * multiply, 2)
                if orgPer >= 1:
                    used -= (fixBuyPrice * buysDict[t]['multi'])
                    totalPer += buysDict[t]['multi']
                    bot.sendMessage(chat_id = chatId, text='누적수익률:' + str((totalPer*10)))
                    # if 'BTC' in t:
                    #     bot.sendMessage(chat_id = chatId, text=msg)
                    buysDict[t]['multi'] = 1
                    buysDict[t]['buy'] = False
                elif orgPer <= -1:
                    used -= (fixBuyPrice * buysDict[t]['multi'])
                    totalPer -= buysDict[t]['multi']
                    bot.sendMessage(chat_id = chatId, text='누적수익률:' + str((totalPer*10)))
                    # if 'BTC' in t:
                    #     bot.sendMessage(chat_id = chatId, text=msg)
                    if buysDict[t]['side'] == 'open_short':
                        buysDict[t]['side'] = 'open_long'
                    else:
                        buysDict[t]['side'] = 'open_short'
                    buysDict[t]['multi'] *= 2
                    buysDict[t]['buy'] = False
                    
                    #현재까지 사용한 최대 배수
                    if buysDict[t]['multi'] > maxMulti:
                        maxMulti = buysDict[t]['multi']
                        bot.sendMessage(chat_id = chatId, text='최대배수:' + str(maxMulti))
                    
                    
                    # #리밋 제한을 8로 걸어보자
                    # if buysDict[t]['multi'] > 2:
                    #     buysDict[t]['multi'] = 1

        time.sleep(1)

    


schedule.every(60).seconds.do(lambda: testStart())

while True:
    schedule.run_pending()

