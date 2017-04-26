# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from parazite1 import *
from healthy import *
<<<<<<< HEAD
from gui1 import *
import random

NB_SAINS = 5
NB_PARASITE = 3
INFECT_CHANCE = 100

list_of_healhies = []
list_of_parazites = []

seed(42)

def start(nb_sains=NB_SAINS, nb_parasite=NB_PARASITE):
    for i in range(nb_sains):
        list_of_healhies.append(Healthy(200, 200)) #changer attributs 
    for i in range(nb_parasite):
        list_of_parazites.append(Parazite(5,6,1))    #changer attributs

    actions_when_collision(list_of_parazites[1],list_of_healhies[2])    #test
        
def actions_when_collision(p1,p2):
    possible_classes = [Healthy, Parazite]
    if isinstance(p1, tuple(possible_classes)) : # si c'est l'un des deux
        if isinstance(p2, tuple(possible_classes)):
            if random.randrange(0,100) < INFECT_CHANCE:
                print "infect him! "    # à faire

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
    
start()
if __name__ == '__main__':                                                                                             
    Gui1App().run()

main()
