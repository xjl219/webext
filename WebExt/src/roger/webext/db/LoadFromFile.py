'''
Created on Dec 8, 2012

@author: lab
'''
import os
import re
import pickle
import MySQLdb

from roger.webext.db import Connect

pathdic = list()
root = '../../../../train_data' 

def start():            
    path_to_file(root)     
    store_record(pathdic)
    return pathdic

def getRecord_from_xml(xml):
    pass

def path_to_file(root):
    root = root + '/'
    for di in os.listdir(root):
        dpath = root + di
        if os.path.isdir(dpath):
            path_to_file(dpath)
        else:
            if str('.txt') in dpath:
                pathdic.append(dpath)

def getRecord_from_file(p_file):
    rdic = dict()
    lines = list()
    with open(p_file) as df:
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
        db = Connect.db('recipe')
        db.db_connect()
        i = 1
        for path in pathdic:
            record = getRecord_from_file(path)
            db.db_insert('train_recipse',[i,pickle.dumps(record['name']),pickle.dumps(record['url']),pickle.dumps(record['material']),pickle.dumps(record['process'])])
            i = i + 1
        db.db_close()
    except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])   

#start()