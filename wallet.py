import numpy as np
import ccxt
import time
import pandas as pd
import copy 
from decimal import Decimal as D
from colorama import Fore, Back, Style
from datetime import datetime
from binance.client import Client

binance = ccxt.binance({'apiKey': 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9', 'secret': 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'})

eth_start = 0.45143225
btc_start = 0.0150993
Ratio_Start = 0.05333

Total_Start_btc = btc_start + (eth_start * Ratio_Start)

list_wait_sell = []
list_wait_buy = []

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
            if df.iloc[i]['LIST'] == "WAIT_SELL" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                list_wait_sell.append(order_tmp)
                #short_set.add(D(str(order_tmp ['price'])))

            elif df.iloc[i]['LIST'] == "WAIT_BUY" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                list_wait_buy.append(order_tmp)
                #long_set.add(D(str(order_tmp ['price'])))

            elif df.iloc[i]['LIST'] == "SELL_PROFIT" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                order_tmp ['OFFLOAD'] = df.iloc[i]['OFFLOAD']
                order_tmp ['src_id'] = df.iloc[i]['ORDERSRCID']
                list_sell_profit.append(order_tmp)

            elif df.iloc[i]['LIST'] == "BUY_PROFIT" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                order_tmp ['OFFLOAD'] = df.iloc[i]['OFFLOAD']
                order_tmp ['src_id'] = df.iloc[i]['ORDERSRCID']
                list_buy_profit.append(order_tmp)

            i += 1
            order_tmp = {}


while True:

    print ("--------- New round ---------")
    list_wait_sell.clear()
    list_wait_buy.clear()
    try:
        importCSV()
    except:
        next
    w = binance.fetch_balance ()
    p = binance.fetchOrderBook('ETH/BTC')
    ### ETH ###
    e1 = 0
    e2 = 0
    ### calcul de la part de ETH provenant du pool BTC ###
    for wb in list_wait_buy:
        e1 +=  wb['amount']
    for ws in list_wait_sell:
        e2 +=  ws['amount']
    
    eth_actual = w['ETH']['total'] - e1 + e2
    eth_pnl = eth_actual - eth_start

    eth_dispo = w['ETH']['total'] - e1
    eth_dispo_from_start = eth_start - e2

    

    ### BTC ###
    b1 = 0
    b2 = 0
    for xb in list_wait_sell:
        b1 +=  (xb['amount'] * xb['price'])
    for xs in list_wait_buy:
        b2 +=  (xs['amount'] * xs['price'])
    btc_actual = w['BTC']['total'] - b1 + b2
    btc_pnl = btc_actual - btc_start

    btc_dispo = w['BTC']['total'] - b1
    btc_dispo_from_start = btc_start - b2
        

    print ("Prix ETH/BTC:", p['asks'][0][0])
    print ("Wallet ETH:",w['ETH']['total'])
    print ("Wallet BTC:",w['BTC']['total'])
    print (" #### ETH #### ")
    print ("ETH PNL: ", eth_pnl)
    print ("ETH actual: ", eth_actual)
    print ("ETH Disponible: ", eth_dispo)
    print ("ETH Disponible from start: ", eth_dispo_from_start)
    print (" #### BTC #### ")
    print ("BTC PNL: ", btc_pnl)
    print ("BTC actual: ", btc_actual)
    print ("BTC Disponible: ", btc_dispo)
    print ("BTC Disponible from start: ", btc_dispo_from_start)
    print (" #### Conclusions #### ")

    total_actual_pnl_btc = btc_pnl + (eth_pnl * p['asks'][0][0])
    print ("Total Actual PNL en BTC: ", total_actual_pnl_btc) 
    #p_null_theorique= (-btc_pnl) / (eth_pnl)

    wallet_now_btc = w['BTC']['total'] + (w['ETH']['total'] * p['bids'][0][0])
    diff_now_wallet = wallet_now_btc - Total_Start_btc
    print ("Wallet actual BTC: ", wallet_now_btc)
    print ("Wallet start BTC: ", Total_Start_btc)
    print ("Difference wallet actual - start wallet : ", diff_now_wallet )
    p_null_now_theorique = (Total_Start_btc - w['BTC']['total']) / w['ETH']['total']
    
    print ("--------- End round ---------")
    time.sleep(60)