class SimuBinance:
    def __init__(self):
        self.historicaldata = []
        self.openorder = []
        self.closedorder = []
        self.index = 0
        self.orderid = 0
        self.wallet_eth = 0
        self.wallet_btc = 0
        self.bid = 0
        self.ask = 0


    def fetch_balance (self):
        r = 
        return r

    def creat_order(self, paire, type, side, amount, price, params = None):
        o = 
        return 0
    
    def create_market_order(self, paire, side, amount, price):
        return 0

    def cancel_order(self, id, paire):
        return 0
    
    def fetch_open_orders(self, paire):
        return 0
    
    def cancel_all_orders(self, paire):
        return 0

    def fetchOrderBook(self, paire):
        return 0
    
    def fetch_balance(self):
        return 0
    
    def fetch_closed_orders(self, paire):
        return 0
    
    def next_iteration(self):
        self.index += 1
        self.bid = self.historicaldata[self.index] - 0.00001
        self.ask = self.historicaldata[self.index]
    
    






binance.fetch_balance ()
o = binance.create_order('ETH/BTC', 'limit', 'sell', sell_order_profit['amount'], sell_order_profit['price'])
o = binance.create_order('ETH/BTC', 'limit', 'buy', (amount / buy_price) + amount , buy_order_profit['price'])
binance.cancel_order(sell_order_profit['id'],'ETH/BTC')
open_orders = binance.fetch_open_orders('ETH/BTC')
binance.cancel_all_orders('ETH/BTC')
eth_btc = binance.fetchOrderBook('ETH/BTC')
w = binance.fetch_balance ()
binance.fetch_closed_orders ('ETH/BTC')
order_buy_profit = binance.create_order('ETH/BTC', 'limit', 'buy', closed_order['filled'], closed_order['price'] - (closed_order['price'] * gain), {})
order_sell_profit = binance.create_order('ETH/BTC', 'limit', 'sell', closed_order['filled'], closed_order['price'] + (closed_order['price'] * gain), {})
b_order = binance.create_market_order('ETH/BTC', 'buy', (amount / b_price) + amount)
s_order = binance.create_market_order('ETH/BTC', 'sell', (amount / b_price) + amount)