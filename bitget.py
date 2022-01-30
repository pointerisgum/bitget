# import time
# import pyupbit
# import datetime
# import requests
# import schedule
# from fbprophet import Prophet
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

access = "xwdEMciw0PeGRfpA8xMaVtnVGmFPFxTR6dkKCnUQ"
secret = "UOxwdGYVZflyTCbMwrlrzB0Ey44GGxSLl70xp8A4"
slackToken = "xoxb-2958422443234-2961015128436-OlEZV7qGyaamz31X3slydehR"
# teleToken = "5225100528:AAGL0OC4m40gsMkB9haFGm0weJMUSKGqY2U"
teleToken = "5225100528:AAGL0OC4m40gsMkB9haFGm0weJMUSKGqY2U"

bot = telegram.Bot(token=teleToken)
# updates = bot.getUpdates()
# chat_id = updates[-1].message.chat_id

# bot.sendMessage(chat_id="-796323955", text='test1')

# for update in updates:
#     print(update.message)

# bot.sendMessage(chat_id=chat_id, text='test2')


try:

    upbit_api.set_loglevel('I')
        
    # CCI 조회(60분봉/10개)
    candle_data = upbit_api.get_candle('KRW-BTC', '15', 200)
    cci = upbit_api.get_cci(candle_data, 1)
    print(cci[0]['CCI'])
        
    #현재 CCI 값 (15분봉 기준)
    

    # df = pyupbit.get_ohlcv('KRW-BTC', interval="minute15", count=180, to="2021-01-17 01:30:00")
    # # ma10 = df.rolling(window=10).mean()
    # # ma30 = df.rolling(window=30).mean()

    # ma10 = df.rolling(window=10).mean()
    # ma30 = df.rolling(window=30).mean()
    # # print(ma10.iloc.count)
    # print(ma30.iloc[-4])
    # print(ma10.iloc[-4])
    # print(ma30.iloc[-3])
    # print(ma10.iloc[-3])
    # print(ma30.iloc[-2])
    # print(ma10.iloc[-2])
    # print(ma30.iloc[-1])
    # print(ma10.iloc[-1])

    # print(ma10.iloc[8])
    # print(ma10.iloc[10])
    # print(ma10.iloc[11])
    # print(ma30.iloc[28])
    # print(ma30.iloc[30])
    # print(ma30.iloc[31])

    # # print(ma10.iloc[0])

    # ma10.iloc[-4]['close']
    # test1=ma10.iloc[-4]-ma30.iloc[-4]
    # test2=ma10.iloc[-3]-ma30.iloc[-3]
    
    # line10=ma10.iloc[-2]-ma30.iloc[-2]
    # line30=ma10.iloc[-1]-ma30.iloc[-1]

    # call='해당없음'
    
    # if test1>0 and test2<0:
    #     call='데드크로스' 
        
    # if test1<0 and test2>0:
    #     call='골든크로스'     

    # print(call)

    
    
    # for i in range(10, int(ma10.raw)):
    #     print(candle_data[i]['candle_date_time_kst'], ma10.iloc[i]['close'])
    #     # print(ma10.iloc[i]['close'])
    # # for i in df.count:
        
    #     test1=ma10.iloc[i]-ma30.iloc[i]
    #     test2=ma10.iloc[i+1]-ma30.iloc[i+1]
        

    #     # print(test1)
    #     print(test2)
    #     # call='해당없음'
        
    #     # if test1>0 and test2<0:
    #     #     call='데드크로스' 
            
    #     # if test1<0 and test2>0:
    #     #     call='골든크로스'     

    #     # print(call)

    
    
    macd_data = upbit_api.get_macd('KRW-BTC', '15', '200', 200)

    for macd_data_for in macd_data:
        logging.info(macd_data_for)
        # print(macd_data_for['DT'], macd_data_for['MACD'])

    # for cci_for in cci:
    #     print(cci_for)
    #     # logging.info(cci_for)

