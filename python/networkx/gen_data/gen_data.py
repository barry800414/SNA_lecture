#!/usr/bin/env python
from __future__ import print_function
import sys
import datetime
import random
from database import *
from sql_cmd import *

# data configuration
lending_action_table = 'lending_actions'
lender_table = 'lenders'
loan_table = 'loans'

lender_column = ['lenders.lender_id', 'country_code', 'inviter_id', 'invitee_count', 'loan_count']
lender_column_name = ['lender_id', 'country_code', 'inviter_id', 'invitee_count', 'loan_count']

loan_column = ['loans.loan_id', 'sector', 'amount', 'borrowers', 'country', 'geo']
loan_column_name = ['loan_id', 'sector', 'amount', 'borrowers', 'country', 'geo']

def fetch_all(cmd, error_message):
    try:
        cursor.execute(cmd)
        rows = cursor.fetchall()
        return rows
    except:
        print('Error: unable to fetch data, (%s)' % (error_message))
        return None

def fetch_one(cmd, error_message):
    try:
        cursor.execute(cmd)
        row = cursor.fetchone()
        return row
    except:
        print('Error: unable to fetch data, (%s)' % (error_message))
        return None

def get_date(string):
    # format: yyyy-mm-dd
    date = string.split('-')
    assert len(date) == 3
    out_str = "%d-%02d-%02d" % (int(date[0]), int(date[1]), int(date[2])) 
    return out_str

def get_lending_action(from_date, to_date):
    _where = "WHERE date >= '%s' AND date < '%s' AND lender_id IS NOT NULL AND loan_id IS NOT NULL" % (from_date, to_date)
    cmd = gen_select_cmd(["lender_id", "loan_id"], lending_action_table, where = _where)
    rows = fetch_all(cmd, 'lending_action table')
    return rows

def get_lenders(from_date, to_date):
    _where = "WHERE date >= '%s' AND date < '%s' AND lender_id IS NOT NULL AND loan_id IS NOT NULL" % (from_date, to_date)
    cmd = '(' + gen_select_cmd(['DISTINCT(lender_id)'], lending_action_table, where = _where) + ') as T1'
    table = cmd + ' LEFT JOIN %s ON T1.lender_id = %s.lender_id' % (lender_table, lender_table)
    cmd = gen_select_cmd(lender_column, table)
    rows = fetch_all(cmd, 'lending_action & lender table')
    return rows

def get_loans(from_date, to_date):
    _where = "WHERE date >= '%s' AND date < '%s' AND lender_id IS NOT NULL AND loan_id IS NOT NULL" % (from_date, to_date)
    cmd = '(' + gen_select_cmd(['DISTINCT(loan_id)'], lending_action_table, where = _where) + ') as T1'
    table = cmd + ' LEFT JOIN %s ON T1.loan_id = %s.loan_id' % (loan_table, loan_table)
    cmd = gen_select_cmd(loan_column, table)
    rows = fetch_all(cmd, 'lending_action & loan table')
    return rows

# remap the first column of rows
def remap(rows):
    id_map = dict()
    new_rows = list()
    cnt = 0
    for row in rows:
        #print(row)
        if str(row[0]) not in id_map:
            id_map[str(row[0])] = cnt 
            cnt += 1
        new_row = [id_map[str(row[0])]]
        new_row.extend(row[1:])
        #print(new_row)
        new_rows.append(new_row)
    return (new_rows, id_map)

