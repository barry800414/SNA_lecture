#!/usr/bin/env python3

import networkx as nx
import random 

# 1. starting from one node, add its neighbors into candidate set
# 2. randomly selecting one node from candidate set, where the prob
#    is proportional to the number of its neighbor node which are in
#    selected set
# Repeat 2 until reaching goad number
# nodes_set = selected_set + candidate + remain_set
def sample_graph1(graph, goal_node_num):
    edge_set = set(graph.edges())
    selected_node_set = set()
    selected_edge_set = set()
    candidate_edge_set = set()
    remain_node_set = set(graph.nodes())
    now_num = 0

    while now_num < goal_node_num:
        #print('selected_edge_set: ', selected_edge_set)
        #print('candidate_edge_set: ', candidate_edge_set) 
        if len(candidate_edge_set) == 0:
            assert len(remain_node_set)!=0
            seed_node = random.sample(remain_node_set, 1)[0]
            #print('seed_node: ', seed_node)
        else:
            seed_edge = random.sample(candidate_edge_set, 1)[0]
            #print('seed_edge: ', seed_edge)
            if seed_edge[0] in selected_node_set:
                seed_node = seed_edge[1]
            else:
                seed_node = seed_edge[0]
            #print('seed_node: ', seed_node)
        
        incident_edge_set = set()
        for e in graph.edges(seed_node):
            incident_edge_set.add((min(e[0], e[1]), max(e[0], e[1])))

        #incident_edge_set = set(graph.edges(seed_node))
        intersect = incident_edge_set & candidate_edge_set
        #print('incident_edge_set:', incident_edge_set)
        #print('intersect: ', intersect)
        selected_edge_set.update(intersect)
        candidate_edge_set = (candidate_edge_set | incident_edge_set) - intersect
        selected_node_set.add(seed_node)
        remain_node_set.remove(seed_node)
        now_num += 1
        if now_num % 100 == 0:
            print(now_num)

    #print(selected_node_set)
    #print(selected_edge_set)
            
    return (selected_node_set, selected_edge_set)






