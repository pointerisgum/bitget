from cgitb import reset
from functools import total_ordering
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
slackToken = "xoxb-2958422443234-2961015128436-OlEZV7qGyaamz31X3slydehR"
# teleToken = "5144034355:AAGsuZQrk9oDIEa2PqzUuQQObXvFrCs3h10"
teleToken = "5895678922:AAHz850tAEy5CP02LvGHYnO4bKbghNnANr8"
chatId = "5046654369"


# #승훈이형꺼
# api_key = "bg_c2e86c21f1af686f340a9d7752275c70"
# secret_key = "556337e606fee895337b40bae2daed577c78ed7cd6f76b8bb0d1ff78181ec10e"
# passphrase = "lsh790308"
# myAvailable = 2000

#내꺼
api_key = "bg_d824038ea0c0f9a80ecc2b62b4e46e3a"
secret_key = "9cb1d21914debdda86deeb202af7b146954c28b85c80bdd22dc9850116b4810a"
passphrase = "larryapi1"
myAvailable = 400

# BTC_Ticker = 'SBTCSUSDT_SUMCBL'
# ETH_Ticker = 'SETHSUSDT_SUMCBL'
# EOS_Ticker = 'SEOSSUSDT_SUMCBL'

coin = 'USDT'
coinType = 'UMCBL'
# coin = 'SUSDT'
# coinType = 'SUMCBL'
leverage = 5
# check_cci = 95
# excuteMargin = 0.004
# buyMargin = 0.0004
# tkMargin = 0.01
# lossMargin = 0.01

# symbol = 'BTCUSDT_UMCBL'


rateList = []
dateList = []
tickerList = []
totalPer = 0.0
upCount = 0
downCount = 0

bot = telegram.Bot(token=teleToken)

marketApi = market.MarketApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
accountApi = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
planApi = plan.PlanApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
positionApi = position.PositionApi(api_key, secret_key, passphrase, use_server_time=False, first=False)

contracts = marketApi.contracts(coinType)







# tickers = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-AAVE", "KRW-LTC", "KRW-SOL", "KRW-BSV", "KRW-AXS", "KRW-ATOM", "KRW-BTG",
#             "KRW-STRK", "KRW-ETC", "KRW-DOT", "KRW-NEO", "KRW-LINK", "KRW-NEAR", "KRW-REP", "KRW-WAVES", "KRW-QTUM", "KRW-FLOW",
#             "KRW-OMG", "KRW-WEMIX", "KRW-KAVA", "KRW-GAS", "KRW-SBD", "KRW-TON", "KRW-SAND", "KRW-XTZ", "KRW-THETA", "KRW-AQT",
#             'KRW-DAWN', 'KRW-BTT']
# tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'LUNAUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL',
#            'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL', 'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL', 'SOLUSDT_UMCBL']
# tickers = ["BTCUSDT_UMCBL"]

# tickers = [BTC_Ticker, ETH_Ticker, EOS_Ticker]


    # return marketApi.candles(ticker, granularity=900,startTime=(endTime * 1000) - ((time*1000)*count), endTime=endTime * 1000) #15분봉 200개

# def get_cci(candle_data, loop_cnt):
#     try:
#         # CCI 데이터 리턴용
#         cci_list = []
 
#         # 오름차순 정렬
            
#         ordered_df = pd.DataFrame(candle_data)

#         # 계산식 : (Typical Price - Simple Moving Average) / (0.015 * Mean absolute Deviation)
#         ordered_df['TP'] = (ordered_df[2] + ordered_df[3] + ordered_df[4]) / 3
#         ordered_df['SMA'] = ordered_df['TP'].rolling(window=4).mean()
#         ordered_df['MAD'] = ordered_df['TP'].rolling(window=4).apply(lambda x: pd.Series(x).mad())
#         ordered_df['CCI'] = (ordered_df['TP'] - ordered_df['SMA']) / (0.015 * ordered_df['MAD'])
 
#         # 개수만큼 조립
#         for i in range(0, len(candle_data)):            
#             cci_list.append({"type": "CCI", "DT": ordered_df[0].loc[i], "CCI": round(ordered_df['CCI'].loc[i], 4)})
 
#         return cci_list
 
#     # ----------------------------------------
#     # 모든 함수의 공통 부분(Exception 처리)
#     # ----------------------------------------
#     except Exception:
#         raise

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


# def getSize(ticker, myAvailable, currentPrice):
#     return round(((myAvailable * 0.1) * leverage) / currentPrice, 3)
#     # if ticker == BTC_Ticker:
#     #     size = str(((myAvailable * 0.1) * leverage) / currentPrice)
#     #     return size
#     # elif ticker == ETH_Ticker:
#     #     size = float(round(((myAvailable * 0.1) * leverage) / currentPrice, 2))
#     #     return size
#     # elif ticker == EOS_Ticker:
#     #     size = int(round(((myAvailable * 0.1) * leverage) / currentPrice, 0))
#     #     return size
#     # return 0


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


