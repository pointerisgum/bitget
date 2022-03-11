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

api_key = "bg_f4ae7e0a6fab17130de0641afb1cda61"
secret_key = "e9a1b99d7ef0cbe0a428afacbc0480ff73c9812e89481f0ec2199af6be9359a3"
passphrase = "bitgetcci"

BTC_Ticker = 'SBTCSUSDT_SUMCBL'
ETH_Ticker = 'ETHUSDT_UMCBL'
EOS_Ticker = 'EOSUSDT_UMCBL'

ticker = BTC_Ticker
coin = 'SUSDT'
leverage = 10
check_cci = 95
excuteMargin = 0.004
buyMargin = 0.0004
tkMargin = 0.008
lossMargin = 0.012

# symbol = BTC_Ticker

access = "xwdEMciw0PeGRfpA8xMaVtnVGmFPFxTR6dkKCnUQ"
secret = "UOxwdGYVZflyTCbMwrlrzB0Ey44GGxSLl70xp8A4"
slackToken = "xoxb-2958422443234-2961015128436-OlEZV7qGyaamz31X3slydehR"
# teleToken = "5225100528:AAGL0OC4m40gsMkB9haFGm0weJMUSKGqY2U"
teleToken = "5203561877:AAHqAT79z2gSQj3--E0CkaHUyOVuZ8DPmxA"
chatId = "5046654369"

# chat = telegram.Bot(token = teleToken)
# updates = chat.getUpdates()
# for u in updates:
#     print(updates[7].message['chat']['id'])

# bot = telegram.Bot(token = teleToken)
# text = '안녕하세요'
# bot.sendMessage(chat_id = "5046654369", text=text)


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
accountApi.margin_mode(ticker, marginCoin=coin, marginMode='fixed')
accountApi.leverage(ticker, marginCoin=coin, leverage=leverage, holdSide='long')
accountApi.leverage(ticker, marginCoin=coin, leverage=leverage, holdSide='short')

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
# tickers = [BTC_Ticker, ETH_Ticker, 'XRPUSDT_UMCBL', 'LUNAUSDT_UMCBL', 'EOUSDT_UMCBL', 'BCHUSDT_UMCBL', 'LTCUSDT_UMCBL',
#            'ADAUSDT_UMCBL', 'ETCUSDT_UMCBL', 'LINKUSDT_UMCBL', 'TRXUSDT_UMCBL', 'DOTUSDT_UMCBL', 'DOGEUSDT_UMCBL', 'SOLUSDT_UMCBL']
# tickers = ["BTCUSDT_UMCBL"]

# tickers = [BTC_Ticker, ETH_Ticker, 'EOUSDT_UMCBL']

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

# def isGoldCheck(candle_data):
#     df = pd.DataFrame(candle_data)
#     df=df['trade_price'].iloc[::-1]
    
#     ma10 = df.rolling(window=10).mean()
#     ma30 = df.rolling(window=30).mean()

#     line10=ma10.iloc[-2]-ma30.iloc[-2]
#     line30=ma10.iloc[-1]-ma30.iloc[-1]
    
#     gold = line10<0 and line30>0
#     return gold

# def isDeadCheck(candle_data):
#     df = pd.DataFrame(candle_data)
#     df=df['trade_price'].iloc[::-1]
    
#     ma10 = df.rolling(window=10).mean()
#     ma30 = df.rolling(window=30).mean()

#     line10=ma10.iloc[-2]-ma30.iloc[-2]
#     line30=ma10.iloc[-1]-ma30.iloc[-1]
    
#     dead = line10>0 and line30<0
#     return dead

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
    # print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), '15min candles call')
    
    candle_data = get_candle(ticker, 900, 100)
    if candle_data == None:
        return
    
    for i in range(0, len(candle_data)):
        candle_data[i][0] = float(candle_data[i][0])
        candle_data[i][1] = float(candle_data[i][1])
        candle_data[i][2] = float(candle_data[i][2])
        candle_data[i][3] = float(candle_data[i][3])
        candle_data[i][4] = float(candle_data[i][4])

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
   