# train_percent: the percentage of training data from original data
# neg_percent: the percentage of negative instance data compare to positive data
def gen_train_and_test_file(lending_action, train_percent, neg_percent, lender_map, loan_map):
    assert train_percent > 0 and train_percent < 1
    assert neg_percent >= 0
    
    action_set = set()
    new_lending_action = list()
    for lender_id, loan_id in lending_action:
        if lender_map.has_key(str(lender_id)) and loan_map.has_key(str(loan_id)):
            new_lender_id = lender_map[str(lender_id)]
            new_loan_id = loan_map[str(loan_id)]
            action_set.add((new_lender_id, new_loan_id))
            new_lending_action.append((new_lender_id, new_loan_id))
    
    total_num = len(new_lending_action)
    train_num = int(total_num * train_percent)
    test_num = total_num - train_num

    # shuffle data and divide data
    random.shuffle(new_lending_action)
    train_action = new_lending_action[0:train_num-1]
    test_action = new_lending_action[train_num:]

    # random sample negative samples
    neg_num = int(test_num * neg_percent)
    lender_num = len(lender_map)
    loan_num = len(loan_map)
    test_neg_action = list()
    cnt = 0
    while cnt < neg_num:
        lender_id = random.randint(0, lender_num-1)
        loan_id = random.randint(0, loan_num-1)
        if (lender_id, loan_id) not in action_set:
            test_neg_action.append((lender_id, loan_id))
            cnt += 1
    return (train_action, test_action, test_neg_action)

# here the lender has been remapped
# c_index : invitee_column_index
def preprocess_inviter(lender, lender_map, c_index):
    hit_num = 0
    for row in lender:
        if row[c_index] in lender_map:
            hit_num += 1
            row[c_index] = lender_map[row[c_index]]
        else:
            row[c_index] = -1
    print('hit num:', hit_num)
    return lender


def write_train_and_test_file(train_action, test_action, test_neg_action):
    write_file('train.csv', ['lender_id', 'loan_id'], train_action)

    test_all = list()
    for lender_id, loan_id in test_action:
        test_all.append((1, lender_id, loan_id))
    for lender_id, loan_id in test_neg_action:
        test_all.append((0, lender_id, loan_id))
    random.shuffle(test_all)
    
    write_file('test.csv', ['label', 'lender_id', 'loan_id'], test_all, ignore_first_column = True)
    write_ans_file('test.ans', test_all)

# write lending_action(training) or lenders or loans file
def write_file(outfile, column, rows, ignore_first_column = False):
    with open(outfile, 'w') as f:
        first_printed = True
        for i in range(0, len(column)):
            if ignore_first_column and i == 0:
                continue
            if first_printed:
                print(column[i], end='', file=f)
                first_printed = False
            else:
                print(", %s" % (column[i]), end='', file=f)
        print('', file=f)
        for row in rows:
            first_printed = True
            for i in range(0, len(row)):
                if ignore_first_column and i == 0:
                    continue
                if first_printed:
                    print(row[i], end='', file=f)
                    first_printed = False
                else:
                    print(", %s" % (row[i]), end='', file=f)
            print('', file=f)

def write_ans_file(outfile, rows):
    with open(outfile, 'w') as f:
        for row in rows:
            print(row[0], file=f)

if __name__ == '__main__':
    if len(sys.argv) != 1+4:
        print('Usage:', sys.argv[0], 'from_date to_date train_percent negative_percent', file=sys.stderr)
        print('Date format: yyyy-mm-dd', file=sys.stderr)
        exit(-1)

    from_date = get_date(sys.argv[1])
    to_date = get_date(sys.argv[2])
    train_percent = float(sys.argv[3])
    neg_percent = float(sys.argv[4])
    print('train_percent:', train_percent)
    print('neg_percent:', neg_percent)

    db = database()
    cursor = db.cursor
    
    lender = get_lenders(from_date, to_date)
    (lender, lender_map) = remap(lender)
    lender = preprocess_inviter(lender, lender_map, 2)
    write_file('lenders.csv', lender_column_name, lender)
    print('# lenders: ', len(lender_map))

    loan = get_loans(from_date, to_date)
    (loan, loan_map) = remap(loan)
    write_file('loans.csv', loan_column_name, loan)
    print('# loans: ', len(loan_map))

    lending_action = get_lending_action(from_date, to_date)
    #print('lending actions:', len(lending_actions))
    (train_action, test_action, test_neg_action) = gen_train_and_test_file(lending_action, 
            train_percent, neg_percent, lender_map, loan_map)
    write_train_and_test_file(train_action, test_action, test_neg_action)
    print('# train: ', len(train_action))
    print('# test:', len(test_action))
    print('# test+neg:', len(test_action) + len(test_neg_action))
    print('# all original data:', len(train_action) + len(test_action)) 

