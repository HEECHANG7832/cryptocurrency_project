import time
import pybithumb
import datetime
from datetime import date, timedelta

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

import pandas as pd


k = 0.8

with open(r"C:\py_workspace\bithumb.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker)
    try:
        yesterday = df.iloc[-2]
    except:
        return 0

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * k
    return target

def buy_crypto_currency(krw, ticker): # won
    balance = bithumb.get_balance(ticker)[2]
    if balance > krw + protectedBalance :
        orderbook = pybithumb.get_orderbook(ticker)
        sell_price = orderbook['asks'][0]['price']
        unit = krw/float(sell_price)
        bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]





now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("BTC")
target_price = get_target_price("BTC")


investRate = 0.5
balance = 2000000
protectedBalance = balance * investRate

print(balance)
print(investRate)
print(protectedBalance)




# yesterday = date.today() - timedelta(1)

# df_yesterday = pd.read_csv(yesterday.strftime('%Y-%m-%d')+'.txt', header=None, sep=' ')
# df_yesterday.columns = ["ticker", "target_price", "ma5", "current_price", "state"]


# print(df_yesterday)

# yesterday_price = df_yesterday[df_yesterday['ticker']=='BTC']['current_price']

# #df_yesterday.loc[,'current_price']



#ticker, target_price, ma5, current_price, state
tickers = pybithumb.get_tickers()
list = []
for ticker in tickers:
    inList = []
    print('.', end='')
    target_price = get_target_price(ticker)
    if target_price == 0:
        print("new ticker")
        continue
    ma5 = get_yesterday_ma5(ticker)
    
    #sell_crypto_currency(ticker)

    current_price = pybithumb.get_current_price(ticker)
    
    
    if (current_price > target_price) and (current_price > ma5):
        print()
        print(ticker, target_price, ma5, current_price)
        inList.append(ticker)
        inList.append(target_price)
        inList.append(ma5)
        inList.append(current_price)

        list.append(inList)
        #buy_crypto_currency(100000, ticker)
        print("\nBUY !!! " + ticker)
        