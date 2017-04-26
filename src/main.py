# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from parazite1 import *
from healthy import *
from random import randint, seed

seed(42)

nb_sains = 5
nb_parasite = 3
hauteur_container = 200
largeur_container = 300
max_velocity = 10
max_vir = 100


def start(nb_sains, nb_parasite): 
    indi = []
    heal = []
    para = []
    for i in range(nb_sains):
        x = randint(0, max_velocity) # voir ligne 23
        heal.append(Healthy([randint(0, largeur_container),randint(0, hauteur_container)],  #crée un individu healthy avec un vecteur pos
        [x , max_velocity - x]))  # et un vecteur speed, somme des composantes vaut max_velocity 
    for a in heal: 
        indi.append(a) # les ajoute a la liste complète des individus
    for i in range(nb_parasite):
        x = randint(0, max_velocity) #voir ligne 29
        para.append(Parazite([randint(0, largeur_container), # crée un parazite avec position aléatoire dans le conteneur
        randint(0, hauteur_container)],[x , max_velocity - x], # un vitesse aléatoire, la somme des composantes vaut max_velocity
        randint(0, max_vir))) # j'ai mis la virulence au hasard, mais on va plutot la défénir par parasite non?
    for i in para: 
        indi.append(i) # ajoute à la liste complète
    for i in heal: #test    
        print i # test 
    for i in para: # test
        print Parazite.getVir(i) #test
    
       

def main():
    print 'le programme de sa mère\n'
    start(nb_sains, nb_parasite)
    
main()