# def get_candle(ticker, time, count):
#     endTime = int(pydatetime.datetime.now().timestamp())
#     try:
#         startTime = (endTime * 1000) - ((time*1000)*count)
#         # start2 = (endTime * 1000) - (((time*2)*1000)*count)
#         # start3 = (endTime * 1000) - (((time*3)*1000)*count)
#         # start4 = (endTime * 1000) - (((time*4)*1000)*count)
#         # start5 = (endTime * 1000) - (((time*5)*1000)*count)
#         day = date.today()
#         day = day.strftime("%Y-%m-%d") + ' 09:00:00'
#         s = int(datetime.strptime(day, '%Y-%m-%d %H:%M:%S').timestamp()) * 1000


#         candles = marketApi.candles(ticker, granularity=60,startTime=s, endTime=s) #15분봉 200개
#         # candles = marketApi.candles(ticker, granularity=3600,startTime=1666224000000, endTime=endTime*1000) #15분봉 200개
#         # candles2 = marketApi.candles(ticker, granularity=time, startTime=start2, endTime=start) #15분봉 200개
#         # candles3 = marketApi.candles(ticker, granularity=time, startTime=start3, endTime=start2) #15분봉 200개
#         # candles4 = marketApi.candles(ticker, granularity=time, startTime=start4, endTime=start3) #15분봉 200개
#         # candles5 = marketApi.candles(ticker, granularity=time, startTime=start5, endTime=start4) #15분봉 200개
#         # candles = candles + candles2 + candles3# + candles4 + candles5
#         if candles == None:
#             print(ticker, time, (endTime * 1000) - ((time*1000)*count), endTime * 1000)
#             return None
#         return candles
#     except Exception:
#         raise

def get_candle(ticker, time, count):
    endTime = int(pydatetime.datetime.now().timestamp())
    try:
        startTime = (endTime * 1000) - ((time*1000)*count)
        # start2 = (endTime * 1000) - (((time*2)*1000)*count)
        # start3 = (endTime * 1000) - (((time*3)*1000)*count)
        # start4 = (endTime * 1000) - (((time*4)*1000)*count)
        # start5 = (endTime * 1000) - (((time*5)*1000)*count)

        candles = marketApi.candles(ticker, granularity='1D', startTime=startTime, endTime=endTime * 1000) #15분봉 200개
        # candles2 = marketApi.candles(ticker, granularity=time, startTime=start2, endTime=start) #15분봉 200개
        # candles3 = marketApi.candles(ticker, granularity=time, startTime=start3, endTime=start2) #15분봉 200개
        # candles4 = marketApi.candles(ticker, granularity=time, startTime=start4, endTime=start3) #15분봉 200개
        # candles5 = marketApi.candles(ticker, granularity=time, startTime=start5, endTime=start4) #15분봉 200개
        # candles = candles + candles2 + candles3# + candles4 + candles5
        if candles == None:
            print(ticker, time, (endTime * 1000) - ((time*1000)*count), endTime * 1000)
            return None
        return candles
    except Exception:
        raise



k_long = 0.5
k_short = 0.5
# k_long = 0.2
# k_short = 0.2

if coin == 'SUSDT':
    tickers = ['SBTCSUSDT_SUMCBL', 'SETHSUSDT_SUMCBL', 'SEOSSUSDT_SUMCBL']
    # tickers = ['SBTCSUSDT_SUMCBL']
    # tickers = ['SEOSSUSDT_SUMCBL']
else:
    # tickers = ['ETCUSDT_UMCBL']
    #'EGLDUSDT_UMCBL', 'KSMUSDT_UMCBL',
    # tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL', 'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL',
    #            'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL','BNBUSDT_UMCBL', 'UNIUSDT_UMCBL', 'ICPUSDT_UMCBL', 'FILUSDT_UMCBL', 'XLMUSDT_UMCBL','AVAXUSDT_UMCBL', 'DASHUSDT_UMCBL', 'XEMUSDT_UMCBL',
    #            'MANAUSDT_UMCBL', 'SANDUSDT_UMCBL', 'CRVUSDT_UMCBL','ARUSDT_UMCBL', 'PEOPLEUSDT_UMCBL', 'LRCUSDT_UMCBL']
    # tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL', 'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL',
    #            'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL','BNBUSDT_UMCBL', 'UNIUSDT_UMCBL', 'ICPUSDT_UMCBL', 'FILUSDT_UMCBL', 'XLMUSDT_UMCBL','AVAXUSDT_UMCBL', 'DASHUSDT_UMCBL', 'XEMUSDT_UMCBL']
    # tickers = ['BTCUSDT_UMCBL', 
    #            'ETHUSDT_UMCBL',
    #            'XRPUSDT_UMCBL','ADAUSDT_UMCBL', 'DOTUSDT_UMCBL', 'SANDUSDT_UMCBL', 'MANAUSDT_UMCBL', 
    #            'LINKUSDT_UMCBL', 'NEOUSDT_UMCBL', 'MATICUSDT_UMCBL', 'SOLUSDT_UMCBL', 'UNIUSDT_UMCBL',
    #            'FILUSDT_UMCBL', 'LUNAUSDT_UMCBL', 'NEARUSDT_UMCBL', 'ALICEUSDT_UMCBL',
    #            'WAVESUSDT_UMCBL', 'DOGEUSDT_UMCBL']
    # tickers = ['SOLUSDT_UMCBL', 'LUNAUSDT_UMCBL']
    tickers = ['BTCUSDT_UMCBL']

