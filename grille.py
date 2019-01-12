# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:53:16 2018

@author: 3415104
"""
import numpy as np
import random
from Adventurer import *

class Case():
    
    def __init__(self, dungeon, i, j):
        self.i = i
        self.j = j
        self.dungeon = dungeon
        
        self.voisin = {}
    
    def action(self, personnage):
        return True

    def __repr__(self):
        return "(" + str(self.i) + ", " + str(self.j) + ")"
        
class StartingPosition(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "startingPosition.png"

        
class Blank(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "blank.png"

class Wall(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "wall.png"

class Enemy(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "enemy.png"
    
    def action(self, personnage):
        if "sword" in personnage.objects:
            return True
        else:
            return False
        
class Trap(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "trap.png"
    
    def action(self, personnage):
        r = random.randint(1,10)
        if r == 1:
            return False
        elif r >7:
            u = 1
        else:
            personnage.goIn(self.dungeon.startingPosition)
            personnage.case.action(personnage)
        return True

class Cracks(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "cracks.png"
        
    def action(self, personnage):
        return False


class GoldenKey(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "goldenKey.png"
        
    def action(self, personnage):
        if "key" not in personnage.objects:
            # Ajout de la clé
            personnage.objects.append("key")
        
        return True

class Treasure(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "treasure.png"
    
    def action(self, personnage):
        if "treasure" not in personnage.objects and "key" in personnage.objects:
            # Ajout de la treasure
            personnage.objects.append("treasure")
        else:
            u = 2
        return True
        
class MagicPortal(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "magicPortal.png"
    
    def action(self, personnage):
        personnage.goIn(self.dungeon.randomCase())
        return personnage.case.action(personnage)
        

class MovingPlatform(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "movingPlatform.png"
        
    def action(self, personnage):
        c = [case for case in self.voisin.values()]
        r = random.randint(0,len(c)-1)
        personnage.goIn(c[r])
        return personnage.case.action(personnage)

class MagicSword(Case):
    def __init__(self, dungeon, i, j):
        Case.__init__(self, dungeon, i, j)
        self.image = "magicSword.png"
        
    def action(self, personnage):
        if "sword" not in personnage.objects:
            # Ajout de la sword
            personnage.objects.append("sword")
        return True
    
class Dungeon():
    
    def __init__(self):
        
        self.possibleSac = [[], ['sword'], ["key"], ["sword","key"], ["key","treasure"], ["sword","key","treasure"]]

        self.cases = []
        
        self.states = []
                
    def instanciation(self, adventurer, Qlearning=False):
        self.adventurer = adventurer
        self.startingPosition = self.getStartingPosition()
        self.adventurer.goIn(self.startingPosition)
        self.createEdge()
        self.createState()
        if not Qlearning:
            self.createTransition()
            self.createReward()
    
    def randomCase(self):
        while True:
            r = random.randint(0, len(self.states) - 1)
            if type(self.states[r].case) != Wall:
                return self.states[r].case
                
    def open(self, nomFichier):
        with open(nomFichier, "r") as fichier:
            donnees = fichier.readlines()
            for i in range(len(donnees)):
                self.cases.append([])
                for j in range(len(donnees[0])-1):
                    val = donnees[i][j]
                    if val == "b":
                        case = Blank(self, i, j)
                    elif val == "0":
                        case = StartingPosition(self, i, j)
                    elif val == "w":
                        case = Wall(self, i, j)
                    elif val == "e":
                        case = Enemy(self, i, j)
                    elif val == "r":
                        case = Trap(self, i, j)
                    elif val == "c":
                        case = Cracks(self, i, j)
                    elif val == "t":
                        case = Treasure(self, i, j)
                    elif val == "s":
                        case = MagicSword(self, i, j)
                    elif val == "k":
                        case = GoldenKey(self, i, j)                
                    elif val == "p":
                        case = MagicPortal(self, i, j)
                    elif val == "-":
                        case = MovingPlatform(self, i, j)  
                    
                    self.cases[i].append(case)
    
    def getStartingPosition(self):
        for ligne in self.cases:
            for case in ligne:
                if type(case) == StartingPosition:
                    return case
                
    def createEdge(self):
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
                state.R[action] = self.rewardOf(state, futurCase)
    
    def rewardOf(self, state, futurCase, alpha=1):
        if alpha < 0.4:
            return 0
        if type(futurCase) == Treasure and "key" in state.objects and "treasure" not in state.objects:
            return 5
        
        elif type(futurCase) == Enemy and "sword" not in state.objects:
            return -5
        
        elif type(futurCase) == GoldenKey and "key" not in state.objects:
            return 5
    
        elif type(futurCase) == MagicSword and "sword" not in state.objects:
            return 5

        elif type(futurCase) == StartingPosition and "treasure" in state.objects:
            return 5
        
        elif type(futurCase) == Cracks:
            return -5
        
        elif type(futurCase) == MovingPlatform:
            state2 = self.getState(futurCase, state.objects)
            return np.mean([self.rewardOf(state2, futurCase2, alpha*0.5) for action2, futurCase2 in state2.case.voisin.items()])
        
        
        elif type(futurCase) == MagicPortal:
            state2 = self.getState(futurCase, state.objects)
            possibles = self.getAllPossibleStates()
            return np.mean([self.rewardOf(state2, state3.case, alpha*0.5) for state3 in possibles])
        
        elif type(futurCase) == Trap:
            return -1
            
        else:
            return 0
                
    def getAllPossibleStates(self):
        v = []
        for state in self.states:
            if type(state.case) != Wall:
                v.append(state)
                
        return v
    
    def statesAfterAction(self, action):
        return list(self.T[action].items())        
    
    
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
    
    def statesAfterAction(self, action):
        return list(self.T[action].items())     
    
    def chooseFuturState(self, action):
        print(self.T)
        v = 0
        r = random.random()
        for state, proba in self.T[action].items():
            v+= proba
            if r < v:
                return state

    def __repr__(self):
        return "Case : " + str(self.case) + ", objects : " + str(self.objects)