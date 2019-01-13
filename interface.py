# -*- coding: utf-8 -*-

import pygame

from pygame.locals import *
from grille import *
from function import *
from solve import *

"""
Affichage
"""
def afficheDecision(dungeon, objects, do_blit=False):
    actions = ["right", "left", "top", "bottom"]
    pygame.init()
    tailleX = 60
    tailleY = 36
    fenetre = pygame.display.set_mode((len(dungeon.cases) * tailleX, len(dungeon.cases[0]) * tailleY))
    imagedecisions = {action:pygame.image.load(action+".png").convert_alpha() for action in actions}
    print(imagedecisions)
    image = [[0 for i in ligne] for ligne in dungeon.cases]
    for i in range(len(dungeon.cases)):
        for j in range(len(dungeon.cases[0])): 
            case = dungeon.cases[i][j]
            image[i][j] = pygame.image.load(case.image).convert()
            fenetre.blit(image[i][j], (j*tailleX,i*tailleY))
            
            # Si on a un choix à faire dans la case
            if type(case) not in [Wall, Cracks, MovingPlatform, MagicPortal]:
                state = dungeon.getState(case, objects)
                if state.decision:
                    fenetre.blit(imagedecisions[state.decision], (j*tailleX,i*tailleY))
     
    continuer = 1
    #Boucle infinie
    if do_blit:
        while continuer:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
                if event.type == QUIT:     #Si un de ces événements est de type QUIT
                    continuer = 0      #On arrête la boucle
        
            pygame.display.flip()
 
def jouer(dungeon):
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
                if event.key == K_LEFT:
                    if "left" in case.voisin.keys():
                        case = case.voisin["left"]
                if event.key == K_RIGHT:
                    if "right" in case.voisin.keys():
                        case = case.voisin["right"]                 
                if event.key == K_UP:
                    if "top" in case.voisin.keys():
                        case = case.voisin["top"]                 
                if event.key == K_DOWN:
                    if "bottom" in case.voisin.keys():
                        case = case.voisin["bottom"]   
                
                # Si on souhaite avoir de l'aide
                if event.key == K_SPACE:
                    if state.decision:
                        case = case.voisin[state.decision]
                        
                adventurer.goIn(case)
                alive = adventurer.case.action(adventurer)
                if not alive:
                    adventurer.goIn(dungeon.startingPosition)
                    adventurer.objects = []
 
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
    display_decisions = False
    while continuer:
        pygame.time.Clock().tick(30)
        case = adventurer.case
        state = dungeon.getState(case, adventurer.objects)

        for i in range(len(dungeon.cases)):
            for j in range(len(dungeon.cases[0])):
                fenetre.blit(image[i][j], (j*tailleX,i*tailleY))

        if display_decisions:
            afficheDecision(dungeon, dungeon.adventurer.objects)
            
        fenetre.blit(perso, (state.case.j*tailleX,state.case.i*tailleY))
        for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
            if event.type == QUIT:     #Si un de ces événements est de type QUIT
                continuer = 0      #On arrête la boucle

            if event.type == KEYDOWN:
                if event.key == K_SPACE: 
                    adventurer.goIn(case.voisin[state.decision])
                    adventurer.case.action(adventurer)

			
                if event.key == K_o:
                    display_decisions = not display_decisions


 

                    #state.afficher()
                    #print(state.objects)
        #Rafraîchissement de l'écran
        pygame.display.flip()

dungeon = Dungeon()
dungeon.open("Dungeon2.txt")
dungeon.instanciation(Adventurer(), False)
#qlearning(dungeon)
#valueIteration(dungeon)
valueIteration(dungeon)
affiche(dungeon)