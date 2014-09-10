#!/usr/bin/env python
from __future__ import print_function
import sys
import networkx as nx
import math
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
    value = dict()
    for pair in pairs:
        n1 = pair[0]
        n2 = pair[1]
        common_nei = nx.common_neighbors(graph, n1, n2)
        score = 0.0
        for n in common_nei:
            score += 1.0 / math.log(len(graph.neighbors(n)) + 1)
        value[pair] = score
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

# get all katz scores for the edge in edges
def get_katz_score(graph, edges, beta, max_length):
    c = Column(1, 'numerical')
    value = dict()
    cnt = 0
    shortest_path_length = nx.all_pairs_shortest_path_length(graph)
    for edge in edges:
        count = __number_of_path(graph, edge, max_length, shortest_path_length)
        score = 0.0
        base = 1.0
        for i in range(1, len(count)):
            base = base * beta
            score += base * count[i]
        value[edge] = score
        cnt += 1
    c.value = value
    return c
        
def __number_of_path(graph, edge, max_length, shortest_path_length):
    spl = shortest_path_length
    stack = list()
    stack.append((edge[0], 0))
    count = [0 for i in range(0, max_length+1)]
    while len(stack) != 0:
        (n, length) = stack.pop()
        nei = graph.neighbors(n)
        for n2 in nei:
            if n2 == edge[1]:
                count[length + 1] += 1
            if (length+1) < max_length and (spl[n2][edge[1]] + length) < max_length:
                stack.append((n2, length + 1))
    return count

# get all hitting time(expected number of steps from u to v) for each edge in edges
def get_hitting_time(graph, edges, max_length):
    c = Column(1, 'numerical')
    value = dict()
    for edge in edges:
        value[edge] = __expected_steps(graph, edge, max_length)
    c.value = value
    return c

def __expected_steps(graph, edge, max_length):
    stack = list()
    stack.append((edge[0], 0, 1.0))
    exp_step = 0.0
    while len(stack) != 0:
        (n, length, now_prob) = stack.pop()
        nei = graph.neighbors(n)
        if len(nei) != 0:
            prob = (1.0 / len(nei)) * now_prob
            for n2 in nei:
                if n2 == edge[1]:
                    exp_step += prob * (length + 1)
                if length+1 < max_length:
                    stack.append((n2, length + 1, prob))
    return exp_step

# rooted pagerank


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

# get all node degree for all nodes in graph
def get_all_node_degree(graph):
    c = Column(1, 'numerical')
    value = dict()
    for v in graph.nodes():
        value[v] = graph.degree(v)
    c.value = value
    return c
