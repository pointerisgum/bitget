from pickle import FALSE, TRUE
import time
import os
import sys
import logging
import traceback
import upbit_api
import pyupbit
import telegram
from datetime import datetime
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
teleToken = "5291971733:AAHc28SrH3VgTFUpKOLhunzMihCz3Btdqj0"
chatId = "-657183044"

api_key = "bg_f4ae7e0a6fab17130de0641afb1cda61"
secret_key = "e9a1b99d7ef0cbe0a428afacbc0480ff73c9812e89481f0ec2199af6be9359a3"
passphrase = "bitgetcci"

BTC_Ticker = 'SBTCSUSDT_SUMCBL'
ETH_Ticker = 'SETHSUSDT_SUMCBL'
EOS_Ticker = 'SEOSSUSDT_SUMCBL'

ticker = BTC_Ticker
coin = 'SUSDT'
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

# chat = telegram.Bot(token = teleToken)
# updates = chat.getUpdates()
# for u in updates:
#     print(updates[0].message['chat']['id'])

# bot = telegram.Bot(token = teleToken)
# text = '안녕하세요'
# bot.sendMessage(chat_id = chatId, text=text)

# try:

#     upbit_api.set_loglevel('I')
        
#     # CCI 조회(60분봉/10개)
#     candle_data = upbit_api.get_candle('KRW-BTC', '15', 200)
#     cci = get_cci(candle_data, 2)
#     print(cci)
#     print(cci[1]['CCI'])
#     price = candle_data[0]['trade_price']    
    
#     macd_data = upbit_api.get_macd('KRW-BTC', '15', '200', 200)

#     for macd_data_for in macd_data:
#         logging.info(macd_data_for)

# except KeyboardInterrupt:
#     logging.error("KeyboardInterrupt Exception 발생!")
#     logging.error(traceback.format_exc())
#     sys.exit(-100)

# except Exception:
#     logging.error("Exception 발생!")
#     logging.error(traceback.format_exc())
#     sys.exit(-200)








import pandas as pd
import requests
import pandas as pd
import time
import webbrowser
import numpy as np

# tickers = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-AAVE", "KRW-LTC", "KRW-SOL", "KRW-BSV", "KRW-AXS", "KRW-ATOM", "KRW-BTG",
#             "KRW-STRK", "KRW-ETC", "KRW-DOT", "KRW-NEO", "KRW-LINK", "KRW-NEAR", "KRW-REP", "KRW-WAVES", "KRW-QTUM", "KRW-FLOW",
#             "KRW-OMG", "KRW-WEMIX", "KRW-KAVA", "KRW-GAS", "KRW-SBD", "KRW-TON", "KRW-SAND", "KRW-XTZ", "KRW-THETA", "KRW-AQT",
#             'KRW-DAWN', 'KRW-BTT']
# tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'LUNAUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL',
#            'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL', 'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL', 'SOLUSDT_UMCBL']
# tickers = ["BTCUSDT_UMCBL"]

tickers = [BTC_Ticker, ETH_Ticker, EOS_Ticker]

def get_candle(ticker, time, count):
    endTime = int(pydatetime.datetime.now().timestamp())
    try:
        candles = marketApi.candles(ticker, granularity=time,startTime=(endTime * 1000) - ((time*1000)*count), endTime=endTime * 1000) #15분봉 200개
        if candles == None:
            print(ticker, time, (endTime * 1000) - ((time*1000)*count), endTime * 1000)
            return None
        return candles
    except Exception:
        raise

    # return marketApi.candles(ticker, granularity=900,startTime=(endTime * 1000) - ((time*1000)*count), endTime=endTime * 1000) #15분봉 200개

def get_cci(candle_data, loop_cnt):
    try:
        # CCI 데이터 리턴용
        cci_list = []
 
        # 오름차순 정렬
            
        ordered_df = pd.DataFrame(candle_data)

        # 계산식 : (Typical Price - Simple Moving Average) / (0.015 * Mean absolute Deviation)
        ordered_df['TP'] = (ordered_df[2] + ordered_df[3] + ordered_df[4]) / 3
        ordered_df['SMA'] = ordered_df['TP'].rolling(window=4).mean()
        ordered_df['MAD'] = ordered_df['TP'].rolling(window=4).apply(lambda x: pd.Series(x).mad())
        ordered_df['CCI'] = (ordered_df['TP'] - ordered_df['SMA']) / (0.015 * ordered_df['MAD'])
 
        # 개수만큼 조립
        for i in range(0, len(candle_data)):            
            cci_list.append({"type": "CCI", "DT": ordered_df[0].loc[i], "CCI": round(ordered_df['CCI'].loc[i], 4)})
 
        return cci_list
 
    # ----------------------------------------
    # 모든 함수의 공통 부분(Exception 처리)
    # ----------------------------------------
    except Exception:
        raise

