# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from parazite1 import *
from healthy import *
from gui1 import *
import random

NB_SAINS = 5
NB_PARASITE = 3
INFECT_CHANCE = 100

list_of_healhies = []
list_of_parazites = []

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

def main():
    print 'le programme de sa mère\n'
    
start()
if __name__ == '__main__':                                                                                             
    Gui1App().run()

