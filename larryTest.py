from pickle import FALSE, TRUE
from re import I
import time
import os
import sys
import logging
import traceback
from tracemalloc import start
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
import datetime

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
leverage = 1
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

marketPrice = marketApi.market_price('BTCUSDT_UMCBL')
if marketPrice is None:
    print('marketPrice is none')

currentPrice = float(marketPrice['data']['markPrice'])

# print(currentPrice)
# currentPrice = getCurrentPrice(currentPrice)
if coin == 'SUSDT':
    account = accountApi.accounts('sumcbl')
else:
    account = accountApi.accounts('umcbl')

myAvailable = float(account['data'][0]['available'])

sizePer = 0.5 #0.1이면 내 자산의 10%
size = round(((myAvailable * sizePer) * leverage) / currentPrice, 3)
print(size)


bot.sendMessage(chat_id=chatId, text='test msg')


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
    endTime = int(pydatetime.datetime.now().timestamp()) * 1000
    try:
        startTime = endTime - ((time*1000)*count)
        # start2 = (endTime * 1000) - (((time*2)*1000)*count)
        # start3 = (endTime * 1000) - (((time*3)*1000)*count)
        # start4 = (endTime * 1000) - (((time*4)*1000)*count)
        # start5 = (endTime * 1000) - (((time*5)*1000)*count)

        candles = marketApi.candles(ticker, granularity=time,startTime=startTime, endTime=endTime) #15분봉 200개
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

    # return marketApi.candles(ticker, granularity=900,startTime=(endTime * 1000) - ((time*1000)*count), endTime=endTime * 1000) #15분봉 200개

def get_candle_time(time, start, end):
    # endTime = int(pydatetime.datetime.now().timestamp()) * 1000
    try:
        # startTime = endTime - ((time*1000)*count)
        # start2 = (endTime * 1000) - (((time*2)*1000)*count)
        # start3 = (endTime * 1000) - (((time*3)*1000)*count)
        # start4 = (endTime * 1000) - (((time*4)*1000)*count)
        # start5 = (endTime * 1000) - (((time*5)*1000)*count)

        candles = marketApi.candles(ticker, granularity=time,startTime=start, endTime=end) #15분봉 200개
        # candles2 = marketApi.candles(ticker, granularity=time, startTime=start2, endTime=start) #15분봉 200개
        # candles3 = marketApi.candles(ticker, granularity=time, startTime=start3, endTime=start2) #15분봉 200개
        # candles4 = marketApi.candles(ticker, granularity=time, startTime=start4, endTime=start3) #15분봉 200개
        # candles5 = marketApi.candles(ticker, granularity=time, startTime=start5, endTime=start4) #15분봉 200개
        # candles = candles + candles2 + candles3# + candles4 + candles5
        if candles == None:
            # print(ticker, time, (endTime * 1000) - ((time*1000)*count), endTime * 1000)
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




buySize = 0
k = 0.5
longOrderId = 0
shortOrderId = 0