tickers = []
tickerList = marketApi.tickers(coinType)
# for t in tickerList['data']:
#     marketPrice = marketApi.market_price(t['symbol'])
#     if marketPrice is None:
#         print('marketPrice is none')
#         continue                    
#     currentPrice = float(marketPrice['data']['markPrice'])
#     if currentPrice > 1:
#         tickers.append(t['symbol'])

buysDict = {}

init = True
isBuyShort = False
isBuyLong = False
highPer = 0

for ticker in tickerList['data']:
    t = ticker['symbol']
    # if symbol != 'FILUSDT_UMCBL':
    tickers.append(t)
    buysDict[t] = 0
    # accountApi.margin_mode(t, coin, 'crossed')
    # time.sleep(0.1)
    # accountApi.leverage(t, coin, leverage, 'long')
    # time.sleep(0.1)
    # accountApi.leverage(t, coin, leverage, 'short')
    # time.sleep(0.1)



# tickerDict = {}
highRun = []
# buysDict = {}


# for t in tickers:
#     test(t)
#     time.sleep(0.05)

# print('total :', round(total, 2), '%')
# print()

# buySizes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
#             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
#             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# longOrderIds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# shortOrderIds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
#                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# longResult = planApi.place_plan('SBTCSUSDT_SUMCBL', marginCoin=coin, size=0.01, side='open_long', orderType='market',
#                             triggerPrice=37905,
#                             executePrice=37905,
#                             triggerType='fill_price',
#                             presetStopLossPrice=36000)


#volumePlace : 사이즈 소숫점 자리 수
#pricePlace : 가격 소숫점 자리 수

def sizeDecimal(t):
    decimal = 0
    for dic in contracts['data']:
        if dic['symbol'] == t:
            decimal = int(dic['volumePlace'])
            break
    
    return decimal

def priceDecimal(t):
    decimal = 0
    for dic in contracts['data']:
        if dic['symbol'] == t:
            decimal = int(dic['pricePlace'])
            if decimal > 0:
                decimal -= 1
            break
    
    return decimal

#마지막자리가 0 또는 5로 끝나야 하는지 여부
def isEndStep(t):
    endStep = 1
    for dic in contracts['data']:
        if dic['symbol'] == t:
            endStep = int(dic['priceEndStep'])
            break
    
    if endStep == 5:
        return True
    return False


def setEndStep(t, price):
    if isEndStep(t) == True:
        priceStr = str(price).split('.')
        if len(priceStr) == 2:
            tail = priceStr[1][:-1]
            return float(priceStr[0] + '.' + tail + '0')
        else:
            leading = priceStr[0][:-1]
            return float(leading + '0')
    else:
        return price
    

def getSize(t):
    # available = 500 #내가 투자 할 총 시드
    # buyAvailable = (available / 2) * (1/len(tickers))
    # buyAvailable = available * (1/len(tickers))
    # if t == 'BTCUSDT_UMCBL':
    #     buyAvailable = 200
    # else:
    #     buyAvailable = 10
    
    buyAvailable = 10
    marketPrice = marketApi.market_price(t)
    if marketPrice is None:
        print('marketPrice is none')
    price = float(marketPrice['data']['markPrice'])
    
    size = round((buyAvailable * leverage) / price, sizeDecimal(t))
    return size

# def getSizePer(t):
#     return 0.1
#     # if t == 'BTCUSDT_UMCBL':
#     #     return 0.3
#     # elif t == 'ETHUSDT_UMCBL':
#     #     return 0.3
#     # else:
#     #     return 0.08

# def getDigits(t):
#     marketPrice = marketApi.market_price(t)
#     if marketPrice is None:
#         print('marketPrice is none')
#         return 0
    
#     price = float(marketPrice['data']['markPrice'])
#     closeStr = str(price).split('.')
#     digits = 1
#     if len(closeStr) == 2:
#             digits = len(closeStr[1])  #소수점 몇자리인지
#     return digits

def getDigits(t):
    volumePlace = 0
    for dic in contracts['data']:
        if dic['symbol'] == t:
            volumePlace = int(dic['volumePlace'])
            break
    
    return int(volumePlace)


def removeLastNum(price):
    closeStr = str(price).split('.')
    if len(closeStr) == 2:
        tail = closeStr[1][:-1]
        return float(closeStr[0] + '.' + tail + '0')
    else:
        return price

# isBuy = False
# isOrder = False

def getTime():
    return datetime.now().strftime("%Y/%m/%d, %H:%M:%S")



def getNowStatus(t):
    endTime = int(pydatetime.datetime.now().timestamp()) * 1000
    time.sleep(0.5)
    historyResult = orderApi.history(t, endTime - (86400 * 1000 * 100), endTime, 1)
    time.sleep(0.5)
    if historyResult is not None:
        historyList = historyResult['data']['orderList']
        if historyList is not None and len(historyList) > 0:
            history = historyList[0]
            if history is not None:
                return history
            else:
                return None
    else:
        print(getTime(), '!!history none!!')
    return None


def limitOrderCancel(t):
    limitList = orderApi.current(t)
    if limitList is not None:
        cancelOrders = []
        for i in range(0, len(limitList['data'])):
            data = limitList['data'][i]
            if data['state'] == 'new':
                orderId = data['orderId']
                cancelOrders.append(orderId)
        
        #등록된 지정가가 있으면 cancel
        if len(cancelOrders) > 0:
            orderApi.cancel_batch_orders(t, coin, cancelOrders)
            print(getTime(), t, '초기화로 인한 지정가 대기 취소')


def cancelPlan(t):
    result = planApi.current_plan(t)
    if result is None:
        return
    
    for data in result['data']:
        planApi.cancel_plan(t, coin, data['orderId'], data['planType'])
        time.sleep(0.1)

    # tickerList = marketApi.tickers(coinType)
    # for ticker in tickerList['data']:
    #     t = ticker['symbol']
    #     result = planApi.current_plan(t)
    #     for data in result['data']:
    #         planApi.cancel_plan(t, coin, data['orderId'], data['planType'])
    #         time.sleep(0.1)
            
def allSell():
    allClse()
    allCancel()
    allLimitOrderCancel()
    
def allClse():
    tickerList = marketApi.tickers('UMCBL')
    for ticker in tickerList['data']:
        t = ticker['symbol']
        result = orderApi.place_order(t, marginCoin=coin, size=99999999, side='close_long', orderType='market', timeInForceValue='normal')
        print(t, 'sell ', result)
        time.sleep(0.1)
        result = orderApi.place_order(t, marginCoin=coin, size=99999999, side='close_short', orderType='market', timeInForceValue='normal')
        print(t, 'sell ', result)
        time.sleep(0.1)

def allCancel():
    tickerList = marketApi.tickers('UMCBL')
    for ticker in tickerList['data']:
        t = ticker['symbol']
        result = planApi.current_plan(t)
        for data in result['data']:
            planApi.cancel_plan(t, coin, data['orderId'], 'normal_plan')
    
def allLimitOrderCancel():
    tickerList = marketApi.tickers('UMCBL')
    for ticker in tickerList['data']:
        t = ticker['symbol']
        limitList = orderApi.current(t)
        if limitList is not None:
            cancelOrders = []
            for i in range(0, len(limitList['data'])):
                data = limitList['data'][i]
                if data['state'] == 'new':
                    orderId = data['orderId']
                    cancelOrders.append(orderId)
            
            #등록된 지정가가 있으면 cancel
            if len(cancelOrders) > 0:
                orderApi.cancel_batch_orders(t, coin, cancelOrders)



