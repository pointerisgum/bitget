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

api_key = "bg_f4ae7e0a6fab17130de0641afb1cda61"
secret_key = "e9a1b99d7ef0cbe0a428afacbc0480ff73c9812e89481f0ec2199af6be9359a3"
passphrase = "bitgetcci"

# symbol = 'BTCUSDT_UMCBL'


access = "xwdEMciw0PeGRfpA8xMaVtnVGmFPFxTR6dkKCnUQ"
secret = "UOxwdGYVZflyTCbMwrlrzB0Ey44GGxSLl70xp8A4"
slackToken = "xoxb-2958422443234-2961015128436-OlEZV7qGyaamz31X3slydehR"
# teleToken = "5225100528:AAGL0OC4m40gsMkB9haFGm0weJMUSKGqY2U"
teleToken = "5225100528:AAGL0OC4m40gsMkB9haFGm0weJMUSKGqY2U"

rateList = []
dateList = []
tickerList = []

bot = telegram.Bot(token=teleToken)

marketApi = market.MarketApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
orderApi = order.OrderApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
accountApi = accounts.AccountApi(api_key, secret_key, passphrase, use_server_time=False, first=False)
leverage = 20

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

tickers = ['SBTCSUSDT_SUMCBL', 'SETHSUSDT_SUMCBL', 'SEOSSUSDT_SUMCBL']

def get_candle(ticker, time, count):
    endTime = int(pydatetime.datetime.now().timestamp())
    try:
        candles = marketApi.candles(ticker, granularity=900,startTime=(endTime * 1000) - ((time*1000)*count), endTime=endTime * 1000) #15분봉 200개
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
        ordered_df['SMA'] = ordered_df['TP'].rolling(window=7).mean()
        ordered_df['MAD'] = ordered_df['TP'].rolling(window=7).apply(lambda x: pd.Series(x).mad())
        ordered_df['CCI'] = (ordered_df['TP'] - ordered_df['SMA']) / (0.015 * ordered_df['MAD'])
 
        # 개수만큼 조립
        for i in range(0, loop_cnt):            
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
    return round(((((c - b) / b) * 100) - 0.08) * leverage, 2)

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
    if ticker == 'SBTCSUSDT_SUMCBL':
        size = round(((myAvailable * 0.1) * leverage) / currentPrice, 3)
        return size
    elif ticker == 'SETHSUSDT_SUMCBL':
        size = round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
        return size
    elif ticker == 'SEOSSUSDT_SUMCBL':
        size = int(round(((myAvailable * 0.1) * leverage) / currentPrice, 0))
        return size
    return 0


