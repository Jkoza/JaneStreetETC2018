from __future__ import print_function
from connection import connect, sendHello, write_to_exchange, read_from_exchange, sendAdd, sendCancel, sendConvert
from time import sleep 
import sys

sys.path.insert(0, '.')
from bank import Bank 
from allStocks import AllStocks
from order import Order
from trade import handleTrade

limits = {
	'BOND' : 100,
	'AAPL' : 100,
	'MSFT' : 100,
	'GOOG' : 100,
	'XLK' : 100,
	'BABZ' : 10,
	'BABA' : 10
}

stocks = ['BOND','AAPL','MSFT','GOOG','XLK','BABZ','BABA']
 			

# ~~~~~============== MAIN LOOP ==============~~~~~

def updateBank(exchange, bank):
	helloResponse = sendHello(exchange)
 	bank.updateStateFromResponse(helloResponse)

def main():
	exchange = connect()
	bank = Bank()
	helloResponse = sendHello(exchange)
	stocksState = AllStocks(helloResponse)
	bank.updateStateFromResponse(helloResponse)
	orderCounter = 1

	while True:
		#sleep(0.1)
		read = read_from_exchange(exchange)
		#if 'symbol' in read and read['symbol'] == 'BOND':
		#	print(read)

		if read['type'] == 'open':
			stocksState.openStocks(read)
		elif read['type'] == 'book':
			stocksState.updateStocks(read)
		elif read['type'] == 'trade':
			# SOMEONE ELSE TRADED DO SOMETHING
			#print("Trade has happened")
			some = 9
		elif read['type'] == 'close':
			stocksState.closeStocks(read)
		elif read['type'] == 'ack':
			orderID = read['order_id']
			if orderID in bank.getOrders():
				order = bank.getOrders()[orderID]
				print("Success " + order.stock + " " + order.orderType + " " + str(order.price)+" "+str(order.quantity))
				order.orderStatus = "success"
		elif read['type'] == 'error' or read['type'] == 'reject':
			print("Got an Error: " + read['error'], file=sys.stderr)
			OrderID = -1
			if read['type'] == 'reject':
				orderID = read['order_id']
			if orderID in bank.getOrders():
				order = bank.getOrders()[orderID]
				print("here is why: " + order.stock)
				order.orderStatus = "cancel"
				sendCancel(exchange, orderID)
		elif read['type'] == 'out':
			orderID=read['order_id']
			if orderID in bank.getOrders():
				order = bank.getOrders()[orderID]
				if order.orderType == "SELL" and order.orderStatus == "cancel":
					bank.deltaQuantity(order.stock, order.quantity)
				bank.deleteOrder(read['order_id'])
		elif read['type'] == 'fill':
			orderID = read['order_id']
			if orderID in bank.getOrders():
				order = bank.getOrders()[orderID]
				print("FILLED " + order.stock + " " + order.orderType + " " + str(order.price)+" "+str(order.quantity))
				order.orderStatus = "fill"
				bank.deltaState(read['dir'], read['price'], read['size'], read['symbol'])

		orderCounter = handleTrade(orderCounter,exchange,stocksState,bank)

if __name__ == "__main__":
	main()

