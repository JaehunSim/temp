import time
import datetime

import winsound
import pyupbit

from binance.client import Client
from forex_python.converter import CurrencyRates

BINANCE_ACCESSKEY = "your_key"
BINANCE_SECRETKEY = "your_key"

binance_client = Client(BINANCE_ACCESSKEY, BINANCE_SECRETKEY)

SLEEP_SECONDS = 60
COIN_HIGH = 3050
COIN_LOW = 2965
COIN2_HIGH = 14.5
COIN2_LOW = 13.85
COIN3_HIGH = 270
COIN3_LOW = 243
USDKRW = CurrencyRates().get_rates("USD")["KRW"]

def repeat_sleep(seconds):
    for i in range(int(seconds*10)):
        time.sleep(0.1)

def get_price(ticker, broker="upbit"):
    if broker == "upbit":
        target_ticker = "KRW-"+ ticker
        price = pyupbit.get_current_price(target_ticker)
    if broker == "binance":
        target_ticker = ticker + "USDT"
        trades = binance_client.get_recent_trades(symbol=target_ticker, limit=1)
        price = trades[0]["price"]
        price = float(price)
    return price

def make_beep():
    winsound.Beep(1000, 500)

TICKER1 = "EOS"
TICKER2 = "UNIUSDT"
TICKER3 = "AAVEUSDT"
tickers = [TICKER1]
monitor_price_high_map = {TICKER1: COIN_HIGH,
                          TICKER2: COIN2_HIGH,
                          TICKER3: COIN3_HIGH}
monitor_price_low_map = {TICKER1: COIN_LOW,
                         TICKER2: COIN2_LOW,
                         TICKER3: COIN3_LOW}

index = 0
while True:
    index += 1
    if index % 200 == 0:
        USDKRW = CurrencyRates().get_rates("USD")["KRW"]
    print("=============================================================")
    for ticker in tickers:
        upbit_price = get_price(ticker, "upbit")
        binance_price = get_price(ticker, "binance")*USDKRW
        korean_premium = (upbit_price - binance_price) / upbit_price * 100
        monitor_price_low = monitor_price_low_map[ticker]
        monitor_price_high = monitor_price_high_map[ticker] 
        
#        if upbit_price <= monitor_price_low or monitor_price_high <= upbit_price:
#            print(ticker*10)
#            make_beep()
        if korean_premium > 0:
            print(ticker*10)
            make_beep()
            
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ticker} upbit_price: {upbit_price:.0f}. ({now})")
        print(f"{ticker} binance_price: {binance_price:.0f}. ({now})")
        print(f"{ticker} korean_premium: {korean_premium:.3f}%. ({now})")
        with open("korean_premium.txt", "a") as log:
            log.write(f"{korean_premium:.3f} {now}\n")
    print("=============================================================")
    repeat_sleep(SLEEP_SECONDS)
