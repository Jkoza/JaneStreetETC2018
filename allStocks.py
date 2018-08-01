import json
from sys import maxsize
from collections import deque

class AllStocks:
	def __init__(self, helloInfo):
		self.stocks = dict()
		for stock in helloInfo['symbols']:
			if stock['symbol'] != 'USD':
				self.stocks[stock['symbol']] = {
						'buy' : dict(),
						'sell' : dict(),
						'buyHigh' : 0,
						'sellLow': maxsize,
						'fairValue': 0,
						'isOpen': False,
						'midValues': deque()
					}
		# for stock in self.stocks.iterkeys():
		# 	print(stock)

	def calculate(self,alist):
		percent = [5,5,10,15,25,40]
		sum = 0.0
		count = 0;
		for i in alist:
			sum += i*percent[count]
			count += 1
		return int(sum / 100)
	
	def updateFairValues(self):
		for name, stock in self.stocks.iteritems():
			if name != "XLK":
				stock['midValues'].append(int((stock['buyHigh'] - stock['sellLow'])/2 + stock['sellLow']))
				if len(stock['midValues']) > 6:
					stock['midValues'].popleft()
					stock['fairValue'] = self.calculate(stock['midValues'])	
					# stock['fairValue'] = sum(stock['midValues']) / len(stock['midValues'])
				else:
					stock['fairValue'] = int((stock['buyHigh'] - stock['sellLow'])/2 + stock['sellLow'])
		stock = self.stocks["XLK"]
		if "XLK" in self.getOpen():
			stock['fairValue'] = int((3000 + 2 * self.stocks['AAPL']['fairValue'] + 3 * self.stocks['MSFT']['fairValue'] + 2 * self.stocks['GOOG']['fairValue'])/10)		

	
	def openStocks(self,response):
		for stock in response['symbols']:
			self.stocks[stock]['isOpen'] = True

	def closeStocks(self,response):
		for stock in response['symbols']:
			self.stocks[stock]['isOpen'] = False

	def getOpen(self):
		ret = list()
		for name,stock in self.stocks.iteritems():
			if stock['isOpen']:
				ret.append(name)
		return ret


	def updateBuy(self,stock):
		buyHigh = 0
		if stock in self.stocks:
			for buy in self.stocks[stock]['buy'].iterkeys():
				if buy > buyHigh:
					buyHigh = buy
		self.stocks[stock]['buyHigh'] = buyHigh

	def updateSell(self,stock):
		sellLow = maxsize
		if stock in self.stocks:
			for sell in self.stocks[stock]['sell'].iterkeys():
				if sell < sellLow:
					sellLow = sell
		self.stocks[stock]['sellLow'] = sellLow

	def updateStocks(self,response): 
		if response['type'] == 'book':
			self.stocks[response['symbol']]['buy'] = dict()
			for buy in response['buy']:
				self.stocks[response['symbol']]['buy'][buy[0]] = buy[1]
			self.stocks[response['symbol']]['sell'] = dict()
			for sell in response['sell']:
				self.stocks[response['symbol']]['sell'][sell[0]] = sell[1]
			self.updateBuy(response['symbol'])
			self.updateSell(response['symbol'])
			self.updateFairValues()

	def getStock(self, stock):
		return self.stocks[stock]

		    	
