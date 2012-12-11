'''
Created on 2012-11-22

@author: roger.luo
'''
from bs4 import BeautifulSoup
import bs4
import re

class contentExtractor():   #for chinese
    """Main content extractor"""
    def __init__(self,page):
        self.text = BeautifulSoup(page)
        self.segments = []

    def getSegement(self):
        self.rmvJunk()
        segements = []
        contents = self.text.find('body').find_all(self.isLeafContentTag)
        
        for segement in contents:
            seg,leng = self.trimAll(segement)
            sl = len(str(segement)) - len(str(segement.get_text().encode('utf-8'))) + leng
            ratio = leng * 1.0 / sl
            if ratio > 0.2:
                segements.append(seg)

        return segements

    def rmvJunk(self):
        scripts = self.text.find_all(['script','style','noscript'])
        for script in scripts:
            script.decompose()
        elems = self.text.find('body').find_all(['p','div'])
        for elem in elems:
            if len(elem.get_text()) < 1 and elem.img == None:
                elem.extract()

    def trimAll(self,segement):
        leng = 0
        seg = str('')
        for string in segement.stripped_strings:
            leng += len(string.encode('utf-8'))
            seg += string
        return seg,leng

    def isLeafContentTag(self,tag):
        if tag.name in set(['p','div']) or re.match("^h[1-6]",tag.name):
            if(tag.descendants != None):
                for child in tag.descendants:
                    if isinstance(child,bs4.element.Tag):
                        if child.name in set(['p','div']) or re.match("^h[1-6]",tag.name):
                            return False
                        else:
                            continue
                return True
            else:
                return True

class domTree():
    
    def __init__(self,page):
        self.soup = BeautifulSoup(page)#can use 'lxml' 'html5lib' parser and others
        self.tree = dict()
    
    def findMaxNode(self):
        pass    
    
    def backTraceTree(self):
        pass
 
 
class contentSegsFromRule():
    
    def __init__(self,page):    
        self.soup = BeautifulSoup(page)
        self.segs = list()
    
    def getConSegs(self):
        for tag in self.soup.find_all(re.compile("script$|style$")):
            tag.decompose()
        for tag in self.soup.find_all(['span','b','em','strong','u','br']):
            tag.unwrap()
        for tag in self.soup.find_all(self.bigLTTRatio):
            tag.extract()
        for tag in self.soup.find_all('img'):
            tag.extract()
        for tag in self.soup.find_all('a'):
            tag.extract()
        for tag in self.soup.find_all(self.contentLeafTag):
            st = tag.getText(strip=True)
            if len(st) > 0:
                self.segs.append(repr(' '.join(st.split())))
        return self.segs

    def contentLeafTag(self,tag):
        if tag.name in set(['p','div','li','ul']) or re.match("^h[1-6]",tag.name):
            if(tag.descendants != None):
                for child in tag.descendants:
                    if isinstance(child,bs4.element.Tag):
                        if child.name in set(['p','div','li','ul']) or re.match("^h[1-6]",tag.name):
                            return False
                        else:
                            continue
                return True
            else:
                return True
            
            
    def bigLTTRatio(self,tag):
        if tag.name in set(['p','div','li','ul']):
            if(tag.descendants != None):
                nn = 0
                an = 0
                for child in tag.descendants:
                    if isinstance(child,bs4.element.Tag):
                        nn = nn + 1
                        if child.name == 'a':
                            an = an + 1
                if nn != 0 and (an * 1.0 / nn >  0.5):
                    return True

