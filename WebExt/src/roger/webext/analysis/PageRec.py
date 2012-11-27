'''
Created on 2012-11-27

@author: roger.luo
'''

from sklearn import tree
X=[]
y=[]
randt = tree.ExtraTreeClassifier()
randt = randt.fit(X,y)