def saveExcel(t, c, b):
    path = '/home/ubuntu/upbit-cci/coint.xlsx'
    
    rate = str(getPer(c, b))
    rateList.append(rate)
    date = str(datetime.now().hour) + ':' + str(datetime.now().minute)
    dateList.append(date)
    tickerList.append(t)

    df = pd.DataFrame({'date':dateList, 'ticker':tickerList, 'rate': rateList})
    df.to_excel(path)
    
def getPer(c, b):
    if b <= 0:
        #디버깅용
        return 0
    
    #(((매도가 - 매수가) / 매수가 ) * 100 ) - 0.08) * 10
    return round(round(((((c - b) / b) * 100) - 0.08) * leverage, 2) + -0.9, 2)

def updateCCI(ticker, sleepSec):
    time.sleep(sleepSec)
    candle_data = get_candle(ticker, 900, 100)
    cci_data = get_cci(candle_data, 100)
    cci = cci_data[-1]['CCI']
    return cci


def getDealPrice(ticker, orderId):
    # buyOrderId = result['data']['orderId']
    isBuyed = False
    while isBuyed == False:
        result = orderApi.detail(ticker, orderId=orderId)
        if result.get('data', None).get('priceAvg', None) is None:
            print('empty')
        else:
            print('not empty')
            isBuyed = True
            print(result['data']['priceAvg'])
            return result['data']['priceAvg']
        time.sleep(0.5)

def getSize(ticker, myAvailable, currentPrice):
    if ticker == BTC_Ticker:
        size = float(round(((myAvailable * 0.1) * leverage) / currentPrice, 3))
        return size
    elif ticker == ETH_Ticker:
        size = float(round(((myAvailable * 0.1) * leverage) / currentPrice, 2))
        return size
    elif ticker == EOS_Ticker:
        size = int(round(((myAvailable * 0.1) * leverage) / currentPrice, 0))
        return size
    return 0

def getUpline(ticker, currentPrice, per):
    if ticker == BTC_Ticker:
        return float(round(currentPrice + (currentPrice * per), 0))
    elif ticker == ETH_Ticker:
        return float(round(currentPrice + (currentPrice * per), 1))
    elif ticker == EOS_Ticker:
        return float(round(currentPrice + (currentPrice * per), 3))
    return 0

    
def getDownline(ticker, currentPrice, per):
    if ticker == BTC_Ticker:
        return float(round(currentPrice - (currentPrice * per), 0))
    elif ticker == ETH_Ticker:
        return float(round(currentPrice - (currentPrice * per), 1))
    elif ticker == EOS_Ticker:
        return float(round(currentPrice - (currentPrice * per), 3))
    return 0

def getOrderId(result):
    isCheck = False
    while isCheck == False:
        if result is None:
            continue
        if result.get('data', None).get('orderId', None) is None:
            print('empty')
        else:
            print('not empty')
            isCheck = True
            return result['data']['orderId']
        time.sleep(0.5)

def getCurrentPrice(price):
    if ticker == BTC_Ticker:
        return float(round(price, 1))
    elif ticker == ETH_Ticker:
        return float(round(price, 1))
    elif ticker == EOS_Ticker:
        return float(round(price, 3))
    return price

gold = False
dead = False

def candles15():
    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), '15min candles call')
    
    candle_data = get_candle(ticker, 900, 100)
    if candle_data == None:
        return
    
    for i in range(0, len(candle_data)):
        candle_data[i][0] = float(candle_data[i][0]) #타임
        candle_data[i][1] = float(candle_data[i][1]) #시가
        candle_data[i][2] = float(candle_data[i][2]) #고가
        candle_data[i][3] = float(candle_data[i][3]) #저가
        candle_data[i][4] = float(candle_data[i][4]) #종가

    global dead
    global gold
    global ma10
    global ma30
    
    df = pd.DataFrame(candle_data)
    # df=df['trade_price'].iloc[::-1]
    df=df[4].iloc[::1] #4번째가 종가임

    ma10 = df.rolling(window=10).mean()
    ma30 = df.rolling(window=30).mean()

    line10=ma10.iloc[-3]-ma30.iloc[-3]
    line30=ma10.iloc[-2]-ma30.iloc[-2]
    
    dead = line10>0 and line30<0
    gold = line10<0 and line30>0
    # gold = True
    # dead = True




# longOrderId = 0
# shortOrderId = 0
buySize = 0
k = 0.5
longOrderId = 0
shortOrderId = 0
 
# def buyCheck():
#     print('buyCheck()')
#     if longOrderId > 0:
#         longDetail = orderApi.detail(ticker, longOrderId)
#         if longDetail is not None:
#             longState = longDetail['data']['state']
#             if longState == 'filled':
#                 #롱 매수시 숏 걸어둔거 취소
#                 print('롱 매수되어 숏 취소')
#                 planApi.cancel_plan(ticker, coin, shortOrderId, 'normal_plan')
#                 longOrderId = 0
#                 shortOrderId = 0
     
