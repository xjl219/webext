'''
Created on 2012-11-27

@author: roger.luo
'''

#from roger.webext.analysis import Segment
import re
import os
import pickle
from bs4 import BeautifulSoup
from roger.webext.learn import GenFeatures
from sklearn.tree import DecisionTreeClassifier

pathdic = list()
root = '../../../../train_data' 

def rmTag(page):
    soup = BeautifulSoup(page)
    for tag in soup.find_all(re.compile('script$|style')):
        tag.decompose()
    soup = soup.find('body')
    for tag in soup.find_all(True):
        tag.unwrap()
    return repr(soup.getText("\r\n",strip=True))

def genVector(text):
    vec = list()
    with open('../../../../mid_dest/keys.pk') as f:
        keys = pickle.load(f)   
    gdf = GenFeatures.genDomainFeatures(text,keys)
    vecdic = gdf.getFeatureDict()
    for v in vecdic:
        vec.append(vecdic[v])
    return vec

def path_to_file(root):
    root = root + '/'
    for di in os.listdir(root):
        dpath = root + di
        if os.path.isdir(dpath):
            path_to_file(dpath)
        else:
            if str('.htm') in dpath:
                pathdic.append(dpath)
                
def genMatrix():
    path_to_file(root)
    matrix = list()
    junkpath = list()
    for path in pathdic:
        with open(path) as f:
            page = f.read()
        text = rmTag(page)
        vec = genVector(text) 
        vec.append(1)
        matrix.append(vec)
    for path in junkpath:
        with open(path) as f:
            page = f.read()
        text = rmTag(page)
        vec = genVector(text) 
        vec.append(0)
        matrix.append(vec)
    return matrix
   
def isRecipePage(page):
    vec = genVector(page)
    with open('../../../../mid_dest/pageClassify.pk','w') as f:
        pf = pickle.load(f)
    if pf.predict(vec) == 0:
        return False
    else:
        return True
     

def main():
    matrix = genMatrix()
    X = [x[:-1] for x in matrix]
    y = [x[-1] for x in matrix]
    pf = DecisionTreeClassifier(random_state=0)
    pf.fit(X,y)
    print pf.predict([0.02456418383518225, 0.030110935023771792, 0.06814580031695722, 0.13549920760697307, 0.06735340729001585])
#    with open('../../../../mid_dest/pageClassify.pk','w') as f:
#        pickle.dump(pf, f)
main()