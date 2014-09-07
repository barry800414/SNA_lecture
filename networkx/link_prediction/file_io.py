#!/usr/bin/env python

'''
Author: Wei-Ming (MsLab)
Usage: deal with I/O part for link prediction project
'''

import networkx as nx
from Column import *

# read the csv file as a list of pairs
def read_data(filename):
    data_list = list()
    with open(filename, 'r') as f:
        line = f.readline().strip()
        entry = line.split(',')
        assert len(entry) == 2
        for line in f:
            entry = (line.strip()).split(',')
            assert len(entry) == 2
            data_list.append( (int(entry[0]), int(entry[1])) )            
    return data_list

# read testing answer file as list of integer
def read_ans(filename):
    ans = list()
    with open(filename, 'r') as f:
        for line in f:
            ans.append(int(line.strip()))
    return ans

# read feature csv file as a list of Columns 
def read_feature_column_major(filename, column_type):
    with open(filename, 'r') as f:
        line = f.readline().strip()
        entry = line.split(',')
        column_name = entry[1:]
        column_num = len(column_name)
        assert len(column_type) == column_num
        
        # generate the list of Columns for later usage
        columns = list()
        for t in column_type:
            c = Column(1, t)
            columns.append(c)
        
        # read in rows 
        for line in f:
            entry = (line.strip()).split(',')
            assert len(entry) == (column_num + 1)
            row_id = int(entry[0])
            for i, column in enumerate(columns):
                value = entry[i+1].strip()
                if len(value) == 0 or value == 'None' or value == 'null':
                    continue
                if column.type == 'categorical':
                    value = value.split('\t')
                    column.value[row_id] = list()
                    for v in value:
                        column.value[row_id].append(v)
                elif column.type == 'numerical':
                    column.value[row_id] = float(value)
        
    return (columns, column_name)

# read feature csv file as a list of rows
def read_feature_row_major(filename):
    with open(filename, 'r') as f:
        line = f.readline().strip()
        entry = line.split(',')
        column_name = entry[1:]
        column_num = len(column_name)
        rows = dict()
        for line in f:
            entry = (line.strip()).split(',')
            assert len(entry) == (column_num + 1)
            row_id = int(entry[0])
            rows[id_num] = entry[1:]
    return (rows, feature_name)

# read training csv file as graph
def read_graph(filename):
    graph = nx.Graph()
    with open(filename, 'r') as f:
        f.readline()
        for line in f:
            entry = line.strip().split(",")
            assert len(entry) == 2
            graph.add_edge(int(entry[0]), int(entry[1]))
    return graph




