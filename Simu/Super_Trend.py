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

client = Client('2pzcSvkiSYf1n36JbjK7aceGucmyk3CIXKKgz6PMYZxJ3MAe3IVcDrwy0qnmlLLq', 'whR3Ti7zCF5uphZtIAGvvZVjyWIBH8z5UEaY7SHg3zZsHi6P3OugIQrk7UXZzvkK')

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


while True:

    Trend = supertrend()
    if (Trend == 1):
        print ("SuperTrend is LONG")
    if (Trend == -1):
        print ("SuperTrend is SHORT")
    
    time.sleep(5)

