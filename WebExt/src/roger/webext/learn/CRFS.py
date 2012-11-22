'''
Created on 2012-11-22
    SVM Classification Application for Extraction Target
@author: 19
'''

print __doc__

from sklearn.tree import DecisionTreeClassifier
import codecs
from roger.webext.analysis import Segment
from roger.webext.learn import GenFeatures

trainSeg = []
trainNoseg = []    
traindata = []
traintarget = []
testdata = []

def getKeys():
    keywords = []
    advs = []
    with codecs.open('./train/foodlist.txt',encoding='utf-8') as food:
        for line in food.readlines():
            keywords.append(line.strip('\n'))
    with codecs.open('./train/burden.txt',encoding='utf-8') as burden:
        for line in burden.readlines():
            keywords.append(line.strip('\n'))
    with codecs.open('./train/adv.txt',encoding='utf-8') as adv:
        for line in adv.readlines():
            advs.append(line.strip('\n'))    
    return [keywords,advs]

with codecs.open('./train/process.txt',encoding='utf-8') as pro:
    for line in pro.readlines():
        trainSeg.append(line.strip('\n'))
with codecs.open('./train/noprocess.txt',encoding='utf-8') as nopro:
    for line in nopro.readlines():
        trainNoseg.append(line.strip('\n'))  
features = getKeys()
trainSC = GenFeatures.genFeatures(trainSeg,features)
trainNSC = GenFeatures.genFeatures(trainNoseg,features)
tM = trainSC.getScoreMatrix()
tNM = trainNSC.getScoreMatrix()

for segM in tM:
    recM = tM[segM]
    traindata.append(recM)
    traintarget.append(1)
for segN in tNM:
    rec = tNM[segN]
    traindata.append(rec)
    traintarget.append(0)
X = traindata
Y = traintarget
clf = DecisionTreeClassifier(random_state=0)
clf.fit(X,Y)
with open('1.html') as f:
    source = f.read()
conEx = Segment.contentExtractor(source)
segSC = GenFeatures.genFeatures(conEx.getSegement(),features)
sM = segSC.getScoreMatrix()
for segs in sM:
    rec = sM[segs]
    testdata.append(rec)

Z = clf.predict(testdata)
num = 0
for segs in sM:
    print segs,Z[num]
    num = num + 1
    