def startAuto(ticker):
    isGoldenCross = False
    isDeadCross = False
    isBuy = False
    upLinePrice = 0.0     #익절 라인 + 0.5%
    downLinePrice = 0.0   #손절 라인 -0.5%
    maxPrice = 0.0        #고가
    buyPrice = 0.0        #매수 가격
    check1 = False
    check2 = False
    check3 = False
    cciCheckCnt = 0
    orderId = 0
    triggerOrderId = 0
    
    while True:
        schedule.run_pending()
        
        cci_candle_data = get_candle(ticker, 300, 100)
        if cci_candle_data == None:
            continue

        for i in range(0, len(cci_candle_data)):
            cci_candle_data[i][0] = float(cci_candle_data[i][0])
            cci_candle_data[i][1] = float(cci_candle_data[i][1])
            cci_candle_data[i][2] = float(cci_candle_data[i][2])
            cci_candle_data[i][3] = float(cci_candle_data[i][3])
            cci_candle_data[i][4] = float(cci_candle_data[i][4])


        cci_data = get_cci(cci_candle_data, 100)
        cci = round(float(cci_data[-1]['CCI']), 0)
        print('cci: ', cci)
        
        currentPrice = float(cci_candle_data[-1][4])
        # print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, currentPrice)
               
        if isBuy == False:
            #한번이라도 골드나 데드가 났고 구매중이 아닐때 상태값이 바뀐 경우
            if isDeadCross == True:
                #데드 -> 골드로 바뀐 경우
                if gold:
                    msg = 'Status Change', 'Golden Cross'
                    bot.sendMessage(chat_id=chatId, text=msg)
                    
                    isGoldenCross = True
                    isDeadCross = False
                    isBuy = False
                    upLinePrice = 0.0     #익절 라인 + 0.5%
                    downLinePrice = 0.0   #손절 라인 -0.5%
                    maxPrice = 0.0        #고가
                    buyPrice = 0.0        #매수 가격
                    check1 = False
                    check2 = False
                    check3 = False
                    cciCheckCnt = 0
                    orderId = 0
                    triggerOrderId = 0
                    
            elif isGoldenCross == True:
                #골드 -> 데드로 바뀐 경우
                if dead:
                    msg = 'Status Change', 'Dead Cross'
                    bot.sendMessage(chat_id=chatId, text=msg)      
                    
                    isGoldenCross = False
                    isDeadCross = True
                    isBuy = False
                    upLinePrice = 0.0     #익절 라인 + 0.5%
                    downLinePrice = 0.0   #손절 라인 -0.5%
                    maxPrice = 0.0        #고가
                    buyPrice = 0.0        #매수 가격
                    check1 = False
                    check2 = False
                    check3 = False
                    cciCheckCnt = 0
                    orderId = 0
                    triggerOrderId = 0

            #한번도 골드나 데드가 안난 경우
            if isGoldenCross == False and isDeadCross == False:                
                # cci_data = get_cci(candle_data, 100)
                # cci = cci_data[-1]['CCI']

                if dead:
                    call='dead cross'
                    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, call)
                    isDeadCross = True
                    # current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                    msg = 'Dead Cross'
                    bot.sendMessage(chat_id=chatId, text=msg)      
                    
                if gold:
                    call='golden cross'
                    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, call)
                    isGoldenCross = True
                    # current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                    msg = 'Golden Cross'
                    bot.sendMessage(chat_id=chatId, text=msg)
            else:
                # cci_data = get_cci(candle_data, 100)
                # cci = cci_data[-2]['CCI']
                
                if isGoldenCross == True:
                    if check1 == False:
                        if cci >= 110:
                            check1 = True
                            msg = 'check1 success', 'CCI:', cci
                            bot.sendMessage(chat_id=chatId, text=msg)
                    elif check2 == False:
                        if cci <= -110:
                            check2 = True
                            msg = 'check2 success', 'CCI:', cci
                            bot.sendMessage(chat_id=chatId, text=msg)
                    elif check3 == False:
                        if cci >= -95:
                            cciCheckCnt += 1
                            if cciCheckCnt >= 30:
                                check3 = True
                                
                                #매수
                                marketPrice = marketApi.market_price(ticker)
                                currentPrice = float(marketPrice['data']['markPrice'])
                                print(currentPrice)
                                currentPrice = getCurrentPrice(currentPrice)

                                maxPrice = currentPrice
                                upLinePrice = math.ceil(getUpline(ticker, currentPrice, tkMargin))
                                downLinePrice = math.ceil(getDownline(ticker, currentPrice, lossMargin))
                                
                                account = accountApi.accounts('sumcbl')
                                myAvailable = float(account['data'][0]['available'])
                                size = getSize(ticker, myAvailable, currentPrice) # round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
                                
                                marketResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_long', orderType='limit',
                                                                    price=math.floor(currentPrice - (currentPrice*buyMargin)), timeInForceValue='normal',
                                                                    presetStopLossPrice=downLinePrice)                                                                
                                orderId = int(getOrderId(marketResult))
                                
                                msg = 'check3 success', 'CCI:', cci, 'CurrentPrice:', currentPrice
                                bot.sendMessage(chat_id=chatId, text=msg)

                                waitCnt = 600 #10분동안 안사지면 주문 취소 후 다시 시작
                                while orderId > 0 and waitCnt >= 0:
                                    detail = orderApi.detail(ticker, orderId)
                                    state = detail['data']['state']
                                    if state == 'filled':
                                        buyPrice = getDealPrice(ticker, orderId)    
                                        msg = 'Buy Long', 'CCI:', cci, 'Price:', buyPrice
                                        bot.sendMessage(chat_id=chatId, text=msg)                            
                                        isBuy = True
                                        trigger = planApi.place_plan(ticker, marginCoin=coin, size=size, side='close_long', orderType='limit',
                                                                     triggerPrice=upLinePrice,
                                                                     executePrice=math.ceil(upLinePrice-(upLinePrice*excuteMargin)),
                                                                     triggerType='fill_price')
                                        triggerOrderId = int(trigger['data']['orderId'])
                                        orderId = 0
                                        break
                                    time.sleep(1)
                                    waitCnt -= 1
                                    
                                #안사진 경우 초기화
                                if waitCnt <= 0:
                                    msg = '지정가를 도달하지 못해 구매하지 못함'
                                    bot.sendMessage(chat_id=chatId, text=msg)

                                    #주문 취소하기
                                    orderApi.cancel_orders(ticker, coin, orderId)
                                    
                                    isGoldenCross = False
                                    isDeadCross = False
                                    isBuy = False
                                    upLinePrice = 0.0     #익절 라인 + 0.5%
                                    downLinePrice = 0.0   #손절 라인 -0.5%
                                    maxPrice = 0.0        #고가
                                    buyPrice = 0.0        #매수 가격
                                    check1 = False
                                    check2 = False
                                    check3 = False
                                    cciCheckCnt = 0
                                    orderId = 0
                                    triggerOrderId = 0
                        else:
                            cciCheckCnt = 0
                        

                        
                    # #매수 타이밍 잡기 (cci:-100 이하로 떨어지고 다시 -100을 뚫었을때)
                    # if cciLow == False:
                    #     if cci <= check_cci*-1:
                    #         cciLow = True
                    #         # msg = 'ver2', ticker, 'Buy Long CCI Check1 Success ', 'CCI:', cci, 'Price:', currentPrice
                    #         # bot.sendMessage(chat_id=chatId, text=msg)
                    # else:
                    #     if cci >= check_cci*-1:
                    #         # 매수 시점
                    #         # 여긴 updateCCI 함수의 sleep으로 인해 값을 갱신해 줘야 함
                    #         # currentPrice = candle_data[0]['trade_price']
                    #         marketPrice = marketApi.market_price(ticker)
                    #         currentPrice = float(marketPrice['data']['markPrice'])
                    #         print(currentPrice)

                    #         maxPrice = currentPrice
                    #         upLinePrice = getUpline(ticker, currentPrice, 0.005)
                    #         downLinePrice = getDownline(ticker, currentPrice, 0.007)
                            
                    #         account = accountApi.accounts('sumcbl')
                    #         myAvailable = float(account['data'][0]['available'])
                    #         size = getSize(ticker, myAvailable, currentPrice) # round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
                    #         buyResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_long', orderType='market', timeInForceValue='normal', presetStopLossPrice=downLinePrice)
                    #         buyOrderId = buyResult['data']['orderId']

                    #         # buyDetail = orderApi.detail(ticker, orderId=buyOrderId)
                    #         buyPrice = getDealPrice(ticker, buyOrderId)
                            
                    #         msg = 'ver2', ticker, 'Buy Long ', 'CCI:', cci, 'Price:', buyPrice
                    #         bot.sendMessage(chat_id=chatId, text=msg)
                            
                    #         isBuy = True   
                                                                         
                if isDeadCross == True:
                    if check1 == False:
                        if cci <= -110:
                            check1 = True
                            msg = 'check1Reverse success', 'CCI:', cci
                            bot.sendMessage(chat_id=chatId, text=msg)
                    elif check2 == False:
                        if cci >= 110:
                            check2 = True
                            msg = 'check2Reverse success', 'CCI:', cci
                            bot.sendMessage(chat_id=chatId, text=msg)
                    elif check3 == False:
                        if cci <= 95:
                            cciCheckCnt += 1
                            if cciCheckCnt >= 30:
                                check3 = True
                                msg = 'check3Reverse success', 'CCI:', cci
                                bot.sendMessage(chat_id=chatId, text=msg)
                                
                                #매수
                                marketPrice = marketApi.market_price(ticker)
                                currentPrice = float(marketPrice['data']['markPrice'])
                                print(currentPrice)
                                currentPrice = getCurrentPrice(currentPrice)

                                maxPrice = currentPrice
                                upLinePrice = math.floor(getUpline(ticker, currentPrice, lossMargin))
                                downLinePrice = math.floor(getDownline(ticker, currentPrice, tkMargin))
                                
                                account = accountApi.accounts('sumcbl')
                                myAvailable = float(account['data'][0]['available'])
                                size = getSize(ticker, myAvailable, currentPrice) # round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
                                
                                #비트코인전용임
                                marketResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_short', orderType='limit',
                                                                    price=math.ceil(currentPrice + (currentPrice*buyMargin)), timeInForceValue='normal',
                                                                    presetStopLossPrice=upLinePrice)
                                orderId = int(getOrderId(marketResult))
                                

                                waitCnt = 600 #10분동안 안사지면 주문 취소 후 다시 시작
                                while orderId > 0 and waitCnt >= 0:
                                    detail = orderApi.detail(ticker, orderId)
                                    state = detail['data']['state']
                                    if state == 'filled':
                                        buyPrice = getDealPrice(ticker, orderId)    
                                        msg = 'Buy Short', 'CCI:', cci, 'Price:', buyPrice
                                        bot.sendMessage(chat_id=chatId, text=msg)                            
                                        isBuy = True
                                        trigger = planApi.place_plan(ticker, marginCoin=coin, size=size, side='close_short', orderType='limit',
                                                                     triggerPrice=downLinePrice,
                                                                     executePrice=math.floor(downLinePrice+(downLinePrice*excuteMargin)),
                                                                     triggerType='fill_price')
                                        triggerOrderId = int(trigger['data']['orderId'])
                                        orderId = 0
                                        break
                                    time.sleep(1)
                                    waitCnt -= 1
                                    
                                #안사진 경우 초기화
                                if waitCnt <= 0:
                                    msg = '지정가를 도달하지 못해 구매하지 못함'
                                    bot.sendMessage(chat_id=chatId, text=msg)

                                    #주문 취소하기
                                    orderApi.cancel_orders(ticker, coin, orderId)

                                    isGoldenCross = False
                                    isDeadCross = False
                                    isBuy = False
                                    upLinePrice = 0.0     #익절 라인 + 0.5%
                                    downLinePrice = 0.0   #손절 라인 -0.5%
                                    maxPrice = 0.0        #고가
                                    buyPrice = 0.0        #매수 가격
                                    check1 = False
                                    check2 = False
                                    check3 = False
                                    cciCheckCnt = 0
                                    orderId = 0
                                    triggerOrderId = 0

                        else:
                            cciCheckCnt = 0

                    
                    # #매수 타이밍 잡기 (cci:+100 이상으로 올라가고 다시 +100으로 내려 갔을때)
                    # if cciHight == False:
                    #     if cci >= check_cci:
                    #         cciHight = True
                    #         # msg = 'ver2', ticker, 'Buy Short CCI Check1 Success ', 'CCI:', cci, 'Price:', currentPrice
                    #         # bot.sendMessage(chat_id=chatId, text=msg)
                    # else:
                    #     if cci <= check_cci:
                    #         #매수 시점
                    #         # #여긴 updateCCI 함수의 sleep으로 인해 값을 갱신해 줘야 함
                    #         # currentPrice = candle_data[0]['trade_price']
                    #         marketPrice = marketApi.market_price(ticker)
                    #         currentPrice = float(marketPrice['data']['markPrice'])
                    #         print(currentPrice)

                    #         maxPrice = currentPrice
                    #         upLinePrice = getUpline(ticker, currentPrice, 0.007)
                    #         downLinePrice = getDownline(ticker, currentPrice, 0.005)
                            
                    #         account = accountApi.accounts('sumcbl')
                    #         myAvailable = float(account['data'][0]['available'])
                    #         size = getSize(ticker, myAvailable, currentPrice) #round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
                    #         buyResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_short', orderType='market', timeInForceValue='normal', presetStopLossPrice=upLinePrice)
                    #         buyOrderId = buyResult['data']['orderId']

                    #         # buyDetail = orderApi.detail(ticker, orderId=buyOrderId)
                    #         buyPrice = getDealPrice(ticker, buyOrderId)

                    #         msg = 'ver2', ticker, 'Buy Short ', 'CCI:', cci, 'Price:', buyPrice
                    #         bot.sendMessage(chat_id=chatId, text=msg)
                            
                    #         isBuy = True
                            
        else:
            #구매중인 경우 판매시점 잡기
            if isGoldenCross == True:                
                #제일 먼저 팔렸는지 체크해서 팔렸으면 초기화
                #손절이던지 익절이던지 어떻게 팔리든 내가 산게 팔린지 체크해야 함
                startTime = (int(pydatetime.datetime.now().timestamp()) - 600) * 1000 #10분전
                endTime = int(pydatetime.datetime.now().timestamp()) * 1000           #현재
                historyResult = orderApi.history(ticker, startTime, endTime, 1)
                historyList = historyResult['data']['orderList']
                if historyList is not None:
                    history = historyList[0]
                    side = history['side']
                    if side == 'close_long':
                        #판매완료 된 경우
                        priceAvg = float(history['priceAvg'])
                        if priceAvg > 0:
                            rate = getPer(priceAvg, buyPrice)
                            msg = 'Sell Long', 'Rate: ', rate
                            bot.sendMessage(chat_id=chatId, text=msg)

                            #트리거 취소하기
                            planApi.cancel_plan(ticker, marginCoin=coin, orderId=triggerOrderId, planType='normal_plan')
                            
                            
                            isGoldenCross = False
                            isDeadCross = False
                            isBuy = False
                            upLinePrice = 0.0     #익절 라인 + 0.5%
                            downLinePrice = 0.0   #손절 라인 -0.5%
                            maxPrice = 0.0        #고가
                            buyPrice = 0.0        #매수 가격
                            check1 = False
                            check2 = False
                            check3 = False
                            cciCheckCnt = 0
                            orderId = 0
                            triggerOrderId = 0

                            #15분봉 업데이트
                            candles15()

                            if ma10.iloc[-1] > ma30.iloc[-1]:
                                isGoldenCross = True
                                isDeadCross = False
                            elif ma10.iloc[-1] < ma30.iloc[-1]:
                                isGoldenCross = False
                                isDeadCross = True
                            else:
                                isGoldenCross = False
                                isDeadCross = False
    
                if currentPrice > maxPrice:
                    #고점 갱신
                    if triggerOrderId > 0:
                        maxPrice = currentPrice
                        if maxPrice > upLinePrice:
                            print('고점 갱신')
                            planApi.modify_plan(ticker, marginCoin=coin, orderId=triggerOrderId, orderType='limit', 
                                                triggerPrice=math.ceil(maxPrice), executePrice=math.ceil(maxPrice-(maxPrice*excuteMargin)),
                                                triggerType='fill_price')
        
                # if currentPrice <= downLinePrice:
                #     #손절
                #     #10배수 썼을 경우 수익률
                #     # marketPrice = marketApi.market_price(ticker)
                #     # price = float(marketPrice['data']['markPrice'])
                #     # # sellResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='close_long', orderType='limit', price=price, timeInForceValue='normal')
                #     # closeResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='close_long', orderType='market', timeInForceValue='normal')
                #     # sellOrderId = closeResult['data']['orderId']

                #     # sellDetail = orderApi.detail(ticker, orderId=sellOrderId)
                #     # sellPrice = getDealPrice(ticker, buyOrderId)

                #     #이거 손절 치기
                #     #limitOrderId
                    
                #     rate = getPer(downLinePrice, buyPrice)
                #     totalRate += rate
                #     msg = 'ver2', ticker, 'Sell Long Stop Loss', 'CCI:', cci, 'Price:', downLinePrice, 'sum:', round(downLinePrice-buyPrice, 1), 'Rate: ', rate
                #     bot.sendMessage(chat_id=chatId, text=msg)

                #     # saveExcel(ticker, currentPrice, buyPrice)
                    
                #     cciLow = False
                #     cciHight = False
                #     isBuy = False
                #     upLinePrice = 0.0     #익절 라인 + 0.5%
                #     downLinePrice = 0.0   #손절 라인 -0.5%
                #     maxPrice = 0.0        #고가
                #     buyPrice = 0.0        #매수 가격
                #     check1 = False
                #     check2 = False
                #     check3 = False
                #     cciCheckCnt = 0
                #     limitOrderId = 0
                #     check1Reverse = False
                #     check2Reverse = False
                #     check3Reverse = False
                #     cciCheckCntReverse = 0
                #     buySize = 0
                #     orderId = 0
                    
                #     if ma10.iloc[-1] > ma30.iloc[-1]:
                #         isGoldenCross = True
                #         isDeadCross = False
                #     elif ma10.iloc[-1] < ma30.iloc[-1]:
                #         isGoldenCross = False
                #         isDeadCross = True
                #     else:
                #         isGoldenCross = False
                #         isDeadCross = False
                #     continue

                # #익절 분기점(+5%)을 뚫었을 경우 고점 대비 -20% 내려오면 익절
                # if maxPrice > upLinePrice:
                #     if currentPrice < maxPrice - (maxPrice * 0.002):
                #         print('currentPrice: ', currentPrice, 'maxPrice: ', maxPrice, 'type: ', type(maxPrice), 'max0.2: ', maxPrice + (maxPrice * 0.002))

                #         #익절
                #         closeResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='close_long', orderType='market', timeInForceValue='normal')
                #         sellOrderId = closeResult['data']['orderId']

                #         sellPrice = getDealPrice(ticker, sellOrderId)

                #         rate = getPer(sellPrice, buyPrice)
                #         totalRate += rate
                #         msg = 'ver2', ticker, 'Sell Long Take Profit', 'CCI:', cci, 'Price:', sellPrice, 'sum:', round(sellPrice-buyPrice, 1), 'Rate: ', rate
                #         bot.sendMessage(chat_id=chatId, text=msg)
                #         # saveExcel(ticker, currentPrice, buyPrice)
                        
                #         cciLow = False
                #         cciHight = False
                #         isBuy = False
                #         upLinePrice = 0.0     #익절 라인 + 0.5%
                #         downLinePrice = 0.0   #손절 라인 -0.5%
                #         maxPrice = 0.0        #고가
                #         buyPrice = 0.0        #매수 가격
                #         check1 = False
                #         check2 = False
                #         check3 = False
                #         cciCheckCnt = 0
                #         limitOrderId = 0
                #         check1Reverse = False
                #         check2Reverse = False
                #         check3Reverse = False
                #         cciCheckCntReverse = 0
                #         buySize = 0
                        
                #         if ma10.iloc[-1] > ma30.iloc[-1]:
                #             isGoldenCross = True
                #             isDeadCross = False
                #         elif ma10.iloc[-1] < ma30.iloc[-1]:
                #             isGoldenCross = False
                #             isDeadCross = True
                #         else:
                #             isGoldenCross = False
                #             isDeadCross = False
                #         continue
                        
            if isDeadCross == True:
                #제일 먼저 팔렸는지 체크해서 팔렸으면 초기화
                #손절이던지 익절이던지 어떻게 팔리든 내가 산게 팔린지 체크해야 함
                startTime = (int(pydatetime.datetime.now().timestamp()) - 6000) * 1000 #100분전
                endTime = int(pydatetime.datetime.now().timestamp()) * 1000           #현재
                historyResult = orderApi.history(ticker, startTime, endTime, 1)
                if historyResult is not None:
                    historyList = historyResult['data']['orderList']
                    if historyList is not None:
                        history = historyList[0]
                        side = history['side']
                        if side == 'close_short':
                            #판매완료 된 경우
                            priceAvg = float(history['priceAvg'])
                            if priceAvg > 0:
                                rate = getPer(priceAvg, buyPrice) * -1
                                msg = 'Sell Short', 'Rate: ', rate
                                bot.sendMessage(chat_id=chatId, text=msg)

                                #트리거 취소하기
                                planApi.cancel_plan(ticker, marginCoin=coin, orderId=triggerOrderId, planType='normal_plan')

                                isGoldenCross = False
                                isDeadCross = False
                                isBuy = False
                                upLinePrice = 0.0     #익절 라인 + 0.5%
                                downLinePrice = 0.0   #손절 라인 -0.5%
                                maxPrice = 0.0        #고가
                                buyPrice = 0.0        #매수 가격
                                check1 = False
                                check2 = False
                                check3 = False
                                cciCheckCnt = 0
                                orderId = 0
                                triggerOrderId = 0

                                #15분봉 업데이트
                                candles15()
                                
                                if ma10.iloc[-1] > ma30.iloc[-1]:
                                    isGoldenCross = True
                                    isDeadCross = False
                                elif ma10.iloc[-1] < ma30.iloc[-1]:
                                    isGoldenCross = False
                                    isDeadCross = True
                                else:
                                    isGoldenCross = False
                                    isDeadCross = False
    
                if currentPrice < maxPrice:
                    #고점 갱신
                    if triggerOrderId > 0:
                        maxPrice = currentPrice
                        if maxPrice > upLinePrice:
                            print('고점 갱신')
                            planApi.modify_plan(ticker, marginCoin=coin, orderId=triggerOrderId, orderType='limit', 
                                                triggerPrice=math.floor(maxPrice), executePrice=math.floor(maxPrice+(maxPrice*excuteMargin)), triggerType='fill_price')
                    
        time.sleep(2)                            
        # time.sleep(len(tickers) * 4)

