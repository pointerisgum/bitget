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

tickers = [BTC_Ticker, ETH_Ticker, EOS_Ticker]

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
    closeStr = str(currentPrice).split('.')
    digits = 1
    if len(closeStr) == 2:
        digits = len(closeStr[1])  #소수점 몇자리인지

    return round(((myAvailable * 0.1) * leverage) / currentPrice, digits)
    # if ticker == BTC_Ticker:
    #     size = str(((myAvailable * 0.1) * leverage) / currentPrice)
    #     return size
    # elif ticker == ETH_Ticker:
    #     size = float(round(((myAvailable * 0.1) * leverage) / currentPrice, 2))
    #     return size
    # elif ticker == EOS_Ticker:
    #     size = int(round(((myAvailable * 0.1) * leverage) / currentPrice, 0))
    #     return size
    # return 0

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
        
        # longPrice = close + ((hight - low) * k)
        # nextHight = float(candle_data[i+1][2]) #다음 봉의 고가
        # if nextHight > longPrice:
        #     #롱 매수
        #     nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
        #     per = (round(((longPrice / nextClose) * 100) - 100, 2) * leverage) - (fee * leverage)
        #     totalPer += per
        #     longTotalPer += per

        # shortPrice = close - ((hight - low) * k)
        # nextLow = float(candle_data[i+1][3]) #다음 봉의 저가
        # if nextLow < shortPrice:
        #     #숏 매수
        #     nextClose = float(candle_data[i+1][4]) #다음 봉의 종가
        #     per = (round(((shortPrice / nextClose) * 100) - 100, 2) * leverage) * (fee * leverage)
        #     totalPer += per
        #     shortTotalPer += per

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
    # tickers = ['BTCUSDT_UMCBL', 'ETHUSDT_UMCBL', 'XRPUSDT_UMCBL', 'EOSUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL', 'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL',
    #            'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL','BNBUSDT_UMCBL', 'UNIUSDT_UMCBL', 'ICPUSDT_UMCBL', 'FILUSDT_UMCBL', 'XLMUSDT_UMCBL','AVAXUSDT_UMCBL', 'DASHUSDT_UMCBL', 'XEMUSDT_UMCBL']
    tickers = ['BTCUSDT_UMCBL']
    # tickers = ['SBTCSUSDT_SUMCBL']

tickers = []
tickerDict = {}

def initTickers():
    global tickers
    global tickerDict
    
    # for i in range(len(tickers)):
    #     key = tickers[i]
    #     dic = tickerDict[key]
    #     if bool(dic.get('orderId')) == True:
    #         if dic['type'] == 'long':
    #             orderApi.place_order(t, marginCoin=coin, size=dic['size'], side='close_long', orderType='market', timeInForceValue='normal')
    #             print(t + 'long' + '시장가로 던짐')
    #         else:
    #             orderApi.place_order(t, marginCoin=coin, size=dic['size'], side='close_short', orderType='market', timeInForceValue='normal')        
    #             print(t + 'short' + '시장가로 던짐')

    tickers = []
    tickerDict = {}    
    result = marketApi.tickers('UMCBL')
    for t in result['data']:
        tickers.append(t['symbol'])
        tickerDict[t['symbol']] = {'lossCnt':1, 'targetPer':0.011, 'cross':''}
    tickers.remove('BTCUSDT_UMCBL')

    
    # tickers = ['GMTUSDT_UMCBL']
    # tickerDict['GMTUSDT_UMCBL'] = {'lossCnt':1, 'targetPer':0.011, 'cross':''}
    #오늘 이미 많이 올라서 임시로 뺄 애들
    # tickers.remove('NEARUSDT_UMCBL')
    # tickers.remove('WAVESUSDT_UMCBL')

# print(tickerDict['XRPUSDT_UMCBL'])
# tickerDict['XRPUSDT_UMCBL']['orderId'] = '123'
# tickerDict['XRPUSDT_UMCBL']['size'] = '3'
# print(tickerDict)
# print(tickerDict['XRPUSDT_UMCBL']['orderId'])
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

def getSizePer():
    return 0.5

def getSize(t):
    available = 100 #내가 투자 할 총 시드
    
    marketPrice = marketApi.market_price(t)
    if marketPrice is None:
        print('marketPrice is none')
    price = float(marketPrice['data']['markPrice'])
    
    if price >= 10000:
        size = round(((available * getSizePer()) * leverage) / price, 3)
    elif price >= 1000:
        size = round(((available * getSizePer()) * leverage) / price, 2)
    elif price >= 100:
        size = round(((available * getSizePer()) * leverage) / price, 1)
    elif price >= 10:
        size = round(((available * getSizePer()) * leverage) / price, 0)
    else:
        size = round(((available * getSizePer()) * leverage) / price, 0)
    
    return size
                   
            
