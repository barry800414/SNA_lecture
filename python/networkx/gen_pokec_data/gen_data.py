#!/usr/bin/env python
from __future__ import print_function
import sys
import networkx as nx
import random
import sample_graph

def get_mapping(nodes_set):
    mapping = dict()
    cnt = 0
    for n in nodes_set:
        mapping[n] = cnt
        cnt += 1
    return mapping

if len(sys.argv) != 5:
    print('Usage:', sys.argv[0], 'edges nodes column goal_num', file=sys.stderr)
    exit(-1)

edge_file = sys.argv[1]
node_file = sys.argv[2]
node_column = sys.argv[3]
goal_num = int(sys.argv[4])

g = nx.Graph()

print('read in edges')
count = 0 
# read in edges
with open(edge_file, 'r') as f:
    for line in f:
        entry = (line.strip()).split('\t')
        g.add_edge(int(entry[0]), int(entry[1]))
        count += 1
        if count % 1000000 == 0:
            print(count)

# random sample graph
print('sampling graph')


'''
now_num = 1
nodes_list = g.nodes()
r = random.randint(0, len(nodes_list) - 1)
selected = set()
selected.add(nodes_list[r])
candidate = set(g.neighbors(nodes_list[r]))
while now_num < goal_num:
    assert len(candidate) != 0
    n = random.sample(candidate, 1)
    selected.add(n[0])
    candidate.update(set(g.neighbors(n[0])))
    now_num += 1
    if now_num % 1000 == 0:
        print(now_num)

mapping = get_mapping(selected)

# get node induced graph
new_g = nx.Graph()
for n1 in selected:
    nei = set(g.neighbors(n1))
    intersect = nei & selected
    for n2 in intersect:
        new_g.add_edge(n1, n2)
'''

(sampled_node_set, sampled_edge_set) = sample_graph.sample_graph1(g, goal_num)
mapping = get_mapping(sampled_node_set)

print('Output edges')
outfile = open('edges.txt', 'w')
for edge in sampled_edge_set:
    print(mapping[edge[0]], mapping[edge[1]], file=outfile)
outfile.close()

print('read in column names')
# read in node column
cols = list()
with open(node_column, 'r') as f:
    for line in f:
        cols.append(line.strip())

print('read in and write node feature')
# read in and write node feature
outfile = open('nodes_profile.csv', 'w')
# write the first column
for i in range(0, len(cols)-1):
    print(cols[i], end=",", file=outfile)
print(cols[len(cols)-1], end='\n', file=outfile)

count = 0 
with open(node_file, 'r') as f:
    for line in f:
        line = line.strip()
        i = line.index('\t')
        node_id = int(line[0:i])
        if node_id in sampled_node_set:
            print(mapping[node_id], end=",", file=outfile)
            feature = line[i+1:].replace(',', '#$#$#$#')
            feature = feature.replace('\t', ',')
            print(feature, file=outfile)
            count += 1
outfile.close()
print(count)

