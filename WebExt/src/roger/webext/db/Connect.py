'''
Created on 2012-11-22

@author: roger.luo
'''
import MySQLdb

class db():   
    def __init__(self,name_t):
        self.conn = None
        self.name_t = name_t
        
    def db_connect(self):
        self.conn=MySQLdb.connect(host='localhost',user='root',passwd='lab123',port=3306)
        self.conn.select_db(self.name_t)
           
    def db_close(self):
        self.conn.close()
    
    def db_insert(self,tab,values):
        cur = self.conn.cursor()
        cur.execute('insert into {0} values {1}'.format(tab,tuple(values)))
        self.conn.commit()
        cur.close()
        
    def db_query(self,tab,id_rec = None):
        cur = self.conn.cursor()
        if id_rec == None:
            cur.execute('select * from %s' % (tab))
        else:
            cur.execute('select * from %s where id_rec = %s' % (tab,id_rec))
        results=cur.fetchall()
        self.conn.commit()
        cur.close()
        return results