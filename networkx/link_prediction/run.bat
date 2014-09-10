python .\link_prediction.py ..\..\gen_pokec_data\train.csv ..\..\gen_pokec_data\test.csv ..\..\gen_pokec_data\test.ans ..\..\gen_pokec_data\pre_nodes_profile.csv config.json train.dat test.dat
..\liblinear-1.94\windows\train.exe train.dat
..\liblinear-1.94\windows\predict.exe test.dat train.dat.model test.predict
pause
