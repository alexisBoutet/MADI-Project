#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 14:22:22 2019

@author: 3415104
"""

# Test si l'implémentation était le soucis
from scipy.optimize import linprog
from function import *


class Adventurer():
    def __init__(self):
        self.objects = []
        self.case = None
    
    def goIn(self, case):
        self.case = case

class Case():
    
    def __init__(self, i, j):
        self.i = i
        self.j = j
        
        self.voisin = {}

class StartingPosition(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "startingPosition.png"

        
class Blank(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "blank.png"

class Wall(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "wall.png"

class Enemy(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "enemy.png"
    
    def action(self, personnage):
        print("Fight")
        
class Trap(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "trap.png"
    
    def action(self, personnage):
        print("Trap")
        r = randint(1,10)
        if r == 1:
            print("You die !")
        elif r >7:
            print("Nothing happenned")
        else:
            personnage.goIn(self.dungeon.startingPosition)
            personnage.case.action(personnage)

class Cracks(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "cracks.png"
        
    def action(self, personnage):
        print("You die !")


class GoldenKey(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "goldenKey.png"
        
    def action(self, personnage):
        if "key" not in personnage.objectInPossession:
            # Ajout de la clé
            personnage.objectInPossession.append("key")

class Treasure(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "treasure.png"
    
    def action(self, personnage):
        print("Arrivé au trésor")
        if "treasure" not in personnage.objectInPossession and "key" in personnage.objectInPossession:
            # Ajout de la treasure
            personnage.objectInPossession.append("treasure")
            print("Tresor ramassé")
        else:
            print("Trésor non ramasé")
        
class MagicPortal(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "magicPortal.png"
    
    def action(self, personnage):
        personnage.goIn(self.dungeon.randomCase())
        personnage.case.action(personnage)
        

class MovingPlatform(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "movingPlatform.png"
        
    def action(self, personnage):
        c = [self.dungeon.caseAfterAction(self, action) for action in self.possibleMove]
        r = randint(0,len(c)-1)
        personnage.goIn(c[r])
        personnage.case.action(personnage)

class MagicSword(Case):
    def __init__(self, i, j):
        Case.__init__(self, i, j)
        self.image = "magicSword.png"
        
    def action(self, personnage):
        if "sword" not in personnage.objectInPossession:
            # Ajout de la sword
            personnage.objectInPossession.append("sword")
            
class Dungeon():
    
    def __init__(self):
        
        self.possibleSac = [[], ['sword'], ["key"], ["sword","key"], ["key","treasure"], ["sword","key","treasure"]]

        self.cases = []
        
        self.states = []
                
    def instanciation(self, adventurer):
        self.adventurer = Adventurer()
        self.startingPosition = self.getStartingPosition()
        self.adventurer.goIn(self.startingPosition)
        self.createEdge()
        self.createState()
        self.createTransition()
        self.createReward()
        
    def openDungeon(self, nomFichier):
        with open(nomFichier, "r") as fichier:
            donnees = fichier.readlines()
            for i in range(len(donnees)):
                self.cases.append([])
                for j in range(len(donnees[0])-1):
                    val = donnees[i][j]
                    if val == "b":
                        case = Blank(i,j)
                    elif val == "0":
                        case = StartingPosition(i,j)
                    elif val == "w":
                        case = Blank(i,j)
                    elif val == "e":
                        case = Blank(i,j)
                    elif val == "r":
                        case = Blank(i,j)
                    elif val == "c":
                        case = Blank(i,j)
                    elif val == "t":
                        case = Treasure(i,j)
                    elif val == "s":
                        case = Blank(i,j)
                    elif val == "k":
                        case = GoldenKey(i,j)                
                    elif val == "p":
                        case = Blank(i,j)
                    elif val == "-":
                        case = Blank(i,j)  
                    
                    self.cases[i].append(case)
    
    def getStartingPosition(self):
        for ligne in self.cases:
            for case in ligne:
                if type(case) == StartingPosition:
                    return case
                
    def createEdge(self):
        possibleMove = ["right", "left", "bottom", "top"]
        for i in range(len(self.cases)):
            for j in range(len(self.cases[i])):
                
                if not(i == 0 or type(self.cases[i-1][j])==Wall):
                    self.cases[i][j].voisin["top"] = self.cases[i-1][j]
                    
                if not(i == len(self.cases)-1 or type(self.cases[i+1][j])==Wall):
                    self.cases[i][j].voisin["bottom"] = self.cases[i+1][j]
                    
                if not(j == 0 or type(self.cases[i][j-1])==Wall):
                    self.cases[i][j].voisin["left"] = self.cases[i][j-1]
                    
                if not(j == len(self.cases[0])-1 or type(self.cases[i][j+1])==Wall):
                    self.cases[i][j].voisin["right"] = self.cases[i][j+1]

                
    def createState(self):
        for ligne in self.cases:
            for case in ligne:
                for objects in self.possibleSac:
                    self.states.append(State(case, objects))
    
    def createTransition(self):
        for state in self.states:
            for action, futurCase in state.case.voisin.items():
                state2 = self.getState(futurCase, state.objects)
                state.T[action][state2] = 1
    
    def createReward(self):
        for state in self.states:
            for action, futurCase in state.case.voisin.items():
                if type(futurCase) == Treasure and "key" in state.objects and "treasure" not in state.objects:
                    state.R[action] = 5
                
                elif type(futurCase) == Enemy:
                    if "sword" in state.objects:
                        state.R[action] = -1
                    else:
                        state.R[action] = -5
                        
                elif type(futurCase) == GoldenKey and "key" not in state.objects:
                    state.R[action] = 5
                
                else:
                    state.R[action] = 0
                
    
    
    def getState(self, case, objects):
        for state in self.states:
            if state.case == case and sorted(objects) == sorted(state.objects):
                return state
        return None
                
class State():
    
    def __init__(self, case, objects):
        self.case = case
        self.objects = objects
        
        self.value = 0
        self.valueBefore = []
        
        self.Q = {}
        for action in self.case.voisin.keys():
            self.Q[action] = 0
        
        self.R = {}
        self.T={}
        for action in self.case.voisin.keys():
            self.T[action] = {}
        
        self.decision = ""
        self.decisionBefore = []
    
    def getAllNeighbourState(self, action):
        return [k for k in self.T[action].keys()]

adventurer = Adventurer()
dungeon = Dungeon()
dungeon.openDungeon("Dungeon2.txt")
dungeon.instanciation(adventurer)

def PL(dungeon):
    dic = {}
    states = dungeon.states
    for i in range(len(states)):
        dic[states[i]] = i
    
    c = np.array([1 for i in states])
    actions = ["right", "left", "top", "bottom"]
    b_ub = []
    a_ub = []
    for action in actions:
        for state in states:
            if action in state.case.voisin.keys():
                b_ub.append(-state.R[action])
                voisin = state.getAllNeighbourState(action)
                
                l= []
                for state2 in states:
                    if state2 in voisin:
                        l.append(state.T[action][state2])
                    else:
                        l.append(0.0)
                        
                line = l
                line[dic[state]]-=1
                a_ub.append(line)
    
    bounds = [(-100, 100) for i in states]
    
    res = linprog(c, a_ub, b_ub, bounds = bounds)
    print(res)
    
    for state in states:
        i = 0
        for action in state.case.voisin.keys():
            v = state.R[action] + sum([state.T[action][state2] * res[dic[state2]] for state2 in state.getAllNeighbourState(action)])
            if v > state.value or i== 0:
                state.value = v
                state.decision = action
            i+=1
    return dungeon



"""
# Test de linprog 
c = np.array([1,1])
b = np.array([-8, -12, -11, -9])*8
print(b)
a = np.array([[-5, 1],[-6,2],[2,-6],[1,-5]])

print(linprog(c, a, b))
"""

#PL(dungeon)