def check():
    # now = int(pydatetime.datetime.now().timestamp())
    # if now < 1649347200:
    #     return
     
    global buySizes
    global longOrderIds
    global shortOrderIds
    # print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), 'check')
    
    for i in range(len(tickers)):
        t = tickers[i]
        # print(t, datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), 'call')
        updateCross(t)
        cross = tickerDict[t]['cross']
        
        isMaxBuy = False
        orderCnt = 0
        for j in range(len(tickers)):
            if bool(tickerDict[tickers[j]].get('orderId')) == True:
                if int(tickerDict[tickers[j]]['orderId']) > 0:
                    orderCnt+=1
                    if orderCnt >= 3:
                        isMaxBuy = True
                        break
            
        #교차 : crossed
        #격리 : fixed
        accountApi.margin_mode(t, coin, 'crossed')
        accountApi.leverage(t, coin, leverage, 'long')
        accountApi.leverage(t, coin, leverage, 'short')

        open = 0
        hight = 0
        low = 0
        close = 0
        
        while True:
            # period: 60, 300, 900, 1800, 3600,14400,43200, 86400, 604800
            candle_data = get_candle(t, 86400, 0)
            
            if candle_data == None:
                time.sleep(1)
                continue
            elif len(candle_data) > 0:
                open = float(candle_data[0][1])
                hight = float(candle_data[0][2])
                low = float(candle_data[0][3])
                close = float(candle_data[0][4])
                # time.sleep(0.1)
                break
        
                       
        buyPrice = -1
        if bool(tickerDict[t].get('orderId')) == True:
            result = orderApi.detail(t, orderId=tickerDict[t]['orderId'])
            if result is not None:
                if result.get('data', None).get('priceAvg', None) is None:
                    buyPrice = -1
                else:
                    buyPrice = float(result['data']['priceAvg'])


        if bool(tickerDict[t].get('sellOrderId')) == True:
            result = orderApi.detail(t, orderId=tickerDict[t]['sellOrderId'])
            if result is not None:
                if result.get('data', None).get('state', None) is not None:
                    if result['data']['state'] == 'filled':
                        del tickerDict[t]['sellOrderId']
    
    
        closeStr = str(close).split('.')
        digits = 1
        if len(closeStr) == 2:
            digits = len(closeStr[1])  #소수점 몇자리인지

        #골든 또는 데드가 났는데 구매하지 않은 경우 무조건 구매
        if isMaxBuy == False and (cross == 'gold' or cross == 'dead') and bool(tickerDict[t].get('orderId')) == False and bool(tickerDict[t].get('sellOrderId')) == False and buyPrice == -1:
            #주문 전 등록된 체결이 안된 주문이 있으면 취소처리를 먼저 해준다
            limitList = orderApi.current(t)
            cancelOrders = []
            for i in range(0, len(limitList['data'])):
                data = limitList['data'][i]
                if data['state'] == 'new':
                    orderId = data['orderId']
                    cancelOrders.append(orderId)
                    
            if len(cancelOrders) > 0:
                if cross == 'gold':
                    print(t, '데드 -> 골드로 포지션 변경되어 주문취소')
                else:
                    print(t, '골드 -> 데드로 포지션 변경되어 주문취소')
                orderApi.cancel_batch_orders(t, coin, cancelOrders)


            lossCnt = tickerDict[t]['lossCnt']
            size = getSize(t) * lossCnt
            if cross == 'gold':
                # buyResult = orderApi.place_order(t, coin, size=size, side='open_long', orderType='limit', price=round(close-(close*0.001), digits), timeInForceValue='normal')
                buyResult = orderApi.place_order(t, coin, size=size, side='open_long', orderType='limit', price=close, timeInForceValue='normal')
                if buyResult is None:
                    print('buyResult is None', 'size : ', size, 'price : ', close)
                else:
                    tickerDict[t]['type'] = 'long'
                    print(t, 'buy long : ', buyResult)
            else:
                # buyResult = orderApi.place_order(t, coin, size=size, side='open_short', orderType='limit', price=round(close+(close*0.001), digits), timeInForceValue='normal')
                buyResult = orderApi.place_order(t, coin, size=size, side='open_short', orderType='limit', price=close, timeInForceValue='normal')
                if buyResult is None:
                    print('buyResult is None', 'size : ', size, 'price : ', close)
                else:
                    tickerDict[t]['type'] = 'short'
                    print(t, 'buy short : ', buyResult)

            if buyResult is None:
                print('buyResult is None')
            else:
                tickerDict[t]['orderId'] = buyResult['data']['orderId']
                tickerDict[t]['size'] = size

        #구매한 경우
        else:
            if buyPrice > 0:
                targetPer = tickerDict[t]['targetPer']
                if tickerDict[t]['type'] == 'long':
                    if close > round(buyPrice + (buyPrice * targetPer), digits):   #1% 먹었을때 매도
                        sellResult = orderApi.place_order(t, coin, size=tickerDict[t]['size'], side='close_long', orderType='limit', price=round(close+(close*0.001), digits), timeInForceValue='normal')
                        if sellResult is None:
                            print('sellResult is None')
                        else:
                            del tickerDict[t]['orderId']
                            tickerDict[t]['sellOrderId'] = sellResult['data']['orderId']
                            tickerDict[t]['lossCnt'] = 1
                            print('win', t)
                    elif close < round(buyPrice - (buyPrice * targetPer), digits): #1% 읽었을때 매도
                        sellResult = orderApi.place_order(t, coin, size=tickerDict[t]['size'], side='close_long', orderType='limit', price=round(close+(close*0.001), digits), timeInForceValue='normal')
                        if sellResult is None:
                            print('sellResult is None')
                        else:
                            del tickerDict[t]['orderId']
                            tickerDict[t]['sellOrderId'] = sellResult['data']['orderId']
                            lossCnt = tickerDict[t]['lossCnt']
                            tickerDict[t]['lossCnt'] = lossCnt * 2
                            print('loss', t, 'lossCnt = ', tickerDict[t]['lossCnt'])
                elif tickerDict[t]['type'] == 'short':
                    if close < round(buyPrice - (buyPrice * targetPer), digits):   #1% 먹었을때 매도
                        sellResult = orderApi.place_order(t, coin, size=tickerDict[t]['size'], side='close_short', orderType='limit', price=round(close-(close*0.001), digits), timeInForceValue='normal')
                        if sellResult is None:
                            print('sellResult is None')
                        else:
                            del tickerDict[t]['orderId']
                            tickerDict[t]['sellOrderId'] = sellResult['data']['orderId']
                            tickerDict[t]['lossCnt'] = 1
                            print('win', t)
                    elif close > round(buyPrice + (buyPrice * targetPer), digits): #1% 읽었을때 매도
                        sellResult = orderApi.place_order(t, coin, size=tickerDict[t]['size'], side='close_short', orderType='limit', price=round(close-(close*0.001), digits), timeInForceValue='normal')
                        if sellResult is None:
                            print('sellResult is None')
                        else:
                            del tickerDict[t]['orderId']
                            tickerDict[t]['sellOrderId'] = sellResult['data']['orderId']
                            lossCnt = tickerDict[t]['lossCnt']
                            tickerDict[t]['lossCnt'] = lossCnt * 2
                            print('loss', t, 'lossCnt = ', tickerDict[t]['lossCnt'])
    
    time.sleep(0.01)  




