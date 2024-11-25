
import numpy as np
import ccxt
import time
import pandas as pd
import copy 
from decimal import Decimal as D
from decimal import ROUND_HALF_UP, ROUND_HALF_DOWN
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
binance_long = ccxt.binance({'apiKey': 'Q6zHYbYaxZB0fZlyaWxava5z7Kib3jQwWMLeoPlwbNFBZareuRivvfR0gtcnGnaw', 'secret': 'eAKILX3y8INA5vij9piQ1IShty4FR754xboZ7cUH5clyRwmVtbi3KjegD0bu78DU'})
binance_short = ccxt.binance({'apiKey': '37fo4lAJ89ldUUvkivMqdsEc48oJ6WO88KBNzPyARlmBi4RsKre8l20IWz6fIzOg', 'secret': 'y2yI9eYI4tKJjq065J3dY3YO7CHUmW3YghH0imhC6TXJiTal28SskkD79FQNytdD'})

#deribit_markets = deribit.load_markets()
binance_markets = binance.load_markets()
binance_markets_long = binance_long.load_markets()
binance_markets_short = binance_short.load_markets()

#client = Client('2pzcSvkiSYf1n36JbjK7aceGucmyk3CIXKKgz6PMYZxJ3MAe3IVcDrwy0qnmlLLq', 'whR3Ti7zCF5uphZtIAGvvZVjyWIBH8z5UEaY7SHg3zZsHi6P3OugIQrk7UXZzvkK')
client = Client('Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9','JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5')
client_long = Client('Q6zHYbYaxZB0fZlyaWxava5z7Kib3jQwWMLeoPlwbNFBZareuRivvfR0gtcnGnaw','eAKILX3y8INA5vij9piQ1IShty4FR754xboZ7cUH5clyRwmVtbi3KjegD0bu78DU')
client_short = Client('37fo4lAJ89ldUUvkivMqdsEc48oJ6WO88KBNzPyARlmBi4RsKre8l20IWz6fIzOg','y2yI9eYI4tKJjq065J3dY3YO7CHUmW3YghH0imhC6TXJiTal28SskkD79FQNytdD')




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

amount = D('0.0008')
min_wallet_amount = D("17")
gain = 0.0035
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

transfert_allowed = False
transfert_eth_long_to_short = D("0")
transfert_btc_short_to_long = D("0")


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
        df = pd.DataFrame(columns=['TIMESTAMP', 'AMOUNT', 'PRICE', 'SIDE','ORDERID','LIST', 'OFFLOAD', 'ORDERSRCID', 'S_PRICE', 'B_PRICE', 'TRANSFERT', 'BTC_TRANSFERED', 'ETH_TRANSFERED','HAS_PROFIT_ORDER'])
        i = 0
        for t in list1:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["WAIT_SELL"] + ["False"] + ["0"] + [t['s_price']] + ["0"] + [t['transfert']] + [t['btc_transfered']] + [t['eth_transfered']] + [t['has_profit_order']]
            i += 1
        for t in list2:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["WAIT_BUY"] + ["False"] + ["0"] + ["0"] + [t['b_price']] +  [t['transfert']] + [t['btc_transfered']] + [t['eth_transfered']] + [t['has_profit_order']]
            i += 1
        for t in list3:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["SELL_PROFIT"] + [t['OFFLOAD']] + [t['src_id']] + ["0"] + ["0"] + ["False"] + ["0"] + ["0"] + ["True"]
            i += 1
        for t in list4:
            df.loc[i] = [t['timestamp']] + [t['amount']] + [t['price']] + [t['side']] + [t['id']] + ["BUY_PROFIT"] + [t['OFFLOAD']] + [t['src_id']] + ["0"] + ["0"] + ["False"] + ["0"] + ["0"] + ["True"]
            i += 1    
        df = df[['TIMESTAMP', 'AMOUNT', 'PRICE', 'SIDE','ORDERID','LIST', 'OFFLOAD','ORDERSRCID','S_PRICE', 'B_PRICE','TRANSFERT', 'BTC_TRANSFERED', 'ETH_TRANSFERED','HAS_PROFIT_ORDER']]
        df.to_csv('TradeOpen.csv')