import logging
import threading
import time

msg = 'start: ', ticker
bot.sendMessage(chat_id=chatId, text=msg)

isGoldCross = False
isDeadCross = False
candleTime = 300
tkLine = 0.012
lsLine = 0.015
buySize = 0.0

# def updateStatus():
#     global buySize
            
#     candle_data = get_candle(ticker, candleTime, 100)
#     if candle_data == None:
#         msg = '캔들 데이터 가져오지 못함'
#         print(msg)
#         bot.sendMessage(chat_id=chatId, text=msg)
#         return
    
#     for i in range(0, len(candle_data)):
#         candle_data[i][0] = float(candle_data[i][0])
#         candle_data[i][1] = float(candle_data[i][1])
#         candle_data[i][2] = float(candle_data[i][2])
#         candle_data[i][3] = float(candle_data[i][3])
#         candle_data[i][4] = float(candle_data[i][4])
    
#     df = pd.DataFrame(candle_data)
#     # df=df['trade_price'].iloc[::-1]
#     df=df[4].iloc[::1] #4번째가 종가임

#     ma10 = df.rolling(window=10).mean()
#     ma30 = df.rolling(window=30).mean()
                                    
#     line10=ma10.iloc[-2]-ma30.iloc[-2]
#     line30=ma10.iloc[-1]-ma30.iloc[-1]
    
