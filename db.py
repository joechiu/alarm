import sqlite3

alist = [
    {'h':2,'m':40,'s':36,'t':0,'c':1,'a':1,'r':0,'sz':32,'oc':99,'d':'Mon, Tue, Wed, Thu','name':'Alarm!','aud':'F:/dev/python/exe/alarm-2/sounds/tada.wav','msg':''},
    {'h':10,'m':41,'s':9,'t':0,'c':1,'a':0,'r':0,'sz':32,'oc':99,'d':'','name':'Hello world!','aud':'','msg':'foo bar!'},
    {'h':2,'m':40,'s':36,'t':1,'c':0,'a':1,'r':1,'sz':32,'oc':99,'d':'','name':'Message alarm!','aud':'F:/dev/python/exe/alarm-2/sounds/ringout.wav','msg':''},
    {'h':16,'m':25,'s':0,'t':0,'c':0,'a':0,'r':0,'sz':32,'oc':99,'d':'Fri','name':'foo bar!','aud':'','msg':'hello world'},
]

# data factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class db(object):
    def __init__(self, *args):
        super().__init__()
        
        self.db = 'db/pyqt-alarm.db'
        self.conn = sqlite3.connect(self.db)
        self.cc = self.conn.cursor()
        
    def list(self, id = 0):
        id = int(id)
        if id == 0:
            sql = "select * from sat"
        else:
            sql = "select * from sat where id = %d" % id
        print(sql)
        c = self.cursor()
        c.execute(sql)
        try:
            return c.fetchall()
        except:
            return []

    def cursor(self):
        self.conn.row_factory = dict_factory
        c = self.conn.cursor()
        return c

    def test(self):
        for row in self.cc.execute('select * from sat'):
            print(row)
        for row in self.c().execute('select * from sat'):
            print(row)

    def d(self, id):
        if not int(id): return
        sql = "delete from sat where id = %d" % id
        try:
            self.cc.execute(sql)
            self.conn.commit()
            return True
        except IOError as e:
            print(e)
            return False
            
    def i(self, h):
        sql = 'insert into sat ('
        sql += ','.join(h.keys())
        sql += ") values ("
        sql += ",".join('?' for x in h.values())
        sql += ")"
        print(sql)
        try:
            self.cc.execute(sql, list(h.values()))
            self.conn.commit()
            return self.cc.lastrowid
        except IOError as e:
            print(e)
            
    def u(self, h):
        sql = 'update sat set '
        kv = []
        for key in h.keys():
            kv.append("{k}=?".format(k=key))
        sql += ','.join(kv)
        sql += ' where id = %d' % h['id']
        print(sql, "\n", h)
        try:
            self.conn.execute(sql, list(h.values()))
            self.conn.commit()
        except IOError as e:
            print(e)
            
    def c(self, i, v):
        self.u({'id':i,'c':v})
            
    def new(self):
        h = {
            'name':'New alarm',
            'h':0,
            'm':0,
            's':0,
            't':0,
            'a':1,
            'r':0,
            'd':'',
            'c':0,
            'aud':'',
            'msg':'',
        }
        return self.i(h)
    
    def sql(self):
        # handy sql if need to init data
        for h in alist:
            sql = 'insert into sat ('
            sql += ','.join(h.keys())
            sql += ") values ('"
            sql += "','".join(str(s) for s in h.values())
            sql += "');"
            print(sql)
            
    def close(self):
        self.conn.close()

def go():
    d = db()
    # d.test()    
    d.sql()
    
# go()