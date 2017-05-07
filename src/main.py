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
from kivy.core.window import Window
from datetime import datetime
from quadtree import Quadtree
from collision import *
import matplotlib.pyplot as plt

seed(42)

dico_id = {}    #on ajoute les id de individu dans le dico
balls_dictionnary = {}  #key:[widget_ball,individual, position]
strain_dictionary = {} #{souche:[vir,transmission, guérison][liste des infectés]}

list_of_healthies = []
list_of_parazites = []

compteur_id = 1

def create_id():
    '''crée un nouvel id pour chaque nouveau parasite'''
    global compteur_id
    idd = "ID" + str(compteur_id)
    compteur_id += 1
    
    return idd
    
def add_one_healthy() :
    '''ajoute une individu sain'''
    try:
        temp = create_id()
        if temp not in dico_id.keys():
            list_of_healthies.append(Healthy(temp))
            dico_id[temp] = list_of_healthies[-1]
            return list_of_healthies[-1]
        else :
            print temp, 'exists in ', dico_id.keys(), "in add_healthy function"
    except: 
        print "could not add health: ID problem"
            
def add_one_parazite(p = None) :
    '''ajoute un parasite'''
    try:
        temp_id = create_id()
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

        if temp_id not in dico_id.keys():
            list_of_parazites.append(Parazite(temp_vir, temp_trans, temp_recov, temp_id))
            temp_strain = list(list_of_parazites[-1].getStrain())
            temp_strain.append(list_of_parazites[-1].getIdd())
            temp_strain = str('Souche:' + temp_strain[0][2:])
            list_of_parazites[-1].setStrain(temp_strain)
            strain_dictionary[temp_strain] = [[temp_vir, temp_trans, temp_recov],[str(temp_id)]]
        
            dico_id[temp_id] = list_of_parazites[-1]
            return list_of_parazites[-1]

        else :
            print temp, 'exists in ', dico_id.keys(), "in add_healthy function"
    except: 
        print "could not add parazite: ID problem"
                 

def kill(root,p):
    '''tue un individu'''
    if not isinstance(p, Individual): 
        print "%s doit être un individu pour être tué" % str(p)
        return
    elif isinstance(p, Healthy):
        list_of_healthies.remove(p)              #d'abord on gère les idd
    elif isinstance(p, Parazite):
        list_of_parazites.remove(p)
    
    #list_of_freed_id.append(p.getIdd())
    del dico_id[p.getIdd()]
    root.remove_widget(balls_dictionnary[p.getIdd()][0])    #puis on enlève la widget (gui)
    del balls_dictionnary[p.getIdd()][0]                    #puis on gère le dico, on tue l'objet
    del balls_dictionnary[p.getIdd()]                       #on tue l'entrée dans le dico
    del p                                                   #et enfin on tue l'objet

def reproduce(root,p):
    '''duplique un individu'''
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
        try :
            for i in p.getResistances() :
                list_of_healthies[-1].addResistance(i)
        except :
            print "\n _________________________________________________\nl'erreur ligne 116 !\n______________________________________________\n"
        
    if isinstance(p, Healthy):
        if uniform(0,1) > GENERATION_RESISTANCE:
            for i in p.getResistances():
                list_of_healthies[-1].addResistance(i)

def guerison(p):
    '''gueris un parasite'''
    if isinstance(p, Parazite):
        list_of_healthies.append(Healthy(p.getIdd()))
        if uniform(0,1) < TRANSMISSION_OF_RESISTANCE_PROB:
            for i in p.getResistances() :
                list_of_healthies[-1].addResistance(i)
            list_of_healthies[-1].addResistance(p.getStrain())
            #print "GUERISON de ",list_of_healthies[-1].getIdd(), " ----------------------  resistances:" , list_of_healthies[-1].getResistances()
        list_of_parazites.remove(p)
        balls_dictionnary[p.getIdd()][1] = list_of_healthies[-1]
        balls_dictionnary[p.getIdd()][0].set_col(BASE_COLOR)
    else : print "pas parazite"
    