#     global isGoldCross
#     global isDeadCross
    
#     gold = line10<0 and line30>0
#     dead = line10>0 and line30<0

#     #상태값이 없는 경우 현재 상태를 가져온다
#     if isGoldCross == False and isDeadCross == False:
#         if ma10.iloc[-1] > ma30.iloc[-1]:
#             isGoldCross = True
#             isDeadCross = False
#         elif ma10.iloc[-1] < ma30.iloc[-1]:
#             isGoldCross = False
#             isDeadCross = True
    
#     #상태가 변경 되자마자 매수 또는 매도
#     if (isGoldCross == True and dead == True) or (isDeadCross == True and gold == True):
#         #조건 충족, 매수
#         marketPrice = marketApi.market_price(ticker)
#         currentPrice = float(marketPrice['data']['markPrice'])
#         account = accountApi.accounts('sumcbl')
#         myAvailable = float(account['data'][0]['available'])
#         size = getSize(ticker, myAvailable, currentPrice)

#         if isGoldCross == True and dead == True: 
#             bot.sendMessage(chat_id=chatId, text='상태변경 골든 -> 데드')
            
#             #들고 있던게 있으면 팔기
#             if buySize > 0.0:
#                 orderApi.place_order(ticker, marginCoin='SUSDT', size=buySize, side='close_long', orderType='market', timeInForceValue='normal')

