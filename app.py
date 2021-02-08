import json, config, cbpro
from flask import Flask, request, jsonify, render_template
from binance.client import Client
from binance.enums import *

app = Flask(__name__)

# BINANCE Client 
client = Client(config.API_KEY, config.API_SECRET, tld='us')

# CBPRO Client 
auth_client = cbpro.AuthenticatedClient(config.CB_API_KEY, config.CB_API_SECRET, config.CB_PASSPHRASE)

# BINANCE ORDER 
def binance_order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

# CBPRO ORDER 
def cbpro_order(side, quantity, symbol):
    try:
        print("We are attempting your order")
        order = auth_client.place_market_order(product_id=symbol, side=side, size=quantity)
    except Exception as e:
        print("An except occured - {}".format(e))
        return False

    return order 

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    #print(request.data)
    data = json.loads(request.data)

    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
            "code": "error",
            "message": "Nice try, invalid passphrase"
        }

    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    order_response = cbpro_order(side, quantity, "XLM-USD")

    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
