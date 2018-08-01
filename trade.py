from connection import connect, sendHello, write_to_exchange, read_from_exchange, sendAdd, sendCancel, sendConvert
from time import sleep 
import sys

sys.path.insert(0, '.')
from bank import Bank 
from allStocks import AllStocks
from order import Order

# HANDLING TRDES

def handleTrade(orderCounter, exchange, stocksState, bank):
	money = bank.getUSD()

	#Trade bonds first if possible
	if not bank.existOrder("BOND", "BUY") and money > -29000: 
		bank.addOrder(orderCounter,sendAdd(exchange, orderCounter, 'BOND', 'BUY', 999, 1))
		orderCounter += 1

	bondInfo = stocksState.getStock("BOND")

	if bondInfo['buyHigh'] > 1000 :
		bank.addOrder(orderCounter, sendAdd(exchange, orderCounter, 'BOND', 'SELL', bondInfo['buyHigh'], 1))
		orderCounter += 1
	
	
	status = bank.getState()
	for name in stocksState.getOpen():
		money = bank.getUSD()
		if name != "BOND":
			stock = stocksState.stocks[name]
			sell = stock['sell']
			buy = stock['buy']
			buyHigh = stock['buyHigh']
			sellLow = stock['sellLow']
			fairValue = stock['fairValue']
			quantity = status[name]
			print(name + " " + str(sellLow) + " " + str(fairValue) + " " + str(buyHigh))
			
			if buyHigh > fairValue and buyHigh in buy:
				amount = min(quantity/2, buy[buyHigh]/2,1)
				orderID = bank.existOrder(name, "SELL")
				if not orderID:
				# 	order = bank.getOrders()[orderID]
				# 	order.life += 1
				# 	if order.life > 50:
				# 		sendCancel(exchange,orderID)
				# 	if order.quantity < amount:
				# 		order.quantity += 1
				# 	sendConvert(exchange, orderID, order.stock, "SELL", order.quantity)
				# else:

					bank.addOrder(orderCounter, sendAdd(exchange, orderCounter, name, 'SELL', buyHigh, amount))
					bank.deltaQuantity(name, -1)
					print("ATTEMPTING TO SELL: " + name)
				orderCounter += 1
	 		if sellLow < fairValue and money > -29000 and sellLow in sell:
	 			amount = min(quantity/2, sell[sellLow]/2,1)
	 			orderID = bank.existOrder(name, "BUY")
				if not orderID:
				# 	order = bank.getOrders()[orderID]
				# 	order.life += 1
				# 	if order.life > 50:
				# 		sendCancel(exchange,orderID)
				# 	if order.quantity < amount:
				# 		order.quantity += 1
				# 	sendConvert(exchange, orderID, order.stock, "BUY", order.quantity)
				# else:
	 				bank.addOrder(orderCounter, sendAdd(exchange, orderCounter, name, 'BUY',sellLow, amount))
	 				print("ATTEMPTING TO BUY: " + name)
 				orderCounter += 1

	return orderCounter
