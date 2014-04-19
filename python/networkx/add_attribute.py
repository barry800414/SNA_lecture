#!/usr/bin/env python3

'''
SNA tutorial (MSLAB)
Author: Wei-Ming(MSLAB, NTU)
'''

import networkx as nx

g = nx.DiGraph()
g.add_nodes_from([0,1,2,3,4,5])
g.add_edges_from([(0,1),(1,2),(2,3),(3,4),(4,5)])

# add attribute to nodes
for i in range(0, 6):
    g.add_node(i, user_id = ('User_' + str(i)), user_type = 0)

# modify attribute of a node
g.node[0]['user_id'] = 'I am User_0'

# get the list of nodes and their attribute
for v in g.nodes(data = True):
    print('Node %d' % v[0], '\t\tattribute:', v[1]['user_id'])
#                                             ^^^^^^^^^^^^^^^ 




# add attribute to edges
for i in range(0, 5):
    g.add_edge(i, i+1, relationship = ('From User_' + str(i) + 'to User_' + str(i+1)))

# modify attribute of a edge
g.edge[0][1]['relationship'] = '0->1'

# get the list of edges and their attribute
for e in g.edges(data = True):
    print('Edge: %d->%d' % (e[0], e[1]) , '\tattribute:', e[2]['relationship'])
#                                                         ^^^^^^^^^^^^^^^^^^^^



