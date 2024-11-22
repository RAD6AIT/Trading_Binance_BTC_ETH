
import numpy as np
import ccxt
import time
import pandas as pd
import copy 
from decimal import Decimal as D
from colorama import Fore, Back, Style
from datetime import datetime
from binance.client import Client
import os
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt



#deribit = ccxt.deribit({'apiKey':'KnRn2Xtf', 'secret':'4XT_imh7EkZioJ3PB1VXI2Ak5AlKJwJluW6hO04m_dM'})

### binance testnet
#binance = ccxt.binance({'apiKey':'2pzcSvkiSYf1n36JbjK7aceGucmyk3CIXKKgz6PMYZxJ3MAe3IVcDrwy0qnmlLLq', 'secret':'whR3Ti7zCF5uphZtIAGvvZVjyWIBH8z5UEaY7SHg3zZsHi6P3OugIQrk7UXZzvkK'})
#binance.set_sandbox_mode(True)

### binance production
binance = ccxt.binance({'apiKey': 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9', 'secret': 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'})

#deribit_markets = deribit.load_markets()
binance_markets = binance.load_markets()

client = Client('2pzcSvkiSYf1n36JbjK7aceGucmyk3CIXKKgz6PMYZxJ3MAe3IVcDrwy0qnmlLLq', 'whR3Ti7zCF5uphZtIAGvvZVjyWIBH8z5UEaY7SHg3zZsHi6P3OugIQrk7UXZzvkK')





b = Total_wallet = binance.fetch_balance ()
eth_wallet_zeroday = b['ETH']['free']
btc_wallet_zeroday = b['BTC']['free']


Ratio_Start = 0.0531
master_round = 1
Total_last_round = 0
Total_Start = Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start
#Total_Start =  0.03813032


list_sell_order = []
list_buy_order = []

list_sell_profit = []
list_buy_profit = []

n = 0
pnl_sell = 0
pnl_buy = 0
last_buy = D('0') 
before_last_buy = D('0')
last_sell = D('0')
before_last_sell = D('0')

amount = D('0.0001')
gain = 0.003
depth = D('0.00003')
step = D('0.00001')
offload_step = D('0.00005')
inload_step = D('0.00005') 

limit_eth = 0.37883225 * 0.9
limit_btc = 0.01906911 * 0.9

first = True
last_sell = 0
last_buy = 0

def GetSellPrice(price):
    price_return = D('0')
    if (step == D('0.00005')):
        if ((price / D('0.00005')) % 1 != 0):
                #print ((price / 0.00005) % 1)
                price_str= str(price)
                if (price_str[-1] == '1'):
                    price_return = price  + D('0.00004')
                elif (price_str[-1] == '2'):
                    price_return  = price  + D('0.00003')
                elif (price_str[-1] == '3'):
                    price_return  = price  + D('0.00002')
                elif (price_str[-1] == '4'):
                    price_return  = price  + D('0.00001')
                elif (price_str[-1] == '6'):
                    price_return  = price  + D('0.00004')
                elif (price_str[-1] == '7'):
                    price_return  = price  + D('0.00003')
                elif (price_str[-1] == '8'):
                    price_return  = price  + D('0.00002')
                elif (price_str[-1] == '9'):
                    price_return  = price  + D('0.00001')                
        else:
                price_return  = price
    else:
        price_return  = D(str(price))
    return price_return

def GetBuyPrice(price):
    price_return = D('0')
    if (step == D('0.00005')):
        if ((price/ D('0.00005')) % 1 != 0):
                #print ((price / 0.00005) % 1)
                price_str= str(price)
                if (price_str[-1] == '1'):
                    price_return = price  - D('0.00001')
                elif (price_str[-1] == '2'):
                    price_return  = price  - D('0.00002')
                elif (price_str[-1] == '3'):
                    price_return  = price  - D('0.00003')
                elif (price_str[-1] == '4'):
                    price_return  = price  - D('0.00004')
                elif (price_str[-1] == '6'):
                    price_return  = price  - D('0.00001')
                elif (price_str[-1] == '7'):
                    price_return  = price  - D('0.00002')
                elif (price_str[-1] == '8'):
                    price_return  = price  - D('0.00003')
                elif (price_str[-1] == '9'):
                    price_return  = price  - D(' 0.00004')                
        else:
                price_return = price
    else:
        price_return  = D(str(price))
    return price_return


