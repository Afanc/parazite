# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

#from BallsContainer import *
from parazite1 import *
from healthy import *
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
from datetime import datetime
from quadtree import Quadtree
from collision import *

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
        list_of_freed_id.remove(idd)
    return idd
    
def add_healthy(nb_sains = NB_SAINS):
    for i in range(nb_sains):
        x = randint(0, MAX_VELOCITY)
        try:
        
            temp = create_id()
            if temp not in dico_id.keys():
                list_of_healhies.append(Healthy([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)], [x , MAX_VELOCITY- x], temp))
                dico_id[temp] = list_of_healhies[-1]
            else :
                print temp, 'exists in ', dico_id.keys(), "in add_healthy function"
        except: 
            print "could not add health: ID problem"
            
      
def add_parazite(nb_parasite=NB_PARASITE):
    for i in range(nb_parasite):
        x = randint(0, MAX_VELOCITY)
        try:
            temp = create_id()
            if temp not in dico_id.keys():
                list_of_parazites.append(Parazite([randint(0, CONTAINER_WIDTH),randint(0, CONTAINER_HEIGHT)],randint(0,MAX_VELOCITY), uniform(0, MAX_VIRULANCE),0,0, temp))    #changer attributs
                dico_id[temp] = list_of_parazites[-1]
            else :
                print temp, 'exists in ', dico_id.keys(), "in add_parazite function"
        except: 
            print "could not add parazite: ID problem"
            
            
def start(nb_sains=NB_SAINS, nb_parasite=NB_PARASITE):
    add_healthy()
    add_parazite()

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
        list_of_healhies.append(Healthy(p.getPosition(), p.getSpeed(), p.getIdd()))
        list_of_parazites.remove(p)
        del p

def cure_the_lucky_ones(dt) :
    for i in iter(list_of_parazites):
        if uniform(0,1) > i.getRecovProb() :    #! RecovProb = 1 --> aucune chance de recover
            guerison(i)

def kill_those_who_have_to_die(dt) :
    for i in enumerate(list_of_healhies):
        if uniform(0,1) > DYING_PROB :    #! RecovProb = 1 --> aucune chance de recover
            kill(i)
    for i in enumerate(list_of_parazites):
        if uniform(0,1) > DYING_PROB*(1 + p.getVir()) :    #! RecovProb = 1 --> aucune chance de recover
            kill(i)

def random_mutation_on_infection(para_i, heal_i) :
    old_attributes = [para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb()]
    attribute_functions = {'0':para_i.set_New_Vir, '1':para_i.set_New_TransmRate, '2':para_i.set_New_RecovProb}

    if uniform(0,1) < CHANCE_OF_MUTATION_ON_INFECTION :      #prob. de mutation
        rand_mod = (randint(0,1)*2-1)*(1+uniform(0, MAX_FITNESS_CHANGE_ON_REPRODUCTION))    #modificateur valant au max 1+0.2 (p. ex)
        rand_index = randint(0,2)
        new_value = max(min(old_attributes[rand_index] * rand_mod, 1),-1)   #new attribute = 1.2*old attribute (au max)
        attribute_functions[str(rand_index)](new_value)                     #on appelle la fonction correspondante

def actions_when_collision(p1,p2):
    possible_classes = [Healthy, Parazite]
    if isinstance(p1, tuple(possible_classes)) :        # si c'est l'un des deux
        possible_classes.remove(type(p1))               #on l'enlève
        if isinstance(p2, tuple(possible_classes)):     #si c'est l'autre
            if uniform(0,1) < INFECT_CHANCE:
                nb_parasite    # à faire

def infect_him(heal_i,para_i) :
    random_mutation_on_infection(para_i, heal_i)


    try:
        temp = create_id()
        if temp not in dico_id.keys():
            list_of_parazites.append(Parazite(heal_i.getPosition(),heal_i.getSpeed(), randint(0, MAX_VIRULANCE),1,1, temp))    #changer attributs
            dico_id[temp] = list_of_parazites[-1]
            list_of_healhies.remove(heal_i)
        else :
            print temp, 'exists in ', dico_id.keys(), "in infect_him function"
    except: 
        print para_i, " could not infect ", heal_i

    
    

#-----------------------main --------------------------
    
def main():
    print 'le programme de sa mère\n'

class mainApp(App):                                                                                                    
    """Represents the whole application."""
    def build(self):
        """Entry point for creating app's UI."""
        root = BallsContainer()
        Clock.schedule_once(root.start_balls,1)         #on attend que la fenêtre soit lancée
        Clock.schedule_interval(root.update, DELTA_TIME)
        Clock.schedule_interval(test, 60*DELTA_TIME)    #ça ça marche
        return root

def test(dt):
    print 'youpila'

#-----------------------Main--------------------------------------

# ----------------------Balls container--------------------------

class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    def start_balls(self,dt):
        for i in range(0,50):
            ball = Ball()
            ball.center = (randint(self.x, self.x+self.width), randint(self.y, self.y+self.height))
            ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),         #à revoir
                             -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
            self.add_widget(ball)

    #@profile
    def update(self,dt):
        quad = Quadtree(0,[self.x,self.x + self.width, self.y, self.y + self.height])
        quad.reset()    #est-ce que ça sert à rien ?
        balls = {}

        for c in self.children: 
            if isinstance(c,Ball) :
                balls[(c.x, c.x + c.width, c.y, c.y + c.height)] = c   #key : position, access : ball

        for i in balls :                                        #obligés de faire un 1e boucle pour toutes les placer
            if balls[i].get_col() != BASE_COLOR:                #petit hack pour les couleurs, on profite des boucles
                balls[i].set_col(BASE_COLOR)

            quad.insert(i)                                      #préparer le quad

        for i in balls:                                         #for each key (=position)
            temp_keys = quad.fetch(i)                           #on fetch les collisions
            other_balls = {key:balls[key] for key in temp_keys} #on crée un nouveau dico avec que les collisions

            for j in other_balls:
                
                if physical_collision(balls, other_balls, i, j):
                    pass

            physical_wall_collisions(balls, i, self)

            #-------------- update balls here -----------------
            balls[i].update(dt)
            #-------------- update balls here -----------------
   

# -------------------- balls container--------------------

#print "A" + str(list_of_healhies[0].getIdd())
#print "B" + str(list_of_freed_id)
#print "C" + str(dico_id)
#
#kill(list_of_healhies[1])
#print "D" + str(list_of_healhies)
#print "E" + str(list_of_freed_id)
#print "F" + str(dico_id)

#actions_when_collision(list_of_parazites[1],list_of_healhies[2])    #test

add_healthy(2)
add_parazite(2)

random_mutation_on_infection(list_of_parazites[0],list_of_healhies[0])
#-----------------------------Kivy GUI-----------------------------------------------
if __name__ == '__main__':  
    mainApp().run()
#-----------------------------Kivy GUI-----------------------------------------------


