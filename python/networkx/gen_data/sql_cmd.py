
def gen_select_cmd(column, table, distinct=False, where=None, order_by=None, limit=None):
    if len(column) == 0:
        column = ["*"]
    if distinct:
        cmd = "SELECT DISTINCT "
    else:
        cmd = "SELECT "
    for i in range(0,len(column)-1):
        cmd += column[i] + ','
    cmd += column[len(column)-1]
    cmd += " FROM (" + table + ") "
    if where != None:
        cmd += where
    if order_by != None:
        cmd += " ORDER BY " + order_by
    if limit != None:
        cmd += " LIMIT " + str(limit)
    return cmd

