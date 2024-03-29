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

api_key = "bg_d824038ea0c0f9a80ecc2b62b4e46e3a"
secret_key = "9cb1d21914debdda86deeb202af7b146954c28b85c80bdd22dc9850116b4810a"
passphrase = "larryapi1"

BTC_Ticker = 'SBTCSUSDT_SUMCBL'
ETH_Ticker = 'SETHSUSDT_SUMCBL'
EOS_Ticker = 'SEOSSUSDT_SUMCBL'

ticker = BTC_Ticker
coin = 'USDT'
leverage = 2
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


import pandas as pd
import requests
import pandas as pd
import time
import webbrowser
import numpy as np

tickers = [BTC_Ticker, ETH_Ticker, EOS_Ticker]

def get_candle(ticker, time, count):
    endTime = int(pydatetime.datetime.now().timestamp())
    try:
        startTime = (endTime * 1000) - ((time*1000)*count)

        candles = marketApi.candles(ticker, granularity=time,startTime=startTime, endTime=endTime * 1000) #15분봉 200개
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
    return round(((myAvailable * 0.1) * leverage) / currentPrice, 3)

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
total = 0.0

def test(ticker):
    # period: 60, 300, 900, 1800, 3600,14400,43200, 86400, 604800
    global total
    k = 0.5
    fee = 0.1
    candle_data = get_candle(ticker, 86400, 5)
    longTotalPer = 0.0
    shortTotalPer = 0.0
    totalPer = 0.0
    
    for i in range(len(candle_data)-1):
        open = float(candle_data[i][1]) #시가
        hight = float(candle_data[i][2]) #고가
        low = float(candle_data[i][3]) #저가
        close = float(candle_data[i][4]) #종가
        
        if open < close:
            #롱
            longPrice = close + ((hight - low) * k)
            nextHight = float(candle_data[i+1][2]) #다음 봉의 고가
            if nextHight > longPrice:
                #롱 매수
                nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
                per = (round(((longPrice / nextClose) * 100) - 100, 2) * leverage) - (fee * leverage)
                totalPer += per
                longTotalPer += per
                # print(per)
            # else:
                # print('롱 매수하지 않음')
        
        if open > close:
            #숏
            shortPrice = close - ((hight - low) * k)
            nextLow = float(candle_data[i+1][3]) #다음 봉의 저가
            if nextLow < shortPrice:
                #숏 매수
                nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
                per = (round(((shortPrice / nextClose) * 100) - 100, 2) * leverage) * (fee * leverage)
                totalPer += per
                shortTotalPer += per
                # print(per)
            # else:
                # print('숏 매수하지 않음')
                
    # print(ticker, 'longTotalPer : ', round(longTotalPer, 2))
    # print(ticker, 'shortTotalPer : ', round(shortTotalPer, 2))
    total += totalPer
    print(ticker, round(totalPer, 2), '%')
    print()





if coin == 'SUSDT':
    tickers = ['SBTCSUSDT_SUMCBL', 'SETHSUSDT_SUMCBL', 'SEOSSUSDT_SUMCBL']
    # tickers = ['SBTCSUSDT_SUMCBL']
else:
    # tickers = ['ETCUSDT_UMCBL']
    #'EGLDUSDT_UMCBL', 'KSMUSDT_UMCBL',
    # tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL', 'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL',
    #            'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL','BNBUSDT_UMCBL', 'UNIUSDT_UMCBL', 'ICPUSDT_UMCBL', 'FILUSDT_UMCBL', 'XLMUSDT_UMCBL','AVAXUSDT_UMCBL', 'DASHUSDT_UMCBL', 'XEMUSDT_UMCBL',
    #            'MANAUSDT_UMCBL', 'SANDUSDT_UMCBL', 'CRVUSDT_UMCBL','ARUSDT_UMCBL', 'PEOPLEUSDT_UMCBL', 'LRCUSDT_UMCBL']
    tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL', 'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL',
               'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL','BNBUSDT_UMCBL', 'UNIUSDT_UMCBL', 'ICPUSDT_UMCBL', 'FILUSDT_UMCBL', 'XLMUSDT_UMCBL','AVAXUSDT_UMCBL', 'DASHUSDT_UMCBL', 'XEMUSDT_UMCBL']

# for t in tickers:
#     test(t)
#     time.sleep(0.05)

# print('total :', round(total, 2), '%')
# print()

buySizes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
longOrderIds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
shortOrderIds = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
               0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# longResult = planApi.place_plan('SBTCSUSDT_SUMCBL', marginCoin=coin, size=0.01, side='open_long', orderType='market',
#                             triggerPrice=37905,
#                             executePrice=37905,
#                             triggerType='fill_price',
#                             presetStopLossPrice=36000)

