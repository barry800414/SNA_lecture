#!/usr/bin/env python3

import networkx as nx

# get all node degree for all nodes in graph
def get_all_node_degree(graph):
    ans = dict()
    for v in graph.nodes():
        ans[v] = graph.degree(v)
    return ans

# get all edge betweenness centrality of all edges in graph
def get_all_edge_betweenness_centrality(graph):
    return nx.edge_betweenness_centrality(graph)

# get all edge embeddedness(number of common neighbors) for the edge in edges
def get_edge_embeddedness(graph, edges):
    ans = dict()
    for edge in edges:
        ans[edge] = common_neighbors(graph, edge[0], edge[1])
    return ans

# get all katz scores for the edge in edges
def get_katz_score(graph, edges, beta, max_length):
    ans = dict()
    for edge in edges:
        count = __number_of_path(graph, edge, max_length)
        score = 0.0
        base = 1.0
        for i in range(1, len(count)):
            base = base * beta
            score += base * count[i]
        ans[edge] = score
    return ans
        
def __number_of_path(graph, edge, max_length):
    stack = list()
    stack.append((edge[0], 0))
    count = [0 for i in range(0, max_length+1)]
    while len(stack) != 0:
        (n, length) = stack.pop()
        nei = graph.neighbors(n)
        for n2 in nei:
            if n2 == edge[1]:
                count[length + 1] += 1
            if length+1 < max_length
                stack.append((n2, length + 1))
    return count

# get all hitting time(expected number of steps from u to v) for each edge in edges
def get_hitting_time(graph, edges, max_length):
    ans = dict()
    for edge in edges:
        ans[edge] = __expected_steps(graph, edge, max_length)
    return ans

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
                if length+1 < max_length
                    stack.append((n2, length + 1, prob))
    return exp_step
