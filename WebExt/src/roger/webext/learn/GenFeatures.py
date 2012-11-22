'''
Created on 2012-11-22

@author: 19
'''

import re

class genFeatures():
    
    def __init__(self,segs,keys):
        self.segs = segs
        self.scoreMatrix = dict()
        self.keys = keys 
    
    def initScoreMatrix(self):
        for seg in self.segs:
            kwratio = self.kwRatio(seg,self.keys[0])
            kwpos = self.kwPos(seg,self.keys[0])
            digitpos = self.digitPos(seg)
            contratio = self.conRatio(seg)
            advratio = self.advRatio(seg,self.keys[1])

            self.scoreMatrix[seg] = [kwratio,kwpos,digitpos,contratio,advratio]
    
    def getScoreMatrix(self):
        self.initScoreMatrix()
        return self.scoreMatrix

    def kwRatio(self,seg,keywords):
        leng = len(seg)
        num = 0
        for kw in keywords:
            if kw in seg:
                num = num + 1
        kwratio = num * 1.0 / leng
        return kwratio

    def kwPos(self,seg,keywords):
        leng = len(seg)
        pos = 0
        num = 0
        kavrpos = 0
        for kw in keywords:
            if kw in seg:
                pos = seg.find(kw) + pos
                num = num + 1
        if num != 0:
            kavrpos = pos * 1.0 / (num * leng)
        return kavrpos
                
    def digitPos(self,seg):
        prevpos = 0
        pos = 0
        num = 0
        avrpos = 0
        digit = re.findall('\d+',seg)
        for d in digit:    
            pos = seg.find(d) - prevpos - len(d) + pos
            prevpos = seg.find(d,0)
            num = num + 1
        if num != 0:
            avrpos = pos * 1.0 / num 
        return avrpos

    def conRatio(self,seg):
        leng = len(seg)
        con = leng - len(re.findall('\W',seg)) + len(re.findall(' ',seg))
        contratio = con * 1.0 / leng
        return contratio

    def advRatio(self,seg,advwords):
        leng = len(seg)
        num = 0
        for aw in advwords:
            if aw in seg:
                num = num + 1
        advratio = num * 1.0 / leng
        return advratio
