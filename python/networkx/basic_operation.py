#!/usr/bin/env python3

'''
SNA tutorial (MSLAB)
Author: Wei-Ming(MSLAB, NTU)
'''

import networkx as nx


### Undirected Graph ###
print('Undirected Graph:')
g = nx.Graph()
g.add_nodes_from([0,1,2,3,4,5])
g.add_edges_from([(0,1),(1,2),(2,3),(3,4),(4,5)])

# degree
for v in g.nodes():
    print('Degree(%d): %d' %(v, g.degree(v)))

# neighbors
for v in g.nodes():
    print('Neighbors(%d): %s' %(v, g.neighbors(v)))


### Directed Graph ###
print('\n\nDirected Graph:')
dg = nx.DiGraph()
dg.add_nodes_from([0,1,2,3,4,5])
dg.add_edges_from([(0,1),(1,2),(2,3),(3,4),(4,5)])

# degree
for v in dg.nodes():
    print('In-degree(%d): %d' %(v, dg.in_degree(v)), '    Out-degree(%d): %d' %(v, dg.out_degree(v)))

# neighbors
for v in dg.nodes():
    print('Successors(%d): %s' %(v, dg.successors(v)), '     Predecessor(%d): %s' %(v, dg.predecessors(v)))



