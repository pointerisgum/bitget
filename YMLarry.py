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

# ticker = BTC_Ticker
coin = 'USDT'
leverage = 20
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

contracts = marketApi.contracts('umcbl')


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
tickerList = marketApi.tickers('UMCBL')
# for t in tickerList['data']:
#     marketPrice = marketApi.market_price(t['symbol'])
#     if marketPrice is None:
#         print('marketPrice is none')
#         continue                    
#     currentPrice = float(marketPrice['data']['markPrice'])
#     if currentPrice > 1:
#         tickers.append(t['symbol'])

for t in tickerList['data']:
    tickers.append(t['symbol'])

tickerDict = {}
highRun = []



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


def initTickers():
    # bot.sendMessage(chat_id=chatId, text='프로그램 초기화')
    print('initTickers()')

    global oneDayJob
        
    schedule.cancel_job(oneDayJob)

    for i in range(len(tickers)):
        t = tickers[i]
        if t in highRun:
            #하이런이 있는 경우 딕셔너리 초기화를 하지 않는다
            print('have highRun')
            continue

        #등록된 지정가가 있을지 모르니 초기화
        limitOrderCancel(t)

        accountApi.margin_mode(t, coin, 'crossed')
        accountApi.leverage(t, coin, leverage, 'long')
        accountApi.leverage(t, coin, leverage, 'short')

        #구매중인게 있을땐 시장가 매도
        if bool(tickerDict.get(t)) == True:
            if bool(tickerDict[t]['long'].get('orderId')) == True:
                orderId = tickerDict[t]['long']['orderId']
                result = planApi.cancel_plan(t, coin, orderId, 'normal_plan')
                if result is not None:
                    print(getTime(), t, '초기화로 스탑리밋 대기 취소')                
                    
            if bool(tickerDict[t]['short'].get('orderId')) == True:
                orderId = tickerDict[t]['short']['orderId']
                result = planApi.cancel_plan(t, coin, orderId, 'normal_plan')
                if result is not None:
                    print(getTime(), t, '초기화로 스탑리밋 대기 취소')                

            if bool(tickerDict[t]['long'].get('size')) == True and bool(tickerDict[t]['long'].get('buy')) == True:
                size = tickerDict[t]['long']['size']
                result = orderApi.place_order(t, marginCoin=coin, size=size, side='close_long', orderType='market', timeInForceValue='normal')
                if result is not None:
                    #msg : 예약 매수 완료
                    print(getTime(), t, '초기화로 인해 시장가 매도')                
                    
            if bool(tickerDict[t]['short'].get('size')) == True and bool(tickerDict[t]['short'].get('buy')) == True:
                size = tickerDict[t]['short']['size']
                result = orderApi.place_order(t, marginCoin=coin, size=size, side='close_short', orderType='market', timeInForceValue='normal')
                if result is not None:
                    #msg : 예약 매수 완료
                    print(getTime(), t, '초기화로 인해 시장가 매도')                

            if bool(tickerDict[t]['long'].get('tkOrderId')) == True:
                tkOrderId = tickerDict[t]['long']['tkOrderId']
                result = planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')
                if result is not None:
                    print(getTime(), t, '초기화로 인해 익절 대기 취소')

            if bool(tickerDict[t]['short'].get('tkOrderId')) == True:
                tkOrderId = tickerDict[t]['short']['tkOrderId']
                result = planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')
                if result is not None:
                    print(getTime(), t, '초기화로 인해 익절 대기 취소')


        tickerDict[t] = {}
        tickerDict[t]['long'] = {}
        tickerDict[t]['short'] = {}

        schedule.cancel_job(oneDayJob)
        oneDayJob = schedule.every(120).seconds.do(lambda: oneDay())


