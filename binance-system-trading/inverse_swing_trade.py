import time
import winsound

from binance.client import Client

ACCESSKEY = "your_key"
SECRETKEY = "your_key"

def get_price(ticker):
    trades = client.get_recent_trades(symbol=ticker, limit=1)
    price = trades[0]["price"]
    price = float(price)
    return price

client = Client(ACCESSKEY, SECRETKEY)


start_price = 1450
destination_price = 450

# index = 0
# while True:
#     index += 1
#     try:
#         margin_account_assets = client.get_margin_account()["userAssets"]
#         for asset in margin_account_assets:
#             if asset["asset"] == "ETH":
#                 current_lended_balance = float(asset["borrowed"])
#             if asset["asset"] == "USDT":
#                 usdt_balance = float(asset["free"])
#         current_price = get_price("ETHUSDT")
#         total_balance = 98 # (usdt_balance/current_price + current_lended_balance) / 2
#         cash_ratio = (start_price-current_price) / (start_price-destination_price)
#         target_eth_balance = total_balance*cash_ratio
#         target_lended_balance = total_balance - target_eth_balance
#         balance_change_needed_amount = round(current_lended_balance - target_lended_balance, 2)
#         if 3 < abs(balance_change_needed_amount):
#             winsound.Beep(1000, 1000)
#         print(f"current_price: {current_price}, balance_change_needed_amount: {balance_change_needed_amount}. {index}")
#         time.sleep(10)
#     except:
#         time.sleep(5)
#         pass 
    
def sample(current_price):
    margin_account_assets = client.get_margin_account()["userAssets"]
    for asset in margin_account_assets:
        if asset["asset"] == "ETH":
            current_lended_balance = float(asset["borrowed"])
        if asset["asset"] == "USDT":
            usdt_balance = float(asset["free"])
    total_balance = 98 # (usdt_balance/current_price + current_lended_balance) / 2
    cash_ratio = (start_price-current_price) / (start_price-destination_price)
    target_eth_balance = total_balance*cash_ratio
    target_lended_balance = total_balance - target_eth_balance
    balance_change_needed_amount = round(current_lended_balance - target_lended_balance, 2)
    return balance_change_needed_amount 

current_price = 1250
print(sample(current_price))