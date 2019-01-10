# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:53:16 2018

@author: 3415104
"""
import numpy as np
from random import randint
from Adventurer import *

class Case():
    def __init__(self, i, j, dungeon):
        self.i = i
        self.j = j
        self.possibleMove = ["right", "left", "top", "bottom"]
        self.dungeon=dungeon
        
        
    def action(self, personnage):
        print("The adventurer is in the room ({}, {})".format(self.i, self.j))

    
    def getIndicePossibleMove(self):
        return [self.getIndiceCaseAction(action) for action in self.possibleMove]

        
    def getIndiceCaseAction(self, action):
        if "right" == action:
            return self.i,self.j+1
        if "left" == action:
           return self.i,self.j-1
        if "top"== action:
            return self.i-1,self.j
        if "bottom" == action:
            return self.i+1,self.j
        
class StartingPosition(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "startingPosition.png"

        
class Blank(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "blank.png"

class Wall(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "wall.png"

class Enemy(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "enemy.png"
    
    def action(self, personnage):
        print("Fight")
        
class Trap(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
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
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "cracks.png"
        
    def action(self, personnage):
        print("You die !")


class GoldenKey(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "goldenKey.png"
        
    def action(self, personnage):
        if "key" not in personnage.objectInPossession:
            # Ajout de la clé
            personnage.objectInPossession.append("key")

class Treasure(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
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
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "magicPortal.png"
    
    def action(self, personnage):
        personnage.goIn(self.dungeon.randomCase())
        personnage.case.action(personnage)
        

class MovingPlatform(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "movingPlatform.png"
        
    def action(self, personnage):
        c = [self.dungeon.caseAfterAction(self, action) for action in self.possibleMove]
        r = randint(0,len(c)-1)
        personnage.goIn(c[r])
        personnage.case.action(personnage)

class MagicSword(Case):
    def __init__(self, i, j, dungeon):
        Case.__init__(self, i, j, dungeon)
        self.image = "magicSword.png"
        
    def action(self, personnage):
        if "sword" not in personnage.objectInPossession:
            # Ajout de la sword
            personnage.objectInPossession.append("sword")
        

# Effectivement, ça ne devrait pas être là
# Convert a txt file to a readable dungeon
def openDungeon(nomFichier, dungeon):
    grid = []
    with open(nomFichier, "r") as fichier:
        donnees = fichier.readlines()
        for i in range(len(donnees)):
            grid.append([])
            for j in range(len(donnees[0])-1):
                val = donnees[i][j]
                if val == "b":
                    case = Blank(i,j, dungeon)
                elif val == "0":
                    case = StartingPosition(i,j, dungeon)
                elif val == "w":
                    case = Wall(i,j, dungeon)
                elif val == "e":
                    case = Enemy(i,j, dungeon)
                elif val == "r":
                    case = Trap(i,j, dungeon)
                elif val == "c":
                    case = Cracks(i,j, dungeon)
                elif val == "t":
                    case = Treasure(i,j, dungeon)
                elif val == "s":
                    case = MagicSword(i,j, dungeon)
                elif val == "k":
                    case = GoldenKey(i,j, dungeon)                
                elif val == "p":
                    case = MagicPortal(i,j, dungeon)
                elif val == "-":
                    case = MovingPlatform(i,j, dungeon)  
                
                grid[i].append(case)
    return grid

# new open pour ne pas tout prendre en compte
# Convert a txt file to a readable dungeon
def openDungeon(nomFichier, dungeon):
    grid = []
    with open(nomFichier, "r") as fichier:
        donnees = fichier.readlines()
        for i in range(len(donnees)):
            grid.append([])
            for j in range(len(donnees[0])-1):
                val = donnees[i][j]
                if val == "b":
                    case = Blank(i,j, dungeon)
                elif val == "0":
                    case = StartingPosition(i,j, dungeon)
                elif val == "w":
                    case = Wall(i,j, dungeon)
                elif val == "e":
                    case = Blank(i,j, dungeon)
                elif val == "r":
                    case = Trap(i,j, dungeon)
                elif val == "c":
                    case = Cracks(i,j, dungeon)
                elif val == "t":
                    case = Treasure(i,j, dungeon)
                elif val == "s":
                    case = MagicSword(i,j, dungeon)
                elif val == "k":
                    case = GoldenKey(i,j, dungeon)                
                elif val == "p":
                    case = MagicPortal(i,j, dungeon)
                elif val == "-":
                    case = MovingPlatform(i,j, dungeon)  
                
                grid[i].append(case)
    return grid
    
    
class Dungeon():
    def __init__(self):
        print("Dungeon ready to be instance")
    
    def addGrid(self, grid):
        self.grid = grid
        
    def addAdventurer(self, adventurer):
        self.adventurer = adventurer
    
    def instanciation(self):
        self.startingPosition = self.getStartingPosition()
        self.adventurer.goIn(self.startingPosition)
        self.calculPossibleMovment()
        self.createState()
        self.createAction()
        self.createTransition()
        self.createReward()
        
    def getStartingPosition(self):
        for ligne in self.grid:
            for case in ligne:
                if type(case) == StartingPosition:
                    return case
    
    def calculPossibleMovment(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                possibleMove = ["right", "left", "bottom", "top"]
                if i == 0 or type(self.grid[i-1][j])==Wall:
                    possibleMove.remove("top")
                if i == len(self.grid)-1 or type(self.grid[i+1][j])==Wall:
                    possibleMove.remove("bottom")
                    
                if j == 0 or type(self.grid[i][j-1])==Wall:
                    possibleMove.remove("left")
                if j == len(self.grid[0])-1 or type(self.grid[i][j+1])==Wall:
                    possibleMove.remove("right")
                    
                self.grid[i][j].possibleMove = possibleMove
    
    def createState(self):
        self.states = []
        # il y a autant d'état par case que de possibilité d'objet dans le sac de l'adventurer
        self.possibleSac = [[], ['sword'], ["key"], ["sword","key"], ["key","treasure"], ["sword","key","treasure"]]
        
        for i in range(len(self.grid)):
            self.states.append([])
            for j in range(len(self.grid[i])):
                self.states[i].append([])
                for objects in self.possibleSac:
                    self.states[i][j].append(State(self.grid[i][j], objects))
    
    def createAction(self):
        
        self.actions = ["right", "left", "bottom", "top"]
    
    def createTransition(self):
        for state in self.getAllStates():
            for action in state.case.possibleMove:
                state2 = self.stateAfterAction(state, action)
                if  type(state2.case) == Trap:
                    state.T[action][state2] = 0.7
                    i, j = self.startingPosition.i, self.startingPosition.j
                    state.T[action][self.getState(i, j, state2.objects)] = 0.3
                
                elif  type(state2.case) == MovingPlatform:
                    neighbours = self.stateNeighbour(state2)
                    for state3 in neighbours:
                        state.T[action][state3] = 1.0/len(neighbours)
                
                elif  type(state2.case) == MagicPortal:
                    neighbours = self.getAllPossibleStateFromState(state2)
                    for state3 in neighbours:
                        state.T[action][state3] = 1.0/len(neighbours)
                
                else:
                    state.T[action][state2] = 1
                
                    
                            
    # Création de la fonction de récompense immédiate
    def createReward(self):
        print("Reward")
        for ligne in self.states:
                for case in ligne:
                    for state in case:
                        for action in state.case.possibleMove:
                            futurState = self.stateAfterAction(state, action)
                            if type(futurState.case) == Enemy:
                                if "sword" in futurState.objects:
                                    print("sword",futurState.objects)
                                    state.R[action] = -1
                                else:
                                    state.R[action] = -10
                                    
                            elif type(futurState.case) == Treasure:
                                if "key" in futurState.objects and not("treasure" in futurState.objects):
                                    print("key not treasure",futurState.objects)
                                    state.R[action] = 5
                                
                                else:
                                    state.R[action] = 0
                            
                            elif type(futurState.case) == MagicSword:
                                if "sword" in futurState.objects:
                                    print("sword",futurState.objects)
                                    state.R[action] = 0
                                else:
                                    state.R[action] = 5
                            
                            elif type(futurState.case) == GoldenKey:
                                if "key" in futurState.objects:
                                    print("key",futurState.objects)
                                    state.R[action] = 0
                                else:
                                    state.R[action] = 5
                            
                            elif type(futurState.case) == Cracks:
                                state.R[action] = -10
                            
                            elif type(futurState.case) == Trap:
                                state.R[action] = -3
                            
                            elif type(futurState.case) == MagicPortal:
                                state.R[action] = -1
                                
                            elif type(futurState.case) == MovingPlatform:
                                state.R[action] = 0
                            
                            elif type(futurState.case) == StartingPosition:
                                if "treasure" in futurState.objects:
                                    print("treasure",futurState.objects)
                                    state.R[action] = 5
                                else:
                                    state.R[action] = 0
                                
                            else :
                                state.R[action] = 0
                                
                            #state.afficher()
                            #futurState.afficher()
    
    def randomCase(self):
        cases = []
        for ligne in self.grid:
            for case in ligne:
                if type(case) != Wall:
                    cases.append(case)
        
        r = randint(0,len(cases)-1)
        return cases[r]
    
    def getAllPossibleStateFromState(self, state):
        s = []
        for sta in self.getAllStates():
            if sta.objects == state.objects and type(sta.case) != Wall:
                s.append(sta)
            """
            elif type(sta.case) == Treasure and "key" in state.objects and "treasure" not in state.object and :
                s.append(sta)
            elif type(sta.case) == GoldenKey and "key" not in state.objects:
                s.append(sta)
                """
        return s
                
    def stateNeighbour(self, state):
        return [self.stateAfterAction(state, action) for action in state.case.possibleMove]
        
    def stateAfterAction(self, state, action):
        i, j = state.case.getIndiceCaseAction(action)
        objet = state.objects
        if type(state.case.getIndiceCaseAction(action)) == Treasure and "key" in state.objects and "treasure" not in state.objects:
            objet = state.objects+["treasure"]
        return self.getState(i,j, objet)
    
    def getState(self, i, j, obj):
        for k in range(len(self.possibleSac)):
            if sorted(self.possibleSac[k]) == sorted(obj):
                return self.states[i][j][k]
    
    def caseAfterAction(self, case, action):
        i, j = case.getIndiceCaseAction(action)
        return self.grid[i][j]
    
    def getStateAdventurer(self, case, adventurer):
        i, j = case.i, case.j
        return self.getState(i, j, adventurer.objectInPossession)
    
    def getAllStates(self):
        s = []
        for ligne in self.states:
            for case in ligne:
                for state in case:
                    s.append(state)
        return s
class State():
    def __init__(self, case, objects):
        self.case = case 
        self.objects = objects
        
        self.value = 0
        self.valueBefore = []
        
        self.Q = {}
        for action in self.case.possibleMove:
            self.Q[action] = 0
        
        self.R = {}
        self.T={}
        for action in self.case.possibleMove:
            self.T[action] = {}
        
        self.decision = ""
        self.decisionBefore = []
        
    def getAllNeighbourState(self, action):
        return [k for k in self.T[action].keys()]
    
    def afficher(self):
        print("Nous sommes sur la case "+str(self.case.i)+" "+str(self.case.j)+" de type "+str(type(self.case)))
        print("T = "+str(self.T))
        print("Q = "+str(self.Q))
        print("R = "+str(self.R))
        print("Value = "+str(self.value))
        print("Déplacement vers "+str(self.decision))
        print("Les objets en possessions sont "+str(self.objects))
        print("")
