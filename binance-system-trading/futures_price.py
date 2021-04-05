import pandas as pd

max_price = 0.42
current_balance = 283345
target_price = 0.0025
spread_start_price = 0.02
spread_end_price = 0.12
spread_steps = 25

max_coin_blance = current_balance*2 / max_price
spread_multiplier = round((spread_end_price/spread_start_price)**(1/spread_steps), 5)

target_balance_list = []
spread_list = [round(spread_start_price*spread_multiplier**x, 4) for x in range(spread_steps+1)]
data = pd.DataFrame(spread_list, columns=["spread"])
data["earnings_rate"] = (data["spread"] - target_price) / target_price
data["earnings_rate_recip"] = 1 / data["earnings_rate"]
data["weight"] = data["earnings_rate_recip"]/data["spread"]
data["weight_ratio"] = data["weight"] / data["weight"].sum()
data["spread_balance"] = data["weight_ratio"]/data["weight_ratio"].sum()*max_coin_blance
data["spread_balance_cumulative"] = data["spread_balance"].cumsum()
data["expected_returns"] = data["spread_balance"]*data["earnings_rate"]*data["spread"]
data["expected_returns_cumulative"] = data["expected_returns"].cumsum()

average_entrance_price = data["spread"][6]
current_sell_balance = data["spread_balance_cumulative"][6]
expected_return = (average_entrance_price - target_price) / target_price*current_sell_balance*average_entrance_price

current_sell_balance = 814959
binance_max_price = current_balance*2 / current_sell_balance
binance_average_entrance_price = 0.0286
binance_expected_return = (binance_average_entrance_price - target_price) / target_price*current_sell_balance*average_entrance_price
