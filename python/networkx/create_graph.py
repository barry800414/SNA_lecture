#!/usr/bin/env python3

import networkx as nx
from graph_utility import * 


'''
SNA tutorial (MSLAB)
Author: Wei-Ming(MSLAB, NTU)
'''

# new a graph (undirected)
g = nx.Graph()

# add nodes
g.add_node(1)
g.add_nodes_from([2,3])
g.add_node('node4')

# add edges
g.add_edge(1,2)
g.add_edges_from([(1,2),(1,3)])
g.add_edge(3,4)

print_graph_info(g)


#remove nodes
g.remove_node(3)
g.remove_nodes_from([3, 'node4'])

#remove edges
g.remove_edge(1,2)


print_graph_info(g)


