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

seed(45)

dico_id = {}    #on ajoute les id de individu dans le dico
list_of_freed_id = [] # on ajoute les id des mort à cette liste

list_of_healthies = []
list_of_parazites = []

balls_dictionnary = {}  #key:[widget_ball,individual, position]

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
        try:
            temp = create_id()
            if temp not in dico_id.keys():
                list_of_healthies.append(Healthy(temp))
                dico_id[temp] = list_of_healthies[-1]
            else :
                print temp, 'exists in ', dico_id.keys(), "in add_healthy function"
        except: 
            print "could not add health: ID problem"
            
def add_one_healthy(res=[]) :
    try:
        temp = create_id()
        if temp not in dico_id.keys():
            list_of_healthies.append(Healthy(temp,res))
            dico_id[temp] = list_of_healthies[-1]
            return list_of_healthies[-1]
        else :
            print temp, 'exists in ', dico_id.keys(), "in add_healthy function"
    except: 
        print "could not add health: ID problem"
            
def add_one_parazite(p = None) :
    try:
        temp = create_id()
        if p != None :      #si pas par défaut, on reprend
            temp_vir = p.getVir()
            temp_trans = p.getTransmRate()
            temp_recov = p.getRecovProb()
        else :              #sinon on crée
            temp_vir = uniform(0,1)
            temp_trans = uniform(0,1)
            temp_recov = uniform(0,1)
            norm = BASE_FITNESS/(temp_vir + temp_trans + temp_recov)
            temp_vir *= norm
            temp_trans *= norm
            temp_recov *= norm

        if temp not in dico_id.keys():
            list_of_parazites.append(Parazite(temp_vir, temp_trans, temp_recov, temp))
            temp_strain = list(list_of_parazites[-1].getStrain())
            #print temp_strain
            #print list_of_parazites[-1].getIdd()
            temp_strain.append(list_of_parazites[-1].getIdd())
            #print temp_strain
            list_of_parazites[-1].setStrain(temp_strain)
            #print "bis :   ", list_of_parazites[-1].getStrain()
            dico_id[temp] = list_of_parazites[-1]

            return list_of_parazites[-1]

        else :
            print temp, 'exists in ', dico_id.keys(), "in add_healthy function"
    except: 
        print "could not add health: ID problem"
                 

def kill(root,p):
    if not isinstance(p, Individual): 
        print "%s doit être un individu pour être tué" % str(p)
        return
    elif isinstance(p, Healthy):
        list_of_healthies.remove(p)              #d'abord on gère les idd
    elif isinstance(p, Parazite):
        list_of_parazites.remove(p)

    list_of_freed_id.append(p.getIdd())     
    del dico_id[p.getIdd()]
    root.remove_widget(balls_dictionnary[p.getIdd()][0])    #puis on enlève la widget (gui)
    del balls_dictionnary[p.getIdd()][0]                    #puis on gère le dico, on tue l'objet
    del balls_dictionnary[p.getIdd()]                       #on tue l'entrée dans le dico
    del p                                                   #et enfin on tue l'objet

