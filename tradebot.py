import json
import pprint
import talib
import numpy, websocket
from binance.client import Client
from binance.enums import *

API_KEY = 'YOUR_API_KEY'
API_SECRET = "YOUR_API_SECRET"

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.01

closes = []
in_position = False

def binance_order(symbol, side, quantity, order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        order = Client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return True

def check_sell_or_buy(last_rsi):
    global in_position

    if last_rsi > RSI_OVERBOUGHT:
        if in_position:
            print('overbought! sell! sell! sell!')
            in_position = False
            order_status = binance_order(TRADE_SYMBOL, SIDE_SELL, TRADE_QUANTITY)
            if order_status:
                in_position = False
            
        else:
            print('It is overbought, but we don\'t own any. Nothing to do.')

    if last_rsi < RSI_OVERSOLD:
        if in_position:
            print('It is oversold, but you already own it, nothing to do.')
        else:
            print('oversold! buy! buy! buy!')
            in_position = True
            order_status = binance_order(TRADE_SYMBOL, SIDE_SELL, TRADE_QUANTITY)
            if order_status:
                in_position = True

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    print('received message')
    json_message = json.loads(message)
    # pprint.pprint(json_message)
    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']
    if is_candle_closed:
        print('candle closed at {}'.format(close))
        closes.append(float(close))
        print('closes')
        print(closes)
        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print('all rsis calculated so far')
            print(rsi)
            last_rsi = rsi[-1]
            print('the current rsi is {}'.format(last_rsi))
            check_sell_or_buy(last_rsi)
        print('closes')
        print(closes)
        
    
ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()