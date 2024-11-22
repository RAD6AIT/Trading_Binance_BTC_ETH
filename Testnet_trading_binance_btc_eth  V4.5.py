
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


Ratio_Start = 0.05553
Total_Start = 0.0398181088425
master_round = 1
Total_last_round = 0



list_sell_order = []
list_buy_order = []

list_wait_sell = []
list_wait_buy = []

list_sell_profit = []
list_buy_profit = []

list_long = []
long_set = set(list_long)

list_short = []
short_set = set (list_short)

n = 0
pnl_sell = 0
pnl_buy = 0

amount = D('0.0005')
gain = 0.003
depth = D('0.00003')
step = D('0.00001')
offload_step = D('0.00005')
inload_step = D('0.00005') 


first = True
last_sell = 0
last_buy = 0
inload_sell = 0
inload_buy = 0

pnl_final_long = 0 
pnl_final_short= 0


def truncate_float(float_number, decimal_places):
    multiplier = 10 ** decimal_places
    return int(float_number * multiplier) / multiplier

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
        df = pd.DataFrame(columns=['TIMESTAMP', 'AMOUNT', 'PRICE', 'SIDE','ORDERID','LIST', 'OFFLOAD', 'ORDERSRCID'])
        i = 0
        for t in list1:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["WAIT_SELL"] + ["False"] + ["0"]
            i += 1
        for t in list2:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["WAIT_BUY"] + ["False"] + ["0"]
            i += 1
        for t in list3:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["SELL_PROFIT"] + [t['OFFLOAD']] + [t['src_id']]
            i += 1
        for t in list4:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["BUY_PROFIT"] + [t['OFFLOAD']] + [t['src_id']]
            i += 1    
        df = df[['TIMESTAMP', 'AMOUNT', 'PRICE', 'SIDE','ORDERID','LIST', 'OFFLOAD','ORDERSRCID']]
        df.to_csv('TradeOpen.csv')

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

def inload(w,eth_btc_ask, eth_btc_bid, inload_sell, inload_buy):
    ## inload
    #print ("### INLOAD ###")
    sell_price = GetSellPrice(D(str(eth_btc_ask)))
    #w = binance.fetch_balance ()
    if (w['ETH']['free'] >= 0.010):
        #n = w['ETH']['free'] / 0.0020
        for sell_order_profit in list_sell_profit:
            if ((D(str(sell_order_profit['price'])) <= sell_price + inload_step) and sell_order_profit['OFFLOAD'] == True):
                try:
                    o = binance.create_order('ETH/BTC', 'limit', 'sell', sell_order_profit['amount'], sell_order_profit['price'])
                        #o = binance.create_order('ETH/BTC', 'limit', 'sell', (amount / sell_price) + amount   , sell_order_profit['price'])
                    sell_order_profit['id'] = o['id']
                    sell_order_profit['OFFLOAD'] = False
                    print ("inload sell_order_profit")
                    inload_sell = inload_sell + 1
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
                    #o = binance.create_order('ETH/BTC', 'limit', 'buy', buy_order_profit['amount'], buy_order_profit['price'])
                    o = binance.create_order('ETH/BTC', 'limit', 'buy', (amount / buy_price) + amount , buy_order_profit['price'])
                    buy_order_profit['id'] = o['id']
                    buy_order_profit['OFFLOAD'] = False
                    print ("inload buy_order_profit")
                    inload_buy = inload_buy +1
                except  Exception as e:
                    print ("exception inload buy_order_profit")
                    print (e)
                    #n -= 1
                    break

