#!/usr/bin/env python
from __future__ import print_function
import sys
import file_io
import convert_feature as cf
import extract_feature as ef 
from Column import *
import random


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

def gen_label_mapping(keys, value):
    labels = dict()
    for key in keys:
        labels[key] = value
    return labels

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print('Usage', sys.argv[0], 'train_file test_file lender_file loan_file')
        exit()
    
    # arguments
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    lender_file = sys.argv[3]
    loan_file = sys.argv[4]

    # read in data
    train_graph = file_io.read_graph(train_file)
    lender_feature = file_io.read_feature_column_major(
            lender_file, ['categorical', 'numerical', 
            'numerical', 'numerical'])
    loan_feature = file_io.read_feature_column_major(
            loan_file, ['categorical', 'numerical', 
            'numerical', 'categorical', 'other'])

    # sample negative samples
    neg_edge_num = train_graph.number_of_edges()
    neg_edges = sample_negative_edges(train_graph, neg_edge_num)
    train_edges = train_graph.edges()
    train_edges.extend(neg_edges)
    train_labels = gen_label_mapping(train_graph.edges(), 1)
    train_labels.update(gen_label_mapping(neg_edges, 0))

    # feature extraction
    # edge_bet_col = get_all_edge_betweenness_centrality(graph)
    print('shortest path length')
    shortest_path_length_col = ef.get_shortest_path_length(train_graph, train_edges)

    print('edge_embedness')
    edge_embed_col = ef.get_edge_embeddedness(train_graph, train_edges)

    print('jaccards coefficient')
    jaccards_col = ef.get_jaccards_coefficient(train_graph, train_edges)
    
    print('adamic/adar score')
    adamic_adar_col = ef.get_adamic_adar_score(train_graph, train_edges)
    
    print('preferential score')
    prefer_col = ef.get_preferential_score(train_graph, train_edges)
    
    #print('katz_score')
    #katz_col = ef.get_katz_score(train_graph, train_graph.edges(), 0.8, 3)
    #print('hitting_time')
    #hitting_col = ef.get_hitting_time(train_graph, train_graph.edges(), 3)
    
    # normalize the feature value
    cf.normalize_column(shortest_path_length_col)
    cf.normalize_column(edge_embed_col)
    cf.normalize_column(jaccards_col)
    cf.normalize_column(adamic_adar_col)
    cf.normalize_column(prefer_col)
    #cf.normalize_column(katz_score)
    #cf.normalize.column(hitting_col)

    # convert to svm format
    #columns = (edge_embed_col, katz_col, hitting_col)
    columns = (shortest_path_length_col, edge_embed_col, 
            jaccards_col, adamic_adar_col, prefer_col)
    cf.convert_to_svm_format(train_edges, columns, sys.stdout, 
            testing_ans = train_labels)
    
