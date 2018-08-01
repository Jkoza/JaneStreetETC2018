from __future__ import print_function

import socket
import json
from order import Order

team_name="FLEX"

# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('test')
	s.connect((exchange_hostname, port))
	return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
	json.dump(obj, exchange)
	exchange.write("\n")

def read_from_exchange(exchange):
	return json.loads(exchange.readline())


# ~~~~~============== Trading ==============~~~~~

def sendHello(exchange):
	write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
	return read_from_exchange(exchange)

def sendAdd(exchange, orderID, stock, direction, price, amount):
	template = {
		"type": "add", 
		"order_id": orderID, 
		"symbol": stock, 
		"dir": direction, 
		"price": price, 
		"size": amount 
	}
	write_to_exchange(exchange, template)
	return Order(direction, orderID, "created", amount, price, stock)


def sendCancel(exchange, orderID):
	template = {
		"type": "cancel", 
		"order_id": orderID
	}

	write_to_exchange(exchange, template)

def sendConvert(exchange, orderID, stock, direction, amount):
	template = {
		"type": "convert", 
		"order_id": orderID, 
		"symbol": stock, 
		"dir": direction, 
		"size": amount
	}

	write_to_exchange(exchange, template)