#             #숏 매수
#             orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_short', orderType='market', timeInForceValue='normal')
#             buySize = size
#             msg = '숏 매수', currentPrice
#             bot.sendMessage(chat_id=chatId, text=msg)
            
#         elif isDeadCross == True and gold == True:
#             bot.sendMessage(chat_id=chatId, text='상태변경 데드 -> 골든')
            
#             #들고 있던게 있으면 팔기
#             if buySize > 0:
#                 orderApi.place_order(ticker, marginCoin='SUSDT', size=buySize, side='close_short', orderType='market', timeInForceValue='normal')

#             #롱 매수
#             orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_long', orderType='market', timeInForceValue='normal')
#             buySize = size
#             msg = '롱 매수', currentPrice
#             bot.sendMessage(chat_id=chatId, text=msg)


            
            
            
def updateStatus():
    candle_data = get_candle(ticker, candleTime, 100)
    if candle_data == None:
        msg = '캔들 데이터 가져오지 못함'
        print(msg)
        bot.sendMessage(chat_id=chatId, text=msg)
        return
    
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
    
    global isGoldCross
    global isDeadCross
    
    gold = line10<0 and line30>0
    dead = line10>0 and line30<0

    #상태값이 없는 경우 현재 상태를 가져온다
    if isGoldCross == False and isDeadCross == False:
        if ma10.iloc[-1] > ma30.iloc[-1]:
            isGoldCross = True
            isDeadCross = False
        elif ma10.iloc[-1] < ma30.iloc[-1]:
            isGoldCross = False
            isDeadCross = True
    
    #상태가 변경 됐으면 60초동안 지속되는지 지켜본다
    if (isGoldCross == True and dead == True) or (isDeadCross == True and gold == True):
        if isGoldCross == True and dead == True: 
            isGoldCross = False
            isDeadCross = True
            msg = '상태변경 골든 -> 데드'
            print(msg)
            bot.sendMessage(chat_id=chatId, text=msg)
        if isDeadCross == True and gold == True:
            isGoldCross = True
            isDeadCross = False
            msg = '상태변경 데드 -> 골든'
            print(msg)
            bot.sendMessage(chat_id=chatId, text=msg)
            
        checkLimitTime = 300
        checkCnt = 0
        keepTime = 60
        # checkLimitTime = 60
        # checkCnt = 0
        # keepTime = 30

        while checkLimitTime > 0:
            checkLimitTime -= 1
            
            tmp_candle_data = get_candle(ticker, candleTime, 100)
            if tmp_candle_data == None:
                msg = '캔들 데이터 가져오지 못함'
                print(msg)
                bot.sendMessage(chat_id=chatId, text=msg)
                continue
            
            for i in range(0, len(tmp_candle_data)):
                tmp_candle_data[i][0] = float(tmp_candle_data[i][0])
                tmp_candle_data[i][1] = float(tmp_candle_data[i][1])
                tmp_candle_data[i][2] = float(tmp_candle_data[i][2])
                tmp_candle_data[i][3] = float(tmp_candle_data[i][3])
                tmp_candle_data[i][4] = float(tmp_candle_data[i][4])
    
            tmp_df = pd.DataFrame(tmp_candle_data)
            tmp_df=tmp_df[4].iloc[::1] #4번째가 종가임

            tmp_ma10 = tmp_df.rolling(window=10).mean()
            tmp_ma30 = tmp_df.rolling(window=30).mean()

            if isGoldCross:
                if tmp_ma10.iloc[-1] > tmp_ma30.iloc[-1]:
                    checkCnt += 1
                else:
                    checkCnt = 0
            elif isDeadCross:
                if tmp_ma10.iloc[-1] < tmp_ma30.iloc[-1]:
                    checkCnt += 1
                else:
                    checkCnt = 0

            if checkCnt >= keepTime:
                #매수 전 5분봉도 일치하는지 확인
                tmp_candle_data = get_candle(ticker, 300, 100)
                if tmp_candle_data == None:
                    msg = '캔들 데이터 가져오지 못함'
                    print(msg)
                    bot.sendMessage(chat_id=chatId, text=msg)
                    continue
                
                for i in range(0, len(tmp_candle_data)):
                    tmp_candle_data[i][0] = float(tmp_candle_data[i][0])
                    tmp_candle_data[i][1] = float(tmp_candle_data[i][1])
                    tmp_candle_data[i][2] = float(tmp_candle_data[i][2])
                    tmp_candle_data[i][3] = float(tmp_candle_data[i][3])
                    tmp_candle_data[i][4] = float(tmp_candle_data[i][4])
        
                tmp_df = pd.DataFrame(tmp_candle_data)
                tmp_df=tmp_df[4].iloc[::1] #4번째가 종가임

                tmp_ma10 = tmp_df.rolling(window=10).mean()
                tmp_ma30 = tmp_df.rolling(window=30).mean()

                is5MinCheck = True
                if isGoldCross:
                    if ma10.iloc[-1] < ma30.iloc[-1]:
                        is5MinCheck = False
                elif isDeadCross:
                    if ma10.iloc[-1] > ma30.iloc[-1]:
                        is5MinCheck = False

                if is5MinCheck == False:
                    msg = '5분봉 불일치'
                    print(msg)
                    bot.sendMessage(chat_id=chatId, text=msg)
                    isGoldCross = False
                    isDeadCross = False
                    break


                #조건 충족, 매수
                marketPrice = marketApi.market_price(ticker)
                currentPrice = float(marketPrice['data']['markPrice'])

                account = accountApi.accounts('sumcbl')
                myAvailable = float(account['data'][0]['available'])
                size = getSize(ticker, myAvailable, currentPrice) # round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
                
                if isGoldCross:
                    print('buy long')
                    upLinePrice = getUpline(ticker, currentPrice, tkLine)
                    downLinePrice = getDownline(ticker, currentPrice, lsLine)
                    maxPrice = upLinePrice
                    
                    orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_long',
                                         orderType='market', timeInForceValue='normal', presetStopLossPrice=downLinePrice)
                    
                    msg = '롱 매수'
                    print(msg)
                    bot.sendMessage(chat_id=chatId, text=msg)

                    #매수 후 판매시점 잡기
                    while True:
                        #매수 중 상태값이 바뀐 경우 바로 매도처리
                        tmp_candle_data = get_candle(ticker, candleTime, 100)
                        if tmp_candle_data == None:
                            msg = '캔들 데이터 가져오지 못함'
                            print(msg)
                            bot.sendMessage(chat_id=chatId, text=msg)
                            continue
            
                        for i in range(0, len(tmp_candle_data)):
                            tmp_candle_data[i][0] = float(tmp_candle_data[i][0])
                            tmp_candle_data[i][1] = float(tmp_candle_data[i][1])
                            tmp_candle_data[i][2] = float(tmp_candle_data[i][2])
                            tmp_candle_data[i][3] = float(tmp_candle_data[i][3])
                            tmp_candle_data[i][4] = float(tmp_candle_data[i][4])
                
                        tmp_df = pd.DataFrame(tmp_candle_data)
                        tmp_df=tmp_df[4].iloc[::1] #4번째가 종가임

                        tmp_ma10 = tmp_df.rolling(window=10).mean()
                        tmp_ma30 = tmp_df.rolling(window=30).mean()

                        tmp_line10=tmp_ma10.iloc[-3]-tmp_ma30.iloc[-3]
                        tmp_line30=tmp_ma10.iloc[-2]-tmp_ma30.iloc[-2]
                        
                        # tmp_gold = tmp_line10<0 and tmp_line30>0
                        tmp_dead = tmp_line10>0 and tmp_line30<0

                        if tmp_dead:
                            orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_long',
                                                    orderType='market', timeInForceValue='normal')
                            msg = '상태값 변경으로 롱 종료'
                            print(msg)
                            bot.sendMessage(chat_id=chatId, text=msg)
                            break


                        #매수 중 상태값이 바뀌지 않은 경우
                        marketPrice = marketApi.market_price(ticker)
                        currentPrice = float(marketPrice['data']['markPrice'])

                        if currentPrice > maxPrice:
                            #고점 갱신
                            msg = '롱 고점 갱신', '현재가', currentPrice, '맥스가', maxPrice
                            print(msg)
                            bot.sendMessage(chat_id=chatId, text=msg)
                            maxPrice = currentPrice
                        
                        if maxPrice > upLinePrice:
                            if currentPrice < maxPrice - (maxPrice * 0.005):
                                msg = '롱 익절', '현재가', currentPrice, '맥스가', maxPrice
                                print(msg)
                                bot.sendMessage(chat_id=chatId, text=msg)
                                orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_long',
                                                     orderType='market', timeInForceValue='normal')
                                break
                        time.sleep(1)
                    
                elif isDeadCross:
                    print('buy short')
                    upLinePrice = getUpline(ticker, currentPrice, lsLine)
                    downLinePrice = getDownline(ticker, currentPrice, tkLine)
                    maxPrice = downLinePrice

                    orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_short',
                                         orderType='market', timeInForceValue='normal', presetStopLossPrice=upLinePrice)
                    
                    msg = '숏 매수'
                    print(msg)
                    bot.sendMessage(chat_id=chatId, text=msg)

                    #매수 후 판매시점 잡기
                    while True:
                        #매수 중 상태값이 바뀐 경우 바로 매도처리
                        tmp_candle_data = get_candle(ticker, candleTime, 100)
                        if tmp_candle_data == None:
                            msg = '캔들 데이터 가져오지 못함'
                            print(msg)
                            bot.sendMessage(chat_id=chatId, text=msg)
                            continue
            
                        for i in range(0, len(tmp_candle_data)):
                            tmp_candle_data[i][0] = float(tmp_candle_data[i][0])
                            tmp_candle_data[i][1] = float(tmp_candle_data[i][1])
                            tmp_candle_data[i][2] = float(tmp_candle_data[i][2])
                            tmp_candle_data[i][3] = float(tmp_candle_data[i][3])
                            tmp_candle_data[i][4] = float(tmp_candle_data[i][4])
                
                        tmp_df = pd.DataFrame(tmp_candle_data)
                        tmp_df=tmp_df[4].iloc[::1] #4번째가 종가임

                        tmp_ma10 = tmp_df.rolling(window=10).mean()
                        tmp_ma30 = tmp_df.rolling(window=30).mean()

                        tmp_line10=tmp_ma10.iloc[-3]-tmp_ma30.iloc[-3]
                        tmp_line30=tmp_ma10.iloc[-2]-tmp_ma30.iloc[-2]
                        
                        tmp_gold = tmp_line10<0 and tmp_line30>0
                        # tmp_dead = tmp_line10>0 and tmp_line30<0

                        if tmp_gold:
                            msg = '상태값 변경으로 숏 종료'
                            print(msg)
                            bot.sendMessage(chat_id=chatId, text=msg)
                            orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_short',
                                                    orderType='market', timeInForceValue='normal')
                            break


                        #매수 중 상태값이 바뀌지 않은 경우
                        marketPrice = marketApi.market_price(ticker)
                        if marketPrice is not None:
                            currentPrice = float(marketPrice['data']['markPrice'])

                            if currentPrice < maxPrice:
                                #고점 갱신
                                msg = '숏 고점 갱신', '현재가', currentPrice, '맥스가', maxPrice
                                print(msg)
                                bot.sendMessage(chat_id=chatId, text=msg)
                                maxPrice = currentPrice

                            if maxPrice < downLinePrice:
                                if currentPrice > maxPrice + (maxPrice * 0.005):
                                    msg = '숏 익절', '현재가', currentPrice, '맥스가', maxPrice
                                    print(msg)
                                    bot.sendMessage(chat_id=chatId, text=msg)
                                    orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_short',
                                                        orderType='market', timeInForceValue='normal')
                                    break
                        time.sleep(1)
                        
                                                
                #한사이클 종료
                msg = '한사이클 종료'
                print(msg)
                bot.sendMessage(chat_id=chatId, text=msg)
                isGoldCross = False
                isDeadCross = False
                break
            
            
            if checkLimitTime <= 1:
                msg = '체크타임 만족 못함'
                print(msg)
                bot.sendMessage(chat_id=chatId, text=msg)

            time.sleep(1)

        


