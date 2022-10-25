import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import requests, json
import numpy as np
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

def check_market_data():
    tickers = input("Enter the symbol of the company you would like to analyze: ")
    period = input("Enter the desired period of market data (surround with quotations): ")
    data = yf.download(tickers, period, interval='1m')

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data.index,
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'], name = 'market data'))
    fig_y = fig.update_layout(title='AAPL live share price evolution', yaxis_title='Stock Price (USD per shares)')
    fig_x = fig.update_xaxes(rangeslider_visible = True, 
rangeselector = dict(
        buttons=list([
            dict(count=15, label='15m', step='minute', stepmode='backward'),
            dict(count=45, label='45m', step='minute', stepmode='backward'),
            dict(count=1, label='HTD', step='hour', stepmode='todate'), 
            dict(count=3, label=-'3h', step='hour', stepmode='backward'),
            dict(step='all')
            ])
        )
                             )
    fig.show()
    print(data)

API_KEY = input("Enter your APi key: ")
API_SECRET_KEY = input("Enter your secret key: ")
BASE_URL = 'https://paper-api.alpaca.markets'
ACCOUNT_URL = '{}/v2/account'.format(BASE_URL)
ORDERS_URL = '{}/v2/orders'.format(BASE_URL)
HEADERS = {'APCA-API-KEY-ID':API_KEY, 'APCA-API-SECRET-KEY':API_SECRET_KEY}


def get_account():
    print('')
    print("USER ACCOUNT INFORMATION")
    r = requests.get(ACCOUNT_URL, headers=HEADERS)
    return json.loads(r.content)

account = get_account()
print(account)


def get_orders():
    print('')
    print('USER ORDER HISTORY AND OUTSTANDING ORDERS')
    r=requests.get(ORDERS_URL, headers=HEADERS)
    return json.loads(r.content)
orders = get_orders()
print(orders)

def create_order(symbol, qty, side, type, time_in_force):
    symbol = input("Enter the symbol of the company you would like to buy or sell")
    qty = input("Enter the number of shares")
    side = input("buy or sell?")
    type = input("market or limit")
    time_in_force = input("type gtc")
    data = {
        'symbol':symbol,
        'qty': qty, 
        'side':side,
        'type': type,
        'time_in_force': time_in_force
        }
    r = requests.post(ORDERS_URL, json=data, headers = HEADERS)
    return json.loads(r.content)
response = create_order(symbol, qty, side, type, time_in_force)
print (response)