def exportCSV(list1, list2, list3, list4):
        df = pd.DataFrame(columns=['TIMESTAMP', 'AMOUNT', 'PRICE', 'SIDE','ORDERID','LIST', 'OFFLOAD'])
        i = 0
        for t in list1:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["LIMIT_SELL"] + ["False"]
            i += 1
        for t in list2:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["LIMIT_BUY"] + ["False"]
            i += 1
        for t in list3:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["SELL_PROFIT"] + [t['OFFLOAD']]
            i += 1
        for t in list4:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["BUY_PROFIT"] + [t['OFFLOAD']]
            i += 1    
        df = df[['TIMESTAMP', 'AMOUNT', 'PRICE', 'SIDE','ORDERID','LIST', 'OFFLOAD']]
        df.to_csv('TradeOpen.csv')

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

def sanity_check_delete(open_orders):
    #open_orders = binance.fetch_open_orders('ETH/BTC')
    print ("Sanity Check Delete")
    
    list_sell_order_tmp1 = copy.copy(list_sell_order)
    for order1 in list_sell_order_tmp1 :
        f = False
        for open_order in open_orders :
            if order1 ['id'] == open_order ['id']:
                f = True
        if (f == False):
            print ("Sanity Check: Sell order list removed")
            list_sell_order.remove(order1)
    
    
    list_buy_order_tmp1 = copy.copy(list_buy_order)
    for order2 in list_buy_order_tmp1:
        f = False
        for open_order in open_orders :
            if order2 ['id'] == open_order ['id'] :
                f = True
        if (f == False):
            print ("Sanity Check: Buy order list removed")
            list_buy_order.remove(order2)

    
    list_sell_profit_tmp1 = copy.copy(list_sell_profit)
    for order3 in list_sell_profit_tmp1:
        f = False
        for open_order in open_orders :
            if order3 ['id']  == open_order ['id'] :
                f = True
        if (f == False and order3['OFFLOAD'] == False):
            print ("Sanity Check: Sell order profit removed id ", order3 ['id'], " offload ", order3 ['OFFLOAD'])
            list_sell_profit.remove(order3)
        
    
    
    list_buy_profit_tmp1 = copy.copy(list_buy_profit)
    for order4 in list_buy_profit_tmp1:
        f = False
        for open_order in open_orders :
            if order4 ['id'] == open_order ['id']:
                f = True
        if (f == False and order4['OFFLOAD'] == False):
            print ("Sanity Check: Buy order profit removed id ", order4 ['id'], " offload ", order4 ['OFFLOAD'])
            list_buy_profit.remove(order4)

def sanity_check_add(open_orders):
    print ("Sanity Check ADD")
    for open_order in open_orders :
        f = False
        if open_order['side'] ==  "sell":
            for order_sell in list_sell_order :
                if (order_sell['id'] == open_order['id']):
                    f= True
            for order_sell_profit in list_sell_profit :
                if (order_sell_profit['id'] == open_order['id']):
                    f= True
            if (f == False):
                open_order['OFFLOAD'] = False
                list_sell_profit.append(open_order)
                print ("Sanity Check ADD SELL PROFIT ORDER")
        
        if open_order['side'] ==  "buy":
            for order_buy in list_buy_order :
                if (order_buy['id'] == open_order['id']):
                    f= True
            for order_buy_profit in list_buy_profit :
                if (order_buy_profit['id'] == open_order['id']):
                    f= True
            if (f == False):
                open_order['OFFLOAD'] = False
                list_buy_profit.append(open_order)
                print ("Sanity Check ADD BUY PROFIT ORDER")

