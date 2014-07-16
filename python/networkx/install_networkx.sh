tar -zxvf networkx-1.9.tar.gz
cd networkx-1.9
python setup.py build
python setup.py install --prefix=$HOME
python3 setup.py build
python3 setup.py install --prefix=$HOME
