from __future__ import print_function

def read_csv_column_major(filename, return_type='dict'):
    with open(filename, 'r') as f:
        first_line = f.readline()
        col_name = first_line.split(',')
        for i in range(0, len(col_name)):
            col_name[i] = col_name[i].strip()
        col_num = len(col_name)
        
        if return_type == 'dict':
            cols = dict()
            for i in range(0, len(col_name)):
                cols[col_name[i]] = list() 
        elif return_type == 'list':
            cols = [list() for i in range(0, col_num)]

        for line in f:
            entry = line.split(',')
            assert len(entry) == col_num
            if return_type == 'dict':
                for i in range(0, len(entry)):
                    cols[col_name[i]].append(entry[i].strip())
            elif return_type == 'list':
                for i in range(0, len(entry)):
                    cols[i].append(entry[i].strip())

    if return_type == 'dict':
        return cols
    elif return_type == 'list':
        return (col_name, cols)
    else:
        return None

def write_csv_column_major(col_name, cols, filename):
    with open(filename, 'w') as f:
        # first line
        f.write(col_name[0])
        for i in range(1, len(col_name)):
            f.write(',' + col_name[i])
        f.write('\n')

        first_col = cols[0]
        col_num = len(cols)
        row_num = len(first_col)
        for i in range(0, row_num):
            f.write(first_col[i])
            for j in range(1, col_num):
                f.write(',' + cols[j][i])
            f.write('\n')

def read_edges_as_set(filename):
    edges_set = set()
    with open(filename, 'r') as f:
        f.readline()
        for line in f:
            entry = line.strip().split(',')
            assert len(entry) == 2
            v1 = int(entry[0])
            v2 = int(entry[1])
            edges_set.add((min(v1, v2), max(v1, v2)))
    return edges_set

def write_training_file(training_edges_list, filename):
    with open(filename, 'w') as f:
        print('user1, user2', file=f)
        for e in training_edges_list:
            print(e[0], e[1], sep=',', file=f)
    return 

def write_testing_file(testing_edges_list, test_filename, ans_filename):
    with open(test_filename, 'w') as test_f:
        with open(ans_filename, 'w') as ans_f:
            print('user1, user2', file=test_f)
            for e in testing_edges_list:
                print(e[0][0], e[0][1], sep=',', file=test_f)
                print(e[1], file=ans_f)
    return 
