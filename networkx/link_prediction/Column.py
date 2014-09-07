
# The class to store the values of one column
class Column():
    def __init__(self, dim, type):
    	#self.value[row_id] is the feature values of 'row_id' item in this column
        self.value = dict()   
        self.type = type
        self.dim = dim

