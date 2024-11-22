import numpy as np
import ccxt
import time
import pandas as pd
import copy 
from decimal import Decimal as D
from colorama import Fore, Back, Style
from datetime import datetime
from binance.client import Client

#binance = ccxt.binance({'apiKey': 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9', 'secret': 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'})
binance = ccxt.binance({'apiKey': 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9', 'secret': 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'})
binance_long = ccxt.binance({'apiKey': 'Q6zHYbYaxZB0fZlyaWxava5z7Kib3jQwWMLeoPlwbNFBZareuRivvfR0gtcnGnaw', 'secret': 'eAKILX3y8INA5vij9piQ1IShty4FR754xboZ7cUH5clyRwmVtbi3KjegD0bu78DU'})
binance_short = ccxt.binance({'apiKey': '37fo4lAJ89ldUUvkivMqdsEc48oJ6WO88KBNzPyARlmBi4RsKre8l20IWz6fIzOg', 'secret': 'y2yI9eYI4tKJjq065J3dY3YO7CHUmW3YghH0imhC6TXJiTal28SskkD79FQNytdD'})

eth_start = 0.39266942
btc_start = 0.01781204
Ratio_Start = 0.05193

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
    list_sell_profit.clear()
    list_buy_profit.clear()
    try:
        importCSV()
    except:
        next
    w_long = binance_long.fetch_balance ()
    w_short = binance_short.fetch_balance ()
    p = binance.fetchOrderBook('ETH/BTC')
    ### ETH ###
    e1 = 0
    e2 = 0
    ### calcul de la part de ETH provenant du pool BTC ###
    #for wb in list_wait_buy:
    #    e1 +=  wb['amount']
    for ws in list_buy_profit:
        e2 +=  ws['amount']
    
    eth_actual = w_short['ETH']['total'] + e2
    eth_pnl = eth_actual - eth_start

    #eth_dispo = w_short['ETH']['total']
    eth_dispo_from_start = eth_start - e2

    

    ### BTC ###
    b1 = 0
    b2 = 0
    #for xb in list_wait_sell:
    #    b1 +=  (xb['amount'] * xb['price'])
    for xs in list_sell_profit:
        b2 +=  (xs['amount'] * xs['price'])
    btc_actual = w_long['BTC']['total'] + b2
    btc_pnl = btc_actual - btc_start

    #btc_dispo = w_long['BTC']['total']
    btc_dispo_from_start = btc_start - b2
        

    print ("Prix ETH/BTC:", p['asks'][0][0])

    print ("Wallet ETH:",w_short['ETH']['total'])
    print ("Wallet BTC:",w_long['BTC']['total'])
    print (" #### ETH #### ")
    print ("ETH PNL: ", eth_pnl)
    print ("ETH Actual: ", eth_actual)
    print ("ETH Start: ", eth_start)
    print ("Price next pnl short:", list_buy_profit[0]['price'])
    print ("ETH Disponible from start: ", eth_dispo_from_start)
    print (" #### BTC #### ")
    print ("BTC PNL: ", btc_pnl)
    print ("BTC actual: ", btc_actual)
    print ("BTC Start: ", btc_start)
    print ("Price next pnl long:", list_sell_profit[0]['price'])
    print ("BTC Disponible from start: ", btc_dispo_from_start)
    print (" #### Conclusions #### ")
    
    total_actual_pnl_btc = btc_pnl + (eth_pnl * p['asks'][0][0])
    print ("Total Actual PNL en BTC: ", total_actual_pnl_btc) 
    #p_null_theorique= (-btc_pnl) / (eth_pnl)

    #wallet_now_btc = w['BTC']['total'] + (w['ETH']['total'] * p['bids'][0][0])
    #diff_now_wallet = wallet_now_btc - Total_Start_btc
    #print ("Wallet actual BTC: ", wallet_now_btc)
    #print ("Wallet start BTC: ", Total_Start_btc)
    #print ("Difference wallet actual - start wallet : ", diff_now_wallet )
    #p_null_now_theorique = (Total_Start_btc - w['BTC']['total']) / w['ETH']['total']
    
    print ("--------- End round ---------")
    time.sleep(60)