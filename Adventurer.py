#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:09:51 2018

@author: 3415104
"""
import numpy as np
from function import *
from scipy.optimize import linprog

class Adventurer():
    def __init__(self, name = "Héro"):
        self.name = name
        self.objectInPossession = []

    def addObject(self, obj):
        self.objectInPossession.append(obj)
    
    def haveObject(self, obj):
        return obj in self.objectInPossession
    
    def loseObject(self, obj):
        self.objectInPossession.remove(obj)
        
    def moveTo(self, direction):
        if direction == "right":
            self.j +=1
        elif direction == "left":
            self.j -=1
        elif direction == "bottom":
            self.i +=1
        else:
            self.i -=1
            
    def goTo(self, i, j):
        self.i = i
        self.j = j
    
    def goIn(self, case):
        self.case = case
    
    def getStringObjects(self):
        s = ""
        if not self.objectInPossession:
            return "empty"
        if "sword" in self.objectInPossession:
            s+="sword"
        if "key" in self.objectInPossession:
            s+="key"
        if "treasure" in self.objectInPossession:
            s+="treasure"
        return s
    

class etat():
    def __init__(self):
        
        self.value = 0
        self.valueBefore = 0
        
        self.R = {}
        self.Q = {}
        
        self.T = {}

treasure = etat()
enemi_bas = etat()
enemi_haut = etat()
blanc = etat()
start = etat()



treasure.R['right'] = -1
treasure.R['bottom'] = -1

enemi_bas.R['top'] = 5
enemi_bas.R['right'] = 0

enemi_haut.R['left'] = 5
enemi_haut.R['bottom'] = 0

blanc.R['top'] = -1
blanc.R['left'] = -1
blanc.R['right'] = 0

start.R["left"] = 0

treasure.T['right'] = {enemi_haut:1}
treasure.T['bottom'] = {enemi_bas:1}

enemi_bas.T['top'] = {treasure:1}
enemi_bas.T['right'] = {blanc:1}

enemi_haut.T['left'] = {treasure:1}
enemi_haut.T['bottom'] = {blanc:1}

blanc.T['top'] = {enemi_haut:1}
blanc.T['left'] = {enemi_bas:1}
blanc.T['right'] = {start:1}

start.T['left'] = {blanc:1}

s = [treasure, enemi_bas, enemi_haut, start, blanc]
"""
t=0
while t < 10:
    for state in s:
        v = []
        for action in state.R.keys():
            v.append(state.R[action] + gamma(t)*sum([state.T[action][state2] * state2.value for state2 in state.T[action].keys()])) 
            
        state.valueBefore = state.value
        state.value = max(v)
    t+=1
"""

def PL(s):
    dic = {}
    states = s
    for i in range(len(states)):
        dic[states[i]] = i
    
    c = np.array([1 for i in states])
    actions = ["right", "left", "top", "bottom"]
    b_ub = []
    a_ub = []
    for action in actions:
        for state in states:
            if action in state.T.keys():
                b_ub.append(-state.R[action])
                voisin = list(state.T[action].keys())
                
                l= []
                for state2 in states:
                    if state2 in voisin:
                        l.append(state.T[action][state2])
                    else:
                        l.append(0.0)
                        
                line = l
                line[dic[state]]-=1
                a_ub.append(np.array(line))
    
    a_ub = np.array(a_ub)
    print(a_ub)
    res = linprog(c, a_ub, b_ub)
    print(res)
    
    for state in states:
        for i in range(len(state.T.keys())):
            action = list(state.T.keys())[i]
            v = state.R[action] + gamma(t)*sum([state.T[action][state2] * res[dic[state2]] for state2 in state.T[action].keys()])
            if v > state.value or i== 0:
                state.value = v
                state.decision = action


