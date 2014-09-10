#!/usr/bin/env python
from __future__ import print_function
import sys
import networkx as nx
import math
import random
from collections import defaultdict

from Column import *

'''
Author: Wei-Ming Chen (MSLab, CSIE, NTU)
Contacts: barry800414@gmail.com
'''

'''
graph: the training graph 
pairs: the pairs of nodes to extract features
       pairs[i][0] denotes the node_1 of i-th pair
       pairs[i][1] denotes the node_2 of i-th pair
'''

NO_PATH_LENGTH = 1000

# get shortest path length for all edges
def get_shortest_path_length(graph, pairs):
    c = Column(1, 'numerical')
    value = dict()
    for pair in pairs:
        n1 = pair[0]
        n2 = pair[1]
        try:
            # TODO Task_1: EDIT HERE, please find shortest 
            # path from n1 to n2
            # value[pair] = ooxx
            pass
        except:
            value[pair] = NO_PATH_LENGTH
    c.value = value
    return c

