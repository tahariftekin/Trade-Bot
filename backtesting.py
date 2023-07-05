import talib, numpy
import pandas as pd
import time

RSI_PERIOD = 14
RSI_OVERBOUGHT = 60
RSI_OVERSOLD = 40

closes = []

indexLine = 0
in_position = False

budget = 100
coin_amount = 0

df = pd.read_csv("BTC-2021min.csv")

# for x in range(len(df)-1, 1, -1):
for x in range(1, len(df)-1, 30):
    indexLine = indexLine + 1
    csv_line = df[x: x+1]
    closeVal = float(csv_line['close'])
    closes.append(closeVal)

    if indexLine > RSI_PERIOD:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes, RSI_PERIOD)
        last_rsi = rsi[-1]
        # print('the current rsi is {}'.format(last_rsi))
        
        if last_rsi < RSI_OVERSOLD:
            if in_position:
                continue
            else:
                print('Oversold! buy! buy! buy!', closeVal)
                budget = budget - budget * 0.001
                coin_amount = budget / closeVal
                # print("Coin amount: ", coin_amount)
                # print("-----------------------------------")
                budget = 0
                in_position = True

        if last_rsi > RSI_OVERBOUGHT:
            if in_position:
                print('Overbought! sell! sell! sell!', closeVal)
                budget = coin_amount * closeVal
                coin_amount = 0
                budget = budget - budget * 0.001
                print("Budget: ", budget)
                print("-----------------------------------")
                in_position = False
            else:
                continue
    time.sleep(0.001)