def reproduce(root,p):
    ball = Ball()
    x = uniform(0,1)
    ball.center = (balls_dictionnary[p.getIdd()][0].center[0] + x, balls_dictionnary[p.getIdd()][0].center[1] + (1-x))
    ball.velocity = balls_dictionnary[p.getIdd()][0].velocity
    root.add_widget(ball)

    healthy = add_one_healthy()
    balls_dictionnary[healthy.getIdd()] = [ball, healthy, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
    
    if isinstance(p, Parazite):
        infect_him(p, balls_dictionnary[healthy.getIdd()][1], parazites_reproducing=True)
        random_mutation_on(balls_dictionnary[list_of_parazites[-1].getIdd()][1], 'reproduction')
    if isinstance(p, Healthy) :
        for i in p.getResistances() :
            list_of_healthies[-1].setResistance(i)
            #if len(list_of_healthies[-1].getResistances()) > 1 :
             #   ball.set_col(SPEC_BASE_COLOR)
        

def guerison(p):
    if isinstance(p, Parazite):
        list_of_healthies.append(Healthy(p.getIdd()))
        if uniform(0,1) < TRANSMISSION_OF_RESISTANCE_PROB:
            list_of_healthies[-1].addResistance(p.getStrain())
            print "guerison de ",list_of_healthies[-1].getIdd(), " ----------------------  resistances:" , list_of_healthies[-1].getResistances()
        list_of_parazites.remove(p)
        balls_dictionnary[p.getIdd()][1] = list_of_healthies[-1]
        balls_dictionnary[p.getIdd()][0].set_col(BASE_COLOR)

def cure_the_lucky_ones(dt) :
    for i in iter(list_of_parazites):
        if uniform(0,1) > (1-BASE_CHANCE_OF_HEALING)*(1+i.getRecovProb()) :    #! RecovProb = 1 --> aucune chance de recover
            pass
            guerison(i)

def mutate_those_who_wish(dt) :
    for i in iter(list_of_parazites) :
        if uniform(0,1) < CHANCE_OF_MUTATION_ON_NOTHING :
            random_mutation_on(i,'living')

def kill_those_who_have_to_die(root,dt) :
    for i in list_of_healthies:
        if uniform(0,1) < DYING_PROB :    #! RecovProb = 1 --> aucune chance de recover
            kill(root,i)
    for i in list_of_parazites:
        if uniform(0,1) < DYING_PROB*(1 + balls_dictionnary[i.getIdd()][1].getVir()) :    #! RecovProb = 1 --> aucune chance de recover
            kill(root,i)

def reproduce_those_you_have_to(root,dt) :
    for i in list_of_healthies:
        if uniform(0,1) < REPRODUCTION_PROB :    #! RecovProb = 1 --> aucune chance de recover
            reproduce(root, i)
    for i in list_of_parazites:
        if uniform(0,1) < REPRODUCTION_PROB :    #! RecovProb = 1 --> aucune chance de recover
            reproduce(root,i)

def random_mutation_on(para_i, what) :
    chance = 0
    fit_change = 0
    if what == 'infection' :
        chance = CHANCE_OF_MUTATION_ON_INFECTION
        fit_change = MAX_FITNESS_CHANGE_ON_INFECTION
    elif what == 'reproduction' :
        chance = CHANCE_OF_MUTATION_ON_REPRODUCTION
        fit_change = MAX_FITNESS_CHANGE_ON_REPRODUCTION
    elif what == 'living' :
        chance = CHANCE_OF_MUTATION_ON_NOTHING
        fit_change = MAX_FITNESS_CHANGE_ON_NOTHING

    if uniform(0,1) < chance:      #prob. de mutation
        old_attributes = [para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb()]
        attribute_functions = {'0':para_i.set_New_Vir, '1':para_i.set_New_TransmRate, '2':para_i.set_New_RecovProb, '3': para_i.setStrain([])}
        
        
        rand_mod = (randint(0,1)*2-1)*(1+uniform(0, fit_change))    #modificateur valant au max 1+0.2 (p. ex)
        rand_index = randint(0,2)
        new_value = max(min(old_attributes[rand_index] * rand_mod, 1),-1)   #new attribute = 1.2*old attribute (au max)
        attribute_functions[str(rand_index)](new_value)                     #on appelle la fonction correspondante
        print "mutation ----------------- nouvelle souche: ", para_i.getIdd()
        new_strain = para_i.getIdd()        
        para_i.setStrain([new_strain])
        
        
        x = randint(0,2)
        random_color = list(balls_dictionnary[list_of_parazites[-1].getIdd()][0].get_col())
        random_color[x] = min(uniform(0,1)*uniform(0,1), 1)
        balls_dictionnary[list_of_parazites[-1].getIdd()][0].set_col(tuple(random_color))
        

def infect_him(para_i,heal_i, parazites_reproducing=False) :
    resistant = False 
    #testing_par = [para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb()]
    testing_par = para_i.getStrain()
    if testing_par in heal_i.getResistances() :
            resistant = True
    if not resistant :
        temp_par = list(para_i.getPar())
        temp_par.append(para_i.getIdd())
        temp_strain = list(para_i.getStrain())
        #print temp_strain
        #print list_of_parazites[-1].getIdd()
        #temp_strain.append(heal_i.getIdd())
        #print temp_strain
        list_of_parazites.append(Parazite(para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb(), heal_i.getIdd(), temp_par, temp_strain))
        print para_i.getIdd(),"infecte :  ", heal_i.getIdd(), "souche : ", list_of_parazites[-1].getStrain()
        list_of_healthies.remove(heal_i)
        balls_dictionnary[heal_i.getIdd()][1] = list_of_parazites[-1]
        balls_dictionnary[list_of_parazites[-1].getIdd()][0].set_col(balls_dictionnary[para_i.getIdd()][0].get_col())

        if random_mutation_on(list_of_parazites[-1], 'infection') :
            x = randint(0,2)
            random_color = list(balls_dictionnary[list_of_parazites[-1].getIdd()][0].get_col())
            random_color[x] = min(uniform(0,1)*uniform(0,1), 1)
            balls_dictionnary[list_of_parazites[-1].getIdd()][0].set_col(tuple(random_color))

def actions_when_collision(p1,p2):
    possible_classes = [Healthy, Parazite]
    if isinstance(p1, tuple(possible_classes)) :        # si c'est l'un des deux
        possible_classes.remove(type(p1))               #on l'enlève
        if isinstance(p2, tuple(possible_classes)):     #si c'est l'autre
            if isinstance(p2, Parazite) :
                p1,p2 = p2,p1                           #on veut que p1 soit le parazite (lisibilité)
            if uniform(0,1) < INFECTION_CHANCE *(1+p1.getTransmRate()) :    #là aussi, infection chance cap at 0.5
                infect_him(p1,p2)




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
        Clock.schedule_interval(root.update_life_and_death, 60*DELTA_TIME)    #ça ça marche
        return root


#-----------------------Main--------------------------------------

# ----------------------Balls container--------------------------

class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    def start_balls(self,dt):
        for i in range(0,NB_SAINS):
            ball = Ball()
            ball.center = (randint(self.x, self.x+self.width), randint(self.y, self.y+self.height))
            ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),         #à revoir
                             -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
            self.add_widget(ball)

            healthy = add_one_healthy()
            balls_dictionnary[healthy.getIdd()] = [ball, healthy, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
        for i in range(0,NB_PARASITE):
            ball = Ball()
            ball.center = (randint(self.x, self.x+self.width), randint(self.y, self.y+self.height))
            ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),         #à revoir
                             -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
            self.add_widget(ball)
            ball.set_col((uniform(0,1),uniform(0,1),0))

            parazite = add_one_parazite()
            balls_dictionnary[parazite.getIdd()] = [ball, parazite, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
            

    #@profile
    def update(self,dt):
        quad = Quadtree(0,[self.x,self.x + self.width, self.y, self.y + self.height])
        quad.reset()    #est-ce que ça sert à rien ?

        for i in balls_dictionnary.keys() :
#            if balls_dictionnary[i][0].get_col() != BASE_COLOR and isinstance(balls_dictionnary[i][1], Healthy):
#                balls_dictionnary[i][0].set_col(BASE_COLOR)
            pos = balls_dictionnary[i][0]
            balls_dictionnary[i][2] = [pos.x, pos.x + pos.width, pos.y, pos.y + pos.height]

            quad.insert(balls_dictionnary[i][2], i)

        for i in balls_dictionnary.keys() :

            temp_balls = quad.fetch(balls_dictionnary[i][2],i)
            temp_keys = [k[1] for k in temp_balls]
            other_balls = {key:balls_dictionnary[key] for key in temp_keys}

            for j in other_balls.keys():
                
                if physical_collision2(balls_dictionnary[i][0], other_balls[j][0]):
                    actions_when_collision(balls_dictionnary[i][1], other_balls[j][1])

            physical_wall_collisions2(balls_dictionnary[i][0], self)

            #-------------- update balls here -----------------
            balls_dictionnary[i][0].update(dt)
            #-------------- update balls here -----------------

    def update_life_and_death(self,dt):
        kill_those_who_have_to_die(self,dt)
        reproduce_those_you_have_to(self,dt)
        cure_the_lucky_ones(dt)
        mutate_those_who_wish(dt)

# -------------------- balls container--------------------

#-----------------------------Kivy GUI-----------------------------------------------
if __name__ == '__main__':  
    mainApp().run()
#-----------------------------Kivy GUI-----------------------------------------------