total = 0.0
orgTotalPer = 0.0


    
def test(ticker, candle_data):
    #          1   5    15   30    1H    4H     12H    1D      1W
    # period: 60, 300, 900, 1800, 3600, 14400, 43200, 86400, 604800
    global total
    global orgTotalPer
    
    k = 0.5
    # leverage = 1
    fee = 0.1
    # candle_data = get_candle(ticker, 86400, 100)
    longTotalPer = 0.0
    shortTotalPer = 0.0
    totalPer = 0.0
    
    if len(candle_data) > 0:
        orgStart = float(candle_data[0][4])
        orgEnd = float(candle_data[-1][4])
        orgPer = (((((orgEnd / orgStart) * 100) - 100)) * leverage)
        print('keep per : ', round(orgPer, 1))
        orgTotalPer += orgPer

    for i in range(1, len(candle_data)-1):
        #전날 어떻게 끝났는지 알아온다
        open = float(candle_data[i][1]) #시가
        hight = float(candle_data[i][2]) #고가
        low = float(candle_data[i][3]) #저가
        close = float(candle_data[i][4]) #종가

        beforeOpen = float(candle_data[i-1][1]) #전날 시가
        beforeHight = float(candle_data[i-1][2]) #전날 고가
        beforeLow = float(candle_data[i-1][3]) #전날 저가
        beforeClose = float(candle_data[i-1][4]) #전날 종가
        
        lPer = 0
        sPer = 0
        isLong = False
        isShort = False
        # if beforeOpen < beforeClose:
        #     #롱
        longPrice = beforeClose + ((beforeHight - beforeLow) * k)
        if hight > longPrice:
            #롱 매수
            per = ((((close / longPrice) * 100) - 100) * leverage) - (fee * leverage)
            # per = ((((nextClose / longPrice) - 1) * 100) * leverage) - (fee * leverage)
            # per = (round(((longPrice / nextClose) * 100) - 100, 2) * leverage) - (fee * leverage)
            totalPer += per
            longTotalPer += per
            isLong = True
            lPer = per
            # print(per)
        # else:
            # print('롱 매수하지 않음')

        # if beforeOpen > beforeClose:
        # #숏
        shortPrice = beforeClose - ((beforeHight - beforeLow) * k)
        if low < shortPrice:
            #숏 매수
            per = (((((close / shortPrice) * 100) - 100) * -1) * leverage) - (fee * leverage)
            # per = ((((nextClose / longPrice) - 1) * 100) * leverage) - (fee * leverage)
            # per = (round(((longPrice / nextClose) * 100) - 100, 2) * leverage) - (fee * leverage)
            totalPer += per
            shortTotalPer += per
            isShort = True
            sPer = per
            # print(per)
        # else:
            # print('롱 매수하지 않음')

        # if isLong == True and isShort == True:
        #     print('롱 숏 둘 다 잡음', 'long per : ', round(lPer,2), 'short per : ', round(sPer,2))
            
            
    # for i in range(len(candle_data)-1):
    # # i = 1
    #     open = float(candle_data[i][1]) #시가
    #     hight = float(candle_data[i][2]) #고가
    #     low = float(candle_data[i][3]) #저가
    #     close = float(candle_data[i][4]) #종가
        
    #     # longPrice = close + ((hight - low) * k)
    #     # nextHight = float(candle_data[i+1][2]) #다음 봉의 고가
    #     # if nextHight > longPrice:
    #     #     #롱 매수
    #     #     nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
    #     #     per = (round(((longPrice / nextClose) * 100) - 100, 2) * leverage) - (fee * leverage)
    #     #     totalPer += per
    #     #     longTotalPer += per

    #     # shortPrice = close - ((hight - low) * k)
    #     # nextLow = float(candle_data[i+1][3]) #다음 봉의 저가
    #     # if nextLow < shortPrice:
    #     #     #숏 매수
    #     #     nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
    #     #     per = (round(((shortPrice / nextClose) * 100) - 100, 2) * leverage) * (fee * leverage)
    #     #     totalPer += per
    #     #     shortTotalPer += per

    #     if open < close:
    #         #롱
    #         longPrice = close + ((hight - low) * k)
    #         nextHight = float(candle_data[i+1][2]) #다음 봉의 고가
    #         if nextHight > longPrice:
    #             #롱 매수
    #             nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
    #             per = ((nextClose / longPrice) * 100) - 100
    #             # per = ((((nextClose / longPrice) - 1) * 100) * leverage) - (fee * leverage)
    #             # per = (round(((longPrice / nextClose) * 100) - 100, 2) * leverage) - (fee * leverage)
    #             totalPer += per
    #             longTotalPer += per
    #             # print(per)
    #         # else:
    #             # print('롱 매수하지 않음')
        
    #     if open > close:
    #         #숏
    #         shortPrice = close - ((hight - low) * k)
    #         nextLow = float(candle_data[i+1][3]) #다음 봉의 저가
    #         if nextLow < shortPrice:
    #             #숏 매수
    #             nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
    #             per = (((nextClose / shortPrice) * 100) - 100) * -1
    #             # per = (((((nextClose / shortPrice) - 1) * 100) * leverage) * -1) - (fee * leverage)
    #             # per = (round(((shortPrice / nextClose) * 100) - 100, 2) * leverage) * (fee * leverage)
    #             totalPer += per
    #             shortTotalPer += per
    #                 # print(per)
    #             # else:
    #                 # print('숏 매수하지 않음')

    print(ticker, 'longTotalPer : ', round(longTotalPer, 2))
    print(ticker, 'shortTotalPer : ', round(shortTotalPer, 2))
    total += totalPer
    print(ticker, round(totalPer, 2), '%')
    # print('keep total per : ', round(orgTotalPer, 1))
    print()


