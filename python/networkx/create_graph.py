#!/usr/bin/env python3
import networkx as nx

'''
SNA tutorial 
Author: Wei-Ming(MSLAB, NTU)
'''

# new a graph (undirected)
g = nx.Graph()

# add nodes
g.add_node(1)
g.add_nodes_from([2,3])

# add edges
g.add_edge(1,2)
g.add_edges_from([(1,2),(1,3)])
g.add_edge(3,4)

print

