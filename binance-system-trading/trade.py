import datetime
import time
import winsound
import win32api

from binance.client import Client

ACCESSKEY = "your_key"
SECRETKEY = "your_key"

COIN_INITIAL_PRICE = 2.58
COIN_DESTINATION_PRICE = 3.19
PRICE_LOW_INTERVAL = 5
CASH_RATIO_AT_DESTINATION = 1
SELL_OFFSET = 0.001
BUY_OFFSET = 0.001
WATCH_INTERVAL = 3
ORDER_INTERVAL = 300
TOTAL_WATCH_COUNT = ORDER_INTERVAL//WATCH_INTERVAL
PRICE_CHANGE_LIMIT = 0.01
LEAST_ORDER_BALANCE_RATIO = 0.05
ROUND_DIGIT = 4
TICKER = "EOS"

def make_beep():
    winsound.Beep(1000, 500)

def rebalance():
    coin_current_price, coin_balance_diff = watch()
    if not coin_current_price or not coin_balance_diff:
        return
    order_id = do_transaction(coin_current_price, coin_balance_diff)
    if not order_id:
        return
    cancel_order(coin_current_price, coin_balance_diff, order_id)
    
def watch():
    coin_current_price = None
    coin_balance_diff = None
    while True:
        try:
            coin_current_price = get_price(TICKER+"USDT")
            if coin_current_price < int(round(COIN_INITIAL_PRICE*(1-BUY_OFFSET), -1)):
                time.sleep(PRICE_LOW_INTERVAL)
                coin_current_price, coin_balance_diff = None, None
                break
            coin_balance_diff = get_balance_diff(coin_current_price)
            order_price = abs(coin_balance_diff*coin_current_price)
            least_order_price = get_total_balance()*LEAST_ORDER_BALANCE_RATIO
            if order_price <= least_order_price:
                datetime_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
                target_price = get_target_price(coin_balance_diff, least_order_price)
                print(f"{order_price:.0f} <= {least_order_price:.0f}. {coin_current_price}. target_price:{target_price:.4f} ({datetime_now})")
                if 0.999 <= coin_current_price/target_price <= 1.001:
                    break
                time.sleep(WATCH_INTERVAL)
                coin_current_price, coin_balance_diff = None, None
            break
        except Exception as e:
            print(e)
            print("watch error occured, retrying")
            synce(client)
            time.sleep(0.5)
            pass
    return coin_current_price, coin_balance_diff

def do_transaction(coin_current_price, coin_balance_diff):
    order_id = None
    while True:
        try:
            position = decide_position(coin_balance_diff)
            order_id = position(coin_current_price, coin_balance_diff)
            wait_transaction(coin_current_price)
            break
        except Exception as e:
            print(e)
            print("Do transaction error occured, retrying")
            break
    return order_id
    
def cancel_order(coin_current_price, coin_balance_diff, order_id):
    while True:
        try:
            cancel_order_result = try_cancel_order(TICKER+"USDT", order_id)
            print_when_ordered(coin_current_price, coin_balance_diff, cancel_order_result)
            break
        except:
            print(3)
            pass

def get_target_price(coin_balance_diff, least_order_price):
    start_price = get_price(TICKER+"USDT")
    if coin_balance_diff < 0:
        d_price = start_price*0.001
    else:
        d_price = start_price*0.001*-1
    coin_current_price = start_price
    for step in range(100):
        coin_current_price = coin_current_price+d_price
        coin_balance_diff = get_balance_diff(coin_current_price)
        order_price = abs(coin_balance_diff*coin_current_price)
        if least_order_price <= order_price:
            target_price = coin_current_price
            break
        time.sleep(0.8)
    target_price = round(target_price, ROUND_DIGIT)
    return target_price
    
def get_balance_diff(coin_current_price, ticker=TICKER):
    cash_ratio = get_cash_ratio(coin_current_price)
    coin_ratio = 1 - cash_ratio
    total_balance = get_total_balance()
    coin_target_price = coin_ratio*total_balance
    coin_target_balance = coin_target_price/coin_current_price
    coin_current_balance = get_balance(ticker=ticker)
    if coin_current_balance == None:
        coin_current_balance = 0
    coin_balance_diff = round(coin_target_balance - coin_current_balance, 2)
    return coin_balance_diff

def get_cash_ratio(coin_current_price):
    cash_ratio = (coin_current_price - COIN_INITIAL_PRICE)/(COIN_DESTINATION_PRICE - COIN_INITIAL_PRICE)*CASH_RATIO_AT_DESTINATION
    return cash_ratio

