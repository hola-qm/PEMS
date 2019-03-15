import networkx as nx
import random
import itertools


#Parameters: Takes a number of agents (int) and their names (list) of size
#           num agents

#Returns: A graph of all the agents with appropriate sizes

def build_graph(num_agents, names, weights, connected=0,num_edges=0):
    G = nx.DiGraph()
    
    for x in range(num_agents):
        G.add_node(names[x], Position=(random.randrange(0, 100), 
                        random.randrange(0, 100)), node_size=weights[x])

    if connected != 0:
    	edges = list(itertools.permutations(names,2))
    	G.add_edges_from(edges,color='#000000')
    else:
    	edges = list(itertools.permutations(names,2))
    	edges = random.sample(edges,num_edges)
    	G.add_edges_from(edges,color='#000000')
    return G


# def complete_graph_from_list(L, create_using=None):
#     G = networkx.empty_graph(len(L),create_using)
#     if len(L)>1:
#         if G.is_directed():
#             edges = itertools.permutations(L,2)
#         else:
#             edges = itertools.combinations(L,2)
#         G.add_edges_from(edges)
#     return G

# S = complete_graph_from_list(["a", "b", "c", "d"])
# print S.edges()