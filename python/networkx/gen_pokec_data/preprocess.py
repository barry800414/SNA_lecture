#!/usr/bin/env python
from __future__ import print_function 
from collections import defaultdict
from HTMLParser import HTMLParser
import json

SEP = '#$#$#$#'
NEW_SEP = '\t'

class MyHTMLParser(HTMLParser):
    def init(self):
        self.accepted_tags = set(['a'])
        self.extract_attrs = set(['href'])
        self.in_accepted_tags = False
        self.replace = [('/klub/', '')]
        self.parsed_result = ''

    def clear_result(self):
        self.parsed_result = ''

    def handle_starttag(self, tag, attrs):
        #print('=================================')
        #print('start_tag:', tag)
        #print('attrs:', attrs)
        if tag in self.accepted_tags:
            self.in_accepted_tags = True
        else:
            self.in_accepted_tags = False

        if self.in_accepted_tags:
            for attr in attrs:
                if attr[0] in self.extract_attrs:
                    if len(self.parsed_result) == 0:
                        self.parsed_result = self.__filter_str(attr[1])
                    else:
                        self.parsed_result += NEW_SEP + self.__filter_str(attr[1])
                    #print('attrs[%s]:' % (attr[0]), self.__filter_str(attr[1]))

    def handle_endtag(self, tag):
        pass
        #print('end_tag:', tag)
    def handle_data(self, data):
        pass
        #print('data:', data)

    def __filter_str(self, string):
        target_str = str(string)
        for r in self.replace:
            new_str = target_str.replace(r[0], r[1])
            target_str = new_str
        return target_str

# preprocess the 'free_text' column in raw data
def free_text_preprocess(column, min_times=2):
    wf = defaultdict(int)
    for element in column:
        entry = element.split(SEP)
        for e in entry:
            wf[e.strip()] += 1
    items = list(wf.items())
    items.sort(key = lambda x:x[1], reverse=True)
    #for w, f in items:
        #print(w, ':' , f)

    new_column = list()
    for element in column:
        entry = element.split(SEP)
        new_element = ''
        for e in entry:
            w = e.strip()
            if wf[w] >= min_times and len(w) > 0 and hasEngLetter(w):
                if len(new_element) == 0:
                    new_element += w
                else:
                    new_element += NEW_SEP + w
        if len(new_element) != 0:
            new_column.append(new_element)
        else:
            new_column.append('null')
    return new_column

# preprocess the 'categorical' column in raw data
def categorical_preprocess(column):
    new_column = list()
    for element in column:
        entry = element.split(SEP)
        new_element = ''
        for e in entry:
            w = e.strip()
            if len(w) > 0 and hasEngLetter(w):
                if len(new_element) == 0:
                    new_element += w
                else:
                    new_element += NEW_SEP + w
        if len(new_element) != 0:
            new_column.append(new_element)
        else:
            new_column.append('null')
    return new_column

def hasEngLetter(string):
    for i in range(0, len(string)):
        if string[i] >= 'a' and string[i] <= 'z':
            return True
        elif string[i] >= 'A' and string[i] <= 'Z':
            return True
    return False

# preprocess the 'numeric' column in raw data
def numeric_preprocess(column):
    return column

# preprocess the 'html_text' column in raw data
def html_text_preprocess(column):
    parser = MyHTMLParser()
    parser.init()

    new_column = list()
    for element in column:
        parser.clear_result()
        parser.feed(element)
        new_element = parser.parsed_result
        if len(new_element) != 0:
            new_column.append(new_element)
        else:
            new_column.append('null')
    return new_column


# main procedure 
import sys
from file_io import *
if __name__=='__main__':
    if len(sys.argv) != 4:
        print(sys.argv, 'config_file in_file out_file', file=sys.stderr)
        exit(-1)
    
    # read in arguments
    config_file = sys.argv[1]
    in_file = sys.argv[2]
    out_file = sys.argv[3]

    # read configuration file
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # read raw data
    [col_names, cols] = read_csv_column_major(in_file, return_type='list')
    assert len(col_names) == len(cols)

    # preprocess the raw data according to configuration file
    new_cols = list()
    new_col_names = list()
    for i in range(0, len(cols)):
        col_name = col_names[i]
        col = cols[i]
        if config[col_name] == 'free_text':
            #print('=================%s===============' % col_name)
            new_cols.append(free_text_preprocess(col))
            new_col_names.append(col_name)
        elif config[col_name] == 'html_text':
            new_cols.append(html_text_preprocess(col))
            new_col_names.append(col_name)
        elif config[col_name] == 'numeric':
            new_cols.append(numeric_preprocess(col))
            new_col_names.append(col_name)
        elif config[col_name] == 'categorical':
            new_cols.append(categorical_preprocess(col))
            new_col_names.append(col_name)
        elif config[col_name] == 'time':
            pass
        elif config[col_name] == 'remove':
            pass
        elif config[col_name] == 'body':
            pass
        elif config[col_name] == 'none':
            new_cols.append(col)
            new_col_names.append(col_name)
        print(col_name, file=sys.stderr)

    '''
    print(new_col_names)
    for i in range(34, 35):
        print(new_col_names[i])
        #print(new_cols[i])
        for e in new_cols[i]:
            print(e)
    '''
    write_csv_column_major(new_col_names, new_cols, out_file)


