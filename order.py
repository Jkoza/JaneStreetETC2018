class Order:

	def __init__(self, orderType, orderID, orderStatus, quantity, price, stock):
		self.orderType = orderType
		self.orderID = orderID
		self.orderStatus = orderStatus
		self.quantity = quantity
		self.price = price
		self.stock = stock
		self.life = 0
