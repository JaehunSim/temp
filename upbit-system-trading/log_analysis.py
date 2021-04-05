def get_trade_info(list_):
    total_balance = 0
    total_eos_balance = 0
    for order in list_:
        balance, price = order
        total_balance += abs(balance*price)
        total_eos_balance += abs(balance)
    mean_price = total_balance / total_eos_balance
    trade_info = {"mean_price": mean_price,
                  "balance": total_eos_balance}
    return trade_info

def get_buy_sell_list(log):
    log_split = log.split("\n")
    sell_list = []
    buy_list = []
    for line in log_split:
        line_split = line.split()
        balance = float(line_split[4])
        price = float(line_split[9])
        if line.startswith("sell"):
            sell_list.append([balance, price])
        else:
            buy_list.append([balance, price])
    return buy_list, sell_list

log = """sell order made for -0.186 amount of KRW-EOS at 4120
sell order made for -0.183 amount of KRW-EOS at 4140
sell order made for -0.218 amount of KRW-EOS at 4160
sell order made for -0.386 amount of KRW-EOS at 4200
sell order made for -0.364 amount of KRW-EOS at 4230
sell order made for -0.254 amount of KRW-EOS at 4260
buy order made for 0.254 amount of KRW-EOS at 4220
sell order made for -0.145 amount of KRW-EOS at 4250
sell order made for -0.361 amount of KRW-EOS at 4280
sell order made for -0.198 amount of KRW-EOS at 4300
sell order made for -0.162 amount of KRW-EOS at 4320
buy order made for 0.144 amount of KRW-EOS at 4290
buy order made for 0.27 amount of KRW-EOS at 4260
buy order made for 0.162 amount of KRW-EOS at 4250
sell order made for -0.307 amount of KRW-EOS at 4290
buy order made for 0.145 amount of KRW-EOS at 4260
buy order made for 0.162 amount of KRW-EOS at 4250
sell order made for -0.468 amount of KRW-EOS at 4310
sell order made for -0.448 amount of KRW-EOS at 4350
sell order made for -0.16 amount of KRW-EOS at 4370
sell order made for -0.249 amount of KRW-EOS at 4390
buy order made for 0.142 amount of KRW-EOS at 4360
buy order made for 0.213 amount of KRW-EOS at 4340
sell order made for -0.213 amount of KRW-EOS at 4380
buy order made for 0.16 amount of KRW-EOS at 4350
sell order made for -0.213 amount of KRW-EOS at 4380
sell order made for -0.195 amount of KRW-EOS at 4400
sell order made for -0.212 amount of KRW-EOS at 4420
sell order made for -0.247 amount of KRW-EOS at 4450
sell order made for -0.21 amount of KRW-EOS at 4470
buy order made for 0.493 amount of KRW-EOS at 4400
buy order made for 0.229 amount of KRW-EOS at 4380
buy order made for 0.355 amount of KRW-EOS at 4350
buy order made for 0.267 amount of KRW-EOS at 4320
buy order made for 0.161 amount of KRW-EOS at 4310
sell order made for -0.214 amount of KRW-EOS at 4340
sell order made for -0.304 amount of KRW-EOS at 4370
sell order made for -0.159 amount of KRW-EOS at 4390
sell order made for -0.159 amount of KRW-EOS at 4400
sell order made for -0.143 amount of KRW-EOS at 4420
buy order made for 0.196 amount of KRW-EOS at 4380
buy order made for 0.159 amount of KRW-EOS at 4370
buy order made for 0.266 amount of KRW-EOS at 4340
sell order made for -0.16 amount of KRW-EOS at 4370"""

buy_list, sell_list = get_buy_sell_list(log)
del log
buy_trade_info = get_trade_info(buy_list)
sell_trade_info = get_trade_info(sell_list)
