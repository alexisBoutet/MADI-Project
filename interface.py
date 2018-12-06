import pygame

from pygame.locals import *
from grille import *
from function import *


adventurer = Adventurer()
dungeon = Dungeon()
grid = openDungeon("Dungeon2.txt", dungeon)
dungeon.addGrid(grid)
dungeon.addAdventurer(adventurer)
dungeon.instanciation()


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
                    
                state.value, state.valueBefore = max([val for val in state.Q.values()]), state.value

    m = [abs(state.value - state.valueBefore) for state in dungeon.getAllStates()]
    if np.max(m)<1e-10:
        continuer = 0
    t+=1


for ligne in dungeon.states:        
    for case in ligne:
        for state in case:
            state.decision = [action for action in state.case.possibleMove if state.Q[action] == np.max([state.Q[action2] for action2 in state.case.possibleMove])][0]




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