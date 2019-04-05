import abcEconomics as abce
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import pylab
import names

from agent import Agent
import agent

simulation_parameters = {'name': 'name',
                         'trade_logging': 'individual',
                         'random_seed': None,
                         'rounds': 10}

def main(simulation_parameters):
    
    test_sim = abce.Simulation(name='tony_test', processes=1, trade_logging='individual')

    total_cost = 0

    num_agents = 2

    names = list(range(0, num_agents))
    money = random.sample(range(1, 50), num_agents) 
    good2 = random.sample(range(1, 50), num_agents)
    good3 = random.sample(range(1,50), num_agents)

    #print(names.get_first_name())

    params = agent.build_agent_parameters(num_agents,names,'money',
                                money,'food', good2, 'other', good3)

    #agents = test_sim.build_agents(Agent, 'agent', agent_parameters=params)

    agents = test_sim.build_agents(Agent, 'agent',
                             agent_parameters=[{'family_name': 'buyer', 'money': 100000,'food': 0}, 
                                               {'family_name': 'seller','money': 0,'food': 100000}])

    agents[0].print_possessions()

    buyer = agents[0].get_name()[0][0]
    seller = agents[1].get_name()[0][0]

    #Graph inital sizes, names
    node_sizes = [agents[0].return_quantity_of_good()[0][0],agents[1].return_quantity_of_good()[0][0]]

    G = nx.DiGraph()
    G.add_node(buyer, Position=(random.randrange(0, 100), random.randrange(0, 100)))
    G.add_node(seller, Position=(random.randrange(0, 50), random.randrange(0, 50)))

    G.add_edge(buyer,seller, weight=total_cost)

    end=False
    r=0

    #Run simulation
    while (r < 10):

        test_sim.advance_round(r)
        r += 1

        agents[0].buy_goods(1,0)
        
        cost = agents[1].sell_goods(0)[0]

        #Ugly but ends the loop when the transactions are no longer possible
        if cost[0] == -1:
            end=True

        total_cost += cost[0]

        #Update node size to reflect good quantity
        node_size_1 = int((agents[0].return_quantity_of_good()[0][0]) * 0.1)
        node_size_2 = int((agents[1].return_quantity_of_good()[0][0]) * 0.1)

        node_sizes = [node_size_1, node_size_2]
        print(node_sizes)
        #Update weight size to reflect money transferred
        G.add_edge(buyer,seller, weight=(total_cost*100))

        #label the edges
        labels = {(buyer,seller):total_cost}
        plt.clf()
        #plot the graphs
        plt.title("100,000 products sold by seller")
        nx.draw_networkx(G, pos=nx.get_node_attributes(G,'Position'),node_list=[buyer, seller], node_size=node_sizes, with_labels=True)

        nx.draw_networkx_edge_labels(G,pos=nx.get_node_attributes(G,'Position'),edge_labels=labels,font_size=30)
        
   
        pylab.draw()

        plt.pause(.5)

    test_sim.finalize()

if __name__ == '__main__':
    main(simulation_parameters)

