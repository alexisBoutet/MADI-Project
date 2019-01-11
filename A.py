#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 14:22:22 2019

@author: 3415104
"""

# Test si l'implémentation était le soucis
from scipy.optimize import linprog
from function import *
import numpy as np
import interface
import random

import pygame

from pygame.locals import *




def affiche():
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
                    
                    
                    adventurer.goIn(dungeon.stateAfterAction(state, state.decision).case)
                    adventurer.case.action(adventurer)
                    case = adventurer.case
                    # Evenement de la pièce
                    state = dungeon.getStateAdventurer(case, adventurer.objects)
                    for i in range(len(dungeon.cases)):
                        for j in range(len(dungeon.cases[0])):
                            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
            
            
                    """ Quel état on est """
                    #state.afficher()
            
            
            
            
            
            
                    #print(state.objects)
                    fenetre.blit(perso, (state.case.j*tailleX,state.case.i*tailleY))
        #Rafraîchissement de l'écran
        pygame.display.flip()
        
"""
# Test de linprog 
c = np.array([1,1])
b = np.array([-8, -12, -11, -9])*8
print(b)
a = np.array([[-5, 1],[-6,2],[2,-6],[1,-5]])

print(linprog(c, a, b))
"""

adventurer = Adventurer()
dungeon = Dungeon()
dungeon.openDungeon("Dungeon2.txt")
dungeon.instanciation(adventurer)


#PL(dungeon)
valueIteration(dungeon)
affiche()