def offload(eth_btc_ask, eth_btc_bid, inload_sell, inload_buy):
    #print ("### OFFLOAD ###")
    sell_price = GetSellPrice(D(str(eth_btc_ask)))
    for sell_order_profit in list_sell_profit:
        if ((D(str(sell_order_profit['price'])) > sell_price + offload_step)):
            if (sell_order_profit['OFFLOAD'] == False):
                try:
                    binance.cancel_order(sell_order_profit['id'],'ETH/BTC')
                    sell_order_profit['OFFLOAD'] = True
                    print ("offload sell_order_profit")
                    inload_sell = inload_sell - 1
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
                    inload_buy = inload_buy - 1
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
    inload (w,eth_btc_ask, eth_btc_bid, inload_sell, inload_buy)

    exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)
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
                        print ("SELL ETH FILLED")
                        print ("exception closed order : buy profit")
                        order_buy_profit = {}
                        order_buy_profit['timestamp'] = client.get_server_time()['serverTime']
                        order_buy_profit['amount'] = closed_order['filled']
                        order_buy_profit['price'] = closed_order['price'] - (closed_order['price'] * gain)
                        order_buy_profit['side']  = "buy"
                        order_buy_profit['id'] = 0
                        order_buy_profit['OFFLOAD'] = True
                        order_buy_profit['src_id'] = order ['id'] 
                        list_buy_profit.append(order_buy_profit)
                        list_sell_order.remove(order)
                        list_wait_sell.append(order)
                        find_order_sell = True
                    else:
                        order_buy_profit['OFFLOAD'] = False
                        order_buy_profit['src_id'] = order ['id'] 
                        list_buy_profit.append(order_buy_profit)
                        list_sell_order.remove(order)
                        list_wait_sell.append(order)
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
                        list_wait_buy_tmp2 = copy.copy(list_wait_buy)
                        for o in list_wait_buy_tmp2:
                            if o['id'] == order ['src_id']:
                                #long_set.remove(D(str(truncate_float(o['price'],5))))
                                try:
                                    long_set.remove(o['b_price'])
                                except:
                                    print ("b_price don't exist in long_set")
                                list_wait_buy.remove(o)
                                pnl_final_long += (closed_order['price'] - o['price'])*closed_order['amount']
                        
            
        elif (closed_order['side'] == 'buy') :
            find_order_buy = False
            list_buy_order_tmp2 = copy.copy(list_buy_order)
            for order in list_buy_order_tmp2 :
                if closed_order['id'] == order ['id'] :
                    try:
                        order_sell_profit = binance.create_order('ETH/BTC', 'limit', 'sell', closed_order['filled'], closed_order['price'] + (closed_order['price'] * gain), {})
                    except :
                        print ("BUY ETH FILLED")
                        print ("exception closed order : sell profit")
                        order_sell_profit  = {}
                        order_sell_profit ['timestamp'] = client.get_server_time()['serverTime']
                        order_sell_profit ['amount'] = closed_order['filled']
                        order_sell_profit ['price'] = closed_order['price'] + (closed_order['price'] * gain)
                        order_sell_profit ['side']  = "sell"
                        order_sell_profit ['id'] = 0
                        order_sell_profit ['OFFLOAD'] = True
                        order_sell_profit ['src_id'] = order ['id']
                        list_sell_profit.append(order_sell_profit)
                        list_buy_order.remove(order)
                        list_wait_buy.append(order)
                        find_order_buy = True
                        
                    else:
                        order_sell_profit['OFFLOAD'] = False
                        order_sell_profit ['src_id'] = order ['id']
                        list_sell_profit.append(order_sell_profit)
                        list_buy_order.remove(order)
                        list_wait_buy.append(order)
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
                        list_wait_sell_tmp2 = copy.copy(list_wait_sell)
                        for o in list_wait_sell_tmp2:
                            if o['id'] == order ['src_id']:
                                #short_set.remove(D(str(truncate_float(o['price'],5))))
                                try:
                                    short_set.remove(o['s_price'])
                                except:
                                    print ("s_price don't exist in long_set")
                                list_wait_sell.remove(o)
                                pnl_final_short += (o['price'] - closed_order['price'])*closed_order['amount']                      
    print ("=======End Closer Order=======")

    print ("=======Calcul PNL=======")
    Total_wallet = binance.fetch_balance ()
    Pnl_btc_ratio = (Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start) - Total_Start
    print ("Wallet BTC: ",Total_wallet['BTC']['total'])
    print ("Wallet ETH: ",Total_wallet['ETH']['total'])
    print ("=======END Calcul PNL=======")
    
    #print ("=======SanityCheck=======")
    #if (n == 0) :
    #    try:
    #        open_orders = binance.fetch_open_orders('ETH/BTC')                     
    #        sanity_check_delete(open_orders)
    #        sanity_check_add(open_orders)
    #    except:
    #        continue
    #else :
    #    try:
    #        open_orders = binance.fetch_open_orders('ETH/BTC')
    #        if (len(last_closed_orders) == len(closed_orders)):
    #            sanity_check_delete(open_orders)
    #        else:
    #            print ("No sanity check")
    #    except:
    #        continue
    #exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)
    #print ("=======EndSanityCheck=======")

    ## offload

    print ("=======OFFLOAD=======")
    offload(eth_btc_ask, eth_btc_bid, inload_sell, inload_buy)
    
    exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)
    print ("=======EndOFFLOAD=======")

    print ("=======SuperTrend=======")
    try:
        Trend = supertrend()
    except :
        Trend = 0
    if (Trend == 1):
        print ("Trend is LONG")
    elif (Trend == -1):
        print ("Trend is SHORT")
    else:
        print ("ERROR Calcul of Trend")
    print ("=======ENDTrend=======")

    ##### Long side
    print ("=======Taking LONG=======")
    print ("eth_btc_ask:", eth_btc_ask)
    b_price = GetSellPrice(D(str(eth_btc_ask)))
    print ("b_price: ", b_price)
    if (Trend == 1):
        if b_price in long_set :
            print ("Position Long on b_price is already take")
        else:
            try:
                b_order = binance.create_market_order('ETH/BTC', 'buy', (amount / b_price) + amount)
                #p=D(str(truncate_float(b_order['price'],5)))
                long_set.add(b_price)
                b_order['b_price'] = b_price
                list_buy_order.append(b_order)
                print ("Taking Long on b_price:", b_price)
            except :
                print ("exception LONG market order on b_price")
    print ("=======END Taking LONG=======")


    #### Short side
    print ("=======Taking SHORT=======")
    print ("eth_btc_bid:", eth_btc_bid)
    s_price = GetBuyPrice(D(str(eth_btc_bid)))
    print ("s_price: ", s_price)
    if (Trend == -1):
        if s_price in short_set :
            print ("Position Short on s_price is already take")
        else:
            try:
                s_order = binance.create_market_order('ETH/BTC', 'sell', (amount / b_price) + amount)
                #p=D(str(truncate_float(s_order['price'],5)))
                short_set.add(s_price)
                s_order['s_price'] = s_price
                list_sell_order.append(s_order)
                print ("Taking Short on s_price:", s_price)
            except :
                print ("exception SHORT market order on s_price")

    
    print ("=======END Taking BUY side=======")
    exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)

    print ("=======STATS=======")
    #print ("Nombre de sell limite order:",len(list_sell_order))
    #print ("Nombre de buy limite order:",len(list_buy_order))
    print ("Nombre de buy profit:",len(list_buy_profit))
    print ("Nombre de sell profit:",len(list_sell_profit))
    print ("Nombre de order profit:", len(list_buy_profit)+len(list_sell_profit))

    ### calcul pnl:
    pnl_latent_long = 0
    pnl_latent_short= 0
    for b in list_wait_buy:
        pnl_latent_long += (eth_btc_bid - b['price'])*b['amount']
    for s in list_wait_sell:
        pnl_latent_short += (s['price'] - eth_btc_ask)*s['amount']
    print ("PNL Waiting Short: ", pnl_latent_short)
    print ("PNL Waiting Long: ", pnl_latent_long)

    print ("PNL FINAL Long:", pnl_final_long)
    print ("PNL FINAL Short:", pnl_final_short)

    print ("Nb de pnl long:", pnl_buy)
    print ("Nb de pnl short:", pnl_sell)
    
    print ("Total actual BTC with ratio start: ",Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start)
    print ("PNL BTC from ratio start: ", Pnl_btc_ratio)
   


    list_buy_order_tmp = []
    list_sell_order_tmp = []
    last_closed_orders = closed_orders
    
    list_buy_profit.sort(key=lambda x: x['price'], reverse=True)
    list_sell_profit.sort(key=lambda x: x['price'])
    
    if (inload_sell < 0):
        inload_sell = 0
    if (inload_buy < 0):
        inload_buy = 0

    print ("=======END ROUND=======")
    time.sleep(5)


    n +=1






    
    
