# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *
from grille import *
from function import *
from solve import *

"""
Affichage
"""

def affiche(dungeon):
    pygame.init()
    tailleX = 60
    tailleY = 36
    fenetre = pygame.display.set_mode((len(dungeon.cases) * tailleX, len(dungeon.cases[0]) * tailleY))
    perso = pygame.image.load("perso.png").convert_alpha()
    image = [[0 for i in ligne] for ligne in dungeon.cases]
    for i in range(len(dungeon.cases)):
        for j in range(len(dungeon.cases[0])): 
            case = dungeon.cases[i][j]
            image[i][j] = pygame.image.load(case.image).convert()
            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
    
    i, j = dungeon.startingPosition.i, dungeon.startingPosition.j
    fenetre.blit(perso, (j*tailleX,i*tailleY))
    adventurer = dungeon.adventurer
    adventurer.goIn(dungeon.startingPosition)
    adventurer.objects = []
    state = dungeon.getState(dungeon.startingPosition, adventurer.objects)
    
    continuer = 1
    #Boucle infinie
    while continuer:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle
                
            
                
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    
                    
                    adventurer.goIn(case.voisin[state.decision])
                    adventurer.case.action(adventurer)
                    case = adventurer.case
                    # Evenement de la pièce
                    state = dungeon.getState(case, adventurer.objects)
                    for i in range(len(dungeon.cases)):
                        for j in range(len(dungeon.cases[0])):
                            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
            
            
                    """ Quel état on est """
                    #state.afficher()
            
            
            
            
            
            
                    #print(state.objects)
                    fenetre.blit(perso, (state.case.j*tailleX,state.case.i*tailleY))
        #Rafraîchissement de l'écran
        pygame.display.flip()

dungeon = Dungeon()
dungeon.open("Dungeon1.txt")
dungeon.instanciation(Adventurer(), True)
#valueIteration(dungeon)
qlearning(dungeon)
affiche(dungeon)