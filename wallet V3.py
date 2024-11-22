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

client = Client('Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9','JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5')

eth_start = (D(str(0.40378122)))+(D(str(0.06648184)))
btc_start = (D(str(0.01915878)))+(D(str(0.00078972)))+(D(str(0.00080919))) + (D(str(0.00179633))) + (D(str(0.00188586))) + (D(str(0.00103549))) + (D(str(0.02012208))) + (D(str(0.00102698))) + (D(str(0.00760180)))+(D(str(0.00343089)))+(D(str(0.00153433)))
Ratio_Start = (D(str(0.04803)))

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
                order_tmp ['amount'] = (D(str(df.iloc[i]['AMOUNT'])))
                order_tmp ['price'] = (D(str( df.iloc[i]['PRICE'])))
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                order_tmp ['s_price'] = df.iloc[i]['S_PRICE']
                order_tmp ['transfert'] = df.iloc[i]['TRANSFERT']
                order_tmp ['btc_transfered'] = df.iloc[i]['BTC_TRANSFERED']
                order_tmp ['eth_transfered'] = df.iloc[i]['ETH_TRANSFERED']
                order_tmp ['has_profit_order'] = df.iloc[i]['HAS_PROFIT_ORDER']
                list_wait_sell.append(order_tmp)
                #short_set.add(D(str(order_tmp ['price'])))

            elif df.iloc[i]['LIST'] == "WAIT_BUY" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = (D(str(df.iloc[i]['AMOUNT'])))
                order_tmp ['price'] = (D(str( df.iloc[i]['PRICE'])))
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                order_tmp ['b_price'] = df.iloc[i]['B_PRICE']
                order_tmp ['transfert'] = df.iloc[i]['TRANSFERT']
                order_tmp ['btc_transfered'] = df.iloc[i]['BTC_TRANSFERED']
                order_tmp ['eth_transfered'] = df.iloc[i]['ETH_TRANSFERED']
                order_tmp ['has_profit_order'] = df.iloc[i]['HAS_PROFIT_ORDER']
                list_wait_buy.append(order_tmp)
                #long_set.add(D(str(order_tmp ['price'])))

            elif df.iloc[i]['LIST'] == "SELL_PROFIT" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = (D(str(df.iloc[i]['AMOUNT'])))
                order_tmp ['price'] = (D(str( df.iloc[i]['PRICE'])))
                order_tmp ['side'] = df.iloc[i]['SIDE']
                order_tmp ['id'] = df.iloc[i]['ORDERID']
                order_tmp ['OFFLOAD'] = df.iloc[i]['OFFLOAD']
                order_tmp ['src_id'] = df.iloc[i]['ORDERSRCID']
                list_sell_profit.append(order_tmp)

            elif df.iloc[i]['LIST'] == "BUY_PROFIT" :
                order_tmp ['timestamp'] = df.iloc[i]['TIMESTAMP']
                order_tmp ['amount'] = (D(str(df.iloc[i]['AMOUNT'])))
                order_tmp ['price'] = (D(str( df.iloc[i]['PRICE'])))
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
    
    try:
        w_long = binance_long.fetch_balance ()
        w_short = binance_short.fetch_balance ()
        p = binance.fetchOrderBook('ETH/BTC')
    except:
        continue

    transfert_eth_long_to_short = D("0")
    transfert_btc_short_to_long = D("0")

    for o in list_wait_sell :
        transfert_btc_short_to_long += D(str(o['btc_transfered']))

    for o in list_wait_buy :
        transfert_eth_long_to_short += D(str(o['eth_transfered']))


    ### ETH ###
    e1 = (D(str(0)))
    e2 = (D(str(0)))
    b_eth = (D(str(0)))
    eth_high_sell = (D(str(0)))
    eth_low_sell = (D(str(1)))
    for ws in list_buy_profit:
        e2 +=  ws['amount']
    for wb in list_wait_sell:
        #b_eth += wb['amount']*wb['price'] - ((wb['amount']*wb['price']) * (D(str(0.001))))
        if (wb['has_profit_order'] == True):
            b_eth += wb['amount']*wb['price']
            if (wb['s_price'] > eth_high_sell):
                eth_high_sell = wb['s_price']
            if (wb['s_price'] < eth_low_sell):
                eth_low_sell = wb['s_price']
    
    eth_btc_actual_pnl = (D(str(w_short['BTC']['total']))) - b_eth
    eth_actual = (D(str(w_short['ETH']['total'] )))+ e2
    eth_pnl = eth_actual - eth_start

    #eth_dispo = w_short['ETH']['total']
    eth_dispo_from_start = eth_start - e2
    eth_btc_actual_pnl_avec_emprunt = eth_btc_actual_pnl + transfert_btc_short_to_long
    

    ### BTC ###
    b1 = (D(str(0)))
    b2 = (D(str(0)))
    e_btc = (D(str(0)))
    eth_high_buy = (D(str(0)))
    eth_low_buy = (D(str(1)))
    for xs in list_sell_profit:
        b2 +=  (xs['amount'] * xs['price'])
    for xb in list_wait_buy:
        #e_btc +=  xb['amount'] - (xb['amount'] * (D(str(0.001))))
        if (xb['has_profit_order'] == True):
            e_btc +=  xb['amount']
            if (xb['b_price'] > eth_high_buy):
                eth_high_buy = xb['b_price']
            if (xb['b_price'] < eth_low_buy):
                eth_low_buy = xb['b_price']


    btc_eth_actual_pnl = (D(str(w_long['ETH']['total']))) - e_btc    
    btc_actual = (D(str(w_long['BTC']['total']))) + b2
    btc_pnl = btc_actual - btc_start

    #btc_dispo = w_long['BTC']['total']
    btc_dispo_from_start = btc_start - b2
    btc_eth_actual_pnl_avec_emprunt = btc_eth_actual_pnl + transfert_eth_long_to_short
        

    print ("Prix ETH/BTC:", p['asks'][0][0])

    print ("Wallet Short ETH:",(D(str(w_short['ETH']['total']))))
    print ("Wallet Short BTC:",(D(str(w_short['BTC']['total']))))
    print ("Wallet Long BTC:",(D(str(w_long['BTC']['total']))))
    print ("Wallet Long ETH:",(D(str(w_long['ETH']['total']))))
    print ("Transfert BTC from short to long: ",transfert_btc_short_to_long)
    print ("Transfert ETH from long to short: ",transfert_eth_long_to_short)
    print (" #### ETH #### ")
    print ("ETH PNL: ", eth_pnl)
    print ("ETH PNL moins emprunt: ", eth_pnl - transfert_eth_long_to_short)
    print ("ETH Actual: ", eth_actual)
    print ("ETH Start: ", eth_start)
    try:
        print ("Price next pnl short:", list_buy_profit[0]['price'])
    except:
        print ("Exception next pnl short")
    print ("ETH High Sell: ", eth_high_sell)
    print ("ETH Low Sell: ", eth_low_sell)    
    print ("ETH Disponible from start: ", eth_dispo_from_start)
    print ("PNL BTC dans le wallet ETH short: ", eth_btc_actual_pnl)
    print ("PNL BTC dans le wallet ETH short avec remboursement emprunt du compte LONG: ", eth_btc_actual_pnl_avec_emprunt )
    print (" #### BTC #### ")
    print ("BTC PNL: ", btc_pnl)
    print ("BTC PNL moins emprunt: ", btc_pnl - transfert_btc_short_to_long)
    print ("BTC actual: ", btc_actual)
    print ("BTC Start: ", btc_start)
    try:
        print ("Price next pnl long:", list_sell_profit[0]['price'])
    except:
        print ("Exception next pnl long")
    print ("ETH High Buy: ", eth_high_buy)
    print ("ETH Low Buy: ", eth_low_buy)
    print ("BTC Disponible from start: ", btc_dispo_from_start)
    print ("PNL ETH dans le wallet BTC long: ", btc_eth_actual_pnl)
    print ("PNL ETH dans le wallet BTC long avec remboursement emprunt du compte SHORT: ", btc_eth_actual_pnl_avec_emprunt)
    print (" #### Conclusions #### ")
    total_btc = btc_start + (btc_pnl - transfert_btc_short_to_long) + eth_btc_actual_pnl_avec_emprunt
    total_eth = eth_start + (eth_pnl - transfert_eth_long_to_short) + btc_eth_actual_pnl_avec_emprunt
    print ("BTC total: ", total_btc, ", PNL Total BTC: ", total_btc - btc_start)
    print ("ETH total: ", total_eth, ", PNL Total ETH: ", total_eth - eth_start)
    total_actual_pnl_btc = btc_pnl + (eth_pnl * (D(str(p['asks'][0][0])))) + eth_btc_actual_pnl + (btc_eth_actual_pnl * (D(str(p['asks'][0][0]))))
    print ("Total Actual PNL en BTC (tous les gains inclus): ", total_actual_pnl_btc)
    total_actual_pnl_btc_emprunt = ((eth_pnl - transfert_eth_long_to_short) * (D(str(p['asks'][0][0])))) + eth_btc_actual_pnl_avec_emprunt + (btc_pnl - transfert_btc_short_to_long) + (btc_eth_actual_pnl_avec_emprunt*(D(str(p['asks'][0][0]))))
    print ("Total Actual PNL en BTC (avec calcul emprunt): ", total_actual_pnl_btc_emprunt)
    btc_wallet_start =  btc_start + eth_start * Ratio_Start
    print ("Total Start Wallet en BTC: ",btc_wallet_start)
    btc_wallet_actual = D(str(w_long['BTC']['total'])) + D(str(w_short['BTC']['total'])) + D(str(w_long['ETH']['total'])) * D(str(p['asks'][0][0])) + D(str(w_short['ETH']['total'])) * D(str(p['asks'][0][0]))
    print ("Total Actual Wallet en BTC: ",btc_wallet_actual)
    pnl_wallet = btc_wallet_actual - btc_wallet_start
    print ("Total PNL Wallet en BTC: ",pnl_wallet)
    btc_wallet_actual_ratio_start =  D(str(w_long['BTC']['total'])) + D(str(w_short['BTC']['total'])) + D(str(w_long['ETH']['total'])) * Ratio_Start + D(str(w_short['ETH']['total'])) * Ratio_Start
    print ("Total Actual Wallet en BTC with ratio start: ",btc_wallet_actual_ratio_start)
    pnl_wallet_ratio_start = btc_wallet_actual_ratio_start - btc_wallet_start
    print ("Total PNL Wallet en BTC with ratio start: ",pnl_wallet_ratio_start )
    #p_null_theorique= (-btc_pnl) / (eth_pnl)

    #wallet_now_btc = w['BTC']['total'] + (w['ETH']['total'] * p['bids'][0][0])
    #diff_now_wallet = wallet_now_btc - Total_Start_btc
    #print ("Wallet actual BTC: ", wallet_now_btc)
    #print ("Wallet start BTC: ", Total_Start_btc)
    #print ("Difference wallet actual - start wallet : ", diff_now_wallet )
    #p_null_now_theorique = (Total_Start_btc - w['BTC']['total']) / w['ETH']['total']
    
    print ("--------- End round ---------")

    #df = pd.DataFrame(columns=['TIMESTAMP', 'PRICE', 'Wallet_Short_ETH', 'Wallet_Short_BTC','Wallet_Long_BTC','Wallet_Long_ETH', 'Transfert_BTC_short_to_long', 'Transfert_ETH_long_to_short'])
    #timestamp = client.get_server_time()['serverTime']
    #df.loc[0] = timestamp + p['asks'][0][0] + (D(str(w_short['ETH']['total']))) + (D(str(w_short['BTC']['total']))) + (D(str(w_long['BTC']['total']))) + (D(str(w_long['ETH']['total']))) + transfert_btc_short_to_long + transfert_eth_long_to_short
    #df = df['TIMESTAMP', 'PRICE', 'Wallet_Short_ETH', 'Wallet_Short_BTC','Wallet_Long_BTC','Wallet_Long_ETH', 'Transfert_BTC_short_to_long', 'Transfert_ETH_long_to_short']
    #df.to_csv('wallet_stats.csv',mode='a', header=False, index=False)
    
    time.sleep(60)