#!/bin/bash
path=../../gen_pokec_data
exec_path=../../liblinear-1.94
./link_prediction.py $path/train.csv $path/test.csv $path/test.ans $path/pre_nodes_profile.csv config.json train.dat test.dat
$exec_path/train train.dat
$exec_path/predict test.dat train.dat.model test.predict
