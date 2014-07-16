#!/bin/bash
path=../../gen_data
./link_prediction.py $path/train.csv $path/test.csv $path/test.ans $path/lenders.csv $path/loans.csv train.dat test.dat
# Task 7 Edit here: call liblinear to train and test
