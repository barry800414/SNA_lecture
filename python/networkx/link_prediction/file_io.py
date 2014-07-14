#!/usr/bin/env python

'''
Author: Wei-Ming (MsLab)
Usage: deal with I/O part for link prediction project
'''

import networkx as nx
from Column import *

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

def read_feature_column_major(filename, column_type):
    with open(filename, 'r') as f:
        line = f.readline().strip()
        entry = line.split(',')
        column_name = entry[1:]
        column_num = len(column_name)
        assert len(column_type) == column_num
        
        columns = list()
        for t in column_type:
            if t == 'categorical' or t == 'numerical':
                c = Column(1, t)
                c.value = dict()
                if t == 'categorical':
                    c.mapping = dict()
                columns.append(c)
            
        for line in f:
            entry = (line.strip()).split(',')
            assert len(entry) == (column_num + 1)
            row_id = int(entry[0])
            for i, column in enumerate(columns):
                value = entry[i+1].strip()
                if len(value) == 0 or value == 'None':
                    continue
                if column.type == 'categorical':
                    mapping = column.mapping
                    if value not in mapping:
                        mapping[value] = len(mapping)
                    column.value[row_id] = mapping[value]
                elif column.type == 'numerical':
                    column.value[row_id] = float(value)
        
        for column in columns:
            if column.type == 'categorical':
                column.dim = len(column.mapping)

    return (columns, column_name)
            
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

def read_graph(filename):
    graph = nx.Graph()
    with open(filename, 'r') as f:
        f.readline()
        for line in f:
            entry = line.strip().split(",")
            assert len(entry) == 2
            graph.add_edge(int(entry[0]), int(entry[1]))
    return graph