def updateCross(t):
    candle_data = get_candle(t, 60, 100)

    for i in range(0, len(candle_data)):
        candle_data[i][0] = float(candle_data[i][0])
        candle_data[i][1] = float(candle_data[i][1])
        candle_data[i][2] = float(candle_data[i][2])
        candle_data[i][3] = float(candle_data[i][3])
        candle_data[i][4] = float(candle_data[i][4])

    
    df = pd.DataFrame(candle_data)
    # df=df['trade_price'].iloc[::-1]
    df=df[4].iloc[::1] #4번째가 종가임

    ma10 = df.rolling(window=10).mean()
    ma30 = df.rolling(window=30).mean()

    line10=ma10.iloc[-2]-ma30.iloc[-2]
    line30=ma10.iloc[-1]-ma30.iloc[-1]
    
    dead = line10>0 and line30<0
    gold = line10<0 and line30>0

    if dead == True or gold == True:
        if dead == True:
            # print(t, '포지션 변경 데드크로스')
            tickerDict[t]['cross'] = 'dead'
        elif gold == True:
            # print(t, '포지션 변경 골든크로스')
            tickerDict[t]['cross'] = 'gold'
    else:
        tickerDict[t]['cross'] = ''

    time.sleep(0.01)


# initTickers()
# check()
# # # schedule.every().day.at("01:00:01").do(lambda: initTickers())
# # # schedule.every().day.at("01:03:00").do(lambda: check())
# checkSchedule = schedule.every(5).seconds.do(lambda: check())





initTickers()
while True:
    check()
    schedule.run_pending()
    time.sleep(1)
