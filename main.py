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

#포트폴리오
#전체중 절반 투자
investRate = 0.5
balance = 2000000
protectedBalance = balance * investRate

print("투자 원금 : ", balance)
print("현금 비중 : ", investRate)
print("여유금 : ", protectedBalance)




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
        inList.append("상승장")

        list.append(inList)
        #buy_crypto_currency(100000, ticker)
        print("\nBUY !!! " + ticker)
        


df = pd.DataFrame(list, columns=["ticker", "target_price", "ma5", "current_price", "state"])

df.to_csv(now.strftime('%Y-%m-%d')+'.txt', header=None, index=None, sep=' ', mode='a')
print(df)



### Connect RDS Mysql

import pymysql

conn = None
cur = None

sql="desc data4"

conn = pymysql.connect(host="springboot2-webservice.ctsnx9",
                      user="",
                      password="",
                      db='springboot2_webservice',
                      charset='utf8')
cur = conn.cursor()
print(cur.execute(sql))

import datetime

day = now.strftime('%Y-%m-%d')

for i in df.index:
    list = df.loc[i,:].tolist()    
    sql="""insert into tables(date_string, ticker, target_price, ma5, current_price) VALUES(\""""+now.strftime('%Y-%m-%d') +"\",\""+ list[0] +"\","+ str(list[1]) +","+ str(list[2]) +","+ str(list[3]) +")"
    print(sql)
    
    
    print(cur.execute(sql))

    
sql="select * from tables"
print(cur.execute(sql))
rows = cur.fetchall()
print(rows)

conn.commit()        
    
    

conn.close()
