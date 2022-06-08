from cgitb import reset
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

access = "xwdEMciw0PeGRfpA8xMaVtnVGmFPFxTR6dkKCnUQ"
secret = "UOxwdGYVZflyTCbMwrlrzB0Ey44GGxSLl70xp8A4"
slackToken = "xoxb-2958422443234-2961015128436-OlEZV7qGyaamz31X3slydehR"
teleToken = "5144034355:AAGsuZQrk9oDIEa2PqzUuQQObXvFrCs3h10"
chatId = "-682086795"


# #승훈이형꺼
api_key = "bg_c2e86c21f1af686f340a9d7752275c70"
secret_key = "556337e606fee895337b40bae2daed577c78ed7cd6f76b8bb0d1ff78181ec10e"
passphrase = "lsh790308"
myAvailable = 2000

#내꺼
# api_key = "bg_d824038ea0c0f9a80ecc2b62b4e46e3a"
# secret_key = "9cb1d21914debdda86deeb202af7b146954c28b85c80bdd22dc9850116b4810a"
# passphrase = "larryapi1"
# myAvailable = 400

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

bot = telegram.Bot(token=teleToken)

marketApi = market.MarketApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
accountApi = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
planApi = plan.PlanApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
positionApi = position.PositionApi(api_key, secret_key, passphrase, use_server_time=False, first=False)

contracts = marketApi.contracts(coinType)


#교차 : crossed
#격리 : fixed

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


def get_candle(ticker, time, count):
    endTime = int(pydatetime.datetime.now().timestamp())
    try:
        startTime = (endTime * 1000) - ((time*1000)*count)
        # start2 = (endTime * 1000) - (((time*2)*1000)*count)
        # start3 = (endTime * 1000) - (((time*3)*1000)*count)
        # start4 = (endTime * 1000) - (((time*4)*1000)*count)
        # start5 = (endTime * 1000) - (((time*5)*1000)*count)

        candles = marketApi.candles(ticker, granularity=time,startTime=startTime, endTime=endTime * 1000) #15분봉 200개
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
for t in tickerList['data']:
    symbol = t['symbol']
    tickers.append(symbol)
    buysDict[symbol] = {}



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
    if t == 'BTCUSDT_UMCBL':
        buyAvailable = 300
    else:
        buyAvailable = 50
    
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
    historyResult = orderApi.history(t, endTime - (86400 * 1000 * 100), endTime, 1)
    if historyResult is not None:
        historyList = historyResult['data']['orderList']
        if historyList is not None and len(historyList) > 0:
            history = historyList[0]
            if history['state'] == 'filled':
                return history
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
            

def initTickers():
    # bot.sendMessage(chat_id=chatId, text='프로그램 초기화')
    print(getTime(), 'initTickers()')
    
    global oneDayJob
        
    schedule.cancel_job(oneDayJob)

    for i in range(len(tickers)):
        t = tickers[i]
        if t in highRun:
            #하이런이 있는 경우 딕셔너리 초기화를 하지 않는다
            print(getTime(), 'have highRun')
            continue

        
        #레버리지 설정
        accountApi.margin_mode(t, coin, 'crossed')
        accountApi.leverage(t, coin, leverage, 'long')
        accountApi.leverage(t, coin, leverage, 'short')

        #지정가에 등록된게 있다면 취소
        limitOrderCancel(t)
        
        #예약매수 걸려 있는것 취소
        cancelPlan(t)

        #예약주문 넣기
        reserveOrder(t)

        # #구매중인게 있을땐 시장가 매도
        # if bool(buysDict.get(t)) == True:
        #     if bool(buysDict[t].get('orderId')) == True:
        #         orderId = buysDict[t]['orderId']
        #         result = planApi.cancel_plan(t, coin, orderId, 'normal_plan')
        #         if result is not None:
        #             print(getTime(), t, '초기화로 스탑리밋 대기 취소')                
                    
        #     if bool(buysDict[t].get('size')) == True:
        #         size = buysDict[t]['size']
        #         result = orderApi.place_order(t, marginCoin=coin, size=size, side=buysDict[t]['side'], orderType='market', timeInForceValue='normal')
        #         if result is not None:
        #             #msg : 예약 매수 완료
        #             print(getTime(), t, '초기화로 인해 시장가 매도')                
                    
        #     if bool(buysDict[t].get('tkOrderId')) == True:
        #         tkOrderId = buysDict[t]['tkOrderId']
        #         result = planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')
        #         if result is not None:
        #             print(getTime(), t, '초기화로 인해 익절 대기 취소')



        # tickerDict[t] = {}
        # tickerDict[t]['long'] = {}
        # tickerDict[t]['short'] = {}

        # buysDict[t] = {}

        schedule.cancel_job(oneDayJob)
        oneDayJob = schedule.every(10).seconds.do(lambda: oneDay())


