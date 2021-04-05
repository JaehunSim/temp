import time
import datetime

import winsound
from binance.client import Client

ACCESSKEY = "your_key"
SECRETKEY = "your_key"

SLEEP_SECONDS = 3
COIN_HIGH = 0.62
COIN_LOW = 0.52
COIN2_HIGH = 24.5
COIN2_LOW = 16
COIN3_HIGH = 0.62
COIN3_LOW = 0.27
COIN4_HIGH = 0.079
COIN4_LOW = 0.070

def repeat_sleep(seconds):
    for i in range(int(seconds*10)):
        time.sleep(0.1)

def get_price(ticker):
    trades = client.get_recent_trades(symbol=ticker, limit=1)
    price = trades[0]["price"]
    price = float(price)
    return price

def make_beep():
    winsound.Beep(1000, 500)

client = Client(ACCESSKEY, SECRETKEY)
TICKER1 = "BATUSDT"
TICKER2 = "UNIUSDT"
TICKER3 = "XRPUSDT"
TICKER4 = "DOGEUSDT"
tickers = [TICKER1]
monitor_price_high_map = {TICKER1: COIN_HIGH,
                          TICKER2: COIN2_HIGH,
                          TICKER3: COIN3_HIGH,
                          TICKER4: COIN4_HIGH}
monitor_price_low_map = {TICKER1: COIN_LOW,
                         TICKER2: COIN2_LOW,
                         TICKER3: COIN3_LOW,
                         TICKER4: COIN4_LOW}

while True:
    print("=============================================================")
    for ticker in tickers:
        price = get_price(ticker)
        monitor_price_low = monitor_price_low_map[ticker]
        monitor_price_high = monitor_price_high_map[ticker] 
        if price <= monitor_price_low or monitor_price_high <= price:
            print(ticker*10)
            make_beep()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ticker} price: {price:.4f}. ({now})")
    print("=============================================================")
    repeat_sleep(SLEEP_SECONDS)