#def get_macd(target_item, tick_kind, inq_range, loop_cnt):
    # candle_data = get_candle(target_item, tick_kind, inq_range)
    # macd = upbit_api.get_macd('KRW-BTC', '15', '200', 200)

    # for macd_for in macd:
    #     print(macd_for)
    #     # logging.info(cci_for)



    # # 전체 지표 조회
    # indicator_data = upbit_api.get_indicators('KRW-BTC', '15', 200, 12)

    # logging.info('전체 지표 조회')
    # for indicator_data_for in indicator_data:
    #     logging.info(indicator_data_for)

except KeyboardInterrupt:
    logging.error("KeyboardInterrupt Exception 발생!")
    logging.error(traceback.format_exc())
    sys.exit(-100)

except Exception:
    logging.error("Exception 발생!")
    logging.error(traceback.format_exc())
    sys.exit(-200)








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
tickers = ["KRW-BTC", "KRW-ETH", "KRW-BCH", "KRW-AAVE", "KRW-LTC", 'KRW-DOT', 'KRW-SAND']
# tickers = ["KRW-BTC"]

def getPer(c, b):
    #(((매도가 - 매수가) / 매수가 ) * 100 ) - 0.08) * 10
    return round(((((c - b) / b) * 100) - 0.08) * 10, 2)

def updateCCI(ticker, sleepSec):
    time.sleep(sleepSec)
    candle_data = upbit_api.get_candle(ticker, '15', 200)
    cci_data = upbit_api.get_cci(candle_data, 1)
    cci = cci_data[0]['CCI']
    return cci

