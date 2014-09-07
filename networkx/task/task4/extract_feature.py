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
    # TODO Task_4: EDIT HERE, finish the get_adamic_adar_score function
    return c

# get all preferetial scores for all pairs
def get_preferential_score(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        nei_x = graph.neighbors(pair[0])
        nei_y = graph.neighbors(pair[1])
        value[pair] = (len(nei_x) + 1) * (len(nei_y) + 1)
    c.value = value
    return c

