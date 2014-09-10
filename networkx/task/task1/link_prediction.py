#!/usr/bin/env python
from __future__ import print_function
import sys
import file_io
import convert_feature as cf
import extract_feature as ef 
from Column import *
import random

'''
Author: Wei-Ming Chen (MSLab, CSIE, NTU)
Contacts: barry800414@gmail.com
'''

def sample_negative_edges(graph, num, method='random_edge'):
    nodes = graph.nodes()
    nodes_num = graph.number_of_nodes()
    cnt = 0
    edges = list()
    while cnt < num:
        r1 = nodes[random.randint(0, nodes_num-1)]
        r2 = nodes[random.randint(0, nodes_num-1)]
        if graph.has_edge(r1, r2) or r1 == r2:
            continue
        else:
            edges.append((r1, r2))
            cnt += 1
    return edges

def gen_label_mapping(keys, values):
    labels = dict()
    if type(values) == list:
        assert len(keys) == len(values)
        for i in range(0, len(keys)):
            labels[keys[i]] = values[i]
    else:
        for key in keys:
            labels[key] = values
    return labels

def update_nodes_from_test_data(graph, pairs):
    for pair in pairs:
        graph.add_node(pair[0])
        graph.add_node(pair[1])
    return graph

def merge_graph(graph1, graph2):
    new_graph = graph1.copy()
    new_graph.add_edges_from(graph2.edges())
    new_graph.add_nodes_from(graph2.nodes())
    return new_graph

def gen_training_data(train_graph, node_feature, filename):    
    print('=========Generating training data=========', file=sys.stderr)

    # sample negative samples
    neg_edge_num = train_graph.number_of_edges()
    neg_edges = sample_negative_edges(train_graph, neg_edge_num)
    train_pairs = train_graph.edges()
    train_pairs.extend(neg_edges)
    random.shuffle(train_pairs)
    train_labels = gen_label_mapping(train_graph.edges(), 1)
    train_labels.update(gen_label_mapping(neg_edges, -1))

    # extract topplogical features
    pair_feature = feature_extraction(train_graph, train_pairs, node_feature)
    
    # if you want to output dummy variable, comment the next line
    node_feature = None

    outfile = open(filename, 'w')
    cf.convert_to_svm_format(train_pairs, node_feature, 
            pair_feature, outfile, testing_ans = train_labels)
    outfile.close()

def gen_testing_data(all_graph, test_pairs, test_labels, 
        node_feature, filename):
    print('=========Generating testing data=========', file=sys.stderr)

    # extract topological features
    pair_feature = feature_extraction(all_graph, test_pairs, node_feature)
    
    # if you want to output dummy variable, comment the next line
    node_feature = None

    outfile = open(filename, 'w')
    cf.convert_to_svm_format(test_pairs, node_feature,  
            pair_feature, outfile, testing_ans = test_labels)
    outfile.close()

def feature_extraction(graph, pairs, node_feature):
    
    print('shortest path length', file=sys.stderr)
    shortest_path_length_col = ef.get_shortest_path_length(graph, pairs)
    

    pair_feature = [
            shortest_path_length_col, 
        ]
    
    return pair_feature

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print('Usage:', sys.argv[0], 'in_train_file in_test_file in_test_ans in_user_profile_file in_config out_train_file out_test_file')
        exit()
    
    # arguments
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    test_ans_file = sys.argv[3]
    user_profile_file = sys.argv[4]
    config_file = sys.argv[5]
    out_train_file = sys.argv[6]
    out_test_file = sys.argv[7]

    # read in data
    train_graph = file_io.read_graph(train_file)
    config = file_io.read_config(config_file)
    user_feature = None
    
    (user_feature, feature_name) = file_io.read_feature_column_major(user_profile_file, config)
    
    #normalize features
    for column in user_feature:
        if column.type == 'numerical':
            cf.normalize_column(column)
        elif column.type == 'categorical':
            cf.convert_to_dummy_variable(column)
    
    test_pair = file_io.read_data(test_file)
    train_graph = update_nodes_from_test_data(train_graph, test_pair)
    test_ans = gen_label_mapping(test_pair, file_io.read_ans(test_ans_file))
    gen_training_data(train_graph, user_feature, out_train_file)
    gen_testing_data(train_graph, test_pair, test_ans, 
            user_feature, out_test_file)

