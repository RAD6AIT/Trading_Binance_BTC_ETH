import os
from binance.client import Client
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Clés API Binance
api_key = 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9'
api_secret = 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'

# Initialisation du client Binance
client = Client(api_key, api_secret)

# Récupération des données historiques
symbol = 'ETHBTC'
interval = '1m'
limit = 5000  # Limite de données à récupérer
klines = client.get_historical_klines(symbol, interval, '1 day ago UTC')

# Conversion des données en DataFrame
data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
data.set_index('timestamp', inplace=True)
data = data.astype(float)

# Fonction ATR
def atr(data, periods):
    tr1 = np.abs(data['high'] - data['low'])
    tr2 = np.abs(data['high'] - data['close'].shift())
    tr3 = np.abs(data['low'] - data['close'].shift())
    tr = np.max([tr1, tr2, tr3], axis=0)
    return tr.rolling(periods).mean()

# Fonction Supertrend
def supertrend(data, periods, multiplier, change_atr=True):
    atr2 = data['tr'].rolling(periods).mean()
    data['atr'] = atr(data, periods) if change_atr else atr2
    data['up'] = data['close'] - (multiplier * data['atr'])
    data['up'] = np.where(data['close'].shift() > data['up'].shift(), np.maximum(data['up'], data['up'].shift()), data['up'])
    data['dn'] = data['close'] + (multiplier * data['atr'])
    data['dn'] = np.where(data['close'].shift() < data['dn'].shift(), np.minimum(data['dn'], data['dn'].shift()), data['dn'])
    data['trend'] = 1
    data['trend'] = np.where((data['trend'].shift() == -1) & (data['close'] > data['dn'].shift()), 1,
                             np.where((data['trend'].shift() == 1) & (data['close'] < data['up'].shift()), -1, data['trend'].shift()))
    return data

# Paramètres Supertrend
periods = 10
multiplier = 3

# Calcul du Supertrend
data['tr'] = np.abs(data['high'] - data['low'])
data = supertrend(data, periods, multiplier)

# Affichage des résultats
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['close'], label='Prix de clôture')
plt.plot(data.index, data['up'], label='Supertrend Up', linestyle='dotted', color='green')
plt.plot(data.index, data['dn'], label='Supertrend Down', linestyle='dotted', color='red')
plt.title('Supertrend - ETH/BTC 1 minute')
plt.xlabel('Temps')
plt.ylabel('Prix')
plt.legend()
plt.grid(True)
plt.show()