def initTickers():
    # bot.sendMessage(chat_id=chatId, text='프로그램 초기화')
    print(getTime(), 'initTickers()')
    
    global init
    global isBuyShort
    global isBuyLong
    global highPer
    global oneDayJob
    global totalPer
    global upCount
    global downCount

    schedule.cancel_job(oneDayJob)

    loop = 0
    movingPrice = 0.0
    oldPrice = 0.0
    targetPrice = 0.0
    longBigStep = 0
    shortBigStep = 0
    
    # while True:
    #     endTime = int(pydatetime.datetime.now().timestamp())
    #     candles = marketApi.candles('BTCUSDT_UMCBL', granularity='1D', startTime=endTime * 1000, endTime=endTime * 1000) #15분봉 200개
    #     if candles != None:
    #         nowPrice = float(candles[-1][4])
    #         if oldPrice == 0:
    #             targetPrice = nowPrice
    #             oldPrice = nowPrice
    #             longBigStep = 0
    #             shortBigStep = 0
    #             continue
            
    #         movingPrice += (nowPrice - oldPrice)
    #         movingPer = round((movingPrice / targetPrice) * 100, 5)
    #         # print(movingPer, movingPrice)
            
    #         oldPrice = nowPrice

    #         if movingPer > 0.1:
    #             loop = 0
    #             movingPrice = 0
    #             targetPrice = nowPrice
    #             longBigStep += 1
    #             shortBigStep = 0
    #             print("long big step", endTime)
    #         if movingPer < -0.1:    
    #             loop = 0
    #             movingPrice = 0
    #             targetPrice = nowPrice
    #             shortBigStep += 1
    #             longBigStep = 0
    #             print("short big step", endTime)
            
    #         if longBigStep >= 5:
    #             print("buy long", endTime)
    #             loop = 0
    #             movingPrice = 0
    #             longBigStep = 0
    #             shortBigStep = 0
    #             targetPrice = nowPrice

    #         if shortBigStep >= 5:
    #             loop = 0
    #             movingPrice = 0
    #             longBigStep = 0
    #             shortBigStep = 0
    #             targetPrice = nowPrice
    #             print("buy short", endTime)
                
                
            
    #         loop += 1
            
    #         if loop >= 20:
    #             # print("end", int(pydatetime.datetime.now().timestamp()))
    #             loop = 0
    #             movingPrice = 0
    #             longBigStep = 0
    #             shortBigStep = 0
    #             targetPrice = nowPrice
    #             # print("reset")
        
        
        
    while True:
        totalPer = 0.0
        upCount = 0
        downCount = 0

        for i in range(len(tickers)):
            time.sleep(0.1)
            t = tickers[i]
            reserveOrder(t)

             

        print('total per : ', totalPer)
        print('upCount : ', upCount)
        print('downCount : ', downCount)
        
        allCnt = len(tickers)
        allPer = totalPer/allCnt
        print('all per : ', allPer)
        # 2123
        #1111
        if isBuyLong == True or isBuyShort == True:
            if isBuyLong == True:
                if allPer < highPer - 1.2:
                    print("sell long")
                    isBuyLong = False
                    bot.sendMessage(chat_id=chatId, text='try long all sell')
                    allSell()
                    bot.sendMessage(chat_id=chatId, text='long sell complete')
                if allPer > highPer:
                    highPer = allPer
                    msg = 'update long price'
                    bot.sendMessage(chat_id=chatId, text=msg)

            elif isBuyShort == True:
                if allPer > highPer + 1.2:
                    print("sell short")
                    isBuyShort = False
                    bot.sendMessage(chat_id=chatId, text='try short all sell')
                    allSell()
                    bot.sendMessage(chat_id=chatId, text='short sell complete')
                if allPer < highPer:
                    highPer = allPer
                    msg = 'update short price'
                    bot.sendMessage(chat_id=chatId, text=msg)
            continue
        
        
        if init == False:
            if upCount < 2 and downCount < 2:
                init = True
            continue
        #a
        
        buyCnt = 0 #몇개 살지
        
        #전체 변동폭이 1.9% 이상일때
        if allPer >= 1.8 or allPer <= -1.8:
            #전체 코인의 75% 이상이 해당될때
            if (upCount/allCnt)*100 > 70:
                print("롱 잡기")
                sortDic = sorted(buysDict.items(), key = lambda item: item[1], reverse=True)
                for i in range(len(sortDic)):
                    per = sortDic[i][1]
                    if per < 2:
                        print("buy long: ", sortDic[i][0], sortDic[i][1])
                        size = getSize(t)
                        orderApi.place_order(t, marginCoin=coin, size=size, side='open_long', orderType='market', timeInForceValue='normal')
                        time.sleep(0.1)
                        tName = t.rstrip("_UMCBL")
                        msg = tName + ' // buy long'
                        bot.sendMessage(chat_id=chatId, text=msg)
                        time.sleep(0.5)
                        #임시로 3개만 사게 함
                        buyCnt += 1
                        if buyCnt >= 3:
                            break
                isBuyLong = True
                highPer = allPer
                init = False
                # return
                
            elif (downCount/allCnt)*100 > 70:
                print("숏 잡기")
                sortDic = sorted(buysDict.items(), key = lambda item: item[1], reverse=False)
                for i in range(len(sortDic)):
                    per = sortDic[i][1]
                    if per > -2:
                        print("buy short: ", sortDic[i][0], sortDic[i][1])
                        size = getSize(t)
                        orderApi.place_order(t, marginCoin=coin, size=size, side='open_short', orderType='market', timeInForceValue='normal')
                        time.sleep(0.1)
                        tName = t.rstrip("_UMCBL")
                        msg = tName + ' // buy short'
                        bot.sendMessage(chat_id=chatId, text=msg)
                        time.sleep(0.5)
                        #임시로 3개만 사게 함
                        buyCnt += 1
                        if buyCnt >= 3:
                            break
                isBuyShort = True
                highPer = allPer
                init = False
                # return

        time.sleep(1)    
    
    schedule.cancel_job(oneDayJob)
    oneDayJob = schedule.every(120).seconds.do(lambda: oneDay())

    
    
#tasdㄴㅁㅇ
def reserveOrder(t):
    global totalPer
    global upCount
    global downCount

    # while True:
    # period: 60, 300, 900, 1800, 3600,14400,43200, 86400, 604800
    time.sleep(0.1)
    candle_data = get_candle(t, 86400, 1)
    time.sleep(0.1)
    
    if candle_data == None:
        time.sleep(0.1)
        # buysDict[t] = {}
        return
    
    #1:O  //  2:H  // 3:L  //  4:C
    if len(candle_data) > 0:
        startPrice = float(candle_data[-1][1]) #오늘 시가
        closePrice = float(candle_data[-1][4]) #현재가 #getMarketPrice(t)
        # print(closePrice)
        per = ((closePrice - startPrice) / startPrice) * 100
        # print(t, 'per = ', per)
        buysDict[t] = per
        totalPer += per
        if per >= 1.8:
            upCount += 1
        elif per <= -1.8:
            downCount += 1
        time.sleep(0.1)








