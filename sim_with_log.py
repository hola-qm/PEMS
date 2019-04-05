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


#from agent import Agent
import agent
from outside_agent import Walmart
from quipu_agent import Quipu_Agent


def main():

	# Read in simulation parameters
	f = open('sim_params_final.csv','r')
	data = np.array(list(csv.reader(f)))
	
	curr_sim = data[1,:]
	
	num_agents = int(curr_sim[1])
	chance_food_inside = float(curr_sim[2])
	chance_raw_inside = float(curr_sim[3])
	quipu = int(curr_sim[5])
	print(quipu)

	f.close()

	test_sim = abce.Simulation(name='quipu_sim', processes=1, trade_logging='off')

	walmart_size = 1000
	names = list(range(0, num_agents+1))
	
	money = random.sample(range(5, 100), num_agents)
	money.append(walmart_size) 

	food = random.sample(range(10, 50), num_agents) 
	quipus = random.sample(range(5, 45), num_agents) 
	other = random.sample(range(1,20), num_agents)

	params = agent.build_agent_parameters(num_agents,names,'money',
							   money,'food', food, 'quipu', quipus, 'other', other)

	agents = test_sim.build_agents(Quipu_Agent, 'agent', agent_parameters=params)
	walmart = test_sim.build_agents(Walmart, 'corporate', agent_parameters=[{'family_name': 'walmart', 'money': 100, 'food': 100, 'other': 100}])
 	
	if quipu == 1:
		ofile  = open('data_with_quipus.csv', 'w')
		print("here")
	else:
		ofile  = open('data_just_money.csv', 'w')
		print("here1")

	writer = csv.writer(ofile, delimiter=',')
	writer.writerow(['Transaction ID', 'Buyer ID', 'Seller ID', 'Type of transaction', 'Currency', 'Failure from Buyer', 'Failure from Seller'])

	r = 0
	num_rounds = 40
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
				buy = agents[x].buy_goods_from_walmart(0,1)[0][0]
				
				sell = walmart[0].walmart_sell_goods(1)[0][0]

				writer.writerow([transaction_id, x, -1, 'food', 'money', buy, sell])

			else:
				#Buy from an agent that is not yourself
				numbers = list(range(0,x)) + list(range(x+1,num_agents))
				curr = random.choice(numbers)
				buy = agents[x].buy_goods(curr,0,quipu)[0][0]
				sell = agents[curr].sell_goods(0,quipu)[0][0]

				if quipu == 1:
					writer.writerow([transaction_id, x, curr, 'food', 'quipu', buy, sell])
				else:
					writer.writerow([transaction_id, x, curr, 'food', 'money', buy, sell])

			# Buy raw materials 1x per week
			if r % 7 == 0:
				transaction_id += 1
				action = random.randint(0,100)

				if action > (chance_raw_inside*100):
					buy = agents[x].buy_goods_from_walmart(0,0)[0][0]
					sell = walmart[0].walmart_sell_goods(0)[0][0]

					writer.writerow([transaction_id, x, -1, 'raw', 'money', buy, sell])

				else:
				#Buy from an agent that is not yourself
					numbers = list(range(0,x)) + list(range(x+1,num_agents))
					curr = random.choice(numbers)
					buy = agents[x].buy_goods(curr,1,quipu)[0][0]
					sell = agents[curr].sell_goods(1,quipu)[0][0]

					if quipu == 1:
						writer.writerow([transaction_id, x, curr, 'food', 'quipu', buy, sell])
					else:
						writer.writerow([transaction_id, x, curr, 'food', 'money', buy, sell])

			transaction_id += 1

	#end of loop
	ofile.close()
	test_sim.finalize()

if __name__ == '__main__':
	main()
