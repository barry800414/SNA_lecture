#!/usr/bin/env python

import networkx as nx
import math
from Column import *

# get all node degree for all nodes in graph
def get_all_node_degree(graph):
    c = Column(1, 'numerical')
    value = dict()
    for v in graph.nodes():
        value[v] = graph.degree(v)
    c.value = value
    return c

# get shortest path length for all edges
def get_shortest_path_length(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        try:
            # TODO Task_1: EDIT HERE, please find shortest 
            # path from pair[0] to pair[1]
            # value[pair] = ooxx
            pass
        except:
            pass
    c.value = value
    return c
