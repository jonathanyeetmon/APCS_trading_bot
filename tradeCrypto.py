## BigMoneyBot
## Jonathan Doredla
## Bot that trades BTC, though it can be changed to other crypto, and I can easily edit the code to trade stocks.

import alpaca_trade_api as tradeapi ## I need to use Alpaca's free to use API
#installs pandas and numpy as a dependency ^
import talib as ta
import time



## lots of documentation was found online from alpaca's website
## also I used this https://github.com/alpacahq/alpaca-trade-api-python


key= 'PK6AMQI7DMU0DN89BF6D'
secretKey= '0NkvMRYAGYOPgUPSH94G8XVW8jHr67yFNTiMwhGu'
## It's hooked up to paper trading and I have no credentials in their so this is not a big deal. I can also regenerate a new key
baseURL = 'https://paper-api.alpaca.markets'   ## for paper trading. It's a different URL for real money trading.

tradeSize ='1'
symbol = 'BTCUSD'   # stock ticker for stocks


api = tradeapi.REST(key, secretKey , baseURL, api_version='v2') ## my connection with alpaca via REST class
account = api.get_account()


def  getPos():
    return float (api.get_position(symbol).qty)

def sma(data, time):
    return (data.close).rolling(time).mean()

def getBars(): # used to get bars and get's my moving averages and RSI
    coinData = api.get_crypto_bars(symbol= symbol, timeframe='1Minute', exchanges='CBSE').df  ## pandas datafram makes it easier
    # api.get_bars(symbol,timeframe) for stocks
    coinData['OneHrSMA'] = sma(coinData,60)
    coinData['TenMinSMA']= sma(coinData,10)
    return coinData




print('\n\n')

#clock = api.get_clock() #tells me when market opens and if it's open at the moment, but I'm not gonna use it cause I'm trading crypto. It's there if I want to trade something else
while True: ##Need a bot that's always running while the market is open
    totalData = getBars()
    rsi = ta.RSI(totalData.open[:-61]) # using TAlib library to calculate RSI over the past 60 minutes
    # RSI is a momentum indicator I will be using in conjunction with my simple moving average's to determin when to trade

    smaBuy = False
    rsiBuy = False
    smaSell = False
    rsiSell = False

    if totalData.TenMinSMA[-1] > totalData.OneHrSMA[-1]:
        smaBuy = True

    if totalData.TenMinSMA[-1] < totalData.OneHrSMA[-1]:
        smaSell = True

    if rsi[-1]>60:
        rsiBuy = True

    print(f"10 min simple moving average: {totalData.TenMinSMA[-1]} " )
    print(f"1 Hour simple moving average: {totalData.OneHrSMA[-1]} ")
    print(f"1 Hour Relative Strength Index: {rsi[-1]}")
    print(f"Simple Moving Average buy indication: {smaBuy}.")
    print(f"Simple Moving Average sell indication: {smaSell}.")
    print(f"Relative Strength Index buy indication: {rsiBuy}.")

    # selling if conditions are met and have some BTC, or whatever coin I want it to be
    if smaSell and rsi[-1]<=60:
        try:
            x = getPos()
        except:
            print(f"Our indicators recommend selling, but there's no {symbol} to sell.")
        else:
            print(f" Our indicators tell us to sell some {symbol}")
            api.submit_order(symbol=symbol, side='sell', type='market', qty=tradeSize)


    # Buying if conditions are met
    if rsiBuy and smaBuy:
        try:
            x = getPos()
        except:
            print(f"You don't own any {symbol}, and our indicators are saying it's time to get some ")
            print(f"We're gonna put an order for {symbol}")
            api.submit_order(symbol=symbol, side='buy', type='market', qty=tradeSize)

        else:
            print("Our indicators say buy")
            print(f"We're already holding some {symbol}, so we're not going to buy more")

    print('\n\n')

    time.sleep(60)#wait's a min before running again becasue bars only update every min










#val= api.get_crypto_bars(symbol = "BTCUSD", timeframe = '1Min',exchanges="CBSE").df
#print(val)



## My first order of bitoin!
## for testing purposes
#api.submit_order(
#    symbol='BTCUSD',
 #   side='buy',
 #   type='market',
 #   qty='0.001',

#)

# I don't want to buy more Bitcoin so I commented it out

#print(api.list_orders())
#print("\n")
#print(api.get_position("BTCUSD")) ## showing my position of bitcoin, which is current 0.004 BTC
#print(api.get_position("BTCUSD").qty)