# #지정가 리스트 긁어오기
# limitList = orderApi.current('SBTCSUSDT_SUMCBL')
# print(limitList)

# cancelOrders = []
# for i in range(0, len(limitList['data'])):
#     data = limitList['data'][i]
#     if data['state'] == 'new':
#         orderId = data['orderId']
#         cancelOrders.append(orderId)
        
# #이게 지정가 취소 API임
# result = orderApi.cancel_batch_orders('SBTCSUSDT_SUMCBL', 'SUSDT', cancelOrders)
# print(result)
        



# endTime = int(pydatetime.datetime.now().timestamp()) * 1000
# startTime = endTime - ((86400*1000)*3)
# result = orderApi.history('SBTCSUSDT_SUMCBL', startTime, endTime, pageSize=10)
# print(result)

# result = result = orderApi.fills('SBTCSUSDT_SUMCBL','884944391409483777')
# print(result)

# result = result = orderApi.cancel_batch_orders('SBTCSUSDT_SUMCBL', 'SUSDT', ['884947623578595328', '884944612642942976'])
# print(result)

# result = orderApi.place_order('SBTCSUSDT_SUMCBL', marginCoin='SUSDT', size=0.01, side='open_long', orderType='limit', price=38000, timeInForceValue='normal')
# print(result)

# # result = planApi.cancel_plan('SBTCSUSDT_SUMCBL', 'SUSDT', '884941906347278337', 'normal_plan')
# # print(result)

# result = planApi.place_plan('SBTCSUSDT_SUMCBL', marginCoin='SUSDT', size=0.01, side='open_long', orderType='limit',
#                             triggerPrice=38702,
#                             executePrice=38702,
#                             triggerType='fill_price')
#                             # presetStopLossPrice=longSL)
# print(result)




if coin == 'SUSDT':
    tickers = ['SBTCSUSDT_SUMCBL', 'SETHSUSDT_SUMCBL', 'SEOSSUSDT_SUMCBL']
else:
    # tickers = ['BTCUSDT_UMCBL']
    #'EGLDUSDT_UMCBL', 'KSMUSDT_UMCBL',
    tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL', 'ADAUSDT_UMCBL',
           'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL', 'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL',
           'BNBUSDT_UMCBL', 'UNIUSDT_UMCBL', 'ICPUSDT_UMCBL', 'FILUSDT_UMCBL', 'XLMUSDT_UMCBL',
           'AVAXUSDT_UMCBL', 'DASHUSDT_UMCBL',
           'XEMUSDT_UMCBL', 'MANAUSDT_UMCBL', 'SANDUSDT_UMCBL', 'CRVUSDT_UMCBL',
           'ARUSDT_UMCBL', 'PEOPLEUSDT_UMCBL',
           'LRCUSDT_UMCBL']


endTime = int(pydatetime.datetime.now().timestamp()) * 1000
startTime = endTime - ((86400*1000)*2) #2부터 해야 전날 데이터를 가져옴
candleTotalData = get_candle_time(86400, startTime, endTime)
for i in range(1, 1):
    tempData = get_candle_time(86400, startTime - (((86400*1000)*100) * i), endTime - (((86400*1000)*100) * i))
    t = tempData + candleTotalData
    candleTotalData = t
    # candleTotalData += tempData
    time.sleep(0.05)

tmpTime = float(candleTotalData[0][0]) / 1000
dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tmpTime))
print(dt)

for t in tickers:
    test(t, candleTotalData)
    # time.sleep(0.05)

print('total :', round(total, 2), '%')
print()


