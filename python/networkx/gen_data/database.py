
import MySQLdb

class database():
    def __init__(self):
        host = "140.112.187.33"
        port_n = 3666
        user = "root"
        database = "kiva"
        pw = "9500354"
        self.db = MySQLdb.connect(host, user, pw, database, port=port_n)
        self.cursor = self.db.cursor()

