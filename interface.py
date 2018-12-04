import pygame

from pygame.locals import *
from grille import *


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
persoObjects = adventurer.getStringObjects()
adventurer.objectInPossession = ["key"]
fenetre.blit(perso, (j*tailleX,i*tailleY))

state = dungeon.getState(i, i, persoObjects)

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