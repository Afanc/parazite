# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from BallsContainer import *
from parazite1 import *
from healthy import *

seed(42)

dico_id = {}    #on ajoute les id de individu dans le dico
list_of_freed_id = [] # on ajoute les id des mort à cette liste

list_of_healhies = []
list_of_parazites = []

def create_id():
    if len(list_of_freed_id) == 0:
        idd = "ID" + str(len(dico_id))
        #regarder si la clé idd est unique dans le dico
    else: 
        idd = list_of_freed_id[-1]
    return idd
    
def add_healthy(nb_sains = NB_SAINS):
    for i in range(nb_sains):
        x = randint(0, MAX_VELOCITY)
        try:
            temp = create_id()
            if temp not in dico_id.keys():
                list_of_healhies.append(Healthy([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)], [x , MAX_VELOCITY- x], temp))
                dico_id[temp] = list_of_healhies[-1]
        except: 
            print "could not add health: ID problem"
            
      
def add_parazite(nb_parasite=NB_PARASITE):
    for i in range(nb_parasite):
        x = randint(0, MAX_VELOCITY)
        #try:
        temp = create_id()
        if temp not in dico_id.keys():
            list_of_parazites.append(Parazite([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)],randint(0,MAX_VELOCITY), randint(0, MAX_VIRULANCE),1,1, temp))    #changer attributs
            dico_id[temp] = list_of_parazites[-1]
        #except: 
            #print "could not add parazite: ID problem"
            
            
def start(nb_sains=NB_SAINS, nb_parasite=NB_PARASITE):
    add_healthy()
    add_parazite()

def actions_when_collision(p1,p2):
    possible_classes = [Healthy, Parazite]
    if isinstance(p1, tuple(possible_classes)) :        # si c'est l'un des deux
        possible_classes.remove(type(p1))               #on l'enlève
        if isinstance(p2, tuple(possible_classes)):     #si c'est l'autre
            if random.randrange(0,100) < INFECT_CHANCE:
                nb_parasite    # à faire

def kill(p):
    if not isinstance(p, Individual): 
        print "%s doit être un individu pour être tué" % str(p)
        return
    elif isinstance(p, Healthy):
        list_of_healhies.remove(p)
        list_of_freed_id.append(p.getIdd())
        del dico_id[p.getIdd()]
        del p
    elif isinstance(p, Parazite):
        list_of_parazites.remove(p)
        list_of_freed_id.append(p.getIdd())
        del dico_id[p.getIdd()] 
        del p


def guerison(p):
    if not isinstance(p, Individual): 
        print "%s doit être un individu pour être tué" % str(p)
    if isinstance(p, Parazite):
        speed = p.getSpeed()
        pos = p.getPosition()
        idd = p.getIdd()
        hourglass = p.getHourglass()
        list_of_healhies.append(Healthy(pos, speed, idd, hourglass))
        list_of_parazites.remove(p)
        del p
        
    
def main():
    print 'le programme de sa mère\n'
    
#start()
if __name__ == '__main__':                                                                                             
    #Gui1App().run()
    print "bravo"



add_healthy(2)
print "A" + str(list_of_healhies[0].getIdd())
print "B" + str(list_of_freed_id)
print "C" + str(dico_id)

kill(list_of_healhies[1])
print "D" + str(list_of_healhies)
print "E" + str(list_of_freed_id)
print "F" + str(dico_id)

#actions_when_collision(list_of_parazites[1],list_of_healhies[2])    #test


#-----------------------------Kivy GUI-----------------------------------------------
if __name__ == '__main__':  
    mainApp().run()
#-----------------------------Kivy GUI-----------------------------------------------