def get_price(ticker):
    trades = client.get_recent_trades(symbol=ticker, limit=1)
    price = trades[0]["price"]
    price = float(price)
    return price

def get_total_balance():
    total_balance = 0
    balances = client.get_account()["balances"]
    for coin in balances:
        asset = coin["asset"]
        free = float(coin["free"])
        locked = float(coin["locked"])
        balance = free + locked
        if asset not in ["USDT"] and balance != 0:
            ticker = asset + "USDT"
            price = float(get_price(ticker))
            total_balance += balance*price
        if asset == "USDT":
            total_balance += balance
    total_balance = round(total_balance, 2)
    return total_balance

def get_balance(ticker):
    balances = client.get_account()["balances"]
    for coin in balances:
        asset = coin["asset"]
        if asset != ticker:
            continue
        free = float(coin["free"])
        locked = float(coin["locked"])
        balance = free + locked
        break
    return balance

def decide_position(coin_balance_diff):
    if coin_balance_diff < 0:
        action = do_sell_order
    else:
        action = do_buy_order
    return action

def do_sell_order(coin_current_price, coin_balance_diff, ticker=TICKER):
    datetime_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    target_ticker = ticker+"USDT"
    target_sell_price = round(coin_current_price*(1+SELL_OFFSET), ROUND_DIGIT)
    coin_balance_diff = abs(coin_balance_diff)
    result = client.order_limit_sell(symbol=target_ticker,
                                     quantity=coin_balance_diff,
                                     price=target_sell_price)
    print(f"sell order requested for {coin_balance_diff} amount of {target_ticker} at {target_sell_price} ({datetime_now})")
    order_id = result["orderId"]
    return order_id

def do_buy_order(coin_current_price, coin_balance_diff, ticker=TICKER):
    datetime_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    target_ticker = ticker+"USDT"
    target_buy_price = round(coin_current_price*(1-BUY_OFFSET), ROUND_DIGIT)
    coin_balance_diff = abs(coin_balance_diff)
    result = client.order_limit_buy(symbol=target_ticker,
                                     quantity=coin_balance_diff,
                                     price=target_buy_price)
    print(f"buy order requested for {coin_balance_diff} amount of {target_ticker} at {target_buy_price} ({datetime_now})")
    order_id = result["orderId"]
    return order_id

def wait_transaction(coin_current_price):
    coin_pre_price = coin_current_price
    while True:
        locked = 0
        for watch_index in range(TOTAL_WATCH_COUNT):
            time.sleep(WATCH_INTERVAL)
            locked = get_maximum_locked()
            if locked == 0:
                break
        if locked == 0:
            break
        price_changed = check_price_change(coin_pre_price)
        if price_changed:
            break
    
def check_price_change(coin_pre_price):
    price_changed = False
    current_price = get_price(TICKER+"USDT")
    if PRICE_CHANGE_LIMIT < abs((current_price - coin_pre_price) / coin_pre_price):
        price_changed = True
    print(f"checking price change... {coin_pre_price} --> {current_price}, price_changed: {price_changed}.")
    return price_changed
    
def get_maximum_locked():
    max_locked = 0
    balances = client.get_account()["balances"]
    for coin in balances:
        if coin["asset"] == "ETHDOWN":
            continue
        locked = float(coin["locked"])
        max_locked = max(max_locked, locked)
    return max_locked

def try_cancel_order(symbol, order_id):
    try:
        result = client.cancel_order(symbol=symbol, orderId=order_id)["status"]
    except:
        result = "error"
    return result

def print_when_ordered(coin_current_price, coin_balance_diff, cancel_order_result, ticker=TICKER):
    target_ticker = ticker+"USDT"
    datetime_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    if "error" in cancel_order_result:
        make_beep()
        if coin_balance_diff < 0:
            target_sell_price = round(coin_current_price*(1+SELL_OFFSET), 4)
            coin_balance_diff = abs(coin_balance_diff)
            print(f"sell order made for {coin_balance_diff} amount of {target_ticker} at {target_sell_price} ({datetime_now})")
        else:
            target_buy_price = round(coin_current_price*(1-BUY_OFFSET), 4)
            print(f"buy order made for {coin_balance_diff} amount of {target_ticker} at {target_buy_price} ({datetime_now})")

def synce(client):
    gt = client.get_server_time()
    tt=time.gmtime(int((gt["serverTime"])/1000))
    win32api.SetSystemTime(tt[0],tt[1],0,tt[2],tt[3],tt[4],tt[5],0)

client = Client(ACCESSKEY, SECRETKEY)
if __name__ == "__main__":
    while True:
        rebalance()
    
