#!/usr/bin/env python
from __future__ import print_function 
import sys
from file_io import *
import random

def generate_data(edges_set, training_num, testing_num, testing_neg_num):
    assert (training_num + testing_num) == len(edges_set)

    #get maximum id of nodes
    max_node_id = -1
    for e in edges_set:
        if e[0] > max_node_id:
            max_node_id = e[0]
        if e[1] > max_node_id:
            max_node_id = e[1]

    #sampling negative edges
    now_num = 0
    neg_edges_set = set()
    while now_num < testing_neg_num:
        v1 = random.randint(0, max_node_id+1)
        v2 = random.randint(0, max_node_id+1)
        if v1 != v2 and (min(v1, v2), max(v1, v2)) not in edges_set:
            if (min(v1, v2), max(v1, v2)) not in neg_edges_set:
                neg_edges_set.add((min(v1, v2), max(v1, v2)))
                now_num += 1 

    # slice the original edges set into training and testing set
    edges_list = list(edges_set)
    random.shuffle(edges_list)
    training_edges_list = edges_list[0:training_num]
    testing_edges_list = list()
    for i in range(training_num, training_num+testing_num):
        testing_edges_list.append((edges_list[i], 1))
    for e in neg_edges_set:
        testing_edges_list.append((e, 0))
    random.shuffle(testing_edges_list)

    return (training_edges_list, testing_edges_list)



if __name__=='__main__':
    if len(sys.argv) != 7:
        print(sys.argv[0], 'in_training_csv out_training_csv out_testing_csv out_ans_file training_ratio neg_edges_times', file=sys.stderr)
        exit(-1)
    
    in_training_csv = sys.argv[1]
    out_training_csv = sys.argv[2]
    out_testing_csv = sys.argv[3]
    out_ans_file = sys.argv[4]
    training_ratio = float(sys.argv[5])
    neg_edges_times = float(sys.argv[6])
    assert training_ratio < 1.0 and training_ratio > 0.0
    assert neg_edges_times > 0.0

    edges_set = read_edges_as_set(in_training_csv)

    total_num = len(edges_set)
    training_num = int(total_num * training_ratio)
    testing_num = total_num - training_num
    testing_neg_num = int(testing_num * neg_edges_times)
    

    (training_edges_list, testing_edges_list) = generate_data(edges_set, training_num, testing_num, testing_neg_num)
    write_training_file(training_edges_list, out_training_csv)
    write_testing_file(testing_edges_list, out_testing_csv, out_ans_file)

    print('total_edges:', total_num)
    print('expected training_edges:', training_num)
    print('expected testing_edges:', testing_num)
    print('expected testing_neg_edges:', testing_neg_num)

    print('actual training_edges:', len(training_edges_list))
    print('actual all_testing_edges:', len(testing_edges_list))
    
