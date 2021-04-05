from trade import get_cash_ratio
from trade import get_balance_diff
from trade import get_total_balance
from trade import check_price_change
from trade import get_price, TICKER

def test():
    coin_current_price = 2.645
    coin_pre_price = 2.6439
    coin_current_price = get_price(TICKER+"USDT")
    price_changed = check_price_change(coin_pre_price)
    cash_ratio = get_cash_ratio(coin_current_price)
    coin_balance_diff = get_balance_diff(coin_current_price)
    order_price = abs(coin_balance_diff*coin_current_price)
    total_balance = get_total_balance()