def cure_the_lucky_ones(dt) :

    for i in iter(list_of_parazites):
        if uniform(0,1) > (1-BASE_CHANCE_OF_HEALING)*(1+i.getRecovProb()) :    #! RecovProb = 1 --> aucune chance de recover
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
        new_value = max(min(old_attributes[rand_index] * rand_mod, 1),0)   #new attribute = 1.2*old attribute (au max)
        attribute_functions[str(rand_index)](new_value)                     #on appelle la fonction correspondante
        new_attributes = [para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb()]
        if what == 'living':
            temp_idd = para_i.getIdd() + '*'
            balls_dictionnary[temp_idd] = balls_dictionnary[para_i.getIdd()]
            del balls_dictionnary[para_i.getIdd()]
            dico_id[temp_idd] = dico_id[para_i.getIdd()]            
            del dico_id[para_i.getIdd()]
            para_i.setIdd(temp_idd)
            #print "---------------------------------------------------LIVING MUTATION", para_i.getIdd()
            
        #nouvelle souche
        new_strain = para_i.getIdd()
        new_strain = 'Souche:' + new_strain[2:]
        para_i.setStrain(new_strain)
        strain_dictionary[new_strain] = [[para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb],[para_i.getIdd()]]
        if what == 'living':
            print  "________________ bug?", para_i.getIdd(),"  ", para_i.getStrain()
        
        x = randint(0,2)
        random_color = list(balls_dictionnary[list_of_parazites[-1].getIdd()][0].get_col())
        random_color[x] = max(min(uniform(-1,1)+random_color[x], 1),0)
        balls_dictionnary[list_of_parazites[-1].getIdd()][0].set_col(tuple(random_color))
    
    else:
        if what == 'infection':

            strain_dictionary[para_i.getStrain()][1].append(para_i.getIdd())


def infect_him(para_i,heal_i, parazites_reproducing=False) :
    resistant = False 
    testing_par = para_i.getStrain()
    if testing_par in heal_i.getResistances() :
        resistant = True
        print "------------------- I RESISTED", heal_i.getResistances()
    if not resistant :
        temp_par = list(para_i.getPar())
        temp_par.append(para_i.getIdd())
        temp_strain = para_i.getStrain()
        list_of_parazites.append(Parazite(para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb(), heal_i.getIdd(), temp_par, temp_strain))
        for i in heal_i.getResistances() :
            list_of_parazites[-1].addResistance(i)
        
        #print " INFECTION", para_i.getIdd(),"infecte :  ", heal_i.getIdd(), "souche : ", list_of_parazites[-1].getStrain()
        list_of_healthies.remove(heal_i)
        balls_dictionnary[heal_i.getIdd()][1] = list_of_parazites[-1]
        balls_dictionnary[list_of_parazites[-1].getIdd()][0].set_col(balls_dictionnary[para_i.getIdd()][0].get_col())

        if random_mutation_on(list_of_parazites[-1], 'infection') :
            x = randint(0,2)
            random_color = list(balls_dictionnary[list_of_parazites[-1].getIdd()][0].get_col())
            random_color[x] = min(uniform(0,1)*uniform(0,1), 1)
            balls_dictionnary[list_of_parazites[-1].getIdd()][0].set_col(tuple(random_color))

def parazite_against_parazite(p1,p2) :
    if p1.getVir() > p2.getVir() :
        p2.setVir(p1.getVir())
        p2.setTransmRate(p1.getTransmRate())
        p2.setRecovProb(p1.getRecovProb())
        balls_dictionnary[p2.getIdd()][0].set_col(balls_dictionnary[p1.getIdd()][0].get_col())
        p2.setStrain(p1.getStrain())
        strain_dictionary[p1.getStrain()][1].append(p2.getIdd())
        print "-------------------combat d'infirmes", p1.getIdd(), " infecte ", p2.getIdd()
        print p2.getStrain()
    elif p2.getVir() > p1.getVir() :
        p1.setVir(p2.getVir())
        p1.setTransmRate(p2.getTransmRate())
        p1.setRecovProb(p2.getRecovProb())
        balls_dictionnary[p1.getIdd()][0].set_col(balls_dictionnary[p2.getIdd()][0].get_col())
        p1.setStrain(p2.getStrain())
        strain_dictionary[p2.getStrain()][1].append(p1.getIdd())
        print "combat d'infirmes", p1.getIdd(), " infecte ", p2.getIdd()