#def exportTransfertCSV():
#    df = pd.DataFrame(columns=['TIMESTAMP','TRANSFERT_ETH_LONG_TO_SHORT','TRANSFERT_BTC_SHORT_TO_LONG'])
#    
#    df.loc[0]['TIMESTAMP'] = client.get_server_time()['serverTime']
#    df.loc[0]['TIMESTAMP'] = transfert_eth_long_to_short
#    df.loc[0]['TIMESTAMP'] = transfert_btc_short_to_long
#    df = df[['TIMESTAMP','TRANSFERT_ETH_LONG_TO_SHORT','TRANSFERT_BTC_SHORT_TO_LONG']]
#    df.to_csv('TransfertsWallet.csv')

#def importTransfertCSV():
#    try:
#        df = pd.read_csv('TransfertsWallet.csv')
#    except IOError:
#        return  
#    try:
#            transfert_eth_long_to_short = df.iloc[-1]['TRANSFERT_ETH_LONG_TO_SHORT']
#            transfert_btc_short_to_long = df.iloc[-1]['TRANSFERT_BTC_SHORT_TO_LONG']
#    except :
#        return

    

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
                order_tmp ['s_price'] = df.iloc[i]['S_PRICE']
                order_tmp ['transfert'] = df.iloc[i]['TRANSFERT']
                order_tmp ['btc_transfered'] = df.iloc[i]['BTC_TRANSFERED']
                order_tmp ['eth_transfered'] = df.iloc[i]['ETH_TRANSFERED']
                order_tmp ['has_profit_order'] = df.iloc[i]['HAS_PROFIT_ORDER']
                if order_tmp ['has_profit_order'] == True :
                    short_set.add(D(str(df.iloc[i]['S_PRICE'])))
                list_wait_sell.append(order_tmp)                

            elif df.iloc[i]['LIST'] == "WAIT_BUY" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = df.iloc[i]['AMOUNT']
                order_tmp ['price'] = df.iloc[i]['PRICE']
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                order_tmp ['b_price'] = df.iloc[i]['B_PRICE']
                order_tmp ['transfert'] = df.iloc[i]['TRANSFERT']
                order_tmp ['btc_transfered'] = df.iloc[i]['BTC_TRANSFERED']
                order_tmp ['eth_transfered'] = df.iloc[i]['ETH_TRANSFERED']
                order_tmp ['has_profit_order'] = df.iloc[i]['HAS_PROFIT_ORDER']
                if order_tmp ['has_profit_order'] == True :
                    long_set.add(D(str(df.iloc[i]['B_PRICE'])))
                list_wait_buy.append(order_tmp)
                
                
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

def inload(w_long,w_short,eth_btc_ask, eth_btc_bid, inload_sell, inload_buy):
    sell_price = GetSellPrice(D(str(eth_btc_ask)))
    if (w_long['ETH']['free'] >= 0.002):
        for sell_order_profit in list_sell_profit:
            p = D(str(sell_order_profit['price']))
            transfered = False
            for o in list_wait_buy:
                if o['id'] == sell_order_profit['src_id']:
                    if o['transfert'] == True:
                        transfered = True
            if ((p <= (sell_price + inload_step)) and sell_order_profit['OFFLOAD'] == True):
                try:
                    sell_order_price = D(str(sell_order_profit['price']))
                    if  sell_order_price < sell_price:
                        o = binance_long.create_market_order('ETH/BTC', 'sell', sell_order_profit['amount'])
                    else:
                        o = binance_long.create_order('ETH/BTC', 'limit', 'sell', sell_order_profit['amount'], sell_order_profit['price'])
                    sell_order_profit['id'] = o['id']
                    sell_order_profit['OFFLOAD'] = False
                    print ("inload sell_order_profit")
                    inload_sell = inload_sell + 1
                except Exception as e:
                    print ("exception inload sell_order_profit")
                    print (e)
                    #break
    
    buy_price = GetBuyPrice(D(str(eth_btc_bid)))
    if (w_short['BTC']['free'] >= 0.0001):
        #n = w['BTC']['free']  / 0.0001
        for buy_order_profit in list_buy_profit:
            transfered = False
            for o in list_wait_sell:
                if o['id'] == buy_order_profit['src_id']:
                    if o['transfert'] == True:
                        transfered = True
            if ((D(str(buy_order_profit['price'])) >= buy_price - inload_step) and buy_order_profit['OFFLOAD'] == True):
                try:
                    buy_order_price = D(str(buy_order_profit['price']))
                    if  buy_order_price  > buy_price:
                        o = binance_short.create_market_order('ETH/BTC', 'buy', buy_order_profit['amount'])
                    else:
                        o = binance_short.create_order('ETH/BTC', 'limit', 'buy', buy_order_profit['amount'], buy_order_profit['price'])
                    buy_order_profit['id'] = o['id']
                    buy_order_profit['OFFLOAD'] = False
                    print ("inload buy_order_profit")
                    inload_buy = inload_buy +1
                except  Exception as e:
                    print ("exception inload buy_order_profit")
                    print (e)
                  
