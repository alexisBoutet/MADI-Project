#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:09:51 2018

@author: 3415104
"""

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