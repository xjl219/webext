'''
Created on 2012-11-27

@author: roger.luo
'''
import MySQLdb
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from numpy import savetxt

from roger.webext.db import Connect
from roger.webext.learn import GenFeatures
from roger.webext.util import Util
from roger.webext.analysis import Segment
from roger.webext.db import LoadFromFile

hpathdic = list()
tpathdic = list()
root = '../../../../train_data' 

def path_to_file(root):
    root = root + '/'
    for di in os.listdir(root):
        dpath = root + di
        if os.path.isdir(dpath):
            path_to_file(dpath)
        else:
            if str('.txt') in dpath: 
                tpathdic.append(dpath)
            else:  
                hpathdic.append(dpath)

def getMatrixFromFile():
    matrix = list()
    path_to_file(root)
    keys = GenFeatures.getDomainKeys()
    for i in range(len(tpathdic)):   
        print hpathdic[i]
        print tpathdic[i]
        with open(hpathdic[i]) as fpage:
            page = fpage.read()   
        csfr = Segment.contentSegsFromRule(page)
        segs = csfr.getConSegs()
        trecord = LoadFromFile.getRecord_from_file(tpathdic[i])
        mlines = trecord['material']
        plines = trecord['process']
        alines = []
        for seg in segs:
            print seg
            for line in mlines:
                if Util.levenshteinDist(seg,' '.join(line.split())) < 5:
                    matrix.append(getVector(seg,keys,0))
                    alines.append(seg)
            for line in plines:
                if Util.levenshteinDist(seg,' '.join(line.split())) < 5:
                    matrix.append(getVector(seg,keys,1))
                    alines.append(seg)                   
        for seg in segs:
            if seg not in alines:
                matrix.append(getVector(seg,keys,3))                    
    return matrix
                                   
def getVector(seg,keys,c):
    vec = list()
    gdf = GenFeatures.genDomainFeatures(seg,keys)
    gcf = GenFeatures.genCommFeatures(seg)
    dfd = gdf.getFeatureDict()
    cfd = gcf.getFeatureDict()
    for f in dfd:
        vec.append(dfd[f])
    for f in cfd:
        vec.append(cfd[f])   
    vec.append(c)
    return vec     
 
def getTrainData():
    mat = list()
    proces = list()
    try:
        db = Connect.db('recipe')
        db.db_connect()
        results = db.db_query("train_recipse")
        db.db_close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    for result in results:         
        mat.append(pickle.loads(result[3]))
        proces.append(pickle.loads(result[4]))
    return mat,proces
    
def getMatrix():
    mat,proces = getTrainData()
    keys = GenFeatures.getDomainKeys()
    matrix = list()
    for ma in mat:
        for m in ma:
            tmp = []
            gdf = GenFeatures.genDomainFeatures(m,keys)
            gcf = GenFeatures.genCommFeatures(m)
            dfd = gdf.getFeatureDict()
            cfd = gcf.getFeatureDict()
            for f in dfd:
                tmp.append(dfd[f])
            for f in cfd:
                tmp.append(cfd[f])
            tmp.append(1)
            matrix.append(tmp)
            tmp = []
    for pro in proces:
        for pr in pro:
            tmp = []
            gdf = GenFeatures.genDomainFeatures(pr,keys)
            gcf = GenFeatures.genCommFeatures(pr)
            dfd = gdf.getFeatureDict()
            cfd = gcf.getFeatureDict()
            for f in dfd:
                tmp.append(dfd[f])
            for f in cfd:
                tmp.append(cfd[f])
            tmp.append(0)
            matrix.append(tmp)
            tmp = []
    return matrix
 
def main():
    #create the training & test sets, skipping the header row with [1:]  
    matrix = getMatrixFromFile()
    target = [x[-1] for x in matrix]
    train = [x[:-1] for x in matrix]
    test = train
    #create and train the random forest
    #multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(train, target)
    predicted_probs = [x[1] for x in rf.predict_proba(test)]

    savetxt('submission.csv', predicted_probs, delimiter=',', fmt='%f')

#if __name__=="__main__":
#main()
getMatrixFromFile()
