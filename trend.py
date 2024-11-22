from binance.client import Client
import pandas as pd
import pandas_ta as ta
import time

client = Client('Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9','JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5')

def supertrend():
    symbol = 'ETHBTC'
    interval = Client.KLINE_INTERVAL_1MINUTE
    klines = client.get_historical_klines(symbol, interval, '1 day ago UTC')

    # Conversion des données en DataFrame
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data = data.astype(float)

    # Calcul du Supertrend 1 min
    data.ta.supertrend(close='close', length=10, multiplier=3, append=True)

    return  data['SUPERTd_10_3.0'].iloc[-1]

def supertrend_all_times():
    symbol = 'ETHBTC'
    interval_1m = Client.KLINE_INTERVAL_1MINUTE
    interval_5m = Client.KLINE_INTERVAL_5MINUTE
    interval_1h = Client.KLINE_INTERVAL_1HOUR
    interval_4h = Client.KLINE_INTERVAL_4HOUR
    interval_1w = Client.KLINE_INTERVAL_1WEEK
    
    klines_1m = client.get_historical_klines(symbol, interval_1m, '1 day ago UTC')
    klines_5m = client.get_historical_klines(symbol, interval_5m, '2 day ago UTC')
    klines_1h = client.get_historical_klines(symbol, interval_1h, '7 day ago UTC')
    klines_4h = client.get_historical_klines(symbol, interval_4h, '14 day ago UTC')
    klines_1w = client.get_historical_klines(symbol, interval_1w, '360 day ago UTC')
    
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

    # Conversion des données en DataFrame
    data_1w = pd.DataFrame(klines_1w, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data_1w['timestamp'] = pd.to_datetime(data_1w['timestamp'], unit='ms')
    data_1w.set_index('timestamp', inplace=True)
    data_1w = data_1w.astype(float)
    # Calcul du Supertrend 4 heures
    data_1w.ta.supertrend(close='close', length=10, multiplier=3, append=True)
    Trend_1w = data_1w['SUPERTd_10_3.0'].iloc[-1]



    return  Trend_1m, Trend_5m, Trend_1h, Trend_4h, Trend_1w



while True:
    try:
        t_1m, t_5m, t_1h, t_4h, t_1w = supertrend_all_times()
        print ("Trend 1m: ", t_1m, ", Trend 5m: " , t_5m, ", Trend 1h: ",t_1h, ", Trend 4h: ",t_4h, ", Trend 1w: ", t_1w)
    except :
        print ("Exception")
    
    time.sleep(60)
