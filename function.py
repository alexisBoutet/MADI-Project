#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:11:32 2018

@author: 3415104
"""


def gamma(i):
    return 0.5**i

def showQ(dungeon, k, t=False):
    s = []
    for j in range(len(dungeon.states)):
        ligne = dungeon.states[j]
        s.append([])
        for i in range(len(ligne)):
            case = ligne[i]
            s[j].append(case[k].value)
        
        print(s[j])     
    
    if t:
        s = []
        for j in range(len(dungeon.states)):
            ligne = dungeon.states[j]
            s.append([])
            for i in range(len(ligne)):
                case = ligne[i]
                s[j].append(case[k].valueBefore)
                print(j,i)
                print(s[j][i])          
    
    return