# updateStatus()
# schedule.every().hour.at(":00").do(updateStatus)
# schedule.every().hour.at(":15").do(updateStatus)
# schedule.every().hour.at(":30").do(updateStatus)
# schedule.every().hour.at(":45").do(updateStatus)

while True:
    schedule.run_pending()
    updateStatus()
    time.sleep(1)

# candles15()
# schedule.every().minute.at(":03").do(candles15) # 매분 23초에 job 실행
# schedule.every(3).seconds.do(lambda: test1()) # 3초마다 job 실행
# schedule.every().hour.at(":54").do(lambda: candles15()) # 매시간 42분에 작업 실행


# startAuto(ticker)

# for i in tickers:
#     t = threading.Thread(target=startAuto, args=(i,)) 
#     t.start()
#     time.sleep(3)




# #테스트 코드
# ticker = BTC_Ticker

# candle_data = get_candle(ticker, 9000, 200)
# for i in range(0, len(candle_data)):
#     candle_data[i][0] = float(candle_data[i][0])
#     candle_data[i][1] = float(candle_data[i][1])
#     candle_data[i][2] = float(candle_data[i][2])
#     candle_data[i][3] = float(candle_data[i][3])
#     candle_data[i][4] = float(candle_data[i][4])
# cci_data = get_cci(candle_data, 100)
# cci = cci_data[-2]['CCI']