def getNowStatus(t):
    endTime = int(pydatetime.datetime.now().timestamp()) * 1000
    historyResult = orderApi.history(t, endTime - (86400 * 1000 * 10), endTime, 1)
    if historyResult is not None:
        historyList = historyResult['data']['orderList']
        if historyList is not None and len(historyList) > 0:
            history = historyList[0]
            if history['state'] == 'filled':
                return history
    else:
        print('!!history none!!')
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
            print(t, '초기화로 인한 지정가 대기 취소')


def oneDay():
    for t in tickers:
    # for i in range(len(tickers)):
        # t = tickers[i]
        # print(t, datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), 'call')
        # print(tickerDict[t])
        # tickerDict[t]['size'] = 0.1
        # print(tickerDict[t])
        
        #교차 : crossed
        #격리 : fixed
        # if isOnce == False:
        #     accountApi.margin_mode(t, coin, 'crossed')
        #     accountApi.leverage(t, coin, leverage, 'long')
        #     accountApi.leverage(t, coin, leverage, 'short')
        #     isOnce = True
        #     time.sleep(1)

        open = 0
        high = 0
        low = 0
        close = 0
        
        nowLow = 0
        nowHigh = 0
        nowClose = 0
        
        while True:
            # period: 60, 300, 900, 1800, 3600,14400,43200, 86400, 604800
            candle_data = get_candle(t, 86400, 2)
            
            if candle_data == None:
                time.sleep(1)
                continue
            
            if len(candle_data) > 1:
                # print(t, candle_data[-2])
                open = float(candle_data[-2][1]) #전날 시가
                high = float(candle_data[-2][2]) #전날 고가
                low = float(candle_data[-2][3]) #전날 저가
                close = float(candle_data[-2][4]) #전날 종가

                nowHigh = float(candle_data[-1][2]) #오늘 종가
                nowLow = float(candle_data[-1][3]) #오늘 종가
                nowClose = float(candle_data[-1][4]) #오늘 종가

                if high > 0 and low > 0 and close > 0:
                    break
                else:
                    time.sleep(1)
            else:
                time.sleep(1)

            
        # buyResult = orderApi.place_order(t, coin, size=getSize(t), side='open_long', orderType='limit', price=candle_data[-1][4], timeInForceValue='normal')
        # detailResult = orderApi.detail(t, buyResult['data']['orderId'])
        # print(detailResult)
        # 900575225571864579
#         if isOrder == False:
#             print(candle_data[-1][4])
#             buyResult = planApi.place_plan(t, marginCoin=coin, size=getSize(t), side='open_long', orderType='limit',
#                                         triggerPrice=candle_data[-1][4],
#                                         executePrice=candle_data[-1][4],
#                                         triggerType='fill_price',
#                                         presetStopLossPrice=40000)
#             isOrder = True
            
# #'orderId':'900578326017454081'
#         while isBuy == False:
#             endTime = int(pydatetime.datetime.now().timestamp()) * 1000           #현재
#             historyResult = orderApi.history(t, endTime - (86400 * 1000 * 10), endTime, 200)
#             historyList = historyResult['data']['orderList']
#             if historyList is not None:
#                 for item in historyList:
#                     if item['clientOid'] == buyResult['data']['orderId']:
#                         print(item)
#                         if item['state'] == 'filled':
#                             buyPrice = item['priceAvg']
#                             print('매수 됨', buyPrice)
#                             isBuy = True
#                             break
#             time.sleep(1)
        
