#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 13:11:32 2018

@author: 3415104
"""

import random
def gamma():
    return 0.9

def alpha(i):
    return 1/(i+1)

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

def generateDungeon(n, m, name):
    empty = 0.5
    wall = 0.2
    enemy = 0.1
    magic_portal = 0.05
    moving_platform = 0.05
    cracks = 0.05
    trap = 0.05
    
    sword = (n-1, 0)
    starting = (n-1, n-1)
    treasure = (0, 0)
    key = (0, n-1)
    f = open(name, "w")
    for i in range(n):
        s = ""
        for j in range(m):
            if (i,j) == sword:
                s+="s"
            elif(i,j) == starting:
                s+="0"
            elif (i,j) == treasure:
                s+="t"
            elif (i,j) == key:
                s+="k"
            else:
                r = random.random()
                if r < empty:
                    s+="b"
                elif r < empty + wall:
                    s+="w"
                elif r < empty + wall + enemy:
                    s+="e"
                elif r < empty + wall + enemy + magic_portal:
                    s+="p"
                elif r < empty + wall + enemy + magic_portal + moving_platform:
                    s+= "-"
                elif r < empty + wall + enemy + magic_portal + moving_platform + cracks:
                    s+= "c"
                elif r < empty + wall + enemy + magic_portal + moving_platform + cracks + trap:
                    s+= "r"
        f.write(s+"\n")
    f.close()
            
        