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
            value[pair] = nx.shortest_path_length(graph, pair[0], pair[1])
        except:
            pass
    c.value = value
    return c


# get all edge betweenness centrality of all edges in graph
def get_all_edge_betweenness_centrality(graph):
    c = Column(1, 'numerical')
    c.value = nx.edge_betweenness_centrality(graph)
    return c

# get all edge embeddedness(number of common neighbors) for the edge in edges
def get_edge_embeddedness(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        value[pair] = len(list(nx.common_neighbors(graph, pair[0], pair[1])))
    c.value = value
    return c

# get all jaccards_coefficent for all pairs
def get_jaccards_coefficient(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        nei_x = set(graph.neighbors(pair[0]))
        nei_y = set(graph.neighbors(pair[1]))
        # TODO Task_3: EDIT HERE, caculate jaccards_coefficient
        # for pair[0] and pair[1]
        # value[pair] = ooxx
    c.value = value
    return c


