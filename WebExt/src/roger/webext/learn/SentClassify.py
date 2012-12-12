'''
Created on 2012-11-27

@author: roger.luo
'''
import MySQLdb
import pickle
import os
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.tree import DecisionTreeClassifier
#from numpy import savetxt
#from sklearn.cross_validation import cross_val_score

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
    tpathdic.sort()
    hpathdic.sort()
    keys = GenFeatures.getDomainKeys()
    for i in range(len(tpathdic)):   
        with open(hpathdic[i]) as fpage:
            page = fpage.read()   
        csfr = Segment.contentSegsFromRule(page)
        segs = csfr.getConSegs()
        trecord = LoadFromFile.getRecord_from_file(tpathdic[i])
        mlines = trecord['material']
        plines = trecord['process']
        alines = []
        for seg in segs:
            for line in mlines:
                if Util.levenshteinDist(seg,' '.join(line.split())) < 5:
                    matrix.append(getVector(seg,keys,0))
                    alines.append(seg)
                else:
                    matrix.append(getVector(line,keys,0))
            for line in plines:
                if Util.levenshteinDist(seg,' '.join(line.split())) < 5:
                    matrix.append(getVector(seg,keys,1))
                    alines.append(seg)  
                else:
                    matrix.append(getVector(line,keys,1))                 
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

def genVector(seg,keys):
    vec = list()
    gdf = GenFeatures.genDomainFeatures(seg,keys)
    gcf = GenFeatures.genCommFeatures(seg)
    dfd = gdf.getFeatureDict()
    cfd = gcf.getFeatureDict()
    for f in dfd:
        vec.append(dfd[f])
    for f in cfd:
        vec.append(cfd[f])   
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

def plotClassify(i,j):
    import pylab as pl
    from matplotlib import colors
    with open('../../../../mid_dest/matrix.pk') as f:
        X = pickle.load(f)
    cmap = colors.LinearSegmentedColormap('red_blue_classes',
    {'red': [(0, 1, 1), (1, 0.7, 0.7)],
     'green': [(0, 0.7, 0.7), (1, 0.7, 0.7)],
     'blue': [(0, 0.7, 0.7), (1, 1, 1)]})
    pl.cm.register_cmap(cmap=cmap)
    pl.figure()
    pl.title("Classify")
    pl.xlabel("Feature x")
    pl.ylabel("Feature y")
    pl.xlim(0,1)
    pl.ylim(0,1)
    t = len(X[1])
    for x in X:
        if x[t-1] == 0:
            pl.plot(x[i], x[j],'o', color='red')
        elif x[t-1] == 1:
            pl.plot(x[i], x[j],'o', color='green')
        else:
            pl.plot(x[i], x[j],'.', color='blue')
    pl.show()

def extractSeg(segs):
    with open('../../../../mid_dest/keys.pk') as f:
        keys = pickle.load(f)
    with open('../../../../mid_dest/sentClassify.pk') as f:
        cf = pickle.load(f)  
    invec = list()
    mat = list()
    pro = list()
    for seg in segs:
        invec.append(genVector(seg,keys))
    predicted = [x for x in cf.predict(invec)]
    for i in range(len(predicted)):
        if predicted[i] == 0:
            mat.append(segs[i])
        elif predicted[i] == 1:
            pro.append(segs[i])
    return mat,pro

def main():
    pass
    #create the training & test sets, skipping the header row with [1:]  
#    with open('../../../../mid_dest/matrix.pk') as f:
#        matrix = pickle.load(f)
#    target = [x[-1] for x in matrix]
#    train = [x[:-1] for x in matrix] 

#    with open('../../../../mid_dest/sentClassify.pk') as f:
#        rf = pickle.load(f)
#    test = train
#    create and train the random forest
#    multi-core CPUs can use: rf = RandomForestClassifier(n_estimators=100, n_jobs=2)
#    rf = RandomForestClassifier(n_estimators=100,n_jobs=4)
#    rf = DecisionTreeClassifier(random_state=0)
#    rf.fit(train, target)
#    with open('../../../../mid_dest/sentClassify.pk','w') as f:
#        pickle.dump(rf, f)
#    predicted_probs = [x for x in rf.predict(test)]
#    savetxt('submission.csv', predicted_probs, delimiter=',', fmt='%f')

#if __name__=="__main__":

def test():
#    plotClassify(4,5)
    with open('../../../../train_data/10/1.htm') as f:
        page = f.read() 
    csfr = Segment.contentSegsFromRule(page)
    segs = csfr.getConSegs()
    mat,pro = extractSeg(segs)
    print mat
    print pro
    
test()

    
