#!/usr/bin/env python
from __future__ import print_function
import sys
import networkx as nx
import math
import random
from collections import defaultdict

from Column import *

'''
Author: Wei-Ming Chen (MSLab, CSIE, NTU)
Contacts: barry800414@gmail.com
'''

'''
graph: the training graph 
pairs: the pairs of nodes to extract features
       pairs[i][0] denotes the node_1 of i-th pair
       pairs[i][1] denotes the node_2 of i-th pair
'''

NO_PATH_LENGTH = 1000


# get all edge embeddedness(number of common neighbors) for the edge in edges
def get_edge_embeddedness(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        n1 = pair[0]
        n2 = pair[1]
        value[pair] = len(list(nx.common_neighbors(graph, n1, n2)))
    c.value = value
    return c

# get all jaccards_coefficent for all pairs
def get_jaccards_coefficient(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        n1 = pair[0]
        n2 = pair[1]
        nei_x = set(graph.neighbors(n1))
        nei_y = set(graph.neighbors(n2))
        # TODO Task_3: EDIT HERE, caculate jaccards_coefficient
        # for n1 and n2 
        # value[pair] = ooxxa
        # Please notice nei_x or nei_y could be empty set
        value[pair] = 0 #delete this line
    c.value = value
    return c

# get shortest path length for all edges
def get_shortest_path_length(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        n1 = pair[0]
        n2 = pair[1]
        try:
            value[pair] = nx.shortest_path_length(graph, n1, n2)
        except:
            value[pair] = NO_PATH_LENGTH
    c.value = value
    return c