def inload(w,eth_btc_ask, eth_btc_bid):
    ## inload
    #print ("### INLOAD ###")
    sell_price = GetSellPrice(D(str(eth_btc_ask)))
    #w = binance.fetch_balance ()
    if (w['ETH']['free'] >= 0.010):
        #n = w['ETH']['free'] / 0.0020
        for sell_order_profit in list_sell_profit:
            if ((D(str(sell_order_profit['price'])) <= sell_price + inload_step) and sell_order_profit['OFFLOAD'] == True):
                try:
                    if (w['ETH']['free'] <= 0.015) :    
                        o = binance.create_order('ETH/BTC', 'limit', 'sell', sell_order_profit['amount'], last_buy + D('0.00005'))
                    else:
                        o = binance.create_order('ETH/BTC', 'limit', 'sell', sell_order_profit['amount'], sell_order_profit['price'])
                        #o = binance.create_order('ETH/BTC', 'limit', 'sell', (amount / sell_price) + amount   , sell_order_profit['price'])
                    sell_order_profit['id'] = o['id']
                    sell_order_profit['OFFLOAD'] = False
                    print ("inload sell_order_profit")
                except Exception as e:
                    print ("exception inload sell_order_profit")
                    print (e)
                    break
    
    buy_price = GetBuyPrice(D(str(eth_btc_bid)))
    if (w['BTC']['free'] >= 0.0005):
        #n = w['BTC']['free']  / 0.0001
        for buy_order_profit in list_buy_profit:
            if ((D(str(buy_order_profit['price'])) >= buy_price - inload_step) and buy_order_profit['OFFLOAD'] == True):
                try:
                    if (w['BTC']['free'] <= 0.00075):
                        o = binance.create_order('ETH/BTC', 'limit', 'buy', (amount / buy_price) + amount , last_sell - D('0.00005'))
                    else:
                        #o = binance.create_order('ETH/BTC', 'limit', 'buy', buy_order_profit['amount'], buy_order_profit['price'])
                        o = binance.create_order('ETH/BTC', 'limit', 'buy', (amount / buy_price) + amount , buy_order_profit['price'])
                    buy_order_profit['id'] = o['id']
                    buy_order_profit['OFFLOAD'] = False
                    print ("inload buy_order_profit")
                        #n -= 1
                except  Exception as e:
                    print ("exception inload buy_order_profit")
                    print (e)
                    #n -= 1
                    break

def offload(eth_btc_ask, eth_btc_bid):
    #print ("### OFFLOAD ###")
    sell_price = GetSellPrice(D(str(eth_btc_ask)))
    for sell_order_profit in list_sell_profit:
        if ((D(str(sell_order_profit['price'])) > sell_price + offload_step)):
            if (sell_order_profit['OFFLOAD'] == False):
                try:
                    binance.cancel_order(sell_order_profit['id'],'ETH/BTC')
                    sell_order_profit['OFFLOAD'] = True
                    print ("offload sell_order_profit")
                except :
                    sell_order_profit['OFFLOAD'] = True
                    print ("exception offload sell_order_profit")

    buy_price = GetBuyPrice(D(str(eth_btc_bid)))
    for buy_order_profit in list_buy_profit:
        if ((D(str(buy_order_profit['price'])) < buy_price - offload_step)):
            if (buy_order_profit['OFFLOAD'] == False):
                try:
                    binance.cancel_order(buy_order_profit['id'],'ETH/BTC')
                    buy_order_profit['OFFLOAD'] = True
                    print ("offload buy_order_profit")
                except :
                    buy_order_profit['OFFLOAD'] = True
                    print ("exception offload buy_order_profit")

def importWallet():
    try:
            df = pd.read_csv('Wallet.csv')
    except IOError:
            return

def supertrend():
    symbol = 'ETHBTC'
    interval = Client.KLINE_INTERVAL_1MINUTE
    klines = client.get_historical_klines(symbol, interval, '1 day ago UTC')

    # Conversion des données en DataFrame
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data = data.astype(float)

    # Calcul du Supertrend
    data.ta.supertrend(close='close', length=10, multiplier=3, append=True)

    return  data['SUPERTd_10_3.0'].iloc[-1]
    
    
    


importCSV()
list_buy_profit.sort(key=lambda x: x['price'], reverse=True)
list_sell_profit.sort(key=lambda x: x['price'])

#importWallet()

### cancel all orders before starting ###

if (len(list_sell_order) == 0 and  len(list_buy_order) == 0 and len(list_sell_profit) == 0 and len(list_buy_profit) == 0):
    open_orders = binance.fetch_open_orders('ETH/BTC')
    if (len(open_orders) > 0):
        binance.cancel_all_orders('ETH/BTC')
        print ("!!! NO orders in the csv => cancelling all old olders in exchange !!!")

