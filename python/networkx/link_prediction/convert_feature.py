#!/usr/bin/env python
from __future__ import print_function
import math

FLOAT_ERR = 10e-15

def float_eq(a, b):
    if math.fabs(a - b) < FLOAT_ERR:
        return True
    else:
        return False

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-1.0 * x))

# normalize the value to [-1, 1] (for numerical column)
def normalize_column(column, normalize='sigmoid'):
    assert column.type == 'numerical'
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

def convert_to_dummy_variable(column):
    assert column.type == 'categorical'
    return 

def convert_to_svm_format(row_ids, columns, outfile, testing_ans = None):
    dim = list()
    now_dim = 1 
    for column in columns:
        dim.append(now_dim)
        now_dim += column.dim
    
    for r_id in row_ids:
        if testing_ans != None:
            print(testing_ans[r_id], end="", file=outfile)
        else:
            print("1", end="", file=outfile)
        for i,column in enumerate(columns):
            if r_id not in column.value:
                continue
            if column.type == 'numerical':
                print(" %d:%f" % (dim[i], column.value[r_id]), end="", file=outfile)
            elif column.type == 'categorical':
                print(" %d:1" % (dim[i] + column.value[r_id]), end="", file=outfile)
        print("", file=outfile)
    return 
