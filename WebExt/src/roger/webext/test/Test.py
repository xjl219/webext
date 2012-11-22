'''
Created on 2012-11-22

@author: 19
'''
import unittest

class Test(unittest.TestCase):
    with open('../../../../data/list.txt') as testf:
        cont = testf.read()
        print cont