def actions_when_collision(p1,p2):
    possible_classes = [Healthy, Parazite, Parazite]
    if isinstance(p1, tuple(possible_classes)) :        # si c'est l'un des deux
        possible_classes.remove(type(p1))               #on l'enlève
        if isinstance(p2, tuple(possible_classes)):     #si c'est l'autre
            if type(p2) == type(p1) :                   #si ce sont deux parazites
                if uniform(0,1) < PARAZITE_FIGHT_CHANCE :
                    parazite_against_parazite(p1,p2)
            else :
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
        Window.bind(on_key_down=root.KeyboardShortcut)                      #pour le clavier
        return root

#-----------------------Main--------------------------------------

# ----------------------Balls container--------------------------

class BallsContainer(Widget):
    """Class for balls container, a main widget."""
    pause = False
    faster_events = []
    num_healthies = NumericProperty(0)
    num_parazites = NumericProperty(0)
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
        self.update_numbers()

    def update_numbers(self) :
        self.num_parazites = len(list_of_parazites)
        self.num_healthies = len(list_of_healthies)

    def on_pause(self):
        Clock.unschedule(self.update)
        Clock.unschedule(self.update_life_and_death)
        return True

    def on_resume(self):
        Clock.schedule_interval(self.update, DELTA_TIME)
        Clock.schedule_interval(self.update_life_and_death, 60*DELTA_TIME)

    def on_touch_down(self, touch):
        if not self.pause :
            return
        listx = []
        listy = []
        for i in strain_dictionary.keys():
            listx.append(strain_dictionary[i][0][0])
            listy.append(len(strain_dictionary[i][1]))
        plt.scatter(listx, listy)
        plt.ylabel('frequency')
        plt.show()
        return 

    def KeyboardShortcut(self, window, keycode, *args) :
        if keycode == 32 and not self.pause:              #SPACE - pour ça je rajoute un print keycode avant et check le int
            self.on_pause()
            self.pause = True

        elif keycode == 32 and self.pause :
            self.on_resume()
            self.pause = False

        elif keycode == 275 :           #right
            self.faster_events.append([Clock.schedule_interval(self.update, DELTA_TIME), Clock.schedule_interval(self.update_life_and_death, 60*DELTA_TIME)])

        elif keycode == 276 :           #left
            if len(self.faster_events)>0 :
                self.faster_events[-1][0].cancel()
                self.faster_events[-1][1].cancel()
                self.faster_events.pop()
          


# -------------------- balls container--------------------



#-----------------------------Kivy GUI-----------------------------------------------
if __name__ == '__main__':  
    mainApp().run()
    
#-----------------------------Kivy GUI-----------------------------------------------


#test pour les résistances
'''
h = add_one_healthy()
ball = Ball()
balls_dictionnary[h.getIdd()] = [ball, h, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
p = add_one_parazite()
balls_dictionnary[p.getIdd()] = [ball, p, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
h1 = list_of_healthies[-1]
p1 = list_of_parazites[-1]

infect_him(p1,h1)

guerison(list_of_parazites[-1])

print list_of_healthies[-1].getResistances()

infect_him(p1, list_of_healthies[-1])

print"doit etre la", list_of_healthies[-1]

p2 = add_one_parazite()
balls_dictionnary[p2.getIdd()] = [ball, p2, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]

infect_him(p2, list_of_healthies[-1])
print "encore par", list_of_parazites[-1].getResistances()

guerison(list_of_parazites[-1])

print list_of_healthies[-1].getResistances()
'''

#test pour le dico de souches
'''
#infection
h = add_one_healthy() #ID1
ball = Ball()
balls_dictionnary['ID1'] = [ball, h, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
p = add_one_parazite()
balls_dictionnary[p.getIdd()] = [ball, p, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
p1 = balls_dictionnary['ID2'][1]
h1 = balls_dictionnary['ID1'][1]
print p1.getStrain()
infect_him(p1, h1)
h1 = balls_dictionnary['ID1'][1]

print type(h1)
print len(list_of_parazites)
print len(list_of_healthies)

p2 = add_one_parazite()
balls_dictionnary[p2.getIdd()] = [ball, p2, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
list_of_parazites[-1].setVir(0)
print list_of_parazites[-1].getStrain()
parazite_against_parazite(balls_dictionnary['ID2'][1], balls_dictionnary['ID3'][1])
print list_of_parazites[-1].getStrain()
print strain_dictionary[balls_dictionnary['ID2'][1].getStrain()]

reproduce(dt, balls_dictionnary['ID2'][1])
'''