# def addTkTrigger(t, marketPrice, buyPrice, tkMargin):
#     if bool(buysDict[t].get('tkOrderId')) == True:
#         tkOrderId = buysDict[t]['tkOrderId']
#         planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')

#     side = buysDict[t]['side']
#     tmpPrice = 0
#     if side == 'open_long':
#         tmpPrice = marketPrice - (((marketPrice - buyPrice) * tkMargin))
#     if side == 'open_short':
#         tmpPrice = marketPrice + (((marketPrice - buyPrice) * tkMargin))
    
#     triggerPrice = setEndStep(t, round(tmpPrice, priceDecimal(t)))
    
#     size = buysDict[t]['size']
#     tkResult = planApi.place_plan(t, marginCoin=coin, size=size, side=side, orderType='market',
#             triggerPrice=triggerPrice,
#             triggerType='fill_price',
#             executePrice=triggerPrice)
#     if tkResult is None:
#         print(getTime(), t, 'planApi.place_plan API Error', 'tkResult is None')
#     if tkResult is not None:
#         buysDict[t]['tkOrderId'] = tkResult['data']['orderId']
        
        
# def getTkMargin(t):
#     per = buysDict[t]['per']
#     if per <= 40:
#         #수익률이 30~40% 사이인 경우 70% 떨어진 경우 익절
#         tkMargin = 0.7
#     elif per <= 50:
#         #수익률이 41~50% 사이인 경우 60% 떨어진 경우 익절
#         tkMargin = 0.6
#     elif per <= 60:
#         #수익률이 51~60% 사이인 경우 50% 떨어진 경우 익절
#         tkMargin = 0.5
#     elif per <= 70:
#         #수익률이 61~70% 사이인 경우 40% 떨어진 경우 익절
#         tkMargin = 0.4
#     else:
#         #수익률이 71% 이상인 경우 30% 떨어진 경우 익절
#         tkMargin = 0.3

def getMarketPrice(t):
    # time.sleep(0.1)
    market = marketApi.market_price(t)
    # time.sleep(0.1)
    if market is None:
        print(getTime(), 'market API is none')
        return None
    
    return float(market['data']['markPrice'])