def oneDay():
    time.sleep(1)
    
    global buySizes
    global longOrderIds
    global shortOrderIds

    for i in range(len(tickers)):
        t = tickers[i]
        print(t, datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), 'call')

        accountApi.margin_mode(t, coin, 'fixed')
        time.sleep(1)
        accountApi.leverage(t, coin, leverage, 'long')
        time.sleep(1)
        accountApi.leverage(t, coin, leverage, 'short')
        time.sleep(1)

        open = 0
        hight = 0
        low = 0
        close = 0
        
        while True:
            # period: 60, 300, 900, 1800, 3600,14400,43200, 86400, 604800
            candle_data = get_candle(t, 86400, 2)
            
            if candle_data == None:
                time.sleep(1)
                continue
            
            if len(candle_data) > 1:
                # print(t, candle_data[-2])
                open = float(candle_data[-2][1]) #전날 고가
                hight = float(candle_data[-2][2]) #전날 고가
                low = float(candle_data[-2][3]) #전날 저가
                close = float(candle_data[-2][4]) #전날 종가

                if hight > 0 and low > 0 and close > 0:
                    break
                else:
                    time.sleep(1)
            else:
                time.sleep(1)


        #지정가 리스트 긁어오기
        limitList = orderApi.current(t)
        cancelOrders = []
        for i in range(0, len(limitList['data'])):
            data = limitList['data'][i]
            if data['state'] == 'new':
                orderId = data['orderId']
                cancelOrders.append(orderId)
                
        #등록된 지정가가 있으면 cancel
        if len(cancelOrders) > 0:
            orderApi.cancel_batch_orders(t, coin, cancelOrders)

        time.sleep(1)

        marketPrice = marketApi.market_price(t)
        if marketPrice is None:
            print('marketPrice is none')
        
        if coin == 'SUSDT':
            account = accountApi.accounts('sumcbl')
        else:
            account = accountApi.accounts('umcbl')
        
        myAvailable = float(account['data'][0]['available'])

        longOrderId = longOrderIds[i]
        shortOrderId = shortOrderIds[i]
        buySize = buySizes[i]


        currentPrice = float(marketPrice['data']['markPrice'])
        size = 0
        sizePer = 0.1 #0.1이면 내 자산의 10%
        longPrice = 0
        shortPrice = 0

        if currentPrice >= 10000:
            longPrice = round(close + ((hight - low) * k), 0)
            shortPrice = round(close - ((hight - low) * k), 0)
            size = round(((myAvailable * sizePer) * leverage) / currentPrice, 3)
        elif currentPrice >= 1000:
            longPrice = round(close + ((hight - low) * k), 1)
            shortPrice = round(close - ((hight - low) * k), 1)
            size = round(((myAvailable * sizePer) * leverage) / currentPrice, 2)
        elif currentPrice >= 100:
            longPrice = round(close + ((hight - low) * k), 1)
            shortPrice = round(close - ((hight - low) * k), 1)
            size = round(((myAvailable * sizePer) * leverage) / currentPrice, 1)
        elif currentPrice >= 10:
            longPrice = round(close + ((hight - low) * k), 2)
            shortPrice = round(close - ((hight - low) * k), 2)
            size = round(((myAvailable * sizePer) * leverage) / currentPrice, 0)
        else:
            longPrice = round(close + ((hight - low) * k), 3)
            shortPrice = round(close - ((hight - low) * k), 3)
            size = round(((myAvailable * sizePer) * leverage) / currentPrice, 0)

        if longOrderId > 0:
            planApi.cancel_plan(t, coin, longOrderId, 'normal_plan')
            longOrderIds[i] = 0
        
        if shortOrderId > 0:
            planApi.cancel_plan(t, coin, shortOrderId, 'normal_plan')
            shortOrderIds[i] = 0

        time.sleep(1)

        result = orderApi.place_order(t, marginCoin=coin, size=buySize, side='close_long', orderType='market', timeInForceValue='normal')
        if result is not None:
            buySizes[i] = 0
            time.sleep(1)
            
        result = orderApi.place_order(t, marginCoin=coin, size=buySize, side='close_short', orderType='market', timeInForceValue='normal')
        if result is not None:
            buySizes[i] = 0
            time.sleep(1)

        longResult = planApi.place_plan(t, marginCoin=coin, size=size, side='open_long', orderType='market',
                                    triggerPrice=longPrice,
                                    executePrice=longPrice,
                                    triggerType='fill_price',
                                    presetStopLossPrice=shortPrice)
        if longResult is not None:
            longOrderIds[i] = int(getOrderId(longResult))
            time.sleep(1)
        else:
            print(t, 'longResult none')

        shortResult = planApi.place_plan(t, marginCoin=coin, size=size, side='open_short', orderType='market',
                                triggerPrice=shortPrice,
                                executePrice=shortPrice,
                                triggerType='fill_price',
                                presetStopLossPrice=longPrice)

        if shortResult is not None:
            shortOrderIds[i] = int(getOrderId(shortResult))
            time.sleep(1)
        else:
            print(t, 'shortResult none')

        buySizes[i] = size

        time.sleep(1)

oneDay()
schedule.every().day.at("01:00:01").do(lambda: oneDay())

while True:
    schedule.run_pending()
