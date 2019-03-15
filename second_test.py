import abcEconomics as abce
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import pylab
import names
import pandas as pd

from agent import Agent
import agent
import graph

simulation_parameters = {'name': 'name',
                         'trade_logging': 'off',
                         'random_seed': None,
                         'rounds': 10}

def main(simulation_parameters):

    test_sim = abce.Simulation(name='quipu_sim', processes=1)

    num_agents = 5

    names = list(range(0, num_agents))

    money = random.sample(range(1000, 5000), num_agents) 
    good2 = random.sample(range(100, 500), num_agents) 
    good3 = random.sample(range(100, 500), num_agents) 

    params = agent.build_agent_parameters(num_agents,names,'money',
                               money,'food', good2, 'other', good3)

    print(params)
    agents = test_sim.build_agents(Agent, 'agent', agent_parameters=params)

    num_edges = 2*num_agents

    G = graph.build_graph(num_agents,names,money)

    node_sizes = money

    r = 0
    while r < 10:

        test_sim.advance_round(r)
        r += 1

        #Select 2 random agents
        buyer = random.randint(0,num_agents-1)
        seller = random.randint(0,num_agents-1)

        #Transact
        action = random.randint(0,1)
        good = random.randint(0,10)

        agents[buyer].buy_goods(seller,good)
        
        cost = agents[seller].sell_goods(good)[0]

        node_size_1 = (agents[buyer].return_curr_money()[0][0])

        node_size_2 = (agents[seller].return_curr_money()[0][0])

        #Buyer gets smaller, seller gets bigger
        node_sizes[buyer] = node_size_1/2
        node_sizes[seller] = node_size_2*2

        plt.clf()

        #Add edge between them
        G.add_edge(buyer,seller)

  
        print(G.nodes())

        #Print
        nx.draw_networkx(G, pos=nx.get_node_attributes(G,'Position'), node_size=(node_sizes))

        pylab.draw()

        plt.pause(1)

    test_sim.finalize()

if __name__ == '__main__':
    main(simulation_parameters)
