'''
Created on 2012-12-10

@author: 19
'''
def levenshteinDist(s, t):
    if len(s) > len(t):
        s, t = t, s
    n = len(s)
    m = len(t)
    if not m : return n
    if not n : return m
    v0 = [ i for i in range(0, m+1) ]
    v1 = [ 0 ] * (m+1)
    cost = 0
    for i in range(1, n+1):
        v1[0] = i
        for j in range(1, m+1):
            if s[i-1] == t[j-1]:
                cost = 0
            else:
                cost = 1
            a = v0[j] + 1
            b = v1[j-1] + 1
            c = v0[j-1] + cost
            v1[j] = min(a, b, c)
        v0 = v1[:]
    return v1[m]