import abcEconomics as abce


class Quipu_Agent(abce.Agent):
	def init(self,family_name,money,food,quipu):
		self.family_name = family_name
		self.create('money', money)
		self.create('food', food)
		self.create('quipu', quipu)

	def buy_goods_with_quipu(self,agent_id):
		if (self['quipu'] > 0):
			self.buy(('agent', agent_id), good='food', quantity=1, price=1, currency='quipu')

	def sell_goods_with_quipu(self):
		for offer in self.get_offers('food'):
			if (offer.currency == 'quipu' and self['food'] > 0):
					self.accept(offer)
					return offer.price * offer.quantity
			else:
				return -1

	def eat_food(self):
		if self['food']>0:
			self.destroy('food', quantity=1)

	#Buys from walmart
	def buy_goods(self,agent_id):
		if self['money'] > 0:
			self.buy(('corporate', agent_id), good='food', quantity=1, price=1)

	def print_possessions(self):
		print("agent:",self.family_name, (self.possessions()))

	def return_food(self):
		return self['food']

	def return_quipu(self):
		return self['quipu']

	def return_money(self):
		return self['money']








