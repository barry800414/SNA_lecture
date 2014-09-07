#!/usr/bin/env python
from __future__ import print_function
import math

FLOAT_ERR = 10e-15

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-1.0 * x))

# normalize the value to [-1, 1] (for numerical column)
def normalize_column(column, normalize='sigmoid'):
    if column.type != 'numerical': 
        return 
    col_value = column.value
    if normalize == 'max':
        values = value.values()
        max_v = max(max(values), abs(min(values)))
        if max_v == 0.0:
            return column
        # normalize the column by maximum value
        for key in col_value.keys():
            col_value[key] = col_value[key] / max_v
        return column
    elif normalize == 'sigmoid':
        # normalize the column by sigmoid function 
        for key in col_value.keys():
            col_value[key] = 2.0 * (sigmoid(col_value[key]) - 0.5)
        return column

# convert categorical column to dummy variable
def convert_to_dummy_variable(column):
    if column.type != 'categorical':
        return 

    mapping = dict()
    new_column_value = dict()
    for row_id, categories in column.value.items():
        new_column_value[row_id] = set()
        for category in categories:
            if category not in mapping:
                mapping[category] = len(mapping)
            new_column_value[row_id].add(mapping[category])
    column.value = new_column_value
    column.dim = len(mapping)
    return column

# convert each row and features to svm format 
def convert_to_svm_format(row_ids, node_feature, pair_feature, outfile, testing_ans = None):
    x_dim = list()
    y_dim = list()
    pair_dim = list()
    now_dim = 1 

    # generate dimension list for later usage
    (pair_dim, now_dim) = gen_dim_list(pair_feature, now_dim)
    (x_dim, now_dim) = gen_dim_list(node_feature, now_dim)
    (y_dim, now_dim) = gen_dim_list(node_feature, now_dim)
    
    for pair_id in row_ids:
        if testing_ans != None:
            print(testing_ans[pair_id], end="", file=outfile)
        else:
            print("1", end="", file=outfile)
       
        # pair feature
        for i,column in enumerate(pair_feature):
            if pair_id not in column.value:
                continue
            if column.type == 'numerical':
                print(" %d:%f" % (pair_dim[i], column.value[pair_id]), end="", file=outfile)
            elif column.type == 'categorical':
                value_list = list(column.value[pair_id])
                value_list.sort()
                for v in value_list:
                    print(" %d:1" % (pair_dim[i] + v), end="", file=outfile)

        x_id = pair_id[0]
        y_id = pair_id[1]
 
        if node_feature != None:
            # x's feature
            for i, column in enumerate(node_feature):
                if x_id not in column.value:
                    continue
                if column.type == 'numerical':
                    print(" %d:%f" % (x_dim[i], column.value[x_id]), end="", file=outfile)
                elif column.type== 'categorical':
                    value_list = list(column.value[x_id])
                    value_list.sort()
                    for v in value_list:
                        print(" %d:1" % (x_dim[i] + v), end="", file=outfile)      

            # y's feature
            for i, column in enumerate(node_feature):
                if y_id not in column.value:
                    continue
                if column.type == 'numerical':
                    print(" %d:%f" % (y_dim[i], column.value[y_id]), end="", file=outfile)
                elif column.type== 'categorical':
                    value_list = list(column.value[y_id])
                    value_list.sort()
                    for v in value_list:
                        print(" %d:1" % (y_dim[i] + v), end="", file=outfile)
        print("", file=outfile)

def gen_dim_list(columns, offset):
    dim = list()
    now_dim = offset
    if columns != None:
        for column in columns:
            dim.append(now_dim)
            now_dim += column.dim
    return (dim, now_dim)
