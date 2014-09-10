#!/bin/bash

python gen_data.py ~/codes/pokec_5k/raw_edges.csv train.csv test.csv test.ans 0.7 1
python preprocess.py config.json ~/codes/pokec_5k/raw_nodes_profile.csv pre_nodes_profile.csv