def oneDay():
    for t in tickers:
        # if t == 'ICPUSDT_UMCBL':
        #     print()

        status = getNowStatus(t)
        if status is None:
            continue
        
        if status['state'] == 'filled' and ((status['side'] == 'open_long') or (status['side'] == 'open_short')):
            multiply = 1
            if status['side'] == 'open_short':
                multiply = -1
                
            buysDict[t]['orderId'] = status['orderId']
            buysDict[t]['size'] = status['size']
            buysDict[t]['side'] = status['side']
    
            marketPrice = getMarketPrice(t)
            if marketPrice is None:
                continue
            
            buyPrice = float(status['priceAvg'])
            orgPer = round((((marketPrice / buyPrice) * 100) - 100) * multiply, 2)
            per = round(orgPer * leverage, 2)
            
            
            # size = status['size']
            # if bool(buysDict[t].get('buySize')) == True:
            #     size = buysDict[t]['buySize']
            
            # if t == 'ICPUSDT_UMCBL':
            #     print()
                
            #-2% 빠진 경우 손절
            # if orgPer < -2:
            #-20% 빠진 경우 손절
            if per <= -10:
                side = 'close_long'
                if multiply == -1:
                    side = 'close_short'
                result = orderApi.place_order(t, marginCoin=coin, size=999999999, side=side, orderType='market', timeInForceValue='normal')
                print(getTime(), t, ' ', status['side'], '손절 실행', result, per)
                buysDict[t] = {} #손절 후 데이터 초기화
                reserveOrder(t)
                continue
            

            #최소 익절라인 퍼센트는 20%로 설정
            minTkPer = 10.0
            if per >= minTkPer:
                if bool(buysDict[t].get('maxPer')) == False:
                    buysDict[t]['maxPer'] = float(minTkPer)
                    print(getTime(), t, ' ', status['side'], '익절 라인 등록', per)
                else:
                    oldMaxPer = buysDict[t]['maxPer']
                    if per > oldMaxPer:
                        buysDict[t]['maxPer'] = per
                        print(getTime(), t, ' ', status['side'], '익절 라인 업데이트', per)


            #최소 익절 라인을 터치 했을때
            if bool(buysDict[t].get('maxPer')) == True:
                maxPer = buysDict[t]['maxPer']
                #고점대비 30% 빠졌을때 익절
                if maxPer * 0.7 > per:
                    side = 'close_long'
                    if multiply == -1:
                        side = 'close_short'
                    result = orderApi.place_order(t, marginCoin=coin, size=999999999, side=side, orderType='market', timeInForceValue='normal')
                    print(getTime(), t, ' ', status['side'], '익절 실행', result, per)
                    buysDict[t] = {} #익절 후 데이터 초기화
                    reserveOrder(t)
                    continue
        else:
            if bool(buysDict[t].get('addLimitBuy')) == False:
                #아직 매수를 안한 경우 매수 조건이 됐는지 체크
                if bool(buysDict[t].get('longPrice')) == True and bool(buysDict[t].get('shortPrice')) == True:
                    #매수 가능한 애들만 longPrice과 shortPrice 값이 있다
                    longPrice = buysDict[t]['longPrice']
                    shortPrice = buysDict[t]['shortPrice']

                    marketPrice = getMarketPrice(t)
                    if marketPrice is None:
                        continue
                    
                    if marketPrice >= longPrice:
                        size = getSize(t)
                        buyPrice = setEndStep(t, round(marketPrice, priceDecimal(t)))
                        orderApi.place_order(t, marginCoin=coin, size=size, side='open_long', orderType='market', timeInForceValue='normal')
                        buysDict[t]['addLimitBuy'] = True
                        print(getTime(), t, '롱 매수')
                    elif marketPrice <= shortPrice:
                        size = getSize(t)
                        buyPrice = setEndStep(t, round(marketPrice, priceDecimal(t)))
                        orderApi.place_order(t, marginCoin=coin, size=size, side='open_short', orderType='market', timeInForceValue='normal')
                        buysDict[t]['addLimitBuy'] = True
                        print(getTime(), t, '숏 매수')                
                    
                    
                    
        # if status['state'] == 'filled':
        #     if (status['side'] == 'open_long') or (status['side'] == 'open_short'):
        #         multiply = 1
        #         if status['side'] == 'open_short':
        #             multiply = -1
                    
        #         buysDict[t]['orderId'] = status['orderId']
        #         buysDict[t]['size'] = status['size']
        #         buysDict[t]['side'] = status['side']
        
        #         marketPrice = getMarketPrice(t)
        #         if marketPrice is None:
        #             continue
                
        #         buyPrice = float(status['priceAvg'])
        #         orgPer = round((((marketPrice / buyPrice) * 100) - 100) * multiply, 2)
        #         per = round(orgPer * leverage, 2)
                
                
        #         # size = status['size']
        #         # if bool(buysDict[t].get('buySize')) == True:
        #         #     size = buysDict[t]['buySize']
                
        #         # if t == 'ICPUSDT_UMCBL':
        #         #     print()
                    
        #         #-2% 빠진 경우 손절
        #         # if orgPer < -2:
        #         #-20% 빠진 경우 손절
        #         if per <= -20:
        #             side = 'close_long'
        #             if multiply == -1:
        #                 side = 'close_short'
        #             result = orderApi.place_order(t, marginCoin=coin, size=999999999, side=side, orderType='market', timeInForceValue='normal')
        #             print(getTime(), t, ' ', status['side'], '손절 실행', result, per)
        #             buysDict[t] = {} #손절 후 데이터 초기화
        #             continue
                

        #         #최소 익절라인 퍼센트는 20%로 설정
        #         if per >= 20:
        #             if bool(buysDict[t].get('maxPer')) == False:
        #                 buysDict[t]['maxPer'] = float(20.00)
        #                 print(getTime(), t, ' ', status['side'], '익절 라인 등록', per)
        #             else:
        #                 oldMaxPer = buysDict[t]['maxPer']
        #                 if per > oldMaxPer:
        #                     buysDict[t]['maxPer'] = per
        #                     print(getTime(), t, ' ', status['side'], '익절 라인 업데이트', per)


        #         #최소 익절 라인을 터치 했을때
        #         if bool(buysDict[t].get('maxPer')) == True:
        #             maxPer = buysDict[t]['maxPer']
        #             #고점대비 30% 빠졌을때 익절
        #             if maxPer * 0.7 > per:
        #                 side = 'close_long'
        #                 if multiply == -1:
        #                     side = 'close_short'
        #                 result = orderApi.place_order(t, marginCoin=coin, size=999999999, side=side, orderType='market', timeInForceValue='normal')
        #                 print(getTime(), t, ' ', status['side'], '익절 실행', result, per)
        #                 buysDict[t] = {} #익절 후 데이터 초기화
        #                 continue

                            
        #     # elif (status['side'] == 'close_long') or (status['side'] == 'close_short'):
        #     else:
        #         if bool(buysDict[t].get('addLimitBuy')) == False:
        #             #아직 매수를 안한 경우 매수 조건이 됐는지 체크
        #             if bool(buysDict[t].get('longPrice')) == True and bool(buysDict[t].get('shortPrice')) == True:
        #                 #매수 가능한 애들만 longPrice과 shortPrice 값이 있다
        #                 longPrice = buysDict[t]['longPrice']
        #                 shortPrice = buysDict[t]['shortPrice']

        #                 marketPrice = getMarketPrice(t)
        #                 if marketPrice is None:
        #                     continue
                        
        #                 if marketPrice >= longPrice:
        #                     size = getSize(t)
        #                     buyPrice = setEndStep(t, round(marketPrice, priceDecimal(t)))
        #                     orderApi.place_order(t, marginCoin=coin, size=size, side='open_long', orderType='market', timeInForceValue='normal')
        #                     buysDict[t]['addLimitBuy'] = True
        #                     print(getTime(), t, '롱 예약 매수')
        #                 elif marketPrice <= shortPrice:
        #                     size = getSize(t)
        #                     buyPrice = setEndStep(t, round(marketPrice, priceDecimal(t)))
        #                     orderApi.place_order(t, marginCoin=coin, size=size, side='open_short', orderType='market', timeInForceValue='normal')
        #                     buysDict[t]['addLimitBuy'] = True
        #                     print(getTime(), t, '숏 예약 매수')
                        

            #     #매도 후 재등록
            #     reserveOrder(t)
            
            
            
            
                # #매도 친 경우 데이터 지워주기
                # if len(buysDict[t]) > 0:
                #     print(getTime(), t, ' 상태값 close로 변경되어 데이터 초기화')
                #     # if bool(buysDict[t].get('tkOrderId')) == True:
                #     #     tkOrderId = buysDict[t]['tkOrderId']
                #     #     result = planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')
                #     #     if result is not None:
                #     #        print(getTime(), t, '포지션 종료로 인해 익절 대기가 있는 경우 취소 처리')
                #     limitOrderCancel(t)
                #     buysDict[t] = {}
        
        time.sleep(1)


        
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



