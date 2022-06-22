from pickle import FALSE, TRUE
import time
import os
import sys
import logging
import traceback
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

access = "xwdEMciw0PeGRfpA8xMaVtnVGmFPFxTR6dkKCnUQ"
secret = "UOxwdGYVZflyTCbMwrlrzB0Ey44GGxSLl70xp8A4"
slackToken = "xoxb-2958422443234-2961015128436-OlEZV7qGyaamz31X3slydehR"
teleToken = "5144034355:AAGsuZQrk9oDIEa2PqzUuQQObXvFrCs3h10"
chatId = "-682086795"


#승훈이형꺼
api_key = "bg_c2e86c21f1af686f340a9d7752275c70"
secret_key = "556337e606fee895337b40bae2daed577c78ed7cd6f76b8bb0d1ff78181ec10e"
passphrase = "lsh790308"
myAvailable = 8000

#내꺼
# api_key = "bg_d824038ea0c0f9a80ecc2b62b4e46e3a"
# secret_key = "9cb1d21914debdda86deeb202af7b146954c28b85c80bdd22dc9850116b4810a"
# passphrase = "larryapi1"
# myAvailable = 800


coin = 'USDT'
leverage = 10
check_cci = 95
excuteMargin = 0.004
buyMargin = 0.0004
tkMargin = 0.01
lossMargin = 0.01

# symbol = 'BTCUSDT_UMCBL'


rateList = []
dateList = []
tickerList = []

bot = telegram.Bot(token=teleToken)

marketApi = market.MarketApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
accountApi = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
planApi = plan.PlanApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
positionApi = position.PositionApi(api_key, secret_key, passphrase, use_server_time=False, first=False)

oldEQ = 0
account = accountApi.accounts('umcbl')
if account is not None:
    oldEQ = round(float(account['data'][0]['equity']), 0)
    # print(oldEQ)


def myEquity():
    account = accountApi.accounts('umcbl')
    if account is not None:
        global oldEQ
        # myAvailable = float(account['data'][0]['available'])
        equity = round(float(account['data'][0]['equity']), 0)
        totalEQ = equity - oldEQ
        msg = '현재 자산 : ' + str(equity) + ' / ' + '손익 : ' + str(totalEQ)
        bot.sendMessage(chat_id=chatId, text=msg)
        oldEQ = equity

schedule.every().day.at("01:00:00").do(lambda: myEquity())

# tickers = []
# result = marketApi.tickers('UMCBL')
# for t in result['data']:
#     tickers.append(t['symbol'])

# def monitoring():
#     for i in range(len(tickers)):
#         t = tickers[i]

#         day = date.today()
#         nowHour = datetime.now().hour
#         if nowHour < 1:
#             day = date.today() + timedelta(days=-1)

#         day = day.strftime("%Y-%m-%d") + ' 01:00:00'

#         startTime = int(time.mktime(datetime.now().strptime(day, '%Y-%m-%d %H:%M:%S').timetuple())) * 1000
#         endTime = int(pydatetime.datetime.now().timestamp()) * 1000           #현재
#         historyResult = orderApi.history(t, startTime, endTime, 10)
#         historyList = historyResult['data']['orderList']
#         if historyList is not None:
#             lastTime = 0
#             lastIdx = 0
#             for i in range(len(historyList)):
#                 cTime = float(historyList[i]['cTime'])
#                 if cTime > lastTime:
#                     lastTime = cTime
#                     lastIdx = i
                    
#             h = historyList[lastIdx]
#             if (h['side'] == 'open_long' or h['side'] == 'open_short') and h['state'] == 'filled':
#                 #매수 한 경우
#                 marketPrice = marketApi.market_price(t)
#                 if marketPrice is not None:
#                     currentPrice = float(marketPrice['data']['markPrice'])
#                     buyPrice = float(h['priceAvg'])
#                     #((현재가/구매가)*100)-100
#                     per = 0
#                     if h['side'] == 'open_long':
#                         per = ((currentPrice/buyPrice)*100)-100
#                         msg = t + ':(long) ' + str(round(per * leverage, 2)) + '%'
#                     if h['side'] == 'open_short':
#                         per = (((currentPrice/buyPrice)*100)-100) * -1
#                         msg = t + ':(short) ' + str(round(per * leverage, 2)) + '%'
                    
#                     bot.sendMessage(chat_id=chatId, text=msg)
#                     print(msg)
#         time.sleep(0.1)



# monitoring()
# schedule.every(600).seconds.do(lambda: monitoring())

# while True:
#     schedule.run_pending()
