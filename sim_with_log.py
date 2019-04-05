'''
Trade specifics: Each agent will have a dollar amount and a Quipu amount

One round equals one day.

Each day, all the agents must buy food. 

Each week, all the agents must buy raw materials.

For each purchase, there is an option:
	-Buy from local vendor (other agent)
	-Buy from outside agent (no more money circulation)
'''
import abcEconomics as abce
import matplotlib.pyplot as plt
import numpy as np
import random
import os
import csv


from agent import Agent
import agent
from outside_agent import Walmart
from quipu_agent import Quipu_Agent


def main():

	# Read in simulation parameters
	f = open('sim_params_final.csv','r')
	reader = csv.reader(f)
	firstline = True
	for row in reader:
		if firstline == True:
			firstline = False
		else:
			num_agents = int(row[1])
			chance_food_inside = float(row[2])
			chance_raw_inside = float(row[3])
			starting_money = int(row[4])
	f.close()

	# chance_raw_outside = 0.88
	# chance_raw_inside = 1 - chance_raw_outside
	# chance_food_inside = 0.83
	# chance_food_outside = 1 - chance_food_inside

	test_sim = abce.Simulation(name='quipu_sim', processes=1,  trade_logging='off')

	#num_agents = 39
	walmart_size = 1000
	names = list(range(0, num_agents+1))
	
	money = random.sample(range(5, 100), num_agents)
	money.append(walmart_size) 

	food = random.sample(range(10, 50), num_agents) 
	quipu = random.sample(range(5, 45), num_agents) 

	params = agent.build_agent_parameters(num_agents,names,'money',
							   money,'food', food, 'quipu', quipu)

	agents = test_sim.build_agents(Quipu_Agent, 'agent', agent_parameters=params)
	walmart = test_sim.build_agents(Walmart, 'corporate', agent_parameters=[{'family_name': 'walmart', 'money': 100, 'food': 100}])
 
	ofile  = open('data.csv', 'w')
	writer = csv.writer(ofile, delimiter=',')
	writer.writerow(['Transaction ID', 'Buyer ID', 'Seller ID', 'Type of transaction', 'Currency', 'Cost'])

	r = 0
	num_rounds = 10
	transaction_id = 0

	while(r < num_rounds):
		
		test_sim.advance_round(r)
		r+=1

		#Each round, select an agent and a random interaction (walmart or not)
		#Each round, every agent eats some food
		for x in range(num_agents):

			action = random.randint(0,100)
			agents[x].eat_food()

			if action > (chance_food_inside*100):
				agents[x].buy_goods(0)
				# Cost = -1 if transaction did not occur
				cost = walmart[0].sell_goods()[0][0]

				writer.writerow([transaction_id, x, -1, 'food', 'money', cost])

			else:
				#Buy from an agent that is not yourself
				numbers = list(range(0,x)) + list(range(x+1,num_agents))
				curr = random.choice(numbers)
				agents[x].buy_goods_with_quipu(curr)
				cost = agents[curr].sell_goods_with_quipu()[0][0]

				writer.writerow([transaction_id, x, curr, 'food', 'quipu', cost])

			# Buy raw materials 1x per week
			if r % 7 == 0:
				transaction_id += 1
				action = random.randint(0,100)

				if action > (chance_raw_inside*100):
					agents[x].buy_goods(0)
					cost = walmart[0].sell_goods()[0][0]

					writer.writerow([transaction_id, x, -1, 'raw', 'money', cost])

				else:
				#Buy from an agent that is not yourself
					numbers = list(range(0,x)) + list(range(x+1,num_agents))
					curr = random.choice(numbers)
					agents[x].buy_goods_with_quipu(curr)
					cost = agents[curr].sell_goods_with_quipu()[0][0]

					writer.writerow([transaction_id, x, curr, 'raw', 'quipu', cost])

			transaction_id += 1
			
	#end of loop
	ofile.close()
	test_sim.finalize()

if __name__ == '__main__':
	main()
