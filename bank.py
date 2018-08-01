class Bank:

	def __init__(self):
		self.state = dict()
		self.orders = dict()

	def updateStateFromResponse(self, response):
		for symbol in response['symbols']:
			self.state[symbol['symbol']] = symbol['position']
	
	def addOrder(self, orderID, order):
		self.orders[orderID] = order

	def deleteOrder(self, orderID):
		self.orders.pop(orderID)

	def getState(self):
		return self.state

	def getUSD(self):
		return self.state['USD']

	def deltaState(self, dir, price, amount, stock):
		if dir == "SELL":
			amount *= -1
		if dir == "BUY":
			self.state[stock] + amount;
		self.state['USD'] - amount*price;

	def deltaQuantity(self, stock, amount):
		self.state[stock] += amount
	
	def getOrders(self):
		return self.orders

	def existOrder(self, stock, orderType):
		for key,order in self.orders.iteritems():
			
			if order.stock == stock and order.orderType == orderType:
				return key
		return 0
