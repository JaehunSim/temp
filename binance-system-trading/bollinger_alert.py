import datetime
import time

import pandas as pd
import winsound
from binance.client import Client

ACCESSKEY = "your_key"
SECRETKEY = "your_key"
TICKER = "DOGEUSDT"
SLEEP_SECONDS = 3

def make_beep():
    winsound.Beep(1000, 500)

def get_price(ticker):
    trades = client.get_recent_trades(symbol=ticker, limit=1)
    price = trades[0]["price"]
    price = float(price)
    return price

def repeat_sleep(seconds):
    for i in range(int(seconds*10)):
        time.sleep(0.1)
        
def get_candle_data(ticker, candle_interval):
    candles = client.get_klines(symbol=ticker, interval=candle_interval)
    columns = "open_time open high low close volume close_time\
        quote_asset_volumn number_of_trades taker_buy_base_asset_volume taker_buy_quote_asset_volume dummy".split()
    data = pd.DataFrame(candles, columns=columns, dtype=float)
    data["open_time"] = data["open_time"].apply(lambda x: datetime.datetime.fromtimestamp(x//1000))
    data["close_time"] = data["close_time"].apply(lambda x: datetime.datetime.fromtimestamp(x//1000))
    data = data.drop("dummy", axis=1)
    data["average"] = (data["open"] + data["high"] + data["low"] + data["close"]) / 4
    return data
    

def get_bollinger_values(ticker, candle_interval, window_size, std_size):
    data = get_candle_data(ticker, candle_interval)
    rolling_mean = data["average"].rolling(window_size).mean()
    rolling_std = data["average"].rolling(window_size).std()
    data['M'] = rolling_mean
    data['BBL'] = rolling_mean - (rolling_std * std_size)
    data['BBH'] = rolling_mean + (rolling_std * std_size)
    last_row = data.iloc[-1, :]
    bbh = round(last_row["BBH"], 2)
    bbm = round(last_row["M"], 2)
    bbl = round(last_row["BBL"], 2)
    return bbh, bbm, bbl





client = Client(ACCESSKEY, SECRETKEY)

ticker = TICKER
candle_interval = "1h"
window_size = 20
std_size = 2
bbh, bbm, bbl = get_bollinger_values(ticker, candle_interval, window_size, std_size)

repeat_index = 0
while True:
    repeat_index += 1
    if repeat_index % 60 == 0:
        bbh, bbm, bbl = get_bollinger_values(ticker, candle_interval, window_size, std_size)
    print("=============================================================")
    price = get_price(ticker)
    monitor_price_high = bbh
    monitor_price_low = bbl
    if price <= monitor_price_low or monitor_price_high <= price:
        print(ticker*10)
        make_beep()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ticker} price: {price:.4f}. ({now})")
    print("=============================================================")
    repeat_sleep(SLEEP_SECONDS)
