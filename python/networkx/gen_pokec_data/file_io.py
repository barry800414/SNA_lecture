
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


def read_csv_row_major(filename):
    pass 


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