def offload(eth_btc_ask, eth_btc_bid, inload_sell, inload_buy):
    #print ("### OFFLOAD ###")
    sell_price = GetSellPrice(D(str(eth_btc_ask)))
    for sell_order_profit in list_sell_profit:
        if ((D(str(sell_order_profit['price'])) > sell_price + offload_step)):
            if (sell_order_profit['OFFLOAD'] == False):
                try:
                    binance_long.cancel_order(sell_order_profit['id'],'ETH/BTC')
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
                    binance_short.cancel_order(buy_order_profit['id'],'ETH/BTC')
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

def supertrend_all_times():
    symbol = 'ETHBTC'
    interval_1m = Client.KLINE_INTERVAL_1MINUTE
    interval_5m = Client.KLINE_INTERVAL_5MINUTE
    interval_1h = Client.KLINE_INTERVAL_1HOUR
    interval_4h = Client.KLINE_INTERVAL_4HOUR
    
    klines_1m = client.get_historical_klines(symbol, interval_1m, '1 day ago UTC')
    klines_5m = client.get_historical_klines(symbol, interval_5m, '2 day ago UTC')
    klines_1h = client.get_historical_klines(symbol, interval_1h, '7 day ago UTC')
    klines_4h = client.get_historical_klines(symbol, interval_4h, '14 day ago UTC')
    
    # Conversion des données en DataFrame
    data_1m = pd.DataFrame(klines_1m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data_1m['timestamp'] = pd.to_datetime(data_1m['timestamp'], unit='ms')
    data_1m.set_index('timestamp', inplace=True)
    data_1m = data_1m.astype(float)
    # Calcul du Supertrend 1 min
    data_1m.ta.supertrend(close='close', length=10, multiplier=3, append=True)
    Trend_1m = data_1m['SUPERTd_10_3.0'].iloc[-1]

    # Conversion des données en DataFrame
    data_5m = pd.DataFrame(klines_5m, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data_5m['timestamp'] = pd.to_datetime(data_5m['timestamp'], unit='ms')
    data_5m.set_index('timestamp', inplace=True)
    data_5m = data_5m.astype(float)
    # Calcul du Supertrend 5 min
    data_5m.ta.supertrend(close='close', length=10, multiplier=3, append=True)
    Trend_5m = data_5m['SUPERTd_10_3.0'].iloc[-1]

    # Conversion des données en DataFrame
    data_1h = pd.DataFrame(klines_1h, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data_1h['timestamp'] = pd.to_datetime(data_1h['timestamp'], unit='ms')
    data_1h.set_index('timestamp', inplace=True)
    data_1h = data_1h.astype(float)
    # Calcul du Supertrend 1 heure
    data_1h.ta.supertrend(close='close', length=10, multiplier=3, append=True)
    Trend_1h = data_1h['SUPERTd_10_3.0'].iloc[-1]

    # Conversion des données en DataFrame
    data_4h = pd.DataFrame(klines_4h, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data_4h['timestamp'] = pd.to_datetime(data_4h['timestamp'], unit='ms')
    data_4h.set_index('timestamp', inplace=True)
    data_4h = data_4h.astype(float)
    # Calcul du Supertrend 4 heures
    data_4h.ta.supertrend(close='close', length=10, multiplier=3, append=True)
    Trend_4h = data_4h['SUPERTd_10_3.0'].iloc[-1]


    return  Trend_1m, Trend_5m, Trend_1h, Trend_4h


def sanity_check_set(short_set,long_set,list_wait_sell,list_wait_buy):
    short_set_cp = short_set.copy()
    for s in short_set_cp:
        f = False
        for ls in list_wait_sell:
            if s == D(str(ls['s_price'])) and ls['has_profit_order'] == True:
                f = True
        if f == False:
            short_set.remove(s)
            print ("sanity check short remove : ", s)
    long_set_cp = long_set.copy()        
    for b in long_set_cp:
        f = False
        for lb in list_wait_buy:
            if b == D(str(lb['b_price'])) and lb['has_profit_order'] == True:
                f = True
        if f == False:
            long_set.remove(b)
            print ("sanity check buy remove : ", b)



    
    


importCSV()
#importTransfertCSV()

list_buy_profit.sort(key=lambda x: x['price'], reverse=True)
list_sell_profit.sort(key=lambda x: x['price'])



### cancel all orders before starting ###

if (len(list_sell_order) == 0 and  len(list_buy_order) == 0 and len(list_sell_profit) == 0 and len(list_buy_profit) == 0):
    open_orders = binance.fetch_open_orders('ETH/BTC')
    if (len(open_orders) > 0):
        binance.cancel_all_orders('ETH/BTC')
        binance_long.cancel_all_orders('ETH/BTC')
        binance_short.cancel_all_orders('ETH/BTC')
        print ("!!! NO orders in the csv => cancelling all old olders in exchange !!!")

timestamp = 0

#init calcul of transferted
for o in list_wait_sell :
    transfert_btc_short_to_long += D(str(o['btc_transfered']))

for o in list_wait_buy :
    transfert_eth_long_to_short += D(str(o['eth_transfered']))



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

    try:
        w = binance.fetch_balance ()
        w_long = binance_long.fetch_balance ()
        w_short = binance_short.fetch_balance ()
    except:
        continue

    print ("=======REMBOURSEMENT=======")
    try:
        w_long = binance_long.fetch_balance ()
        w_short = binance_short.fetch_balance ()
    except:
        continue
    b_price = GetSellPrice(D(str(eth_btc_ask)))
    s_price = GetBuyPrice(D(str(eth_btc_bid)))
    list_wait_sell_tmp_r = copy.copy(list_wait_sell)
    for s in list_wait_sell_tmp_r:
        if (s['transfert'] == True and s['has_profit_order'] == False):
            t_amount = s['btc_transfered']
            try:
                params={
                "fromEmail" : "algolongeth_virtual@rr5c6nswnoemail.com",
                "toEmail" : "algoshorteth_virtual@7y44jnu5noemail.com",
                "fromAccountType" : "SPOT",
                "toAccountType" : "SPOT",
                "asset" : "BTC",
                "amount" : t_amount
                }
                tr= binance.sapiPostSubAccountUniversalTransfer(params)
            except Exception as e:
                    print ("Exception Remboursement long to short")
                    break
            list_wait_sell.remove(s)
            transfert_btc_short_to_long -=  D(str(t_amount))
            print ("Remboursement BTC from long to short, order short number ", s['id'], " , and amount: ", t_amount, " BTC")
            time.sleep(1)
        elif (s['price'] + (0.005 * s['price']) > s_price and s['transfert'] == True):
            t_amount = s['btc_transfered']
            try:
                params={
                "fromEmail" : "algolongeth_virtual@rr5c6nswnoemail.com",
                "toEmail" : "algoshorteth_virtual@7y44jnu5noemail.com",
                "fromAccountType" : "SPOT",
                "toAccountType" : "SPOT",
                "asset" : "BTC",
                "amount" : t_amount
                }
                tr= binance.sapiPostSubAccountUniversalTransfer(params)
            except Exception as e:
                    print ("Exception Remboursement long to short")
                    break
            s['transfert'] = False
            s['btc_transfered'] = 0
            transfert_btc_short_to_long -=  D(str(t_amount))
            print ("Remboursement BTC from long to short, order short number ", s['id'], " , and amount: ", t_amount, " BTC")
            time.sleep(1)

    list_wait_buy_tmp_r = copy.copy(list_wait_buy)
    for b in list_wait_buy_tmp_r:
        if (b['transfert'] == True and b['has_profit_order'] == False):
            t_amount = b['eth_transfered']
            try:
                params={
                "fromEmail" : "algoshorteth_virtual@7y44jnu5noemail.com",
                "toEmail" : "algolongeth_virtual@rr5c6nswnoemail.com",
                "fromAccountType" : "SPOT",
                "toAccountType" : "SPOT",
                "asset" : "ETH",
                "amount" : t_amount
                }
                tr= binance.sapiPostSubAccountUniversalTransfer(params)
            except Exception as e:
                    print ("Exception Remboursement short to long")
                    break
            list_wait_buy.remove(b)
            transfert_eth_long_to_short -=  D(str(t_amount))
            print ("Remboursement ETH from short to long, order short number ", b['id'], " , and amount: ", t_amount, " ETH")
            time.sleep(1)
        elif (b['price'] - (0.005 * b['price']) < b_price and b['transfert'] == True):
            t_amount = b['eth_transfered']
            try:
                params={
                "fromEmail" : "algoshorteth_virtual@7y44jnu5noemail.com",
                "toEmail" : "algolongeth_virtual@rr5c6nswnoemail.com",
                "fromAccountType" : "SPOT",
                "toAccountType" : "SPOT",
                "asset" : "ETH",
                "amount" : t_amount
                }
                tr= binance.sapiPostSubAccountUniversalTransfer(params)
            except Exception as e:
                    print ("Exception Remboursement short to long")
                    break
            b['transfert'] = False
            b['eth_transfered'] = 0
            transfert_eth_long_to_short -=  D(str(t_amount))
            print ("Remboursement ETH from short to long, order short number ", b['id'], " , and amount: ", t_amount, " ETH")
            time.sleep(1)
        
        
            

    
    exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)
    print ("=======END REMBOURSEMENT=======")

    print ("=======Inload=======")
    inload (w_long,w_short,eth_btc_ask, eth_btc_bid, inload_sell, inload_buy)

    exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)
    print ("=======End Inload=======")

    print ("=======Closer Order=======")
    print ("Closed Order check")
    try:
        closed_orders_long = binance_long.fetch_closed_orders ('ETH/BTC')
        closed_orders_short = binance_short.fetch_closed_orders ('ETH/BTC')
        #open_orders_long = binance.fetch_open_orders('ETH/BTC')
    except:
        print ("Binance Timed OUT call open and close orders")
        continue
    print ("order filled:", len(closed_orders_long) + len(closed_orders_short))
    #print ("order open:", len(open_orders))
    
    for closed_order in closed_orders_long :
        if (closed_order['side'] == 'sell') :
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
                            if o['transfert'] == True:
                                o['has_profit_order'] = False
                            else:
                                list_wait_buy.remove(o)
                            pnl_final_long += (closed_order['price'] - o['price'])*closed_order['amount']
        elif (closed_order['side'] == 'buy') :
            list_buy_order_tmp2 = copy.copy(list_buy_order)
            for order in list_buy_order_tmp2 :
                if closed_order['id'] == order ['id'] :
                    try:
                        order_sell_profit = binance_long.create_order('ETH/BTC', 'limit', 'sell', closed_order['filled'], closed_order['price'] + (closed_order['price'] * gain), {})
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

    for closed_order in closed_orders_short :
        if (closed_order['side'] == 'sell') :
            list_sell_order_tmp2 = copy.copy(list_sell_order)
            for order in list_sell_order_tmp2 :
                if closed_order['id'] == order ['id'] :   
                    #price_gain = closed_order['price'] - (closed_order['price'] * gain)
                    price_gain = ((0.999*closed_order['price'])/(1+gain))*0.999     
                    try:
                        order_buy_profit = binance_short.create_order('ETH/BTC', 'limit', 'buy', (closed_order['cost']/price_gain), price_gain, {})
                        #order_buy_profit = binance_short.create_order('ETH/BTC', 'limit', 'buy', closed_order['filled'], closed_order['price'] - (closed_order['price'] * gain), {})
                    except :
                        print ("SELL ETH FILLED")
                        print ("exception closed order : buy profit")
                        order_buy_profit = {}
                        order_buy_profit['timestamp'] = client.get_server_time()['serverTime']
                        order_buy_profit['amount'] = (closed_order['cost']/price_gain)
                        #order_buy_profit['amount'] = closed_order['filled']
                        order_buy_profit['price'] =  price_gain
                        #order_buy_profit['price'] = closed_order['price'] - (closed_order['price'] * gain)
                        order_buy_profit['side']  = "buy"
                        order_buy_profit['id'] = 0
                        order_buy_profit['OFFLOAD'] = True
                        order_buy_profit['src_id'] = order ['id']
                        order_buy_profit['cost'] =  closed_order['cost']
                        list_buy_profit.append(order_buy_profit)
                        list_sell_order.remove(order)
                        list_wait_sell.append(order)
                        find_order_sell = True
                    else:
                        order_buy_profit['OFFLOAD'] = False
                        order_buy_profit['src_id'] = order ['id']
                        order_buy_profit['cost'] =  closed_order['cost']
                        #order_buy_profit['amount'] = (closed_order['cost']/price_gain)
                        order_buy_profit['amount'] = closed_order['filled']
                        list_buy_profit.append(order_buy_profit)
                        list_sell_order.remove(order)
                        list_wait_sell.append(order)
                        find_order_sell = True
                        last_sell = closed_order['price']
                        print ("SELL ETH FILLED")
                        print ("Add buy profit order")
        elif (closed_order['side'] == 'buy') :
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
                                print ("s_price don't exist in short_set")
                            if o['transfert'] == True:
                                o['has_profit_order'] = False
                            else:    
                                list_wait_sell.remove(o)
                            pnl_final_short += (o['price'] - closed_order['price'])*closed_order['amount']
                            #pnl_final_short += closed_order['amount'] - o['amount']
    print ("=======End Closer Order=======")

    #print ("=======Calcul PNL=======")
    #Total_wallet_long = binance_long.fetch_balance ()
    #Total_wallet_short = binance_short.fetch_balance ()
    #Pnl_btc_ratio = (Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start) - Total_Start
    #print ("Wallet BTC: ",Total_wallet['BTC']['total'])
    #print ("Wallet ETH: ",Total_wallet['ETH']['total'])
    #print ("=======END Calcul PNL=======")
    
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
        Trend, Trend_5m, Trend_1h, Trend_4h = supertrend_all_times()
    except :
        Trend = 0
    if (Trend == 1):
        print ("Trend is LONG")
    elif (Trend == -1):
        print ("Trend is SHORT")
    else:
        print ("ERROR Calcul of Trend")
    print ("=======ENDTrend=======")

    sanity_check_set(short_set,long_set,list_wait_sell,list_wait_buy)

    ##### Long side
    print ("=======Taking LONG=======")
    print ("eth_btc_ask:", eth_btc_ask)
    b_price = GetSellPrice(D(str(eth_btc_ask)))
    print ("b_price: ", b_price)
    if (Trend == 1):
        if b_price in long_set :
            print ("Position Long on b_price is already take")
        else:
            if (Trend == 1 and Trend_5m == 1 and Trend_1h == 1 and Trend_4h == 1):
                a = 2 * amount
            else:
                a = amount
            try:
                b_order = binance_long.create_market_order('ETH/BTC', 'buy', a / b_price)
                #p=D(str(truncate_float(b_order['price'],5)))
                long_set.add(b_price)
                b_order['b_price'] = b_price
                b_order['transfert'] = False
                b_order['btc_transfered'] = 0
                b_order['eth_transfered'] = 0
                b_order['has_profit_order'] = True
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
            if (Trend == -1 and Trend_5m == -1 and Trend_1h == -1 and Trend_4h == -1):
                a = 2 * amount
            else:
                a = amount
            try:
                s_order = binance_short.create_market_order('ETH/BTC', 'sell', a / s_price)
                #p=D(str(truncate_float(s_order['price'],5)))
                short_set.add(s_price)
                s_order['s_price'] = s_price
                s_order['transfert'] = False
                s_order['btc_transfered'] = 0
                s_order['eth_transfered'] = 0
                s_order['has_profit_order'] = True
                list_sell_order.append(s_order)
                print ("Taking Short on s_price:", s_price)
            except :
                print ("exception SHORT market order on s_price")

    exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)

    print ("=======END Taking BUY side=======")
    


    print ("=======TRANSFERTS=======")
    try:
        w_long = binance_long.fetch_balance ()
        w_short = binance_short.fetch_balance ()
    except:
        continue

    if (w_long['BTC']['total'] < amount and w_short['ETH']['total'] < (amount / b_price)):
        transfert_allowed = True
    else:
        transfert_allowed = False
        
    
    if (w_long['BTC']['total'] < amount and Trend == 1 and w_short['BTC']['total'] > (min_wallet_amount * amount) and transfert_allowed == True):
        t_amount = D("0")
        for s in list_wait_sell:
            if (s['price'] + (0.01 * s['price']) < s_price and s['transfert'] == False):
                ## transfert
                #t_amount = D(str(s['price'] * s['amount']))
                t_amount = s['price'] * s['amount']
                try:
                    params={
                    "fromEmail" : "algoshorteth_virtual@7y44jnu5noemail.com",
                    "toEmail" : "algolongeth_virtual@rr5c6nswnoemail.com",
                    "fromAccountType" : "SPOT",
                    "toAccountType" : "SPOT",
                    "asset" : "BTC",
                    "amount" : t_amount
                    }
                    tr= binance.sapiPostSubAccountUniversalTransfer(params)
                except Exception as e:
                    print ("Exception Transfert short to long")
                    break
                s['transfert'] = True
                s['btc_transfered'] = t_amount
                transfert_btc_short_to_long +=  D(str(t_amount))
                print ("Transfert BTC from short to long, order short number ", s['id'], " , and amount: ", t_amount, " BTC")
                time.sleep(1)
                break

    if (w_short['ETH']['total'] < (amount / b_price) and Trend == -1 and w_long['ETH']['total'] > ((min_wallet_amount * amount)/b_price) and transfert_allowed == True):
        t_amount = D("0")
        for b in list_wait_buy:
            if (b['price'] - (0.01 * b['price']) > b_price and b['transfert'] == False):
                ## transfert
                #t_amount = D(str(b['amount']))
                t_amount = b['amount']
                try:
                    params={
                    "fromEmail" : "algolongeth_virtual@rr5c6nswnoemail.com",
                    "toEmail" : "algoshorteth_virtual@7y44jnu5noemail.com",
                    "fromAccountType" : "SPOT",
                    "toAccountType" : "SPOT",
                    "asset" : "ETH",
                    "amount" : t_amount
                    }
                    tr= binance.sapiPostSubAccountUniversalTransfer(params)
                except Exception as e:
                    print ("Exception Transfert long to short")
                    break
                b['transfert'] = True
                b['eth_transfered'] = t_amount
                transfert_eth_long_to_short +=  D(str(t_amount))
                print ("Transfert ETH from long to short, order short number ", b['id'], " , and amount: ", t_amount, " ETH")
                time.sleep(1)
                break
    exportCSV(list_wait_sell,list_wait_buy,list_sell_profit,list_buy_profit)
    print ("=======END TRANSFERTS=======")
    


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
    print ("PNL Waiting Short en BTC: ", pnl_latent_short)
    print ("PNL Waiting Long en BTC: ", pnl_latent_long)

    print ("PNL FINAL Long en BTC:", pnl_final_long)
    print ("PNL FINAL Short en BTC:", pnl_final_short)

    print ("Nb de pnl long:", pnl_buy)
    print ("Nb de pnl short:", pnl_sell)

    print ("Transfert BTC from short to long: ",transfert_btc_short_to_long)
    print ("Transfert ETH from long to short: ",transfert_eth_long_to_short)

    #print ("Total actual BTC with ratio start: ",Total_wallet['BTC']['total'] + Total_wallet['ETH']['total'] * Ratio_Start)
    #print ("PNL BTC from ratio start: ", Pnl_btc_ratio)
   


    list_buy_order_tmp = []
    list_sell_order_tmp = []
    
    list_buy_profit.sort(key=lambda x: x['price'], reverse=True)
    list_sell_profit.sort(key=lambda x: x['price'])
    
    if (inload_sell < 0):
        inload_sell = 0
    if (inload_buy < 0):
        inload_buy = 0

    #exportTransfertCSV()

    print ("=======END ROUND=======")

    

    time.sleep(5)


    n +=1






    
    
