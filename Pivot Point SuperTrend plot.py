import numpy as np
import pandas as pd
from binance.client import Client
import matplotlib.pyplot as plt

# Initialize Binance client
api_key = 'Z9XxJxeQHG84eR2xh5A6A9Prt0e1eUsr2AelJjn27yJL0Kis4ynrzUYe0sZlabK9'
api_secret = 'JGDrUkKwKJZvJyVSbyDC7QTVG3Nd2sKJW2LkcQnPGDy9AnHxCSncd44UREDhHyb5'
client = Client(api_key, api_secret)

def fetch_binance_data(symbol, interval):
    klines = client.get_klines(symbol=symbol, interval=interval)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = df['close'].astype(float)
    return df

def pivot_high_low(prd, series):
    high = series.rolling(prd).max()
    low = series.rolling(prd).min()
    return high, low

def atr(prd, series):
    tr = pd.DataFrame(index=series.index)
    tr['hl'] = abs(series - series.shift(1))
    tr['hc'] = abs(series - series.shift(prd))
    tr['lc'] = abs(series.shift(1) - series.shift(prd))
    tr['true_range'] = tr[['hl', 'hc', 'lc']].max(axis=1)
    atr_val = tr['true_range'].rolling(prd).mean()
    return atr_val

def pivot_point_supertrend(prd, atr_factor, atr_period, show_pivot=False, show_sr=False):
    # Fetch Binance data for ETH/BTC pair at 1-minute interval
    df = fetch_binance_data(symbol='ETHBTC', interval='1m')
    close = df['close']
    
    # Calculate Pivot High/Low
    ph, pl = pivot_high_low(prd, close)
    
    # Plot source data
    plt.figure(figsize=(10, 6))
    plt.plot(close.index, close, label='Close Price', color='black')

    # Draw Pivot Points if "showpivot" is enabled
    if show_pivot:
        plt.scatter(ph.index, ph, color='red', marker='^', label='High Pivot')
        plt.scatter(pl.index, pl, color='green', marker='v', label='Low Pivot')
    
    # Calculate Center line using pivot points
    center = (ph.combine_first(pl) * 2 + ph.combine_first(pl).shift(1) * 2 + ph.combine_first(pl).shift(2)) / 3
    
    # Upper/Lower bands calculation
    atr_val = atr(atr_period, close)
    up = center + (atr_factor * atr_val)
    dn = center - (atr_factor * atr_val)
    
    # Plot SuperTrend
    plt.plot(up.index, up, label='Upper Band')
    plt.plot(dn.index, dn, label='Lower Band')
    
    # Get S/R levels using Pivot Points
    resistance = ph.combine_first(pd.Series(dtype=float))
    support = pl.combine_first(pd.Series(dtype=float))
    
    # Plot S/R levels
    if show_sr:
        plt.scatter(support.index, support, color='blue', marker='o', label='Support')
        plt.scatter(resistance.index, resistance, color='orange', marker='o', label='Resistance')

    plt.legend()
    plt.xlabel('Timestamp')
    plt.ylabel('Price')
    plt.title('Pivot Points and SuperTrend Indicator')
    plt.show()

# Example usage:
prd = 2
atr_factor = 3
atr_period = 10
show_pivot = True
show_sr = True

pivot_point_supertrend(prd, atr_factor, atr_period, show_pivot, show_sr)