#         print()
        # marketPrice = marketApi.market_price(t)
        # if marketPrice is None:
        #     print('marketPrice is none')
        #     #API 에러가 났을시 컨티뉴해서 다음 턴에 다시 시도한다
        #     continue
                    
        # currentPrice = float(marketPrice['data']['markPrice'])
        currentPrice = float(candle_data[-1][4])
        
        #가격이 0.1보다 작은건 패스
        if currentPrice <= 0.1:
            continue
        
        # print('currentPrice : ', currentPrice)
        # print('price : ', float(candle_data[-1][4]))
        
        # market = marketApi.market_price(t)
        # if market is None:
        #     print('marketPrice is none')
        # marketPrice = float(market['data']['markPrice'])

        buffer = high - low
        beforePer = round(((high - low) / low) * 100, 2)
        if beforePer < 4:
            #변동폭이 4% 미만일 경우 4%로 고정
            buffer = low * 0.04
        elif beforePer > 8:
            #변동폭이 8% 이상일 경우 8%로 고정
            buffer = low * 0.08
        
        #minTradeNum : 사이즈 소숫점 자리 수
        #pricePlace : 가격 소숫점 자리 수
              
        long_buffer = setEndStep(t, round((buffer) * k_long, priceDecimal(t)))
        short_buffer = setEndStep(t, round((buffer) * k_short, priceDecimal(t)))
        longPrice = setEndStep(t, round(close + long_buffer, priceDecimal(t)))
        shortPrice = setEndStep(t, round(close - short_buffer, priceDecimal(t)))

