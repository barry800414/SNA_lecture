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
        if len(nei_x) == 0 or len(nei_y) == 0:
            value[pair] = 0.0
        else:
            union = nei_x | nei_y
            intersect = nei_x & nei_y
            value[pair] = float(len(intersect)) / len(union)
    c.value = value
    return c

# get all adamic/adar scores for all pairs
def get_adamic_adar_score(graph, pairs):
    c = Column(1, 'numerical')
    # TODO Task_4: EDIT HERE, finish the get_adamic_adar_score function
    # hint: you can copy the structure from other function
    #       you may use 'math' module in python 
    c.value[pairs[0]] = 1 # delete this line
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

