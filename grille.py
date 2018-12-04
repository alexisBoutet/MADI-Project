# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 12:53:16 2018

@author: 3415104
"""
import numpy as np
from random import randint

class Case():
    def __init__(self, i, j, dungeon):
        self.i = i
        self.j = j
        self.possibleMove = ["right", "left", "top", "bottom"]
        self.dungeon=dungeon
        
        
    def action(self, personnage):
        print("The adventurer is in the room ({}, {})".format(self.i, self.j))
    
    def getRecompense(self):
        return 0
    
    def getPossibleMove(self):
        return self.possibleMove
    
    def setPossibleMove(self, move):
        self.possibleMove = move
    
    def getIndicePossibleMove(self):
        ind = []
        if "right" in self.possibleMove:
            ind.append((self.i,self.j+1))
        if "left" in self.possibleMove:
            ind.append((self.i,self.j-1))
        if "top" in self.possibleMove:
            ind.append((self.i-1,self.j))
        if "bottom" in self.possibleMove:
            ind.append((self.i+1,self.j))
        return ind
        
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
            
    def getRecompense(self):
        return 10
        
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
    
    
class Dungeon():
    def __init__(self):
        # Initialisation de la position de l'aventurier
        # Trouver la position de départ
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
                if j == len(self.grid)-1 or type(self.grid[i][j+1])==Wall:
                    possibleMove.remove("right")
                    
                self.grid[i][j].setPossibleMove(possibleMove)
    
    def createState(self):
        self.states = []
        # il y a autant d'état par case que de possibilité d'objet dans le sac de l'avdventurer
        self.possibleSac = ["empty", "sword", "key", "swordkey", "swordkeytreasure"]
        
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
            for action in state.case.getPossibleMove():
                state2 = self.stateAfterAction(state, action)
                if  type(state2.case) == Trap:
                    state.T[action][state2] = 0.7
                    i, j = self.startingPosition.i, self.startingPosition.j
                    k = self.possibleSac.index(state.objects)
                    state.T[action][self.states[i][j][k]] = 0.3
                
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
                        for action in state.case.getPossibleMove():
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
                                    state.R[action] = 20
                                
                                else:
                                    state.R[action] = 0
                            
                            elif type(futurState.case) == MagicSword:
                                if "sword" in futurState.objects:
                                    print("sword",futurState.objects)
                                    state.R[action] = 0
                                else:
                                    state.R[action] = 10
                            
                            elif type(futurState.case) == GoldenKey:
                                if "key" in futurState.objects:
                                    print("key",futurState.objects)
                                    state.R[action] = 0
                                else:
                                    state.R[action] = 10
                            
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
                                    state.R[action] = 20
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
        return s
                
    def stateNeighbour(self, state):
        ind = state.case.getIndicePossibleMove()
        k = self.possibleSac.index(state.objects)
        if type(state.case.getIndiceCaseAction(action)) == Treasure and "key" in state.objects and "treasure" not in state.objects:
            k = self.possibleSac.index(state.objects+"treasure")
        return [self.states[i][j][k] for (i,j) in ind]
        
    def stateAfterAction(self, state, action):
        i, j = state.case.getIndiceCaseAction(action)
        k = self.possibleSac.index(state.objects)
        if type(state.case.getIndiceCaseAction(action)) == Treasure and "key" in state.objects and "treasure" not in state.objects:
            k = self.possibleSac.index(state.objects+"treasure")
        return self.states[i][j][k]
    
    def getState(self, i, j, obj):
        k = self.possibleSac.index(obj)
        return self.states[i][j][k]
    
    def caseAfterAction(self, case, action):
        i, j = case.getIndiceCaseAction(action)
        return self.grid[i][j]
    
    def getStateAdventurer(self, case, adventurer):
        obj = adventurer.getStringObjects()
        print(obj)
        i, j = case.i, case.j
        return self.getState(i, j, obj)
    
    def getAllStates(self):
        s = []
        for ligne in dungeon.states:
            for case in ligne:
                for state in case:
                    s.append(state)
        return s
class State():
    def __init__(self, case, objects):
        self.case = case 
        self.objects = objects
        
        self.value = 0
        self.valueBefore = 0
        
        self.Q = {}
        for action in self.case.getPossibleMove():
            self.Q[action] = 0
        
        self.R = {}
        self.T={}
        for action in self.case.getPossibleMove():
            self.T[action] = {}
        
        self.decision = ""
        
    def getAllNeighbourState(self, action):
        return self.T[action].keys()
    
    def afficher(self):
        print("Nous sommes sur la case "+str(self.case.i)+" "+str(self.case.j)+" de type "+str(type(self.case)))
        print("T = "+str(self.T))
        print("Q = "+str(self.Q))
        print("R = "+str(self.R))
        print("Value = "+str(self.value))
        print("Déplacement vers "+str(self.decision))
        print("Les objets en possessions sont "+str(self.objects))
        print("")
            
        
        

adventurer = Adventurer()
dungeon = Dungeon()
grid = openDungeon("Dungeon2.txt", dungeon)
dungeon.addGrid(grid)
dungeon.addAdventurer(adventurer)
dungeon.instanciation()

def gamma(i):
    return 0.99**i

# Lancement de  l'itération à la valeur
continuer = 1
t=0
while continuer:
    print(gamma(t))
    for ligne in dungeon.states:
        for case in ligne:
            for state in case:
                for action in state.case.getPossibleMove():
                    
                    q = state.Q[action]
                    state.Q[action] = state.R[action] + gamma(t)*sum([state.T[action][state2] * state2.value for state2 in state.getAllNeighbourState(action)])
                    
                    if state.objects == "swordkey" and state.case.i == 0 and state.case.j == 2:
                        print(action, q, state.Q[action])
                        input()
                state.value, state.valueBefore = max([val for val in state.Q.values()]), state.value

    m = [abs(state.value - state.valueBefore) for state in dungeon.getAllStates()]
    if np.max(m)<1e-10:
        continuer = 0
    t+=1


for ligne in dungeon.states:        
    for case in ligne:
        for state in case:
            state.decision = [action for action in state.case.getPossibleMove() if state.Q[action] == np.max([state.Q[action2] for action2 in state.case.getPossibleMove()])][0]




def affichage():
    for state in dungeon.getAllStates():
        if state.objects == "key":
            state.afficher()

#affichage()
"""
for ligne in dungeon.states:
    for case in ligne:
        for state in case:
            state.decision = state.case.getPossibleMove()[0]


            
a = np.array([[1 if stateEnd == dungeon.stateAfterAction(stateStart, stateStart.decision) else 0 for stateEnd in dungeon.getAllStates()] for stateStart in dungeon.getAllStates()])
print(a)
for i in range(len(a)):
    a[i,i] = -1

b = [-state.R[state.decision] for state in dungeon.getAllStates()]
print(b)
x = np.linalg.solve(a, b)
"""