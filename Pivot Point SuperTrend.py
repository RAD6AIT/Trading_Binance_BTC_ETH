import numpy as np
import pandas as pd
from binance.client import Client
from datetime import datetime

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
    atr = tr['true_range'].rolling(prd).mean()
    return atr

def pivot_point_supertrend(prd, atr_factor, atr_period, show_pivot=False, show_label=True, show_cl=False, show_sr=False):
    # Fetch Binance data for ETH/BTC pair at 1-minute interval
    df = fetch_binance_data(symbol='ETHBTC', interval='1m')
    close = df['close']
    
    # Calculate Pivot High/Low
    ph, pl = pivot_high_low(prd, close)
    
    # Draw Pivot Points if "showpivot" is enabled
    if show_pivot:
        ph_indices = ph.dropna().index
        for idx in ph_indices:
            print(f'High Pivot at {idx}')
        pl_indices = pl.dropna().index
        for idx in pl_indices:
            print(f'Low Pivot at {idx}')
    
    # Calculate Center line using pivot points
    center = (ph.combine_first(pl) * 2 + ph.combine_first(pl).shift(1) * 2 + ph.combine_first(pl).shift(2)) / 3
    
    # Upper/Lower bands calculation
    up = center - (atr_factor * atr(atr_period, close))
    dn = center + (atr_factor * atr(atr_period, close))
    
    # Get the trend
    trend = pd.Series(np.zeros_like(close), index=close.index)
    for i in range(1, len(close)):
        if close.iloc[i-1] > up.iloc[i-1]:
            trend.iloc[i] = max(up.iloc[i], trend.iloc[i-1])
        elif close.iloc[i-1] < dn.iloc[i-1]:
            trend.iloc[i] = min(dn.iloc[i], trend.iloc[i-1])
        else:
            trend.iloc[i] = trend.iloc[i-1]
            
    # Plot the trend
    # (Please implement plotting according to your preference)
    
    # Check and plot the signals
    bsignal = (trend == 1) & (trend.shift(1) == -1)
    ssignal = (trend == -1) & (trend.shift(1) == 1)
    # (Please implement plotting according to your preference)
    
    # Get S/R levels using Pivot Points
    resistance = ph.combine_first(pd.Series(dtype=float))
    support = pl.combine_first(pd.Series(dtype=float))
    
    # If enabled then show S/R levels
    if show_sr:
        print("Support Levels:")
        print(support.dropna())
        print("Resistance Levels:")
        print(resistance.dropna())

    # Alerts
    buy_signal = (trend == 1) & (trend.shift(1) == -1)
    sell_signal = (trend == -1) & (trend.shift(1) == 1)
    trend_changed = np.concatenate(([False], np.diff(trend) != 0))
    
    return buy_signal, sell_signal, trend_changed

# Example usage:
prd = 2
atr_factor = 3
atr_period = 10
show_pivot = False
show_label = True
show_cl = False
show_sr = False

buy_signal, sell_signal, trend_changed = pivot_point_supertrend(prd, atr_factor, atr_period, show_pivot, show_label, show_cl, show_sr)

# Get the most recent signal
if buy_signal.any() and sell_signal.any():
    # Check which signal occurred last
    last_buy_timestamp = buy_signal.index[-1]
    last_sell_timestamp = sell_signal.index[-1]

    if last_buy_timestamp > last_sell_timestamp:
        print("Last signal: Buy")
    else:
        print("Last signal: Sell")
elif buy_signal.any():
    print("Last signal: Buy")
elif sell_signal.any():
    print("Last signal: Sell")
else:
    print("No signals detected.")