#     if shortOrderId > 0:   
#         shortDetail = orderApi.detail(ticker, shortOrderId)
#         if shortDetail is not None:
#             shortState = shortDetail['data']['state']
#             if shortState == 'filled':
#                 #숏 매수시 롱 걸어둔거 취소
#                 print('숏 매수되어 롱 취소')
#                 planApi.cancel_plan(ticker, coin, longOrderId, 'normal_plan')
#                 longOrderId = 0
#                 shortOrderId = 0


def startAuto():
    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), 'call')

    open = 0
    hight = 0
    low = 0
    close = 0
    
    global buySize
    global longOrderId
    global shortOrderId

    while True:
        candle_data = get_candle(ticker, 3600, 2)
        
        if candle_data == None:
            time.sleep(1)
            continue
        
        if len(candle_data) > 1:
            open = float(candle_data[1][1]) #고가
            hight = float(candle_data[1][2]) #고가
            low = float(candle_data[1][3]) #저가
            close = float(candle_data[1][4]) #종가

            if hight > 0 and low > 0 and close > 0:
                break
            else:
                time.sleep(1)
        else:
            time.sleep(1)


    marketPrice = marketApi.market_price(ticker)
    if marketPrice is None:
        print('marketPrice is none')
    
    currentPrice = float(marketPrice['data']['markPrice'])
    print(currentPrice)
    currentPrice = getCurrentPrice(currentPrice)    
    account = accountApi.accounts('sumcbl')
    myAvailable = float(account['data'][0]['available'])
    size = getSize(ticker, myAvailable, currentPrice)

    #이전에 걸어둔 예약 매수가 있다면 취소
    if longOrderId > 0:
        planApi.cancel_plan(ticker, coin, longOrderId, 'normal_plan')
    
    if shortOrderId > 0:
        planApi.cancel_plan(ticker, coin, shortOrderId, 'normal_plan')


    #구매중인게 있을 수 있으니 시작과 동시에 시장가 매도
    result = orderApi.place_order(ticker, marginCoin=coin, size=buySize, side='close_long', orderType='market', timeInForceValue='normal')
    if result is not None:
        msg = 'sell long', currentPrice
        bot.sendMessage(chat_id=chatId, text=msg)
        
    result = orderApi.place_order(ticker, marginCoin=coin, size=buySize, side='close_short', orderType='market', timeInForceValue='normal')
    if result is not None:
        msg = 'sell short', currentPrice
        bot.sendMessage(chat_id=chatId, text=msg)
    
    if open <= close:
        #롱 예약
        price = math.ceil(close + ((hight - low) * k))
        msg = 'add long', price
        bot.sendMessage(chat_id=chatId, text=msg)
        longResult = planApi.place_plan(ticker, marginCoin=coin, size=size, side='open_long', orderType='limit',
                                    triggerPrice=price,
                                    executePrice=price,
                                    triggerType='fill_price')
        # longResult = orderApi.place_order(ticker, marginCoin=coin, size=buySize, side='open_long',
        #                     orderType='limit', price=math.ceil(close + ((hight - low) * k)), timeInForceValue='normal')
        longOrderId = int(getOrderId(longResult))
    else:
        #숏 예약
        price = math.ceil(close - ((hight - low) * k))
        msg = 'add short', price
        bot.sendMessage(chat_id=chatId, text=msg)

        shortResult = planApi.place_plan(ticker, marginCoin=coin, size=size, side='open_short', orderType='limit',
                                triggerPrice=price,
                                executePrice=price,
                                triggerType='fill_price')
        # shortResult = orderApi.place_order(ticker, marginCoin=coin, size=buySize, side='open_short',
        #                     orderType='limit', price=math.ceil(close - ((hight - low) * k)), timeInForceValue='normal')
        shortOrderId = int(getOrderId(shortResult))

    buySize = size


msg = 'start 4hour larry'
bot.sendMessage(chat_id=chatId, text=msg)

# candles15()
# schedule.every().minute.at(":03").do(candles15) # 매분 23초에 job 실행
# schedule.every(3).seconds.do(lambda: test1()) # 3초마다 job 실행
# schedule.every().hour.at(":54").do(lambda: candles15()) # 매시간 42분에 작업 실행

# startAuto()
# # schedule.every(1).seconds.do(lambda: buyCheck())
# # schedule.every().hour.do(lambda: startAuto())
# schedule.every().hour.at(":01").do(lambda: startAuto()) # 매시간 42분에 작업 실행

schedule.every().day.at("00:00:05").do(startAuto)
schedule.every().day.at("00:04:05").do(startAuto)
schedule.every().day.at("00:08:05").do(startAuto)
schedule.every().day.at("00:12:05").do(startAuto)
schedule.every().day.at("00:16:05").do(startAuto)
schedule.every().day.at("00:20:05").do(startAuto)
# schedule.every().hour.at(":41").do(lambda: startAuto())
# schedule.every().hour.at(":42").do(lambda: startAuto())
# schedule.every().hour.at(":43").do(lambda: startAuto())
# schedule.every().hour.at(":44").do(lambda: startAuto())

while True:
    schedule.run_pending()
    time.sleep(1)
