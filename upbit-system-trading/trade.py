import datetime
import time

import pyupbit

ACCESSKEY = "your_key"
SECRETKEY = "your_key"
COIN_INITIAL_PRICE = 280
COIN_DESTINATION_PRICE = 360
PRICE_LOW_INTERVAL = 5
CASH_RATIO_AT_DESTINATION = 1
SELL_OFFSET = 0
BUY_OFFSET = 0
WATCH_INTERVAL = 5
ORDER_INTERVAL = 300
TOTAL_WATCH_COUNT = ORDER_INTERVAL//WATCH_INTERVAL
PRICE_CHANGE_LIMIT = 0.005
TICKER = "BAT"

def rebalance():
    while True:
        try:
            coin_current_price = get_current_price(TICKER)
            break
        except:
            pass
    if coin_current_price < int(round(COIN_INITIAL_PRICE*(1-BUY_OFFSET), -1)):
        time.sleep(PRICE_LOW_INTERVAL)
        return
    while True:
        try:
            coin_balance_diff = get_balance_diff(coin_current_price)
            break
        except:
            pass
    order_price = abs(coin_balance_diff*coin_current_price)
    while True:
        try:
            least_order_price = get_total_balance()*0.02
            break
        except:
            pass
    if order_price <= least_order_price:
        time.sleep(WATCH_INTERVAL)
        return
    position = decide_position(coin_balance_diff)
    while True:
        try:
            uuid = position(coin_current_price, coin_balance_diff)
            break
        except:
            pass
    while True:
        try:
            wait_transaction(coin_current_price)
            break
        except:
            pass
    while True:
        try:
            cancel_order = upbit.cancel_order(uuid)[0]
            print_when_ordered(coin_current_price, coin_balance_diff, cancel_order)
            break
        except:
            pass

def get_current_price(ticker):
    target_ticker = "KRW-"+ ticker
    coin_current_price = pyupbit.get_current_price(target_ticker)
    return coin_current_price
    

def get_balance_diff(coin_current_price, ticker=TICKER):
    cash_ratio = (coin_current_price - COIN_INITIAL_PRICE)/(COIN_DESTINATION_PRICE - COIN_INITIAL_PRICE)*CASH_RATIO_AT_DESTINATION
    coin_ratio = 1 - cash_ratio
    total_balance = get_total_balance()
    coin_target_price = coin_ratio*total_balance
    coin_target_balance = coin_target_price/coin_current_price
    coin_current_balance = upbit.get_balance(ticker=ticker)
    if coin_current_balance == None:
        coin_current_balance = 0
    coin_balance_diff = round(coin_target_balance - coin_current_balance, 3)
    return coin_balance_diff

def get_total_balance():
    total_balance = 0
    balances = upbit.get_balances()[0]
    for coin in balances:
        balance = float(coin["balance"])
        price = 1
        currency = coin["currency"]
        if currency not in ["KRW", "SHIFT"]:
            ticker = "KRW-" + currency
            price = pyupbit.get_current_price(ticker=ticker)
        if price:
            total_balance += balance*price
    total_balance = round(total_balance, -2)
    return total_balance

def decide_position(coin_balance_diff):
    if coin_balance_diff < 0:
        action = do_sell_order
    else:
        action = do_buy_order
    return action

def do_sell_order(coin_current_price, coin_balance_diff, ticker=TICKER):
    datetime_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    target_ticker = "KRW-"+ ticker
    target_sell_price = int(round(coin_current_price*(1+SELL_OFFSET)))
    coin_balance_diff = abs(coin_balance_diff)
    result = upbit.sell_limit_order(target_ticker, target_sell_price, coin_balance_diff)
    print(f"sell order requested for {coin_balance_diff} amount of {target_ticker} at {target_sell_price} ({datetime_now})")
    uuid = result[0]["uuid"]
    return uuid

def do_buy_order(coin_current_price, coin_balance_diff, ticker=TICKER):
    datetime_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    target_ticker = "KRW-"+ ticker
    target_buy_price = int(round(coin_current_price*(1-BUY_OFFSET)))
    coin_balance_diff = abs(coin_balance_diff)
    result = upbit.buy_limit_order(target_ticker, target_buy_price, coin_balance_diff)
    print(f"buy order requested for {coin_balance_diff} amount of {target_ticker} at {target_buy_price} ({datetime_now})")
    uuid = result[0]["uuid"]
    return uuid

def wait_transaction(coin_current_price):
    coin_pre_price = coin_current_price
    while True:
        locked = 0
        for watch_index in range(TOTAL_WATCH_COUNT):
            time.sleep(WATCH_INTERVAL)
            locked = get_maximum_locked()
            if locked == 0:
                break
        price_changed = check_price_change(coin_pre_price)
        if price_changed or locked == 0:
            break
    
def check_price_change(pre_price):
    price_changed = False
    current_price = get_current_price(TICKER)
    if PRICE_CHANGE_LIMIT < abs((current_price - pre_price) / pre_price):
        price_changed = True
    return price_changed
    

def get_maximum_locked():
    locked = 0
    balances = upbit.get_balances()[0]
    for balance in balances:
        locked = max(float(balance["locked"]), locked)
    return locked

def print_when_ordered(coin_current_price, coin_balance_diff, cancel_order, ticker=TICKER):
    target_ticker = "KRW-"+ ticker
    datetime_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    if "error" in cancel_order:
        if coin_balance_diff < 0:
            target_sell_price = int(round(coin_current_price*(1+SELL_OFFSET)))
            coin_balance_diff = abs(coin_balance_diff)
            print(f"sell order made for {coin_balance_diff} amount of {target_ticker} at {target_sell_price} ({datetime_now})")
        else:
            target_buy_price = int(round(coin_current_price*(1-BUY_OFFSET)))
            print(f"buy order made for {coin_balance_diff} amount of {target_ticker} at {target_buy_price} ({datetime_now})")

upbit = pyupbit.Upbit(ACCESSKEY, SECRETKEY)
while True:
    rebalance()