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

# get all clustering coefficient score for all pairs
def get_cc_score(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()

    # calculate clustering coefficient scores for all nodes
    cc = nx.clustering(graph)
    for pair in pairs:
        x = pair[0]
        y = pair[1]
        value[pair] = cc[x] + cc[y]
    c.value = value
    return c


# get all hittig time value of all pairs
def get_hitting_time(graph, pairs, trials, max_step):
    c = Column(1, 'numerical')
    value = dict()

    pairs_set = set(pairs)
    hitting_time = dict()
    for n in graph.nodes():
        hitting_time[n] = defaultdict(float)
    
    # calculating hitting time
    for n1 in graph.nodes():
        print(n1)
        # run random walks for given starting node
        expected_steps = random_walk(graph, n1, trials, max_step)
        for n2 in expected_steps.keys():
            if (n1,n2) in pairs_set or (n2,n1) in pairs_set:
                hitting_time[n1][n2] = expected_steps[n2]
    
    for pair in pairs:
        n1 = pair[0]
        n2 = pair[1]
        if n2 in hitting_time[n1] and n1 in hitting_time[n2]:
            if hitting_time[n1][n2] == 0.0:
                hitting_time[n1][n2] = NO_PATH_LENGTH
            if hitting_time[n2][n1] == 0.0:
                hitting_time[n2][n1] = NO_PATH_LENGTH
            value[pair] = hitting_time[n1][n2] + hitting_time[n2][n1]
    c.value = value
    return c

def random_walk(graph, start_node, trials, max_step):
    for t in range(0, trials):
        count = dict()
        for n in graph.nodes():
            count[n] = defaultdict(int)

        now_node = start_node
        for s in range(1,max_step+1):
            nei = graph.neighbors(now_node)
            if len(nei) == 0:
                break
            next_node = random.sample(nei, 1)[0]
            count[next_node][s] += 1
            now_node = next_node

    expected_steps = dict()
    for n in graph.nodes():
        expected_steps[n] = 0.0
        for step, c in count[n].items():
            expected_steps[n] += step * c 
        expected_steps[n] = expected_steps[n] / trials
    return expected_steps

# get all common categories
def get_common_categories_col(converted_column, pairs):
    if converted_column.type != 'categorical':
        return None

    c = Column(1, 'numerical')
    value = dict()

    for pair in pairs:
        n1 = pair[0]
        n2 = pair[1]
        
        if n1 in converted_column.value:
            f1 = converted_column.value[n1] # a set of integers
        else:
            f1 = set()
        if n2 in converted_column.value:
            f2 = converted_column.value[n2] # a set of integers
        else:
            f2 = set()

        union = f1 | f2
        intersect = f1 & f2
        if len(union) != 0 and len(intersect) != 0:
            value[pair] = len(intersect) / len(union)
        else:
            pass  #value[pair] = 0.0
    c.value = value
    return c

