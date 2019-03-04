import networkx as nx
import random


#Parameters: Takes a number of agents (int) and their names (list) of size
#           num agents

#Returns: A graph of all the agents with appropriate sizes

def build_graph(num_agents, names, weights):
    G = nx.DiGraph()
    
    for x in range(num_agents):
        G.add_node(names[x], Position=(random.randrange(0, 100), 
                        random.randrange(0, 100)), node_size=weights[x])

    return G