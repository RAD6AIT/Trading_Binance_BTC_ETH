import numpy as np
import ccxt
import time
import pandas as pd
import copy 
from decimal import Decimal as D
from colorama import Fore, Back, Style
from datetime import datetime
from binance.client import Client

list_sell_order = []
list_buy_order = []
list_sell_profit = []
list_buy_profit = []

def importCSV():
        try:
            df = pd.read_csv('TradeOpen.csv')
        except IOError:
            return
        i = 0
        order_tmp = {}
        while i < len(df.index):
            if df.iloc[i]['LIST'] == "LIMIT_SELL" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = str(df.iloc[i]['ORDERID'])
                list_sell_order.append(order_tmp)
            elif df.iloc[i]['LIST'] == "LIMIT_BUY" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = str(df.iloc[i]['ORDERID'])
                list_buy_order.append(order_tmp)
            elif df.iloc[i]['LIST'] == "SELL_PROFIT" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = str(df.iloc[i]['ORDERID'])
                order_tmp ['OFFLOAD'] = df.iloc[i]['OFFLOAD']
                list_sell_profit.append(order_tmp)
            elif df.iloc[i]['LIST'] == "BUY_PROFIT" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = str(df.iloc[i]['ORDERID'])
                order_tmp ['OFFLOAD'] = df.iloc[i]['OFFLOAD']
                list_buy_profit.append(order_tmp)
            i += 1
            order_tmp = {}

def moyenne_sell_profit():
    n = 0
    p = 0
    for order in list_sell_profit :
        p += order['price']
        n +=1
    return (p/n)

def moyenne_buy_profit():
    n = 0
    p = 0
    for order in list_buy_profit :
        p += order['price']
        n +=1
    return (p/n)

binance = ccxt.binance({'apiKey': 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9', 'secret': 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'})
Last_Total = 0

w = binance.fetch_balance ()
eth_btc = binance.fetchOrderBook('ETH/BTC')
eth_btc_ask = eth_btc['asks'][0][0]
Total_Start = w['BTC']['total'] + w['ETH']['total'] * eth_btc_ask

while True:


    importCSV()
    print ("############################################")
    print ("moyenne sell profit ", moyenne_sell_profit())
    print ("moyenne buy profit ", moyenne_buy_profit())

    
    w = binance.fetch_balance ()
    eth_btc = binance.fetchOrderBook('ETH/BTC')
    eth_btc_ask = eth_btc['asks'][0][0]
    print ("ETH/BTC ASK ", eth_btc_ask)
    print ("ETH free ", w['ETH']['free'], " used ", w['ETH']['used'], " total ", w['ETH']['total'])
    print ("BTC free ", w['BTC']['free'], " used ", w['BTC']['used'], " total ", w['BTC']['total'])
    Total = w['BTC']['total'] + w['ETH']['total'] * eth_btc_ask
    print ("Total BTC = ", Total)
    print ("Diff ", Total - Last_Total)
    print ("Diff from start", Total - Total_Start)
    Last_Total = Total

    time.sleep(10)