def startAuto(ticker):
    isGoldenCross = False
    isDeadCross = False
    cciLow = False
    cciHight = False
    isBuy = False
    upLinePrice = 0.0     #익절 라인 + 0.5%
    downLinePrice = 0.0   #손절 라인 -0.5%
    maxPrice = 0.0        #고가
    buyPrice = 0.0        #매수 가격
    totalRate = 0.0       #누적 손익
    
    while True:        
        candle_data = get_candle(ticker, 900, 100)
        
        for i in range(0, len(candle_data)):
            candle_data[i][0] = float(candle_data[i][0])
            candle_data[i][1] = float(candle_data[i][1])
            candle_data[i][2] = float(candle_data[i][2])
            candle_data[i][3] = float(candle_data[i][3])
            candle_data[i][4] = float(candle_data[i][4])

        cci_data = get_cci(candle_data, 100)
        cci = cci_data[-1]['CCI']
        
        currentPrice = candle_data[-1][4]
        print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, currentPrice)

        df = pd.DataFrame(candle_data)
        # df=df['trade_price'].iloc[::-1]
        df=df[4].iloc[::1] #4번째가 종가임

        ma10 = df.rolling(window=10).mean()
        ma30 = df.rolling(window=30).mean()

        line10=ma10.iloc[-3]-ma30.iloc[-3]
        line30=ma10.iloc[-2]-ma30.iloc[-2]
        
        dead = line10>0 and line30<0
        gold = line10<0 and line30>0
               
        if isBuy == False:
            #한번이라도 골드나 데드가 났고 구매중이 아닐때 상태값이 바뀐 경우
            if isDeadCross == True:
                #데드 -> 골드로 바뀐 경우
                if gold:
                    # msg = ticker, 'Golden Cross  ', 'CCI:', cci, 'Price:', currentPrice
                    # bot.sendMessage(chat_id="-796323955", text=msg)
                    
                    isGoldenCross = True
                    isDeadCross = False
                    cciLow = False
                    cciHight = False
                    isBuy = False
                    upLinePrice = 0.0
                    downLinePrice = 0.0
                    maxPrice = 0.0
                    buyPrice = 0.0
            elif isGoldenCross == True:
                #골드 -> 데드로 바뀐 경우
                if dead:
                    # msg = ticker, 'Dead Cross  ', 'CCI:', cci, 'Price:', currentPrice
                    # bot.sendMessage(chat_id="-796323955", text=msg)      
                    
                    isGoldenCross = False
                    isDeadCross = True
                    cciLow = False
                    cciHight = False
                    isBuy = False
                    upLinePrice = 0.0
                    downLinePrice = 0.0
                    maxPrice = 0.0
                    buyPrice = 0.0

            #한번도 골드나 데드가 안난 경우
            if isGoldenCross == False and isDeadCross == False:                
                cci_data = get_cci(candle_data, 100)
                cci = cci_data[-1]['CCI']

                if dead:
                    call='데드크로스'
                    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, call)
                    isDeadCross = True
                    # current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                    # msg = ticker, 'Dead Cross  ', 'CCI:', cci, 'Price:', currentPrice
                    # bot.sendMessage(chat_id="-796323955", text=msg)      
                    
                if gold:
                    call='골든크로스'
                    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, call)
                    isGoldenCross = True
                    # current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                    # msg = ticker, 'Golden Cross  ', 'CCI:', cci, 'Price:', currentPrice
                    # bot.sendMessage(chat_id="-796323955", text=msg)
            else:
                cci_data = get_cci(candle_data, 100)
                cci = cci_data[-2]['CCI']
                
                if isGoldenCross == True:
                    #매수 타이밍 잡기 (cci:-100 이하로 떨어지고 다시 -100을 뚫었을때)
                    if cciLow == False:
                        if cci <= -100:
                            cciLow = True
                            # msg = ticker, 'Buy Long CCI Check1 Success ', 'CCI:', cci, 'Price:', currentPrice
                            # bot.sendMessage(chat_id="-796323955", text=msg)
                    else:
                        if cci >= -100:
                            # 매수 시점
                            # 여긴 updateCCI 함수의 sleep으로 인해 값을 갱신해 줘야 함
                            # currentPrice = candle_data[0]['trade_price']
                            marketPrice = marketApi.market_price(ticker)
                            currentPrice = float(marketPrice['data']['markPrice'])
                            print(currentPrice)

                            maxPrice = currentPrice
                            buyPrice = currentPrice
                            upLinePrice = round(buyPrice + (buyPrice * 0.005), 0)
                            downLinePrice = round(buyPrice - (buyPrice * 0.007), 0)
                            
                            account = accountApi.accounts('sumcbl')
                            myAvailable = float(account['data'][0]['available'])
                            size = getSize(ticker, myAvailable, currentPrice) # round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
                            buyResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='open_long', orderType='market', timeInForceValue='normal', presetStopLossPrice=downLinePrice)
                            buyOrderId = buyResult['data']['orderId']

                            # buyDetail = orderApi.detail(ticker, orderId=buyOrderId)
                            buyPrice = getDealPrice(ticker, buyOrderId)
                            
                            msg = ticker, 'Buy Long ', 'CCI:', cci, 'Price:', buyPrice
                            bot.sendMessage(chat_id="-796323955", text=msg)
                            
                            isBuy = True   
                                                                         
                if isDeadCross == True:
                    #매수 타이밍 잡기 (cci:+100 이상으로 올라가고 다시 +100으로 내려 갔을때)
                    if cciHight == False:
                        if cci >= 100:
                            cciHight = True
                            # msg = ticker, 'Buy Short CCI Check1 Success ', 'CCI:', cci, 'Price:', currentPrice
                            # bot.sendMessage(chat_id="-796323955", text=msg)
                    else:
                        if cci <= 100:
                            #매수 시점
                            # #여긴 updateCCI 함수의 sleep으로 인해 값을 갱신해 줘야 함
                            # currentPrice = candle_data[0]['trade_price']
                            marketPrice = marketApi.market_price(ticker)
                            currentPrice = float(marketPrice['data']['markPrice'])
                            print(currentPrice)

                            maxPrice = currentPrice
                            buyPrice = currentPrice
                            upLinePrice = round(buyPrice + (buyPrice * 0.007), 0)
                            downLinePrice = round(buyPrice - (buyPrice * 0.005), 0)
                            
                            account = accountApi.accounts('sumcbl')
                            myAvailable = float(account['data'][0]['available'])
                            size = getSize(ticker, myAvailable, currentPrice) #round(((myAvailable * 0.1) * leverage) / currentPrice, 2)
                            buyResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='open_short', orderType='market', timeInForceValue='normal', presetStopLossPrice=upLinePrice)
                            buyOrderId = buyResult['data']['orderId']

                            # buyDetail = orderApi.detail(ticker, orderId=buyOrderId)
                            buyPrice = getDealPrice(ticker, buyOrderId)

                            msg = ticker, 'Buy Short ', 'CCI:', cci, 'Price:', buyPrice
                            bot.sendMessage(chat_id="-796323955", text=msg)
                            
                            isBuy = True
                            
        else:
            #구매중인 경우 판매시점 잡기
            if isGoldenCross == True:                
                #차익
                sum = currentPrice - buyPrice
                        
                if currentPrice > maxPrice:
                    #고점 갱신
                    maxPrice = currentPrice
        
                if currentPrice <= downLinePrice:
                    #손절
                    #10배수 썼을 경우 수익률
                    # marketPrice = marketApi.market_price(ticker)
                    # price = float(marketPrice['data']['markPrice'])
                    # # sellResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_long', orderType='limit', price=price, timeInForceValue='normal')
                    # closeResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_long', orderType='market', timeInForceValue='normal')
                    # sellOrderId = closeResult['data']['orderId']

                    # sellDetail = orderApi.detail(ticker, orderId=sellOrderId)
                    # sellPrice = getDealPrice(ticker, buyOrderId)

                    rate = getPer(downLinePrice, buyPrice)
                    totalRate += rate
                    msg = ticker, 'Sell Long Stop Loss', 'CCI:', cci, 'Price:', sellPrice, 'sum:', round(downLinePrice-buyPrice, 1), 'Rate: ', rate, 'TotalRate: ', totalRate
                    bot.sendMessage(chat_id="-796323955", text=msg)

                    # saveExcel(ticker, currentPrice, buyPrice)
                    
                    cciLow = False
                    cciHight = False
                    isBuy = False
                    upLinePrice = 0.0     #익절 라인 + 0.5%
                    downLinePrice = 0.0   #손절 라인 -0.5%
                    maxPrice = 0.0        #고가
                    buyPrice = 0.0        #매수 가격
                    
                    if ma10.iloc[-1] > ma30.iloc[-1]:
                        isGoldenCross = True
                        isDeadCross = False
                    elif ma10.iloc[-1] < ma30.iloc[-1]:
                        isGoldenCross = False
                        isDeadCross = True
                    else:
                        isGoldenCross = False
                        isDeadCross = False


                #익절 분기점(+5%)을 뚫었을 경우 고점 대비 -20% 내려오면 익절
                if maxPrice > upLinePrice:
                    if currentPrice < maxPrice - (maxPrice * 0.002):
                        #익절
                        closeResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_long', orderType='market', timeInForceValue='normal')
                        sellOrderId = closeResult['data']['orderId']

                        sellPrice = getDealPrice(ticker, sellOrderId)

                        rate = getPer(sellPrice, buyPrice)
                        totalRate += rate
                        msg = ticker, 'Sell Long Take Profit', 'CCI:', cci, 'Price:', sellPrice, 'sum:', round(sellPrice-buyPrice, 1), 'Rate: ', rate, 'TotalRate: ', totalRate
                        bot.sendMessage(chat_id="-796323955", text=msg)
                        # saveExcel(ticker, currentPrice, buyPrice)
                        
                        cciLow = False
                        cciHight = False
                        isBuy = False
                        upLinePrice = 0.0     #익절 라인 + 0.5%
                        downLinePrice = 0.0   #손절 라인 -0.5%
                        maxPrice = 0.0        #고가
                        buyPrice = 0.0        #매수 가격

                        if ma10.iloc[-1] > ma30.iloc[-1]:
                            isGoldenCross = True
                            isDeadCross = False
                        elif ma10.iloc[-1] < ma30.iloc[-1]:
                            isGoldenCross = False
                            isDeadCross = True
                        else:
                            isGoldenCross = False
                            isDeadCross = False

                        
            if isDeadCross == True:
                #차익
                sum = buyPrice - currentPrice
                        
                if currentPrice < maxPrice:
                    #고점 갱신
                    maxPrice = currentPrice
        
                if currentPrice > upLinePrice:
                    #손절
                    # closeResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_short', orderType='market', timeInForceValue='normal')
                    # sellOrderId = closeResult['data']['orderId']

                    # sellDetail = orderApi.detail(ticker, orderId=sellOrderId)
                    # sellPrice = getDealPrice(ticker, buyOrderId)

                    rate = getPer(upLinePrice, buyPrice) * -1
                    totalRate += rate
                    msg = ticker, 'Sell Short Stop Loss', 'CCI:', cci, 'Price:', sellPrice, 'sum:', round(buyPrice-upLinePrice, 1), 'Rate: ', rate, 'TotalRate: ', totalRate
                    bot.sendMessage(chat_id="-796323955", text=msg)
                    # saveExcel(ticker, currentPrice, buyPrice)
                    
                    cciLow = False
                    cciHight = False
                    isBuy = False
                    upLinePrice = 0.0     #익절 라인 + 0.5%
                    downLinePrice = 0.0   #손절 라인 -0.5%
                    maxPrice = 0.0        #고가
                    buyPrice = 0.0        #매수 가격

                    if ma10.iloc[-1] > ma30.iloc[-1]:
                        isGoldenCross = True
                        isDeadCross = False
                    elif ma10.iloc[-1] < ma30.iloc[-1]:
                        isGoldenCross = False
                        isDeadCross = True
                    else:
                        isGoldenCross = False
                        isDeadCross = False

                #익절 분기점(+5%)을 뚫었을 경우 고점 대비 -20% 내려오면 익절
                if maxPrice < downLinePrice:
                    if currentPrice > maxPrice + (maxPrice * 0.002):
                        #익절
                        closeResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_short', orderType='market', timeInForceValue='normal')
                        sellOrderId = closeResult['data']['orderId']

                        # sellDetail = orderApi.detail(ticker, orderId=sellOrderId)
                        sellPrice = getDealPrice(ticker, sellOrderId)

                        rate = getPer(sellPrice, buyPrice) * -1
                        totalRate += rate
                        msg = ticker, 'Sell Short Take Profit', 'CCI:', cci, 'Price:', sellPrice, 'sum:', round(buyPrice-sellPrice, 1), 'Rate: ', rate, 'TotalRate: ', totalRate
                        bot.sendMessage(chat_id="-796323955", text=msg)
                        # saveExcel(ticker, currentPrice, buyPrice)

                        cciLow = False
                        cciHight = False
                        isBuy = False
                        upLinePrice = 0.0     #익절 라인 + 0.5%
                        downLinePrice = 0.0   #손절 라인 -0.5%
                        maxPrice = 0.0        #고가
                        buyPrice = 0.0        #매수 가격

                        if ma10.iloc[-1] > ma30.iloc[-1]:
                            isGoldenCross = True
                            isDeadCross = False
                        elif ma10.iloc[-1] < ma30.iloc[-1]:
                            isGoldenCross = False
                            isDeadCross = True
                        else:
                            isGoldenCross = False
                            isDeadCross = False

        time.sleep(1)                            
        # time.sleep(len(tickers) * 4)


