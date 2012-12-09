'''
Created on 2012-11-27

@author: roger.luo
'''
import MySQLdb
import pickle
from sklearn.ensemble import RandomForestClassifier
from numpy import savetxt

from roger.webext.db import Connect
from roger.webext.learn import GenFeatures

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

def getTrainMatrix():
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
    matrix = getTrainMatrix()
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
main()