###
        if nowHigh > longPrice:
            # print(t, '이미 롱 매수 타이밍 지남')
            continue
        elif nowLow < shortPrice:
            # print(t, '이미 숏 매수 타이밍 지남')
            continue
        
        if longPrice == shortPrice:
            print('롱가격과 숏가격이 같아서 패스 (문제있는거임)')
            continue
        # if getDigits(currentPrice) > 1:
        #     longPrice = round(close + long_buffer, getDigits(currentPrice))
        #     shortPrice = round(close - short_buffer, getDigits(currentPrice))
        # else:
        #     longPrice = removeLastNum(round(close + long_buffer, getDigits(currentPrice)))
        #     shortPrice = removeLastNum(round(close - short_buffer, getDigits(currentPrice)))
        
        nowStatus = getNowStatus(t)
        
        if bool(tickerDict[t].get('reservation')) == False:
            #예약 매수 걸려있지 않은 경우 롱 숏 잡아두기
            size = getSize(t) 
            
            #손절라인은 전날 종가 (변동성 돌파 후 다시 종가를 터치 했을때)
            lossPrice = setEndStep(t, round(close, priceDecimal(t)))
            
            print(t, '롱 매수 예약 가격 : ', longPrice)
            print(t, '롱 손절 예약 가격 : ', lossPrice)
            
            buyResult = planApi.place_plan(t, marginCoin=coin, size=size, side='open_long', orderType='limit',
                            triggerPrice=longPrice,
                            executePrice=longPrice,
                            triggerType='fill_price',
                            presetStopLossPrice=lossPrice)
            if type(buyResult) == str:
                continue
            
            if buyResult is not None:
                tickerDict[t]['long']['orderId'] = buyResult['data']['orderId']   #예약 아이디
                tickerDict[t]['long']['size'] = size   #매수 건 사이즈
                tickerDict[t]['long']['buy'] = False   #매수가 됐는지 여부
                msg = t + ' long 예약매수 완료 ' + str(round(longPrice * size , 2))
                print(getTime(), msg)
                # bot.sendMessage(chat_id=chatId, text=msg)
            else:
                # bot.sendMessage(chat_id=chatId, text=(t + '예약매수 에러'))
                print(t, 'buy api none')
                
            
            print(t, '숏 매수 예약 가격 : ', shortPrice)
            print(t, '숏 손절 예약 가격 : ', lossPrice)

            buyResult = planApi.place_plan(t, marginCoin=coin, size=size, side='open_short', orderType='limit',
                            triggerPrice=shortPrice,
                            executePrice=shortPrice,
                            triggerType='fill_price',
                            presetStopLossPrice=lossPrice)
            
            if type(buyResult) == str:
                continue

            if buyResult is not None:
                # print('숏 예약 아이디 : ', buyResult['data']['orderId'])
                tickerDict[t]['short']['orderId'] = buyResult['data']['orderId']   #예약 아이디
                tickerDict[t]['short']['size'] = size   #매수 건 사이즈
                tickerDict[t]['short']['buy'] = False   #매수가 됐는지 여부
                msg = t + ' short 예약매수 완료 ' + str(round(longPrice * size , 2))
                print(getTime(), msg)
                # bot.sendMessage(chat_id=chatId, text=msg)
            else:
                print(t, 'buy api none')
                # bot.sendMessage(chat_id=chatId, text=(t + '예약매수 에러'))                
                                
            tickerDict[t]['reservation'] = True    #예약 걸었는지 여부
            
            # print(buyResult)
        
        else:
            # #예약 매수가 걸려 있는 상태라면 매수 여부 체크
            # if bool(tickerDict[t]['long'].get('orderId')) == True and bool(tickerDict[t]['long'].get('buy')) == False:
            if bool(tickerDict[t]['long'].get('buy')) == False:
                if nowStatus is not None and nowStatus['side'] == 'open_long':
                    buyPrice = nowStatus['priceAvg']
                    tickerDict[t]['long']['buy'] = True
                    tickerDict[t]['long']['price'] = buyPrice
                    msg = t + ' long 매수 완료 ' + str(buyPrice)
                    print(getTime(), msg)
                    # bot.sendMessage(chat_id=chatId, text=msg)
                    
            # if bool(tickerDict[t]['short'].get('orderId')) == True and bool(tickerDict[t]['short'].get('buy')) == False:
            if bool(tickerDict[t]['short'].get('buy')) == False:
                if nowStatus is not None and nowStatus['side'] == 'open_short':
                    buyPrice = nowStatus['priceAvg']
                    tickerDict[t]['short']['buy'] = True
                    tickerDict[t]['short']['price'] = buyPrice
                    msg = t + ' short 매수 완료 ' + str(buyPrice)
                    print(getTime(), msg)
                    # bot.sendMessage(chat_id=chatId, text=msg)
        
            if bool(tickerDict[t]['long'].get('buy')) == True or bool(tickerDict[t]['short'].get('buy')) == True: 
                #매수 된 경우
                position = 'long'
                side = 'close_long'
                multiply = 1
                if bool(tickerDict[t]['short'].get('buy')) == True:
                    position = 'short'
                    side = 'close_short'
                    multiply = -1
                
                try:
                    highRun.remove(t)
                except ValueError:
                    pass


                #먼저 조건에 도달하여 매도가 됐는지 확인
                isSell = False
                if nowStatus is not None and nowStatus['side'] == side and nowStatus['state'] == 'filled':
                    #매도 됨
                    if position == 'long':
                        tickerDict[t]['long'] = {}
                    if position == 'short':
                        tickerDict[t]['short'] = {}
                    
                    isSell = True
                    msg = t + ' ' + position + ' 매도 완료 ' + str(nowStatus['totalProfits'])
                    print(getTime(), msg)
                    # bot.sendMessage(chat_id=chatId, text=msg)
                                        
                    
                    #스탑리밋에 등록된게 있으면 취소
                    if bool(tickerDict[t][position].get('tkOrderId')) == True:
                        tkOrderId = tickerDict[t][position]['tkOrderId']
                        result = planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')
                        print('tk result : ', t, result)
                        if result is None:
                            print(t, '익절 라인 걸어둔거 취소하려고 했으나 에러남 왜 때문이지?')

                    #포지션이 변경 됐을때 예약대기가 취소되어서 이 부분은 주석처리 함                    
                    # #지정가에 등록된게 있다면 그것도 취소    
                    # limitOrderCancel(t)
                    
                if isSell == True:
                    continue    


                market = marketApi.market_price(t)
                if market is None:
                    print('market is none')
                    #API 에러가 났을시 컨티뉴해서 다음 턴에 다시 시도한다
                    continue
                    
                marketPrice = float(market['data']['markPrice'])

                buyPrice = tickerDict[t][position]['price']
                per = round((((marketPrice / buyPrice) * 100) - 100) * leverage * multiply, 2)
                # print(t, 'per : ', per)

                if per >= 30:
                    if bool(tickerDict[t][position].get('tkMargin')) == False:
                        tickerDict[t][position]['tkMargin'] = 0.0
                    
                    # if bool(tickerDict[t][position].get('oldPer')) == False:
                    #     tickerDict[t][position]['oldPer'] = 0.0

                    if bool(tickerDict[t][position].get('maxPer')) == False:
                        tickerDict[t][position]['maxPer'] = 0.0

                    if per < 50:
                        #수익률이 30~49% 사이인 경우 70% 떨어진 경우 익절
                        tkMargin = 0.7
                    elif per < 100:
                        #수익률이 50~99% 사이인 경우 50% 떨어진 경우 익절
                        tkMargin = 0.5
                    else:
                        #수익률이 100% 이상인 경우 30% 떨어진 경우 익절
                        tkMargin = 0.3
                        highRun.append(t)
                    
                    maxPer = tickerDict[t][position]['maxPer']
                    # oldPer = tickerDict[t][position]['oldPer']
                    
                    #수익률이 최고가 대비 올랐을때만 업데이트
                    if per > maxPer:
                        tickerDict[t][position]['maxPer'] = per
                        
                        oldTkMargin = tickerDict[t][position]['tkMargin']
                        if oldTkMargin != tkMargin:
                            msg = t + ' ' + position + ' 익절라인 업데이트 : ' + str(round(((1-tkMargin) * 100.0), 2)) + '%'
                            print(getTime(), msg)
                            # bot.sendMessage(chat_id=chatId, text=msg)
                            
                        tickerDict[t][position]['tkMargin'] = tkMargin

                        if bool(tickerDict[t][position].get('tkOrderId')) == True:
                            tkOrderId = tickerDict[t][position]['tkOrderId']
                            planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')

                        # triggerPrice = marketPrice - (((marketPrice - buyPrice) * tkMargin) * (multiply))
                        triggerPrice = marketPrice - (((marketPrice - buyPrice) * tkMargin))
                        triggerPrice = setEndStep(t, round(triggerPrice, priceDecimal(t)))
                        
                        size = tickerDict[t][position]['size']
                        tkResult = planApi.place_plan(t, marginCoin=coin, size=size, side=side, orderType='limit',
                                triggerPrice=triggerPrice,
                                triggerType='fill_price',
                                executePrice=triggerPrice)
                        if tkResult is not None:
                            tickerDict[t][position]['tkOrderId'] = tkResult['data']['orderId']

                        
                        
                    # if per > oldPer:    #수익률이 올랐을때만 업데이트
                    #     oldTkMargin = tickerDict[t][position]['tkMargin']
                    #     if oldTkMargin != tkMargin:
                    #         msg = t + ' ' + position + ' 익절라인 업데이트 : ' + str((1-tkMargin) * 100.0) + '%'
                    #         print(getTime(), msg)
                    #         # bot.sendMessage(chat_id=chatId, text=msg)

                    #     tickerDict[t][position]['tkMargin'] = tkMargin

                    #     if bool(tickerDict[t][position].get('tkOrderId')) == True:
                    #         tkOrderId = tickerDict[t][position]['tkOrderId']
                    #         planApi.cancel_plan(t, coin, tkOrderId, 'normal_plan')

                    #     triggerPrice = marketPrice - (((marketPrice - buyPrice) * tkMargin) * (multiply*-1))
                    #     triggerPrice = setEndStep(t, round(triggerPrice, priceDecimal(t)))
                        
                    #     size = tickerDict[t][position]['size']
                    #     tkResult = planApi.place_plan(t, marginCoin=coin, size=size, side=side, orderType='limit',
                    #             triggerPrice=triggerPrice,
                    #             triggerType='fill_price',
                    #             executePrice=triggerPrice)
                    #     if tkResult is not None:
                    #         tickerDict[t][position]['tkOrderId'] = tkResult['data']['orderId']
                            
                    # tickerDict[t][position]['oldPer'] = per
                        

        time.sleep(1)
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
schedule.every().day.at("01:00:01").do(lambda: initTickers())


print('start')
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








