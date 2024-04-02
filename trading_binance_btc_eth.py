import numpy as np
import ccxt
import time
from colorama import Fore, Back, Style


deribit = ccxt.deribit({'apiKey':'KnRn2Xtf', 'secret':'4XT_imh7EkZioJ3PB1VXI2Ak5AlKJwJluW6hO04m_dM'})
binance = ccxt.binance({'apiKey':'sFjpJ2sBglfFBxKFe8d6hwLmgB1Ri0nQ5OCnQEroOF6VcpKJ0KVEMS5Qn3Ps1FEU', 'secret':'HYr2sMQnsVGvQEZ25IqC0cUUI4H0ko7qvvSRW30OujDSACjH3rXJN07v2GNhfVms'})

deribit_markets = deribit.load_markets()
binance_markets = binance.load_markets()

eth_wallet_zeroday = 0.098901
btc_wallet_zeroday = 0

while True:
    eth_btc = binance.fetch_ticker('ETH/BTC')
    print ("eth_btc bid: "+str(eth_btc['bid']))
    print ("eth_btc ask: "+str(eth_btc['ask']))
    
