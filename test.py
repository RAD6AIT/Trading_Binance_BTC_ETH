import os
from binance.client import Client
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt

# Clés API Binance
api_key = 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9'
api_secret = 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'

# Initialisation du client Binance
client = Client(api_key, api_secret)

# Récupération des données historiques
symbol = 'ETHBTC'
interval = Client.KLINE_INTERVAL_1MINUTE
limit = 5000  # Limite de données à récupérer
klines = client.get_historical_klines(symbol, interval, '1 day ago UTC')

# Conversion des données en DataFrame
data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
data.set_index('timestamp', inplace=True)
data = data.astype(float)

# Calcul du Supertrend
data.ta.supertrend(close='close', length=10, multiplier=3, append=True)
print(data.columns)

# Affichage des résultats
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['close'], label='Prix de clôture')
#plt.plot(data.index, data['SUPERT_7_3.0'], label='Supertrend', linestyle='dotted', color='red')
#plt.plot(data.index, data['SUPERTd_7_3.0'], label='Supertrend Direction', linestyle='dotted', color='green')
plt.plot(data.index, data['SUPERTl_10_3.0'], label='Supertrend long', linestyle='dotted', color='green')
plt.plot(data.index, data['SUPERTs_10_3.0'], label='Supertrend short', linestyle='dotted', color='red')
plt.title('Supertrend - ETH/BTC 1 minute')
plt.xlabel('Temps')
plt.ylabel('Prix')
plt.legend()
plt.grid(True)
plt.show()