# bot.sendMessage(chat_id=chatId, text='program start')


# while True:
#     t = 'SBTCSUSDT_SUMCBL'
#     multiply = 1
    
#     candle_data = get_candle(t, 86400, 2)
#     m = marketApi.market_price(t)
#     marketPrice = float(m['data']['markPrice'])
#     # print('marketPrice : ', marketPrice)
    
#     # currentPrice = float(candle_data[-1][4])
#     # print('currentPrice : ', currentPrice)

#     endTime = int(pydatetime.datetime.now().timestamp()) * 1000
#     historyResult = orderApi.history(t, endTime - (86400 * 1000 * 10), endTime, 1)
#     historyList = historyResult['data']['orderList']
#     if historyList is not None:
#         if len(historyList) > 0:
#             nowStatus = historyList[0]
#             if nowStatus['state'] == 'filled' and (nowStatus['side'] == 'open_long' or nowStatus['side'] == 'open_short'):
#                 buyPrice = float(nowStatus['priceAvg'])
#                 # per1 = round((((currentPrice / buyPrice) * 100) - 100) * leverage * multiply, 2)
#                 # print(t, 'currentPrice per : ', per1)
#                 per2 = round((((marketPrice / buyPrice) * 100) - 100) * leverage * multiply, 2)
#                 print(per2)

#     # time.sleep(0.1)

oneDayJob = schedule.every(120).seconds.do(lambda: oneDay())
schedule.cancel_job(oneDayJob)
initTickers()
# schedule.every().day.at("01:01:01").do(lambda: initTickers())



# schedule.every(1).seconds.do(lambda: oneDay())




print(getTime(), 'start')
# initTickers()
# schedule.every().hour.at(":00").do(lambda: initTickers())
# schedule.every().hour.at(":15").do(lambda: initTickers())
# schedule.every().hour.at(":30").do(lambda: initTickers())
# schedule.every().hour.at(":45").do(lambda: initTickers())





# schedule.every().day.at("15:57:00").do(lambda: initTickers())

# schedule.every().day.at("01:00:01").do(lambda: oneDay())

# schedule.every().hour.at(":00").do(lambda: initTickers())
# schedule.every().hour.at(":15").do(lambda: initTickers())
# schedule.every().hour.at(":30").do(lambda: initTickers())
# schedule.every().hour.at(":45").do(lambda: initTickers())


# schedule.every().day.at("20:00:01").do(lambda: oneDay())
# schedule.every().day.at("21:00:01").do(lambda: oneDay())
# schedule.every().day.at("22:00:01").do(lambda: oneDay())
# schedule.every().day.at("23:00:01").do(lambda: oneDay())
# schedule.every().day.at("00:00:01").do(lambda: oneDay())


# oneDay()
# # schedule.every(15).minute.do(lambda: oneDay())
# schedule.every(1).hour.do(lambda: oneDay())
# schedule.every().hour.at(":00").do(lambda: oneDay())
# schedule.every().hour.at(":15").do(lambda: oneDay())
# schedule.every().hour.at(":30").do(lambda: oneDay())
# schedule.every().hour.at(":45").do(lambda: oneDay())

# oneDay()
# schedule.every().day.at("01:00:05").do(lambda: oneDay())

# oneDay()
# time.sleep(30)
# oneDay()

# schedule.every().day.at('15:53:01').do(lambda: oneDay())

while True:
    schedule.run_pending()
    # time.sleep(1)

#123