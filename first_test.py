import abcEconomics as abce
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import pylab

simulation_parameters = {'name': 'name',
                         'trade_logging': 'off',
                         'random_seed': None,
                         'rounds': 10}

class Agent(abce.Agent):
    def init(self,family_name,money,products):
        self.family_name = family_name
        self.create('money', money)
        self.create('clothes', products)

    def buy_goods(self,agent_id):
        self.buy(('agent', agent_id), good='clothes', quantity=10000, price=1)

    def sell_goods(self):
        for offer in self.get_offers('clothes'):
            if offer.price >= 0 and self['clothes'] > 0:
                self.accept(offer)
                return offer.price * offer.quantity
            else:
                return -1
    def print_possessions(self):
        print('    ' + self.family_name + str(dict(self.possessions())))
 
    def get_name(self):
       return self.family_name

    def return_quantity_of_good(self):
        return self['clothes']

    def return_curr_money(self):
        return self['money']

def get_fig(G,agents):
    node_sizes = [agents[0].return_quantity_of_good()[0][0],agents[1].return_quantity_of_good()[0][0]]
    print(node_sizes)

    nx.draw_networkx(G, pos=nx.get_node_attributes(G,'Position'), node_size=node_sizes, with_labels=True)

def main(simulation_parameters):
    
    test_sim = abce.Simulation(name='quipu_sim', processes=1)

    total_cost = 0

    agents = test_sim.build_agents(Agent, 'agent',
                                 agent_parameters=[{'family_name': 'buyer', 'money': 100000,'products': 0}, 
                                                   {'family_name': 'seller','money': 0,'products': 100000}])

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
    while (end==False):

        test_sim.advance_round(r)
        r += 1

        agents[0].buy_goods(1)
        
        cost = agents[1].sell_goods()[0]

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

