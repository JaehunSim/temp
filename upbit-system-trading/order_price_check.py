import pyupbit

ACCESSKEY = "your_key"
SECRETKEY = "your_key"
upbit = pyupbit.Upbit(ACCESSKEY, SECRETKEY)
EOS_INITIAL_PRICE = 3500
EOS_DESTINATION_PRICE = 6500
CASH_RATIO_AT_DESTINATION = 0.8
SELL_OFFSET = 0
BUY_OFFSET = 0
LEAST_ORDER_PRICE = 1500
WATCH_INTERVAL = 30
ORDER_INTERVAL = 480
PRICE_CHANGE_LIMIT = 0.003
TOTAL_BALANCE = 800000
PRICE_OFFSET = 20
EOS_CURRENT_PRICE = 4460 + PRICE_OFFSET
EOS_CURRENT_BALANCE = 162.1
TICKER = "EOS"

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

def do_sell_order(target_ticker, eos_current_price, eos_balance_diff):
    target_sell_price = int(round(eos_current_price*(1+SELL_OFFSET), -1))
    eos_balance_diff = abs(eos_balance_diff)
    result = upbit.sell_limit_order(target_ticker, target_sell_price, eos_balance_diff)
    print(f"sell order requested for {eos_balance_diff} amount of {target_ticker} at {target_sell_price}")
    uuid = result[0]["uuid"]
    return uuid

def do_buy_order(target_ticker, eos_current_price, eos_balance_diff):
    target_buy_price = int(round(eos_current_price*(1-BUY_OFFSET), -1))
    eos_balance_diff = abs(eos_balance_diff)
    result = upbit.buy_limit_order(target_ticker, target_buy_price, eos_balance_diff)
    print(f"buy order requested for {eos_balance_diff} amount of {target_ticker} at {target_buy_price}")
    uuid = result[0]["uuid"]
    return uuid

def get_essentials():
    cash_ratio = (EOS_CURRENT_PRICE - EOS_INITIAL_PRICE)/(EOS_DESTINATION_PRICE - EOS_INITIAL_PRICE)*CASH_RATIO_AT_DESTINATION
    eos_ratio = 1 - cash_ratio
    eos_target_price = eos_ratio*TOTAL_BALANCE
    eos_target_balance = eos_target_price/EOS_CURRENT_PRICE
    eos_balance_diff = round(eos_target_balance - EOS_CURRENT_BALANCE, 3)
    order_price = abs(eos_balance_diff*EOS_CURRENT_PRICE)
    return eos_balance_diff, order_price

def get_order_price():
    eos_initial_price = 4200
    eos_destination_price = 4800
    total_balance = get_total_balance()
    eos_current_price = pyupbit.get_current_price("KRW-EOS")
    eos_current_price = 4580
    cash_ratio = (eos_current_price - eos_initial_price)/(eos_destination_price - eos_initial_price)*CASH_RATIO_AT_DESTINATION
    eos_ratio = 1 - cash_ratio
    eos_target_price = eos_ratio*total_balance
    eos_target_balance = eos_target_price/eos_current_price
    eos_current_balance = upbit.get_balance(ticker="EOS")
    eos_balance_diff = round(eos_target_balance - eos_current_balance, 3)
    order_price = abs(eos_balance_diff*eos_current_price)
    return eos_current_price, order_price, eos_balance_diff

def check_price_change(pre_price):
    price_changed = False
    current_price = get_current_price(TICKER)
    if PRICE_CHANGE_LIMIT < abs((current_price - pre_price) / pre_price):
        price_changed = True
    return price_changed

def get_current_price(ticker):
    target_ticker = "KRW-"+ ticker
    eos_current_price = pyupbit.get_current_price(target_ticker)
    return eos_current_price

coin_current_price = get_current_price(TICKER)
coin_current_price = 300
coin_balance_diff = get_balance_diff(coin_current_price)
order_price = abs(coin_balance_diff*coin_current_price)
# essentials = get_essentials()
eos_current_price,  order_price, eos_balance_diff = get_order_price()
price_changed = check_price_change(4500)
