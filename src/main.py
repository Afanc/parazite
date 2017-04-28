# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from parazite1 import *
from healthy import *
from gui1 import *
import random

NB_SAINS = 5
NB_PARASITE = 3
INFECT_CHANCE = 100
CONTAINER_HEIGHT= 200
CONTAINER_WIDTH= 300
MAX_VELOCITY= 10
MAX_VIRULANCE= 100
list_of_id = []

list_of_healhies = []
list_of_parazites = []

seed(42)

def add_healthy(nb_sains = NB_SAINS):
    for i in range(nb_sains):
        x = randint(0, MAX_VELOCITY)
        list_of_healhies.append(Healthy([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)], [x , MAX_VELOCITY- x])) 

def add_parazite(nb_parasite=NB_PARASITE):
    for i in range(nb_parasite):
        x = randint(0, MAX_VELOCITY)
        list_of_parazites.append(Parazite([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)],randint(0,MAX_VELOCITY), randint(0, MAX_VIRULANCE)))    #changer attributs

def start(nb_sains=NB_SAINS, nb_parasite=NB_PARASITE):
    add_healthy()
    add_parazite()

def actions_when_collision(p1,p2):
    possible_classes = [Healthy, Parazite]
    if isinstance(p1, tuple(possible_classes)) :        # si c'est l'un des deux
        possible_classes.remove(type(p1))               #on l'enlève
        if isinstance(p2, tuple(possible_classes)):     #si c'est l'autre
            if random.randrange(0,100) < INFECT_CHANCE:
                print "infect him! "    # à faire

def main():
    print 'le programme de sa mère\n'
    
start()
if __name__ == '__main__':                                                                                             
    Gui1App().run()

main()
actions_when_collision(list_of_parazites[1],list_of_healhies[2])    #test