def startAuto(ticker):
    isGoldenCross = FALSE
    isDeadCross = FALSE
    cciLow = FALSE
    cciHight = FALSE
    isBuy = FALSE
    cciUpdateSec = 15
    upLinePrice = 0     #익절 라인 + 0.5%
    downLinePrice = 0   #손절 라인 -0.5%
    maxPrice = 0        #고가
    buyPrice = 0        #매수 가격
    
    while True:
        
        candle_data = upbit_api.get_candle(ticker, '15', 200)

        cci_data = upbit_api.get_cci(candle_data, 1)
        cci = cci_data[0]['CCI']

        currentPrice = candle_data[0]['trade_price']

        df = pd.DataFrame(candle_data)
        df=df['trade_price'].iloc[::-1]
        
        ma10 = df.rolling(window=10).mean()
        ma30 = df.rolling(window=30).mean()

        line10=ma10.iloc[-2]-ma30.iloc[-2]
        line30=ma10.iloc[-1]-ma30.iloc[-1]
        
        dead = line10>0 and line30<0
        gold = line10<0 and line30>0
               
        print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, 'line10: ', round(line10, 1), 'line30: ', round(line30, 1), 'ma10: ', round(ma10.iloc[-1], 1), 'ma30: ', round(ma30.iloc[-1], 1))

        if isBuy == TRUE:
            #구매중에 데드가 골드로 바뀔 경우에 대한 처리
            if dead:
                #데드크로스
                if isGoldenCross == TRUE:
                    #골드가 났었는데 데드로 바뀐 경우 들고 있던 코인 시장가 매도 후 리셋                                    
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Dead Cross  ', 'CCI:', cci, 'Price:', currentPrice
                    bot.sendMessage(chat_id="-796323955", text=msg)
                    
                    sum = currentPrice - buyPrice
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Long Throw', 'CCI:', cci, 'Price:', currentPrice, 'sum:', sum, 'rate:', getPer(currentPrice, buyPrice)
                    bot.sendMessage(chat_id="-796323955", text=msg)
                    
                    isGoldenCross = FALSE
                    isDeadCross = TRUE
                    cciLow = FALSE
                    cciHight = FALSE
                    isBuy = FALSE
                    upLinePrice = 0
                    downLinePrice = 0
                    maxPrice = 0
                    buyPrice = 0
                    
            if gold:
                #골든크로스
                if isDeadCross == TRUE:
                    #데드가 났었는데 골드로 바뀐 경우 들고 있던 코인 시장가 매도 후 리셋                                 
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Golden Cross  ', 'CCI:', cci, 'Price:', currentPrice
                    bot.sendMessage(chat_id="-796323955", text=msg)

                    sum = currentPrice - buyPrice
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Short Throw', 'CCI:', cci, 'Price:', currentPrice, 'sum:', sum, 'rate:', getPer(currentPrice, buyPrice) * -1
                    bot.sendMessage(chat_id="-796323955", text=msg)
                    
                    isGoldenCross = TRUE
                    isDeadCross = FALSE
                    cciLow = FALSE
                    cciHight = FALSE
                    isBuy = FALSE
                    upLinePrice = 0
                    downLinePrice = 0
                    maxPrice = 0
                    buyPrice = 0
        else:
            if isDeadCross == TRUE:
                #데드에서 골드로 바뀐 경우
                if gold:
                    isDeadCross = FALSE
                    isGoldenCross = TRUE
            elif isGoldenCross == TRUE:
                #골드에서 데드로 바뀐 경우
                if dead:
                    isDeadCross = TRUE
                    isGoldenCross = FALSE

        if isBuy == FALSE:
            if isGoldenCross == FALSE and isDeadCross == FALSE:                
                cci_data = upbit_api.get_cci(candle_data, 1)
                cci = cci_data[0]['CCI']

                if dead:
                    call='데드크로스'
                    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, call)
                    isDeadCross = TRUE
                    current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Dead Cross  ', 'CCI:', cci, 'Price:', current_price
                    bot.sendMessage(chat_id="-796323955", text=msg)      
                           
                if gold:
                    call='골든크로스'
                    print(datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, call)
                    isGoldenCross = TRUE
                    current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Golden Cross  ', 'CCI:', cci, 'Price:', current_price
                    bot.sendMessage(chat_id="-796323955", text=msg)
            else:
                cci_data = upbit_api.get_cci(candle_data, 1)
                cci = cci_data[0]['CCI']
                
                if isGoldenCross == TRUE:
                    #매수 타이밍 잡기 (cci:-100 이하로 떨어지고 다시 -100을 뚫었을때)
                    if cciLow == FALSE:
                        if cci <= -100:
                            cci = updateCCI(ticker, cciUpdateSec)
                            if cci <= -100:
                                cciLow = TRUE
                    else:
                        if cci >= -100:
                            cci = updateCCI(ticker, cciUpdateSec)
                            if cci >= -100:
                                #매수 시점
                                #여긴 updateCCI 함수의 sleep으로 인해 값을 갱신해 줘야 함
                                candle_data = upbit_api.get_candle(ticker, '15', 1)
                                currentPrice = candle_data[0]['trade_price']
                                
                                maxPrice = currentPrice
                                buyPrice = currentPrice
                                upLinePrice = buyPrice + (buyPrice * 0.005)
                                downLinePrice = buyPrice - (buyPrice * 0.01)
                                msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Buy Long ', 'CCI:', cci, 'Price:', currentPrice
                                bot.sendMessage(chat_id="-796323955", text=msg)
                                isBuy = TRUE   
                                             
                if isDeadCross == TRUE:
                    #매수 타이밍 잡기 (cci:+100 이상으로 올라가고 다시 +100으로 내려 갔을때)
                    if cciHight == FALSE:
                        if cci >= 100:
                            cci = updateCCI(ticker, cciUpdateSec)
                            if cci >= 100:
                                cciHight = TRUE
                    else:
                        if cci <= 100:
                            cci = updateCCI(ticker, cciUpdateSec)
                            if cci <= 100:
                                #매수 시점
                                #여긴 updateCCI 함수의 sleep으로 인해 값을 갱신해 줘야 함
                                candle_data = upbit_api.get_candle(ticker, '15', 1)
                                currentPrice = candle_data[0]['trade_price']
                                maxPrice = currentPrice
                                buyPrice = currentPrice
                                upLinePrice = buyPrice + (buyPrice * 0.005)
                                downLinePrice = buyPrice - (buyPrice * 0.01)
                                msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Buy Short ', 'CCI:', cci, 'Price:', currentPrice
                                bot.sendMessage(chat_id="-796323955", text=msg)
                                isBuy = TRUE
                            
        else:
            #구매중인 경우 판매시점 잡기
            if isGoldenCross == TRUE:                
                #차익
                sum = currentPrice - buyPrice
                        
                if currentPrice > maxPrice:
                    #고점 갱신
                    maxPrice = currentPrice
        
                if currentPrice < downLinePrice:
                    #손절
                    #10배수 썼을 경우 수익률
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Long Stop Loss', 'CCI:', cci, 'Price:', currentPrice, 'sum:', sum, 'rate:', getPer(currentPrice, buyPrice)
                    bot.sendMessage(chat_id="-796323955", text=msg)

                    cciLow = FALSE
                    cciHight = FALSE
                    isBuy = FALSE
                    upLinePrice = 0     #익절 라인 + 0.5%
                    downLinePrice = 0   #손절 라인 -0.5%
                    maxPrice = 0        #고가
                    buyPrice = 0        #매수 가격

                #익절 분기점(+5%)을 뚫었을 경우 고점 대비 -20% 내려오면 익절
                if maxPrice > upLinePrice:
                    if currentPrice < maxPrice - (maxPrice * 0.002):
                        #익절
                        msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Long Take Profit', 'CCI:', cci, 'Price:', currentPrice, 'sum:', sum, 'rate:', getPer(currentPrice, buyPrice)
                        bot.sendMessage(chat_id="-796323955", text=msg)

                        cciLow = FALSE
                        cciHight = FALSE
                        isBuy = FALSE
                        upLinePrice = 0     #익절 라인 + 0.5%
                        downLinePrice = 0   #손절 라인 -0.5%
                        maxPrice = 0        #고가
                        buyPrice = 0        #매수 가격

                        
            if isDeadCross == TRUE:
                #차익
                sum = buyPrice - currentPrice
                        
                if currentPrice < maxPrice:
                    #고점 갱신
                    maxPrice = currentPrice
        
                if currentPrice > upLinePrice:
                    #손절
                    msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Short Stop Loss', 'CCI:', cci, 'Price:', currentPrice, 'sum:', sum, 'rate:', getPer(currentPrice, buyPrice) * -1
                    bot.sendMessage(chat_id="-796323955", text=msg)

                    cciLow = FALSE
                    cciHight = FALSE
                    isBuy = FALSE
                    upLinePrice = 0     #익절 라인 + 0.5%
                    downLinePrice = 0   #손절 라인 -0.5%
                    maxPrice = 0        #고가
                    buyPrice = 0        #매수 가격

                #익절 분기점(+5%)을 뚫었을 경우 고점 대비 -20% 내려오면 익절
                if maxPrice < downLinePrice:
                    if currentPrice > maxPrice + (maxPrice * 0.002):
                        #익절
                        msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Short Take Profit', 'CCI:', cci, 'Price:', currentPrice, 'sum:', sum, 'rate:', getPer(currentPrice, buyPrice) * -1
                        bot.sendMessage(chat_id="-796323955", text=msg)
                          
                        cciLow = FALSE
                        cciHight = FALSE
                        isBuy = FALSE
                        upLinePrice = 0     #익절 라인 + 0.5%
                        downLinePrice = 0   #손절 라인 -0.5%
                        maxPrice = 0        #고가
                        buyPrice = 0        #매수 가격

                
            # if isGoldenCross == TRUE:
            #     if cci >= 100:
            #         #cci가 100 이상 올라갔을때 판매
            #         current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
            #         msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Long ', 'CCI:', cci, 'Price:', current_price
            #         bot.sendMessage(chat_id="-796323955", text=msg)
                    
            #         #판매 후 리셋
            #         isGoldenCross = FALSE
            #         isDeadCross = FALSE
            #         cciLow = FALSE
            #         cciHight = FALSE
            #         isBuy = FALSE
                    
            # if isDeadCross == TRUE:
            #     if cci <= -100:
            #         #cci가 100 이하로 내려 갔을때 판매
            #         current_price = pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
            #         msg = datetime.now().strftime("%Y/%m/%d, %H:%M:%S"), ticker, ' Sell Short ', 'CCI:', cci, 'Price:', current_price
            #         bot.sendMessage(chat_id="-796323955", text=msg)
                    
            #         #판매 후 리셋
            #         isGoldenCross = FALSE
            #         isDeadCross = FALSE
            #         cciLow = FALSE
            #         cciHight = FALSE
            #         isBuy = FALSE

        time.sleep(len(tickers) * 2)


import logging
import threading
import time

for i in tickers:
    t = threading.Thread(target=startAuto, args=(i,)) 
    t.start()
    time.sleep(2)

