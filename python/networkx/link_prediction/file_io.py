#!/usr/bin/env python3

'''
Author: Wei-Ming (MsLab)
Usage: deal with I/O part for link prediction project
'''

import networkx as nx

def read_data(filename):
    data_list = list()
    with open(filename, 'r') as f:
        line = f.readline().strip()
        entry = f.split(',')
        assert len(entry) == 2
        assert entry[0] == 'lender_id'
        assert entry[1] == 'loan_id'
        for line in f:
            entry = (line.strip()).split(',')
            assert len(entry) == 2
            data_list.append( (int(entry[0]), int(entry[1])) )            
    return data_list

def read_feature(filename):
    features = dict()
    with open(filename, 'r') as f:
        line = f.readline().strip()
        entry = f.split(',')
        c_num = len(entry)
        feature_name = entry[1:]
        for line in f:
            entry = (line.strip()).split(',')
            assert len(entry) == c_num
            id_num = int(entry[0])
            features[id_num] = list()
            for i in range(1, c_num)
                features[id_num].append(entry[i])
    return (features, feature_name)
 
def read_graph(filename):
    graph = nx.Graph()
    with open(filename, 'r') as f:
        f.readline()
        for line in f:
            entry = line.strip().split(",")
            assert len(entry) == 2
            graph.add_edge(int(entry[0]), int(entry[1]))
    return graph