def reserveOrder(t):
    high = 0
    low = 0
    close = 0
    nowLow = 0
    nowHigh = 0
    
    while True:
        # period: 60, 300, 900, 1800, 3600,14400,43200, 86400, 604800
        time.sleep(0.1)
        candle_data = get_candle(t, 86400, 2)
        time.sleep(0.1)
        
        if candle_data == None:
            time.sleep(1)
            continue
        
        if len(candle_data) > 1:
            # print(getTime(), t, candle_data[-2])
            high = float(candle_data[-2][2]) #전날 고가
            low = float(candle_data[-2][3]) #전날 저가
            close = float(candle_data[-2][4]) #전날 종가

            nowHigh = float(candle_data[-1][2]) #오늘 종가
            nowLow = float(candle_data[-1][3]) #오늘 종가

            if high > 0 and low > 0 and close > 0:
                break
            else:
                time.sleep(1)
        else:
            time.sleep(1)

        
    currentPrice = float(candle_data[-1][4])
    
    #가격이 0.1보다 작은건 패스
    if currentPrice <= 10:
        print(t, '가격이 10 예약 매수 미만이라 패스')
        return
            
    buffer = high - low
    beforePer = round(((high - low) / low) * 100, 2)
    if beforePer < 4:
        #변동폭이 4% 미만일 경우 4%로 고정
        buffer = low * 0.04
    elif beforePer > 6:
        #변동폭이 6% 이상일 경우 6%로 고정
        buffer = low * 0.06
    
    #minTradeNum : 사이즈 소숫점 자리 수
    #pricePlace : 가격 소숫점 자리 수
    
    long_buffer = setEndStep(t, round((buffer) * k_long, priceDecimal(t)))
    short_buffer = setEndStep(t, round((buffer) * k_short, priceDecimal(t)))
    longPrice = setEndStep(t, round(close + long_buffer, priceDecimal(t)))
    shortPrice = setEndStep(t, round(close - short_buffer, priceDecimal(t)))

    # if nowHigh > longPrice:
    #     # print(getTime(), t, '이미 롱 매수 타이밍 지남')
    #     return
    # elif nowLow < shortPrice:
    #     # print(getTime(), t, '이미 숏 매수 타이밍 지남')
    #     return
    
    if currentPrice > longPrice or currentPrice < shortPrice:
        print(getTime(), t, '매수 타이밍 지남')
        return
    
    if longPrice == shortPrice:
        print(getTime(), '롱가격과 숏가격이 같아서 패스 (문제있는거임)')
        return
    
    
    #이미 등록된게 있는지 검사
    didLong = False
    didShort = False
    result = planApi.current_plan(t)
    if result is None:
        return
    
    for data in result['data']:
        if data['side'] == 'open_long':
            didLong = True
        elif data['side'] == 'open_short':
            didShort = True
            
        # result = planApi.cancel_plan(t, coin, data['orderId'], data['planType'])
        # print(getTime(), t, '예약 대기 취소', result)
        # time.sleep(0.5)
        

    
    
    size = getSize(t) 
    buysDict[t]['buySize'] = size
    
    #손절라인은 -2%
    # lossPrice = setEndStep(t, round(low * 0.02, priceDecimal(t)))
    
    if didLong == False:
        buyResult = planApi.place_plan(t, marginCoin=coin, size=size, side='open_long', orderType='limit',
                        triggerPrice=longPrice,
                        executePrice=longPrice,
                        triggerType='fill_price')
                        # presetStopLossPrice=longPrice-lossPrice)
        print(getTime(), t, '롱 매수 예약 : ', longPrice, buyResult['msg'])
        # print(getTime(), t, '롱 손절 예약 가격 : ', longPrice-lossPrice)
        # print(getTime(), t, '롱 예약매수 결과 : ', buyResult['msg'])
    
    if didShort == False:
        buyResult = planApi.place_plan(t, marginCoin=coin, size=size, side='open_short', orderType='limit',
                triggerPrice=shortPrice,
                executePrice=shortPrice,
                triggerType='fill_price')
                # presetStopLossPrice=shortPrice+lossPrice)
        print(getTime(), t, '숏 매수 예약 : ', shortPrice, buyResult['msg'])
        # print(getTime(), t, '숏 손절 예약 가격 : ', shortPrice+lossPrice)
        # print(getTime(), t, '숏 예약매수 결과 : ', buyResult)

    if didLong == False or didShort == False:
        print(t, '예약주문완료')

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


def oneDay():
    for t in tickers:
        # if t == 'ICPUSDT_UMCBL':
        #     print()

        status = getNowStatus(t)
        if status is None:
            continue
        
        if status['state'] == 'filled':
            if (status['side'] == 'open_long') or (status['side'] == 'open_short'):
                multiply = 1
                if status['side'] == 'open_short':
                    multiply = -1
                    
                buysDict[t]['orderId'] = status['orderId']
                buysDict[t]['size'] = status['size']
                buysDict[t]['side'] = status['side']
        
                market = marketApi.market_price(t)
                if market is None:
                    print(getTime(), 'market API is none')
                    #API 에러가 났을시 컨티뉴해서 다음 턴에 다시 시도한다
                    continue
                
                marketPrice = float(market['data']['markPrice'])
                buyPrice = float(status['priceAvg'])
                orgPer = round((((marketPrice / buyPrice) * 100) - 100) * multiply, 2)
                per = round(orgPer * leverage, 2)
                
                
                size = status['size']
                if bool(buysDict[t].get('buySize')) == True:
                    size = buysDict[t]['buySize']
                
                # if t == 'ICPUSDT_UMCBL':
                #     print()
                    
                #-2% 빠진 경우 손절
                # if orgPer < -2:
                #-20% 빠진 경우 손절
                if per >= -20:
                    side = 'close_long'
                    if multiply == -1:
                        side = 'close_short'
                    result = orderApi.place_order(t, marginCoin=coin, size=999999999, side=side, orderType='market', timeInForceValue='normal')
                    print(getTime(), t, ' ', status['side'], '손절 실행', result, per)
                    buysDict[t] = {} #손절 후 데이터 초기화
                    return
                

                #최소 익절라인 퍼센트는 30%로 설정
                if per >= 20:
                    if bool(buysDict[t].get('maxPer')) == False:
                        buysDict[t]['maxPer'] = float(20.00)
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
                        return

                            
            elif (status['side'] == 'close_long') or (status['side'] == 'close_short'):
                #매도 후 재등록
                reserveOrder(t)
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
# initTickers()
schedule.every().day.at("01:00:01").do(lambda: initTickers())



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

