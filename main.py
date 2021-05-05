#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 3.21 수익률 모니터링 만들기


# In[2]:


import time
import pybithumb
import datetime
from datetime import date, timedelta

import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

import pandas as pd


# In[3]:



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



# In[8]:



now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("BTC")
target_price = get_target_price("BTC")

#포트폴리오
#전체중 절반 투자
investRate = 0.5
balance = 2000000
protectedBalance = balance * investRate

print("투자 원금 : ", balance)
print("현금 비중 : ", investRate)
print("여유금 : ", protectedBalance)


# In[6]:




# yesterday = date.today() - timedelta(1)

# df_yesterday = pd.read_csv(yesterday.strftime('%Y-%m-%d')+'.txt', header=None, sep=' ')
# df_yesterday.columns = ["ticker", "target_price", "ma5", "current_price", "state"]


# print(df_yesterday)

# yesterday_price = df_yesterday[df_yesterday['ticker']=='BTC']['current_price']

# #df_yesterday.loc[,'current_price']


# In[9]:




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
    
    sell_crypto_currency(ticker)

    current_price = pybithumb.get_current_price(ticker)
    
    
    if (current_price > target_price) and (current_price > ma5):
        print()
        print(ticker, target_price, ma5, current_price)
        inList.append(ticker)
        inList.append(target_price)
        inList.append(ma5)
        inList.append(current_price)
        inList.append("상승장")

        list.append(inList)
        buy_crypto_currency(100000, ticker)
        print("\nBUY !!! " + ticker)


# In[10]:


df = pd.DataFrame(list, columns=["ticker", "target_price", "ma5", "current_price", "state"])

df.to_csv(now.strftime('%Y-%m-%d')+'.txt', header=None, index=None, sep=' ', mode='a')
print(df)


# In[19]:





# In[49]:


# import pybithumb
# import numpy as np

# list = []
# data = pd.DataFrame(list, columns=['bull3', 'ror3', 'bull5', 'ror5', 'bull10', 'ror10', 'bull30', 'ror30'])

# def get_hpr(ticker):
#     df = pybithumb.get_ohlcv(ticker)
#     #df = df['2020']

#     df['ma3'] = df['close'].rolling(window=3).mean().shift(1) #ma3
#     df['range'] = (df['high'] - df['low']) * 0.5 #range
#     df['target'] = df['open'] + df['range'].shift(1) #shift range
#     df['bull3'] = df['open'] > df['ma3'] #

#     fee = 0.0032
#     df['ror3'] = np.where((df['high'] > df['target']) & df['bull3'],
#                           df['close'] / df['target'] - fee,
#                           1)
    
#     df['ma5'] = df['close'].rolling(window=5).mean().shift(1) #ma3
#     df['range'] = (df['high'] - df['low']) * 0.5 #range
#     df['target'] = df['open'] + df['range'].shift(1) #shift range
#     df['bull5'] = df['open'] > df['ma5'] #

#     fee = 0.0032
#     df['ror5'] = np.where((df['high'] > df['target']) & df['bull5'],
#                           df['close'] / df['target'] - fee,
#                           1)
    
#     df['ma10'] = df['close'].rolling(window=10).mean().shift(1) #ma3
#     df['range'] = (df['high'] - df['low']) * 0.5 #range
#     df['target'] = df['open'] + df['range'].shift(1) #shift range
#     df['bull10'] = df['open'] > df['ma10'] #

#     fee = 0.0032
#     df['ror10'] = np.where((df['high'] > df['target']) & df['bull10'],
#                           df['close'] / df['target'] - fee,
#                           1)
    
#     df['ma30'] = df['close'].rolling(window=30).mean().shift(1) #ma3
#     df['range'] = (df['high'] - df['low']) * 0.5 #range
#     df['target'] = df['open'] + df['range'].shift(1) #shift range
#     df['bull30'] = df['open'] > df['ma30'] #

#     fee = 0.0032
#     df['ror30'] = np.where((df['high'] > df['target']) & df['bull30'],
#                           df['close'] / df['target'] - fee,
#                           1)
    
#     df['ror'] = np.where(1,
#                           df['close'] / df['target'] - fee,
#                           1)
#     df['rorbull'] = np.where(df['ror'] >= 1.0,
#                             1,
#                             0)
    
#     #df['hpr'] = df['ror'].cumprod()
#     #df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#     print(df.loc[:, df.columns.isin(['volume','rorbull', 'bull3', 'bull5','bull10', 'bull30'])].head(20))
#     return 0 #df['hpr'][-2]


# tickers = pybithumb.get_tickers()

# hprs = []
# ticker = 'BTC'
# #for ticker in tickers:
# hpr = get_hpr(ticker)
# hprs.append((ticker, hpr))


# #sorted_hprs = sorted(hprs, key=lambda x:x[1])
# #print(sorted_hprs[-5:])


# 

# In[6]:


df


# In[3]:


# import pybithumb
# import numpy as np

# #for coin in  pybithumb.get_tickers():
# #    print(coin, pybithumb.get_market_detail(coin))


# df = pybithumb.get_candlestick("BTC")
# print(df.tail(5))
    


# In[ ]:




