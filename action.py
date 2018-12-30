# this class will be used to set the action objects
# including checkbox, labels and the other settings
# there are two acts in a process
# 1. alist which keeps all act list in one process until quit. the i is the index 
# 2. the current list (h) which contains the active actions. the i is the current row

import inspect

class a:
    
    def __init__(a, am):
        a.am = am
        a.h = am.h
        a.all = am.alist
        
    def set(a, i, k, v):
        a.h[i]['act'][k] = v
        
    def get(a, i, k):
        try:
            act = a.h[i]['act']
        except:
            act = a.am.act
            
        try:
            return act[k]
        except:
            return None
        
    def ga(a, i, k):
        try:
            act = a.all[i]['act']
            return act[k]
        except:
            return None
        
    def p(a):
        print("hello i am an act")
        
    def isit(a, i):
        print(a.all)
        for x,e in enumerate(a.all):
            t = a.ga(x, 't')
            ai = a.ga(x, 'i')
            print('i=',i,'ai:',ai,'t=',t)
            if i==ai and t:
                return True
        return False
    
    def i(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def cc(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def snz(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def sound(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def cb(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def nn(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def anim(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def tt(a, i):
        return a.get(i, inspect.stack()[0][3])
        
    def ct(a, i):
        return a.get(i, inspect.stack()[0][3])        
        
    def t(a, i):
        return a.get(i, inspect.stack()[0][3])        
        
    def w(a, i):
        return a.get(i, inspect.stack()[0][3])