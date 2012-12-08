'''
Created on 2012-11-27

@author: roger.luo
'''

import os 
import re
import MySQLdb
import pickle

def path_to_file(root):
    root = root + '/'
    for di in os.listdir(root):
        dpath = root + di
        if os.path.isdir(dpath):
            path_to_file(dpath)
        else:        
           if str(".txt") in dpath:
                pathdic.append(dpath)

def getRecord_from_xml(xml):
    pass

def getRecord_from_file(file):
    rdic = dict()
    lines = list()
    with open(file) as df:
        for line in  df.readlines():
            if len(line.strip()) > 0:
                lines.append(line.strip())
    rdic['name'] = lines[1]
    rdic['url'] = lines[2][5:]

    dr = 0
    for i in range(len(lines)):
        if re.match('^directions:',lines[i].lower()) != None:
          dr = i
          break
    rdic['material'] = lines[4:dr]
    rdic['process'] = lines[dr+1:]   
    return rdic

def store_record(pathdic):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='lab123',port=3306)
        conn.select_db("recipe")
        cur=conn.cursor()
        i = 1
        for path in pathdic:
            record = getRecord_from_file(path)
            cur.execute('insert into train_recipse values(%s,%s,%s,%s,%s)',
                        [i,pickle.dumps(record['name']),pickle.dumps(record['url']),pickle.dumps(record['material']),pickle.dumps(record['process'])])
            i = i + 1
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    
def get_record(id):
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='lab123',port=3306)
        conn.select_db("recipe")
        cur=conn.cursor()
        count=cur.execute('select * from train_recipse where id_rec = %s',id)
        results=cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            results = None
    return results

def get_all():
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='lab123',port=3306)
        conn.select_db("recipe")
        cur=conn.cursor()
        count=cur.execute('select * from train_recipse')
        results=cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
            results = None
    return results   
   
#pathdic = list()
#root = '../../../../train_data'               
#path_to_file(root)
#store_record(pathdic)