import logging
import threading
import time

startAuto('SEOSSUSDT_SUMCBL')

for i in tickers:
    t = threading.Thread(target=startAuto, args=(i,)) 
    t.start()
    time.sleep(3)




# #테스트 코드
# ticker = 'SBTCSUSDT_SUMCBL'

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
# buyResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='open_long', orderType='market', timeInForceValue='normal', presetStopLossPrice=downLinePrice)
# buyOrderId = buyResult['data']['orderId']


# # buyDetail = orderApi.detail(ticker, orderId=buyOrderId)
# buyPrice = getDealPrice(ticker, buyOrderId)

# msg = 'Test Message BitGet ', ticker, 'Buy Long ', 'CCI:', cci, 'Price:', buyPrice
# bot.sendMessage(chat_id="-796323955", text=msg)
# time.sleep(10)





# closeResult = orderApi.place_order(ticker, marginCoin='SUSDT', size=size, side='close_long', orderType='market', timeInForceValue='normal')

# sellOrderId = closeResult['data']['orderId']

# # sellDetail = orderApi.detail(ticker, orderId=sellOrderId)
# sellPrice = getDealPrice(ticker, buyOrderId)

# rate = getPer(sellPrice, buyPrice) * -1
# msg = 'Test Message BitGet ', ticker, 'Sell Short Take Profit', 'CCI:', cci, 'Price:', sellPrice, 'Rate: ', rate
# bot.sendMessage(chat_id="-796323955", text=msg)