timestamp = 0

while True:
    
    sell_price = D('0')
    buy_price = D('0')

    print ("=======new round=======")
    print ("Master round: ", master_round)
    print ("round number: ", n)

    try:
        eth_btc = binance.fetchOrderBook('ETH/BTC')
    except:
        continue
    eth_btc_ask = eth_btc['asks'][0][0]
    eth_btc_bid = eth_btc['bids'][0][0]
    
    w = binance.fetch_balance ()
    print ("=======Inload=======")
    inload (w,eth_btc_ask, eth_btc_bid)

    exportCSV(list_sell_order,list_buy_order,list_sell_profit,list_buy_profit)
    print ("=======End Inload=======")

    print ("=======Closer Order=======")
    print ("Closed Order check")
    try:
        closed_orders = binance.fetch_closed_orders ('ETH/BTC')
        open_orders = binance.fetch_open_orders('ETH/BTC')
    except:
        print ("Binance Timed OUT call open and close orders")
        continue

    print ("order filled:", len(closed_orders))
    print ("order open:", len(open_orders))

    for closed_order in closed_orders :
        
        if (closed_order['side'] == 'sell') :
            find_order_sell = False
            list_sell_order_tmp2 = copy.copy(list_sell_order)
            for order in list_sell_order_tmp2 :
                if closed_order['id'] == order ['id'] :
                    try:
                        order_buy_profit = binance.create_order('ETH/BTC', 'limit', 'buy', closed_order['filled'], closed_order['price'] - (closed_order['price'] * gain), {})
                    except :
                        print ("exception closed order : buy profit")
                        order_buy_profit = {}
                        order_buy_profit['timestamp'] = client.get_server_time()['serverTime']
                        order_buy_profit['amount'] = closed_order['filled']
                        order_buy_profit['price'] = closed_order['price'] - (closed_order['price'] * gain)
                        order_buy_profit['side']  = "buy"
                        order_buy_profit['id'] = 0
                        order_buy_profit['OFFLOAD'] = True
                        list_buy_profit.append(order_buy_profit)
                        list_sell_order.remove(order)
                        find_order_sell = True
                    else:
                        order_buy_profit['OFFLOAD'] = False
                        list_buy_profit.append(order_buy_profit)
                        list_sell_order.remove(order)
                        find_order_sell = True
                        last_sell = closed_order['price']
                        print ("SELL ETH FILLED")
                        print ("Add buy profit order")
                    
            if (find_order_sell == False):
                list_sell_profit_tmp2 = copy.copy(list_sell_profit)
                for order in list_sell_profit_tmp2 :
                    if closed_order['id'] == order ['id'] :
                        list_sell_profit.remove(order)
                        print ("PNL BUY ETH -> SELL ETH")
                        pnl_buy += 1 
            
        elif (closed_order['side'] == 'buy') :
            find_order_buy = False
            list_buy_order_tmp2 = copy.copy(list_buy_order)
            for order in list_buy_order_tmp2 :
                if closed_order['id'] == order ['id'] :
                    try:
                        order_sell_profit = binance.create_order('ETH/BTC', 'limit', 'sell', closed_order['filled'], closed_order['price'] + (closed_order['price'] * gain), {})
                    except :
                        print ("exception closed order : sell profit")
                        order_sell_profit  = {}
                        order_sell_profit ['timestamp'] = client.get_server_time()['serverTime']
                        order_sell_profit ['amount'] = closed_order['filled']
                        order_sell_profit ['price'] = closed_order['price'] + (closed_order['price'] * gain)
                        order_sell_profit ['side']  = "sell"
                        order_sell_profit ['id'] = 0
                        order_sell_profit ['OFFLOAD'] = True
                        list_sell_profit.append(order_sell_profit)
                        list_buy_order.remove(order)
                        find_order_buy = True
                        
                    else:
                        order_sell_profit['OFFLOAD'] = False
                        list_sell_profit.append(order_sell_profit)
                        list_buy_order.remove(order)
                        find_order_buy = True
                        last_buy = closed_order['price']
                        print ("BUY ETH FILLED")
                        print ("Add Sell profit order")

            if (find_order_buy == False):
                list_buy_profit_tmp2 = copy.copy(list_buy_profit)
                for order in list_buy_profit_tmp2 :
                    if closed_order['id'] == order ['id'] :
                        list_buy_profit.remove(order)
                        print ("PNL SELL ETH -> BUY ETH")
                        pnl_sell += 1
    
    print ("=======End Closer Order=======")
    print ("=======Calcul PNL=======")
    Total_wallet = binance.fetch_balance ()
    if (master_round == 1):
        Total_round = (Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start) - Total_Start
    else:
        Total_round = (Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start) - Total_last_round
    print ("Diff PNL from last master round: ",Total_round)
    print ("Total BTC ratio start: ",Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start)
    
    if (Total_round > 0.0001):
        try:
            os.remove('TradeOpen.csv')
            print ("Bravo Gain superieur de 0.0020, remise à zéro de TradeOpen.csv")
            binance.cancel_all_orders('ETH/BTC')
            print ("!!! Cancelling all olders in exchange !!!")
            list_sell_order = []
            list_buy_order = []
            list_sell_profit = []
            list_buy_profit = []
            Total_last_round = Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start
            master_round +=1
            print ("=======END Calcul PNL - Remise à zéro de la boucle et de toutes les variables=======")
            continue
        except:
            print ("exception suppression TradeOpen.csv")
            continue
    print ("=======END Calcul PNL=======")
    
    print ("=======SanityCheck=======")
    if (n == 0) :
        try:
            open_orders = binance.fetch_open_orders('ETH/BTC')                     
            sanity_check_delete(open_orders)
            sanity_check_add(open_orders)
        except:
            continue
    else :
        try:
            open_orders = binance.fetch_open_orders('ETH/BTC')
            if (len(last_closed_orders) == len(closed_orders)):
                sanity_check_delete(open_orders)
            else:
                print ("No sanity check")
        except:
            continue
    exportCSV(list_sell_order,list_buy_order,list_sell_profit,list_buy_profit)
    print ("=======EndSanityCheck=======")

    ## offload
    print ("=======OFFLOAD=======")
    offload(eth_btc_ask, eth_btc_bid)
    
    exportCSV(list_sell_order,list_buy_order,list_sell_profit,list_buy_profit)
    print ("=======EndOFFLOAD=======")

    params={
    "timeInForce": "PO"
    }

    #SuperTrend
    print ("=======SuperTrend=======")
    Trend = supertrend()

    print ("****** Trend ******")
    if (Trend == 1):
        print ("Trend Haussier => on quote le bid(buy)")
    elif (Trend == -1):
        print ("Trend Baissier => on quote le ask(sell)")
    print ("=======EndSuperTrend=======")

    print ("=======Quotation SELL side=======")
    ##### sell side
    print ("eth_btc_ask:", eth_btc_ask)
    sell_price = GetSellPrice(D(str(eth_btc_ask)))
    print ("sell_price: ", sell_price)
    print ("last_sell ", last_sell)
    print ("before_last_sell ", before_last_sell)
    

    ### temporaire
    sell_depth = sell_price +  depth
    
    while (sell_price <= sell_depth):
        
        sell_tag = False
        list_sell_order_tmp3 = copy.copy(list_sell_order)
        for order in list_sell_order_tmp3 :
            ## check if the price is already quoted
            if (sell_price == D(str(order['price']))):
                sell_tag = True
            
            if ((D(str(order['price'])) > sell_depth + depth) or Trend == 1):
                try:
                    binance.cancel_order(order['id'],'ETH/BTC')
                    list_sell_order.remove(order)
                    print ("cancell sell limit order")
                except :
                    print ("exception cancell sell limit order")
                
        #if (sell_tag == False and sell_price != last_sell  and sell_price != before_last_sell and sell_price > D('0.04999'))
        if (sell_tag == False and sell_price > D('0.04999') and w['ETH']['free'] >= 0.0020 and Trend == -1 and sell_price != last_sell  and sell_price != before_last_sell) :
            try:
                order_sell = binance.create_order('ETH/BTC', 'limit', 'sell', (amount / sell_price) + amount , sell_price, params)
                last_sell = sell_price
                before_last_sell = last_sell - step
                list_sell_order.append(order_sell)
                print ("Add sell limit order ", sell_price)
            except :
                print ("exception add sell limit order")
        elif (sell_tag == False and sell_price < D('0.04999') and w['ETH']['free'] >= 0.0020 and Trend == -1 and sell_price != last_sell  and sell_price != before_last_sell):
            if (w['ETH']['free'] > limit_eth):
                try:
                    order_sell = binance.create_order('ETH/BTC', 'limit', 'sell', (amount / sell_price) + amount , sell_price, params)
                    last_sell = sell_price
                    before_last_sell = last_sell - step
                    list_sell_order.append(order_sell)
                    print ("Add sell limit order ", sell_price)
                except :
                    print ("exception add sell limit order")

                

        sell_price = sell_price + step      

    print ("=======END Quotation SELL side=======")
    
    ##### buy side
    print ("=======Quotation BUY side=======")
    print ("eth_btc_bid:", eth_btc_bid)
    buy_price = GetBuyPrice(D(str(eth_btc_bid)))
    print ("buy_price: ", buy_price)
    print ("last_buy ", last_buy)
    print ("before_last_buy ", before_last_buy)

    ### temporaire
    buy_depth = buy_price -  depth
          
    while (buy_price >= buy_depth):
        ## check if the price is already quoted
        buy_tag = False

        list_buy_order_tmp3 = copy.copy(list_buy_order)
        for order in list_buy_order_tmp3 :
            ## check if the price is already quoted

            if (buy_price ==  D(str(order['price']))):
                buy_tag = True
            
            if ((D(str(order['price'])) < buy_depth - depth) or Trend == -1):
                try:
                    binance.cancel_order(order['id'],'ETH/BTC')
                    list_buy_order.remove(order)
                    print ("cancell buy limit order")
                except :
                    print ("exception cancell buy limit order")
                    
                
        #if (buy_tag == False and buy_price != last_buy and buy_price != before_last_buy and buy_price < D('0.06'))         
        if (buy_tag == False and buy_price < D('0.06') and w['BTC']['free'] >= 0.0001 and Trend == 1 and buy_price != last_buy and buy_price != before_last_buy) :
            ## check if the price is already quoted
            ## else push limit order
            try:
                order_buy = binance.create_order('ETH/BTC', 'limit', 'buy', (amount / buy_price) + amount, buy_price, params)
                last_buy = buy_price
                before_last_buy = last_buy + step
                list_buy_order.append(order_buy)
                print ("Add buy limit order ", buy_price)
            except :
                print ("exception add buy limit order ")
                    
        elif (buy_tag == False and buy_price > D('0.06') and w['BTC']['free'] >= 0.0001 and Trend == 1 and buy_price != last_buy and buy_price != before_last_buy):
            if (w['BTC']['free'] > limit_btc):
                try:
                    order_buy = binance.create_order('ETH/BTC', 'limit', 'buy', (amount / buy_price) + amount, buy_price, params)
                    last_buy = buy_price
                    before_last_buy = last_buy + step
                    list_buy_order.append(order_buy)
                    print ("Add buy limit order ", buy_price)
                except :
                    print ("exception add buy limit order ")
            
        ## decrement price
        buy_price = buy_price - step

    exportCSV(list_sell_order,list_buy_order,list_sell_profit,list_buy_profit)
    print ("=======END Quotation BUY side=======")
    print ("=======STATS=======")
    print ("Nombre de sell limite order:",len(list_sell_order))
    print ("Nombre de buy limite order:",len(list_buy_order))
    print ("Nombre de buy profit:",len(list_buy_profit))
    print ("Nombre de sell profit:",len(list_sell_profit))
    print ("Nombre de order:", len(list_sell_order)+len(list_buy_order)+len(list_buy_profit)+len(list_sell_profit))
    print ("PNL Short ETH: ", pnl_sell)
    print ("PNL Long ETH: ", pnl_buy)

    list_buy_order_tmp = []
    list_sell_order_tmp = []
    last_closed_orders = closed_orders
    
    list_buy_profit.sort(key=lambda x: x['price'], reverse=True)
    list_sell_profit.sort(key=lambda x: x['price'])
    
    print ("=======END ROUND=======")
    time.sleep(5)


    n +=1






    
    
