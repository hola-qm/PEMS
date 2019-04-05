#Quipu Simulation Take 1

'''Goal: With 10 agents, create a template
for a simulation with the folowing levers:
	1. Type of connection (all connected or random connections)
	2. Starting $ amount (money that can be spent on everything)
	3. Starting Quipu amount (money that can only be spent in the Quipu market)
	4. % chance that purchases go to local vendors

For now, there will only be three goods: Food, clothes, plumbing
There will be two currencies: Pesos and Quipus'''


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
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import pylab
import pandas as pd
import sys
import csv

from agent import Agent
import agent
from outside_agent import Walmart
from quipu_agent import Quipu_Agent
import graph


def main():

	chance_raw_outside = 0.88
	chance_raw_inside = 1 - chance_raw_outside
	chance_food_inside = 0.83
	chance_food_outside = 1 - chance_food_inside

	test_sim = abce.Simulation(name='quipu_sim', processes=1,  trade_logging='off')

	num_agents = 5
	walmart_size = 1000
	names = list(range(0, num_agents+1))
	
	money = random.sample(range(100, 200), num_agents)
	money.append(walmart_size) 

	food = random.sample(range(10, 50), num_agents) 
	quipu = random.sample(range(10, 50), num_agents) 

	params = agent.build_agent_parameters(num_agents,names,'money',
							   money,'food', food, 'quipu', quipu)

	agents = test_sim.build_agents(Quipu_Agent, 'agent', agent_parameters=params)
	walmart = test_sim.build_agents(Walmart, 'corporate', agent_parameters=[{'family_name': 'walmart', 'money': 100, 'food': 100}])


	color_map = ['red']*(num_agents+1)
	color_map[num_agents] = 'blue'
	
	G = graph.build_graph(num_agents+1,names,money,1,num_agents)

	edges = G.edges()

	nx.draw_networkx(G, pos=nx.get_node_attributes(G,'Position'), node_size=money, node_color = color_map, width=3,with_labels = True)
	plt.pause(1)

	money_over_time = []
	food_over_time = []
	quipus_over_time = []

	r = 0
	num_rounds = 10

	while(r < num_rounds):

		test_sim.advance_round(r)
		r+=1

		curr_money = 0
		curr_quipus = 0
		curr_food = 0
	#Each round, select an agent and a random interaction (walmart or not)
	#Each round, every agent eats some food
		for x in range(num_agents):
			curr_money += agents[x].return_money()[0][0]
			curr_food += agents[x].return_food()[0][0]
			curr_quipus += agents[x].return_quipu()[0][0]

			colors = []

			action = random.randint(0,1)
			agents[x].eat_food()

			if action == 0:
				agents[x].buy_goods(0)
				walmart[0].sell_goods()

				for u,v in edges:
					if (u == x and v == num_agents) or (u == num_agents and v == x):
						colors.append('g')
					else:
						colors.append('#000000')

			else:
				numbers = list(range(0,x)) + list(range(x+1,num_agents))
				curr = random.choice(numbers)
				agents[x].buy_goods_with_quipu(curr)
				agents[curr].sell_goods_with_quipu()

				for u,v in edges:
					if(u == x and v == curr) or (u == curr and v == x):
						colors.append('g') 
					else:
						colors.append('#000000')

			nx.draw_networkx(G, pos=nx.get_node_attributes(G,'Position'), node_size=money, 
										node_color = color_map,edge_color=colors,with_labels =True,width=3)
		
			plt.pause(0.2)

		money_over_time.append(curr_money)
		food_over_time.append(curr_food)
		quipus_over_time.append(curr_quipus)

	plt.close()
	#end of loop
	test_sim.finalize()
	test_sim.graphs()
	r_list = list(range(0,num_rounds))

	# f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharex=True, figsize=(15,5))
	# ax1.plot(r_list,money_over_time,'r',label='money over time')
	# ax2.plot(r_list,food_over_time,'b',label='food over time')
	# ax3.plot(r_list,quipus_over_time,'g',label='quipus over time')
	# ax1.legend(loc='best')
	# ax2.legend(loc='best')
	# ax3.legend(loc='best')
	# plt.show()
	# plt.pause(5)
	# plt.close('all')
	sys.exit()

if __name__ == '__main__':
	main()








