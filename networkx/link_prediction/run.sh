#!/bin/bash
path=../gen_data
./link_prediction.py $path/train.csv $path/test.csv $path/test.ans $path/lenders.csv $path/loans.csv train.dat test.dat
./liblinear-1.94/train train.dat
./liblinear-1.94/predict test.dat train.dat.model test.predict