# marketPrice = marketApi.market_price(ticker)
# currentPrice = float(marketPrice['data']['markPrice'])
# print(currentPrice)

# maxPrice = currentPrice
# buyPrice = currentPrice
# upLinePrice = round(buyPrice + (buyPrice * 0.005), 0)
# downLinePrice = round(buyPrice - (buyPrice * 0.007), 0)

# account = accountApi.accounts('sumcbl')
# myAvailable = float(account['data'][0]['available'])
# size = round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
# buyResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='open_long', orderType='market', timeInForceValue='normal', presetStopLossPrice=downLinePrice)
# buyOrderId = buyResult['data']['orderId']


# # buyDetail = orderApi.detail(ticker, orderId=buyOrderId)
# buyPrice = getDealPrice(ticker, buyOrderId)

# msg = 'ver2', 'Test Message BitGet ', ticker, 'Buy Long ', 'CCI:', cci, 'Price:', buyPrice
# bot.sendMessage(chat_id=chatId, text=msg)
# time.sleep(10)





# closeResult = orderApi.place_order(ticker, marginCoin=coin, size=size, side='close_long', orderType='market', timeInForceValue='normal')

# sellOrderId = closeResult['data']['orderId']

# # sellDetail = orderApi.detail(ticker, orderId=sellOrderId)
# sellPrice = getDealPrice(ticker, buyOrderId)

# rate = getPer(sellPrice, buyPrice) * -1
# msg = 'ver2', 'Test Message BitGet ', ticker, 'Sell Short Take Profit', 'CCI:', cci, 'Price:', sellPrice, 'Rate: ', rate
# bot.sendMessage(chat_id=chatId, text=msg)
