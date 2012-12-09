'''
Created on 2012-11-22

@author: roger.luo
'''
import os
import re
import nltk
from nltk.tokenize import RegexpTokenizer, wordpunct_tokenize

sdir = '../../../../domain_data/'

def getDomainKeys():
    keys = dict()
    keyvalues = list()
    for di in os.listdir(sdir):
        with open(sdir+di) as f:
            for line in f.readlines():
                keyvalues.append(line.strip().lower())
        keys[di[:-4]] = keyvalues
        keyvalues = []
    return keys

class genDomainFeatures():
    
    def __init__(self,seg,keys):
        self.seg = seg
        self.featureDict = dict()
        self.keys = keys 
    
    def getFeatureDict(self):
        self.countRatio()
        self.allKeysRatio()
        return self.featureDict
        
    def countRatio(self):
        tokenp = wordpunct_tokenize(self.seg)
        tokenizer = RegexpTokenizer('\s+',gaps=True)
        tokens = tokenizer.tokenize(self.seg)
        l = len(tokens)
        for key in self.keys:
            coms = [elem for elem in tokenp if elem.lower() in self.keys[key]]
            ratio = len(coms) * 1.0 / l
            self.featureDict[key+'_countRatio'] = ratio
                 
    def allKeysRatio(self):
        tokenp = wordpunct_tokenize(self.seg)
        tokenizer = RegexpTokenizer('\s+',gaps=True)
        tokens = tokenizer.tokenize(self.seg)
        keyset = set()
        for key in self.keys:
            keyset = keyset.union(set(self.keys[key]))
        coma = [elem for elem in tokenp if elem.lower() in keyset]
        self.featureDict['all_Ratio'] = len(coma) * 1.0 / len(tokens)
            
    
class genCommFeatures():
    
    def __init__(self,seg):
        self.seg = seg
        self.featureDict = dict()
    
    def getFeatureDict(self):
        self.commaRatio()
        self.endWithComma()
        self.nunAndVerbRatio()
        return self.featureDict
    
    def commaRatio(self):   
        tokenp = wordpunct_tokenize(self.seg)
        tokenizer = RegexpTokenizer('\s+',gaps=True)
        tokens = tokenizer.tokenize(self.seg)
        num = len(tokenp) - len(tokens)
        self.featureDict['commaRatio'] = num *1.0/len(tokenp)
    
    def startWithDigit(self):
        if re.search('^\d',self.seg):
            self.featureDict['startWithDigit'] = 1
        else:
            self.featureDict['startWithDigit'] = 0
    
    def endWithComma(self):
        if re.search('\W$',self.seg):
            self.featureDict['endWithComma'] = 1
        else:
            self.featureDict['endWithComma'] = 0
    
    def nunAndVerbRatio(self):
        token = wordpunct_tokenize(self.seg)
        tag = nltk.pos_tag(token)
        nnum = 0
#        vnum = 0
        for t in tag:
            if re.search('^N',t[1]):
                nnum = nnum + 1
#            if re.search('^V',t[1]):
#                vnum = vnum + 1
        tokenizer = RegexpTokenizer('\s+',gaps=True)
        tokens = tokenizer.tokenize(self.seg)
        self.featureDict['nunRatio'] = nnum * 1.0 /(len(tokens))
#        self.featureDict['verbNum'] = vnum
        if len(tag) > 3 and re.search('LS',tag[0][1]) and (re.search('N',tag[1][1]) or re.search('N',tag[2][1])):
            self.featureDict['simpleGram'] = 1
        else:
            self.featureDict['simpleGram'] = 0
