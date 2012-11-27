'''
Created on 2012-11-22
    SVM Classification Application for Extraction Target
@author: roger.luo
'''

print __doc__

from sklearn.tree import DecisionTreeClassifier
from roger.webext.analysis import Segment
from roger.webext.learn import GenFeatures

trainSeg = []
trainNoseg = []    
traindata = []
traintarget = []
testdata = []


with open('./train/process.txt') as pro:
    for line in pro.readlines():
        trainSeg.append(line.strip('\n'))
with open('./train/noprocess.txt') as nopro:
    for line in nopro.readlines():
        trainNoseg.append(line.strip('\n'))  
features = GenFeatures.getKeys()
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
    
