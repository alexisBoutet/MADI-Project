# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *
from grille import *
from function import *

from scipy.optimize import linprog



adventurer = Adventurer()
dungeon = Dungeon()
grid = openDungeon("Dungeon2.txt", dungeon)
dungeon.addGrid(grid)
dungeon.addAdventurer(adventurer)
dungeon.instanciation()

def PL(dungeon):
    dic = {}
    states = dungeon.getAllStates()
    for i in range(len(states)):
        dic[states[i]] = i
    
    c = np.array([1 for i in states])
    actions = ["right", "left", "top", "bottom"]
    b_ub = []
    a_ub = []
    for action in actions:
        for state in states:
            if action in state.case.possibleMove:
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
        for i in range(len(state.case.possibleMove)):
            action = state.case.possibleMove[i]
            v = state.R[action] + sum([state.T[action][state2] * res[dic[state2]] for state2 in state.getAllNeighbourState(action)])
            if v > state.value or i== 0:
                state.value = v
                state.decision = action
    return dungeon
                
                
                
    

def valueIteration(dungeon):
    
    # Lancement de  l'itération à la valeur
    continuer = 1
    t=0
    while continuer:
        print(gamma(t))
        for ligne in dungeon.states:
            for case in ligne:
                for state in case:
                    for action in state.case.possibleMove:
                        
                        q = state.Q[action]
                        state.Q[action] = state.R[action] + gamma(t)*sum([state.T[action][state2] * state2.value for state2 in state.getAllNeighbourState(action)])
                        if state.case.i == 0 and state.case.j == 2 and "key" in state.objects and "sword" in state.objects and "treasure" not in state.objects and action=="left":
                            print("Action en cours : "+action)
                            print("Valeur de cette action : "+str(state.R[action]))
                            print([state.T[action][state2] * state2.value for state2 in state.getAllNeighbourState(action)])
                            print(state.value)
                            q = state.Q[action]
                            print(q)
                            
                    state.valueBefore.append(state.value)
                    state.value = max([val for val in state.Q.values()])
    
        m = [abs(state.value - state.valueBefore[-1]) for state in dungeon.getAllStates()]
        
        #showQ(dungeon, 0)
        if np.max(m)<1e-5:
            continuer = 0
        t+=1
    
    
    for ligne in dungeon.states:        
        for case in ligne:
            for state in case:
                state.decision = [action for action in state.case.possibleMove if state.Q[action] == np.max([state.Q[action2] for action2 in state.case.possibleMove])][0]

    return dungeon

def policyIteration(dungeon):
    continuer = 1
    
    while continuer:
        conv = 1
        t = 0
        while conv:
            for state in dungeon.getAllStates():
                state.valueBefore.append(state.value)
                if state.decision:
                    state.value = gamma(t) * sum([state.T[state.decision][state2] * state2.value for state2 in state.getAllNeighbourState(state.decision)])
                else:
                    state.value = gamma(t) * sum([state.T[state.case.possibleMove[0]][state2] * state2.value for state2 in state.getAllNeighbourState(state.case.possibleMove[0])])
        
            m = [abs(state.value - state.valueBefore[-1]) for state in dungeon.getAllStates()]
            
            #showQ(dungeon, 0)
            if np.max(m)<1e-5:
                conv = 0
            t+=1
            
        for state in dungeon.getAllStates():
            for i in range(len(state.case.possibleMove)):
                action = state.case.possibleMove[i]
                somme = state.R[action] + gamma(t)*sum([state.T[action][state2] * state2.value for state2 in state.getAllNeighbourState(action)])
                
                if i == 0 or somme > state.value:
                    state.value = somme
                    state.decisionBefore.append(state.decision)
                    state.decision = action
        
        if [0 if state.decision == state.decisionBefore else 1 for state in dungeon.getAllStates()]:
            return dungeon

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

"""
Affichage
"""

def affiche():
    pygame.init()
    tailleX = 60
    tailleY = 36
    fenetre = pygame.display.set_mode((len(grid) * tailleX, len(grid[0]) * tailleY))
    perso = pygame.image.load("perso.png").convert_alpha()
    image = [[0 for i in ligne] for ligne in dungeon.grid]
    for i in range(len(grid)):
        for j in range(len(grid[0])): 
            case = grid[i][j]
            image[i][j] = pygame.image.load(case.image).convert()
            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
    
    i, j = adventurer.case.i, adventurer.case.j
    fenetre.blit(perso, (j*tailleX,i*tailleY))
    
    state = dungeon.getState(i, i, adventurer.objectInPossession)
    
    continuer = 1
    #Boucle infinie
    while continuer:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
                
            
                
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    
                    
                    adventurer.goIn(dungeon.caseAfterAction(case, state.decision))
                    adventurer.case.action(adventurer)
                    case = adventurer.case
                    # Evenement de la pièce
                    state = dungeon.getStateAdventurer(case, adventurer)
                    for i in range(len(grid)):
                        for j in range(len(grid[0])):
                            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
            
            
                    """ Quel état on est """
                    state.afficher()
            
            
            
            
            
            
                    #print(state.objects)
                    fenetre.blit(perso, (state.case.j*tailleX,state.case.i*tailleY))
        #Rafraîchissement de l'écran
        pygame.display.flip()

valueIteration(dungeon)
affiche()