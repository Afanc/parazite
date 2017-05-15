# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python


from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ListProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
from kivy.app import App
from functools import partial
from os.path import isfile

import matplotlib.pyplot as plt
import csv 
import time 
import os 
import sys

from quadtree import Quadtree
from collision import *
from parazite1 import *
from healthy import *
from trade_off import trade_off
from del_useless_files import * # si on arrive à faire en sorte que ça se lance tout seul quand on ferme le programme ce serait top
from CHANGING_CONST import *

Window.size = (800, 600)


balls_dictionnary = {}  #id:[widget_ball,individual, position] # pour les individus vivants
strain_dictionary = {} #{souche:[vir,transmission, guérison][liste des infectés]} contient toutes les souches qui ont existé
dico_of_strains_for_csv = {}  #{souche:variable.writerow()}

list_of_healthies = [] #liste des individus sains vivants
list_of_parazites = [] #liste des parasites vivants

if isfile('csv_nb_total_sains_infectes') and 'y' != raw_input("le fichier data existe déjà, le remplaçer? (y/n)"): exit() #écrit les headers dans le dossier 
else:
    with open("nb_total_sains_infectes.csv","w") as csv_nb_total_sains_infectes: #creer le fichier des données générales de la population 
        writer = csv.writer(csv_nb_total_sains_infectes)
        writer.writerow(["temps","population totale","individus sains","individus infectés","pourcentage de la population infectée", "virulence moyenne","taux de guérison","taux de transmission"]) #header des données générales de la pop


def create_id(): 
    '''crée un nouvel id pour chaque nouveau parasite'''
    global compteur_id # on appelle le compteur_id qui permet de créer des ID nouveaux
    idd = "ID" + str(compteur_id) # les ID sont un string qui composés d'ID + un numéro unique
    compteur_id += 1 # on incrémente le compteur global
    
    return idd # la fonction retourne l'idd
    
def add_one_healthy() :
    '''ajoute une individu sain'''
    try:
        temp = create_id() # on commence par lui créer un ID
        list_of_healthies.append(Healthy(temp)) # on l'ajoute à la liste des individus vivants
        return list_of_healthies[-1] # la fonction add_one_healthy retourne l'individu crée
    except: 
        print "could not add health" # imprime un  message si il n'arrive pas à le créer
            
def add_one_parazite(effect = None) :
    '''ajoute un parasite, peut prendre un effet 'effect' en argument'''
    try:
        temp_id = create_id() #commence par créer un ID
        if effect != None and TRADE_OFF == 'leo': #si un effet est donné en argument ...
            effect = float(effect)
            attribute = trade_off(effect_arg = effect) #on utillise la fonction trade_off pour
            temp_vir = attribute[0] #créer une virulence 
            temp_trans = attribute[1] #crée un taux de transmision
            temp_recov = attribute[2]#crée un taux de guérison
        elif TRADE_OFF == 'leo' : #si rien n'est donné en argument et que la méthode de trade_off est "léo"         
            attribute = trade_off() #on utilise trade off sans spécifier d'effet
            temp_vir = attribute[0] # pour créer une virulance,
            temp_trans = attribute[1] #un taux de transmision,
            temp_recov = attribute[2] # un taux de guérison.
        elif TRADE_OFF == 'dariush': # Enfin, si la méthode de trade_off est 'dariush', on crée 
            temp_vir = uniform(0,1) #une virulance,
            temp_trans = uniform(0,1) # un taux de transmission,
            temp_recov = uniform(0,1) # une probabilité de guérison.
            norm = BASE_FITNESS/(temp_vir + temp_trans + temp_recov) # On crée une variable pour les normaliser
            temp_vir *= norm # et on normalise les trois paramètre.
            temp_trans *= norm 
            temp_recov *= norm

        list_of_parazites.append(Parazite(temp_vir, temp_trans, temp_recov, temp_id)) #on ajoute le parasite à la liste
        temp_strain = list(list_of_parazites[-1].getStrain()) # la souche est pour l'instant "[]" par défaut
        temp_strain.append(list_of_parazites[-1].getIdd()) # on lui ajoute l'ID dans la liste
        temp_strain = str('Souche-' + temp_strain[0][2:])# On modifie la variable temporaire pour que les souches et les ID soient bien distincts
        list_of_parazites[-1].setStrain(temp_strain) #On modifie la souche du parasite pour la souche temporaire
        strain_dictionary[temp_strain] = [[temp_vir, temp_trans, temp_recov],[str(temp_id)]] #et on stocke la souche et l'individu infecté dans le dico des souches
        New_strain_in_csv(temp_strain, temp_vir, temp_trans, temp_recov)
        return list_of_parazites[-1] # la fonction retourne l'individu crée
    except: 
        print "could not add parazite: problem" #messsge d'erreur
                 

def kill(root,p):
    '''tue un individu, prend un individu 'p' en argument'''
    if not isinstance(p, Individual): # vérifie que l'instance donnée en argument soit un individu
        print "%s doit être un individu pour être tué" % str(p) # sinon imprime un message d'erreur
        return # et ne retourne rien
    elif isinstance(p, Healthy): # si c'est un healthy....
        list_of_healthies.remove(p)  #il faut le retirer de la bonne liste
    elif isinstance(p, Parazite): # si c'est un parasite 
        list_of_parazites.remove(p) # il faut le retirer de la bonne liste
    root.remove_widget(balls_dictionnary[p.getIdd()][0])    #puis on enlève la widget (gui)
    del balls_dictionnary[p.getIdd()][0]                    #puis on gère le dico des balles, on tue l'objet
    del balls_dictionnary[p.getIdd()]                       #on tue l'entrée dans le dico
    del p                                                   #et enfin on tue l'objet
    
    
def reproduce(root,p):
    '''duplique un individu, prend un individu 'p' en argument'''
    ball = Ball() # crée une balle et la stocke dans la variable ball
    x = uniform(0,1) # crée une nombre aléatoire entre zéro et un....
    ball.center = (balls_dictionnary[p.getIdd()][0].center[0] + x, balls_dictionnary[p.getIdd()][0].center[1] + (1-x)) # pour le placement de la boule
    ball.velocity = balls_dictionnary[p.getIdd()][0].velocity 
    root.add_widget(ball) #ajoute la balle au container
    healthy = add_one_healthy() 
    balls_dictionnary[healthy.getIdd()] = [ball, healthy, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
    if isinstance(p, Parazite): # si son parent est parasité 
        infect_him(p, balls_dictionnary[healthy.getIdd()][1], parazites_reproducing=True) #l'enfant est parasité par la même souche à la naissance...
        random_mutation_on(balls_dictionnary[list_of_parazites[-1].getIdd()][1], 'reproduction') #si il n'y a pas de mutation
        try :
            if uniform(0,1) > TRANSMISSION_RESISTANCE: #permet de lancer le programme avec ou sans le passage des résistance
                for i in p.getResistances() : # Chaque resistance du parent
                    list_of_healthies[-1].addResistance(i) # est passée au jeune
        except :
            print "\n _________________________________________________\nerreur dans reproduce !\n______________________________________________\n"
        
    if isinstance(p, Healthy): #si healthy 
        if uniform(0,1) < TRANSMISSION_RESISTANCE: # si le progrmme est lancé avec GENERATION_RESISTANCE = 1
            for i in p.getResistances(): # chaque resistance du parent
                list_of_healthies[-1].addResistance(i) #est passée au jeune

def guerison(p):
    '''gueris un parasite, prend un parasite 'p' en argument '''
    try:
        list_of_healthies.append(Healthy(p.getIdd()))
        if uniform(0,1) < RESISTANCE_AFTER_RECOVERY:
            for i in p.getResistances() :
                list_of_healthies[-1].addResistance(i)
            list_of_healthies[-1].addResistance(p.getStrain())
        list_of_parazites.remove(p)
        balls_dictionnary[p.getIdd()][1] = list_of_healthies[-1]
        balls_dictionnary[p.getIdd()][0].set_col(BASE_COLOR)
    except : print "problème dans guérison"
    
def cure_the_lucky_ones(dt) :
    '''On parcourt la liste de tous les parasites. A chaque itération on tire un nombre au hasard entre 0 et 1 et on le compare à la constante BASE_CHANCE_OF_HEALING * la probabilité de guérison spécifique au parasite en question. Si le nombre tiré est inférieur on transforme le parasite en individu sain en appelant la fonction guérison.
'''
    if TRADE_OFF == 'dariush':
        for i in iter(list_of_parazites): #Parcours la liste des parasites. 
            if uniform(0,1) < BASE_CHANCE_OF_HEALING *(1-i.getRecovProb()) :  #  Si la probabilité de guérison de base * 1 + la probabilité de guérison spécifique au parasite est plus grande qu'un nombre au hasard entre 0 et 1 
                guerison(i) #l'individu est guéri. !si le taux de guérison vaut 1, plus de chances de guérir.
    elif TRADE_OFF == 'leo' :
        for i in iter(list_of_parazites): #Parcours la liste des parasites. 
            if uniform(0,1) < BASE_CHANCE_OF_HEALING *(1+i.getRecovProb()) :  #  Si la probabilité de guérison de base * 1 + la probabilité de guérison spécifique au parasite est plus grande qu'un nombre au hasard entre 0 et 1 
                guerison(i) #l'individu est guéri. !si le taux de guérison vaut 1, plus de chances de guérir.


def mutate_those_who_wish(dt) : 
    '''On parcourt la liste des parasites. Si la probabilité de mutation spontanée) de base (CHANCE_OF_MUTATION_ON_NOTHING est plus grande qu'un nombre au hasard entre 0 et 1, on utilise la fonction random_mutation_on pour faire muter un parasite, avec l'argument what = living '''
    for i in iter(list_of_parazites) : #Parcours la liste des parasites.
        if uniform(0,1) < CHANCE_OF_MUTATION_ON_NOTHING : # Si la probabilité de mutation spontanée de base est plus grande qu'un nombre au hasard entre 0 et 1
            random_mutation_on(i,'living') # on utilise la fonction pour faire muter un parasites, avec l'argument what = 'living'

def kill_those_who_have_to_die(root,dt) : 
    '''On parcourt la liste des parasites et des individus sains, on compare une valeur tirée au hasard avec la constante DYING_PROB qui représente leur risque de mourir à chaque instant, si la valeur tirée est inférieure l’individu meurt. Les parasites ont plus de risque de mourir qui dépend de leur virulence car la valeur DYING_PROB est multiplié par la valeur de virulence du parasite et qui dépend de chaque souche.
'''
    for i in list_of_healthies:
        if uniform(0,1) < DYING_PROB :    #! RecovProb = 1 --> aucune chance de recover
            kill(root,i)
    for i in list_of_parazites:
        if uniform(0,1) < DYING_PROB*(1 + balls_dictionnary[i.getIdd()][1].getVir()) :    #! RecovProb = 1 --> aucune chance de recover
            kill(root,i)
            
def reproduce_those_who_have_to(root,dt) :
    '''On parcourt la liste de tous les individus sains, puis celle des parasites. Pour chaque individu on tire une valeur au hasard et on compare avec la constante REPRODUCTION_PROB, si la valeur tirée au hasard est inférieure à la constante, on appelle la fonction reproduce et l’individu se reproduit.
'''
    for i in list_of_healthies:
        if uniform(0,1) < REPRODUCTION_PROB :    #! RecovProb = 1 --> aucune chance de recover
            reproduce(root, i)
    for i in list_of_parazites:
        if uniform(0,1) < REPRODUCTION_PROB :    #! RecovProb = 1 --> aucune chance de recover
            reproduce(root,i)

def random_mutation_on(para_i, what) :
    '''Cette fonction applique la mutation selon le cas donné en argument, 'infection', 'reproduction' ou 'living' et selon la façon de calculer les trades-off 'leo' ou 'dariush' '''  
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
        if TRADE_OFF == 'dariush':
            old_attributes = [para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb()]
            attribute_functions = {'0':para_i.set_New_Vir, '1':para_i.set_New_TransmRate, '2':para_i.set_New_RecovProb, '3': para_i.setStrain([])}
            
            rand_mod = (randint(0,1)*2-1)*(1+uniform(0, fit_change))    #modificateur valant au max 1+0.2 (p. ex)
            rand_index = randint(0,2)
            new_value = max(min(old_attributes[rand_index] * rand_mod, 1),0)   #new attribute = 1.2*old attribute (au max)
            attribute_functions[str(rand_index)](new_value)                     #on appelle la fonction correspondante
            new_attributes = [para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb()]
        elif TRADE_OFF == 'leo':
            trade_off(para_i)
            
        if what == 'living':
            temp_idd = para_i.getIdd() + 'mut'
            balls_dictionnary[temp_idd] = balls_dictionnary[para_i.getIdd()]
            del balls_dictionnary[para_i.getIdd()]
            para_i.setIdd(temp_idd)
            
        #nouvelle souche
        new_strain = para_i.getIdd()
        new_strain = 'Souche-' + new_strain[2:]
        para_i.setStrain(new_strain)
        strain_dictionary[new_strain] = [[para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb],[para_i.getIdd()]]
        
        New_strain_in_csv(new_strain,para_i.getVir(),para_i.getTransmRate(), para_i.getRecovProb()) #ajoute la souche au csv
        
        x = randint(0,2)
        random_color = list(balls_dictionnary[list_of_parazites[-1].getIdd()][0].get_col())
        random_color[x] = max(min(uniform(-1,1)+random_color[x], 1),0)
        balls_dictionnary[list_of_parazites[-1].getIdd()][0].set_col(tuple(random_color))
    
    else:
        if what == 'infection': #ça marche parce qu'on ne teste plus parasite reproducting
            strain_dictionary[para_i.getStrain()][1].append(para_i.getIdd())
        
def infect_him(para_i,heal_i, parazites_reproducing=False) :
    resistant = False 
    testing_par = para_i.getStrain()
    if testing_par in heal_i.getResistances() :
        resistant = True
    if heal_i.getIdd() in strain_dictionary[para_i.getStrain()][1] and resistant == False:
        print "ALERTE GENERALE--------------------------------------------"
    if not resistant :
        temp_par = list(para_i.getPar())
        temp_par.append(para_i.getIdd())
        temp_strain = para_i.getStrain()
        list_of_parazites.append(Parazite(para_i.getVir(), para_i.getTransmRate(), para_i.getRecovProb(), heal_i.getIdd(), temp_par, temp_strain))
        for i in heal_i.getResistances() :
            list_of_parazites[-1].addResistance(i)
        
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
        if uniform(0,1) < INFECTION_CHANCE *(1+p1.getTransmRate()) : 
            p2.setVir(p1.getVir())
            p2.setTransmRate(p1.getTransmRate())
            p2.setRecovProb(p1.getRecovProb())
            balls_dictionnary[p2.getIdd()][0].set_col(balls_dictionnary[p1.getIdd()][0].get_col())
            p2.setStrain(p1.getStrain())
            strain_dictionary[p1.getStrain()][1].append(p2.getIdd())
    elif p2.getVir() > p1.getVir() :
        parazite_against_parazite(p2,p1)
    
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

def New_strain_in_csv(tempStrain, tempVir, tempTrans, tempRecov):
    if MODE == "war" or MODE == 'all_night_long':
        with open("data/" + tempStrain +".csv","w") as NewStrainFile:
            dico_of_strains_for_csv[tempStrain] = csv.writer(NewStrainFile) #création du fichier .csv avec le nom de la souche
            dico_of_strains_for_csv[tempStrain].writerow(["Souche","temps[s]","nombre infection secondaires","population totale en vie","parasites de cette souche en vie","pourcentage de la population de parasites", #header du csv
            "virulence: "+ str(tempVir), "taux de transmision: "+ str(tempTrans), "probabilité de guérison contre le parasite: " + str(tempRecov)])
        
        
#-----------------------main --------------------------
    
class mainApp(App) :
    """Represents the whole application."""
    def build(self) :
        """Gestion temporelle des fonctions. Passe les argument "globaux" par défaut. """
        global Event
        root = BallsContainer()
        
        args = None                 #passage d'argument
        if len(sys.argv) > 1 :
            args = sys.argv[1]

        Clock.schedule_once(partial(root.update_files, filename = args),1.1)         #on attend que la fenêtre soit lancée
        Event = Clock.schedule_interval(partial(root.update_files, filename = args), 60*DELTA_TIME)

        Clock.schedule_once(root.start_balls,1)         #on attend que la fenêtre soit lancée
        Clock.schedule_once(root.update_life_and_death,1.1)         #on attend que la fenêtre soit lancée
        Clock.schedule_interval(root.update, DELTA_TIME)
        Clock.schedule_interval(root.update_life_and_death, 60*DELTA_TIME)    #ça ça marche
        Window.bind(on_key_down=root.Keyboard)                      #pour le clavier

        return root

#-----------------------Main--------------------------------------

# ----------------------Balls container--------------------------

class BallsContainer(Widget):
    """Classe du widget principal, qui contient les boules """
    pause = False
    faster_events = []
    num_healthies = NumericProperty(0)
    num_parazites = NumericProperty(0)
    nb_coll, mean_vir, mean_trans, mean_recov,last_clock, duration, paused = NumericProperty(0),NumericProperty(0),NumericProperty(0),NumericProperty(0),NumericProperty(0), NumericProperty(0), NumericProperty(0)
    top_idds = ListProperty([[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
    temp_widg_to_remove_list = []
#    starting_time = time.time()

    def start_balls(self,dt):
        ''' Est apellée une fois, au temps dt(défini dans build). Ajoute les boules. '''
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

            if len(sys.argv) > 2 :                     #ICI on check pour theory tester
                parazite = add_one_parazite(sys.argv[2]) #sys.argv[2] = effect = charge parasitaire
            else :
                parazite = add_one_parazite()
            balls_dictionnary[parazite.getIdd()] = [ball, parazite, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]

        if len(sys.argv) > 2 : #mode theory tester
            for _ in range(10) :
                reproduce(self, list_of_parazites[-1])

    #@profile
    def update(self,dt):
        '''Sert de manager pour les position et les vitesse des boules à l'aide des dictionnaires. Appelle les fonctions qui gèrent les collisions. Est appelé tousles dt, un interval de temps défini dans build. '''
        quad = Quadtree(0,[self.x,self.x + self.width, self.y, self.y + self.height])
        quad.reset()    #est-ce que ça sert à rien ?
        for i in balls_dictionnary.keys() :
            pos = balls_dictionnary[i][0]       #gotta update position (dic) here ! before the quad !
            balls_dictionnary[i][2] = [pos.x, pos.x + pos.width, pos.y, pos.y + pos.height]
            
            quad.insert(balls_dictionnary[i][2], i)     #we insert the balls in the quad

        for i in balls_dictionnary.keys() :

            temp_balls = quad.fetch(balls_dictionnary[i][2],i)  #fetch the collisions for each ball
            temp_keys = [k[1] for k in temp_balls]              #get the keys of those collisions
            other_balls = {key:balls_dictionnary[key] for key in temp_keys}     #create a new dic with the collisions

            for j in other_balls.keys():            #and for each of those collisions, action !
                
                if physical_collision2(balls_dictionnary[i][0], other_balls[j][0]):
                    actions_when_collision(balls_dictionnary[i][1], other_balls[j][1])
                    self.nb_coll += 1
            physical_wall_collisions2(balls_dictionnary[i][0], self)

            #-------------- update balls here -----------------
            balls_dictionnary[i][0].update(dt)              #update the positions of the balls (widget)
            #-------------- update balls here -----------------
            
    def update_life_and_death(self,dt):
        '''Appelé tous les dt(défini dans build, normalement toutes les secondes), met à jour toutes les morts, guérison, reproduction. En mode théory tester, la fonction shall_we_kill_the_simulation, en mode all_night_long, la fonction all_nighter.'''
        kill_those_who_have_to_die(self,dt)
        reproduce_those_who_have_to(self,dt)
        cure_the_lucky_ones(dt)
        mutate_those_who_wish(dt)
        self.shall_we_kill_the_simulation(dt)
        self.all_nighter()
        print strain_dictionary
    
    def update_files(self, dt, filename = None) :
        '''Sert à la gestion temporelle de l'écriture dans les fichiers. appelé tous les dt(défini dans build, normalement toutes les secondes)'''
        self.update_numbers(filename)
        self.update_data_files(dt)
        
       
    def all_nighter(self) :
        ''' Uniquement utilisé dans le mode all_night_long, qui permet de maintenir la population à un nombre gérable par l'ordinateur'''
        global REPRODUCTION_PROB, DYING_PROB
        if MODE=='all_night_long' and len(list_of_parazites) < 1:
            for i in range (0,NB_PARASITE):    
                ball = Ball()
                ball.center = (randint(self.x, self.x+self.width), randint(self.y, self.y+self.height))
                ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),         #à revoir
                             -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
                self.add_widget(ball)
                ball.set_col((uniform(0,1),uniform(0,1),0))
                parazite = add_one_parazite()
                balls_dictionnary[parazite.getIdd()] = [ball, parazite, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
        if len(list_of_healthies) + len(list_of_parazites) > 300 and MODE != 'war':
            DYING_PROB = ROOF_DYING_PROB
        elif len(list_of_healthies)<= 250 and MODE != 'war':
            DYING_PROB = STOCK_DYING_PROB
        else :
            pass
        if len(list_of_healthies) + len(list_of_parazites) < 50 and MODE != 'war':
            REPRODUCTION_PROB = BOTTOM_REPRODUCTION_PROB
        elif len(list_of_healthies) + len(list_of_parazites) > 50 and MODE != 'war':
            REPRODUCTION_PROB = STOCK_REPRODUCTION_PROB
    
       
    def update_numbers(self, filename = None) :
        ''' Met à jour les chiffre affichés'''
        self.num_parazites = len(list_of_parazites)
        self.num_healthies = len(list_of_healthies)

        sumvir, sumrecov, sumtrans = 0,0,0

        tempdic = {}
        self.top_idds = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

        for i in balls_dictionnary.keys() :
            if isinstance(balls_dictionnary[i][1], Parazite) :
                sumvir += float(balls_dictionnary[i][1].getVir())
                sumtrans += float(balls_dictionnary[i][1].getTransmRate())
                sumrecov +=  float(balls_dictionnary[i][1].getRecovProb())

                if balls_dictionnary[i][1].getStrain() in tempdic.keys() :
                    tempdic[balls_dictionnary[i][1].getStrain()][0] += 1
                else :
                    tempdic[balls_dictionnary[i][1].getStrain()] = [1, balls_dictionnary[i][1].getIdd()]

        tempdic2 = dict(tempdic)
        for i in range(0,3) :
            if len(tempdic2) == 0 :
                self.top_idds[i] = [0,0,0,0,0,[1,1,1]]
            else :
                key = self.idd_max(tempdic2)
                ind = balls_dictionnary[tempdic2[key][1]]
                self.top_idds[i]= ['ID'+key[7:], tempdic2[key][0], ind[1].getVir(), ind[1].getTransmRate(), ind[1].getRecovProb(), ind[0].get_col()] #add [souche,number,vir,trans,recov,color]
                del tempdic2[key]

        try :
            
            self.mean_trans = sumtrans/len(list_of_parazites)
            self.mean_recov = sumrecov/len(list_of_parazites)
            self.mean_vir = sumvir/len(list_of_parazites) 
            
        except:
            self.mean_vir, self.mean_trans, self.mean_recov = 0,0,0
        
        #_---------------gestion du temps sans les pauses--------
        if self.pause == False:
            self.duration = time.clock()- self.paused 
        
        #------------------------------- Enregistrement des données--------------------
        if filename is not None or len(sys.argv) > 1:
            if len(sys.argv) > 2 :
                arg = "data_effect_tester/"+str(sys.argv[2]) + '.csv'       #si on mass-effect
                print "saved in data_effect_tester/"
            elif len(sys.argv) > 1 :
                arg = "data_per_param/"+str(sys.argv[1]) + '.csv'           #si on other param
            else :
                arg = "data_per_param/"+str(filename)+'.csv'

            if not isfile(str(arg)) :
                with open(str(arg), 'w') as par:
                    csv_file = csv.writer(par, delimiter=',')
                    if len(sys.argv) > 2 :                  #si on mass-effect
                            csv_file.writerow(['time', 'secondary_infections'])
                    elif len(sys.argv) > 1:
                        csv_file.writerow(['time', 'healthies', 'parazites', 'mean_vir', 'mean_trans', 'mean_recov'])
            else :
                with open(str(arg), 'a') as par :
                    csv_file =csv.writer(par, delimiter=',')
                    if len(sys.argv) > 2 and len(strain_dictionary) > 0:                  #si on mass-effect
                        csv_file.writerow([self.duration,len(strain_dictionary['Souche-101'][1])])
                    elif len(sys.argv) > 1 :                #si on other param
                        csv_file.writerow([self.duration,len(list_of_healthies), len(list_of_parazites),self.mean_vir,self.mean_trans,self.mean_recov])
        #=========GUI BULLSHIT==================================
        temp_wig = []
        for c in self.children:
            if not isinstance(c, Ball) :
                temp_wig.append(c)              #pour éviter de trop grosses boucles
        if isinstance(temp_wig[0], Label) :         #magouille parce que les widgets font n'importe quoi
            temp_wig = list(reversed(temp_wig))
        for c in temp_wig :                     #tout ça rien que pour avoir un ordre de widget agréable, pff
            if isinstance(c,Button) :
                self.remove_widget(c)
                self.add_widget(c)
        for c in temp_wig :
            if isinstance(c,Label) :
                self.remove_widget(c)
                self.add_widget(c)

        for c in self.temp_widg_to_remove_list :
            self.remove_widget(c)
        for i in range(0,3) :
            ball = Ball()
            ball.size = 10,10
            ball.center = (self.width-112,self.height-80*i-17)
            ball.velocity = (0,0)
            if len(self.top_idds) > i:
                ball.set_col(self.top_idds[i][5])
            else :
                ball.set_col((0,0,0))
            self.add_widget(ball)
            self.temp_widg_to_remove_list.append(ball)

    def shall_we_kill_the_simulation(self, dt) :
        '''En mode theory_tester, arrète la simulation quand il n'y a plus de parasite ou si le temps défini c'est écoulé'''
        
        if MODE == 'theory_tester':
            print self.duration
            if len(list_of_parazites) == 0 or self.duration > SIMULATION_TIME :
                self.on_stop()


        #=========GUI BULLSHIT==================================
    def update_data_files(self,dt):
        if MODE == 'war' or MODE == 'all_night_long':
            simulation_time = self.duration
            nb_of_healthies = len(list_of_healthies) #liste des individus sains vivants
            total_nb_of_parazites_alive = len(list_of_parazites) #liste des parasites vivants
            total_population = nb_of_healthies +  total_nb_of_parazites_alive
            if nb_of_healthies > 0 :
                percentage_of_parazites_in_pop = round((float(total_nb_of_parazites_alive)/total_population)*100,2) #pourcentage de parasite dans la population totale
            else :
                percentage_of_parazites_in_pop = 0 # pour éviter division par zéro
                
            #inscription dans le fichier src/nb_sains_infectes.csv
            with open("nb_total_sains_infectes.csv","a") as csv_nb_total_sains_infectes: #creer le fichier des données générales de la population 
                writer = csv.writer(csv_nb_total_sains_infectes)
                writer.writerow([simulation_time,total_population,nb_of_healthies,total_nb_of_parazites_alive,percentage_of_parazites_in_pop,self.mean_vir,self.mean_recov,self.mean_trans])
            
            #parcours les souches et met à jour le fichier "souche.csv" qui leur correspond
            for strain_id in strain_dictionary:
                total_nb_of_infections = len(strain_dictionary[strain_id][1]) #nombre total d'infection secondaires
                nb_of_parazites_alive = 0 # nombre de parasites de cette souche en vie à l'instant t
                for id_infected_by_this_strain in strain_dictionary[strain_id][1]:  # on parcours la liste des id qui ont été infectés par cette souche
                    if id_infected_by_this_strain in balls_dictionnary: #on prend la liste des id qui ont été inféctés par cette souche et on compare avec la liste des invidividus encore en vie
                        nb_of_parazites_alive += 1    
                if total_nb_of_parazites_alive != 0:
                    percentage_of_all_infections = round((float(nb_of_parazites_alive)/total_nb_of_parazites_alive) * 100, 2) #quelle importance a cette souche comparée au total des autres   
                else :
                    percentage_of_all_infections = 0.0
                if nb_of_parazites_alive > 0 :    #on contnu de mettre à jour le fichier csv seuelment si la souche est encore active ( au moins 1 parasite encore en vie)
                        with open("data/" + strain_id + ".csv","a") as UpdateStrainFile:
                            dico_of_strains_for_csv[strain_id] = csv.writer(UpdateStrainFile)
                            dico_of_strains_for_csv[strain_id].writerow([simulation_time,strain_id,total_nb_of_infections,
                                                                total_population,nb_of_parazites_alive, percentage_of_all_infections])
        
    def on_pause(self):
        '''Arrète de mettre à jour update, update_life_and_death et update_files '''
        global Event
        Clock.unschedule(self.update)
        Clock.unschedule(self.update_life_and_death)
        args = None                 #passage d'argument
        if len(sys.argv) > 1 :
            args = sys.argv[1]
        Clock.unschedule(Event)
        

    def on_resume(self):
        '''recommence de mettre à jour update, update_life_and_death, update_files'''
        global Event
        Clock.schedule_interval(self.update, DELTA_TIME)
        Clock.schedule_interval(self.update_life_and_death, 60*DELTA_TIME)
        args = None                 #passage d'argument
        if len(sys.argv) > 1 :
            args = sys.argv[1]
        Event = Clock.schedule_interval(partial(self.update_files, filename = args), 60*DELTA_TIME)

        
        
    def on_stop(self):
        '''Ferme l'application'''
        App.get_running_app().stop()
        return True

    def on_touch_down(self, touch):
        """Géré par kivy, quand on clique sur la fenêtre, affiche un graphique du nombre d'infections decondaire en fonction de la virulance"""
        if not self.pause :
            return
        
        listx = []
        listy = []
        for i in strain_dictionary.keys():
            listx.append(strain_dictionary[i][0][0])
            listy.append(len(strain_dictionary[i][1]))
        plt.scatter(listx, listy)
        plt.ylabel('Secondary infections')
        plt.plot((self.mean_vir, self.mean_vir), (0,len(list_of_parazites) + len(list_of_healthies)), 'k-',color = 'r')
        plt.title('Nb of sec. infections following virulance at time = ' + str(self.duration) + 'sec')
        plt.show()
        return 

    def Keyboard(self, window, keycode, *args) :
        """Géré par Kivy, permet d'utiliser les inputs du clavier"""
        if keycode == 32 and not self.pause:              #SPACE - pour ça je rajoute un print keycode avant et check le int
            self.duration = time.clock() - self.paused
            self.paused -= time.clock()
            self.on_pause()
            self.pause = True
            
        elif keycode == 32 and self.pause :
            self.on_resume()
            self.pause = False
            self.paused += time.clock()

        elif keycode == 275 :           #right
            self.faster_events.append([Clock.schedule_interval(self.update, DELTA_TIME), Clock.schedule_interval(self.update_life_and_death, 60*DELTA_TIME)])

        elif keycode == 276 :           #left
            if len(self.faster_events)>0 :
                self.faster_events[-1][0].cancel()
                self.faster_events[-1][1].cancel()
                self.faster_events.pop()
        
        elif keycode == 115:# s pour stop
            self.on_stop()


    def idd_max(self,dico):
        '''Appelé dans update numbers, pour gérer les trois top IDs'''
        a = [i[0] for i in dico.values()]
        b=list(dico.keys())
        return b[a.index(max(a))]
        
#            
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
#    def theory_tester(self,dt):
#        if TEST_THEORY == 1:
#            global CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION, PARAZITE_FIGHT_CHANCE 
#            CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION, PARAZITE_FIGHT_CHANCE,GENERATION_RESISTANCE = 0,0,0,0,0
#            if len(list_of_parazites) == 0 or self.duration - self.last_clock >= 15 :       #time - change here
#                try:
#                    eff = (list_of_parazites[-1].getVir()*100)**0.5
#                except:
#                    eff = 0.2
#                print "effect = ", str(eff)
#                print "to get this results"
#
#                self.place_neuve(dt)
#
#                print "nb heal :", len(list_of_healthies)
#                print "nb par : ", len(list_of_parazites)
#
#                self.start_balls(dt)
#                for i in range(0,NB_PARASITE):
#                    ball = Ball()
#                    ball.center = (randint(self.x, self.x+self.width), randint(self.y, self.y+self.height))
#                    ball.velocity = (-MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED),         #à revoir
#                                     -MAX_BALL_SPEED + random() * (2 * MAX_BALL_SPEED))
#                    self.add_widget(ball)
#                    ball.set_col((uniform(0,1),uniform(0,1),0))
#
#                    parazite = add_one_parazite(effect = eff)
#                    balls_dictionnary[parazite.getIdd()] = [ball, parazite, [ball.x, ball.x + ball.width, ball.y, ball.y + ball.height]]
#                self.last_clock = self.duration
#                print "nb heal :", str(len(list_of_healthies))
#                print "nb par : ", str(len(list_of_parazites))
#                if (list_of_parazites[-1].getVir()*100)**0.5 >=9.81:
#                    self.pause()

#if isfile('data.csv') and 'y' != raw_input("le fichier data existe déjà, le remplaçer? (y/n)"): exit() #écrit les headers dans le dossier 
#
#csv_nb_total_sains_infectes = csv.writer(open("nb_total_sains_infectes.csv","wb")) #creer le fichier des données générales de la population 
#csv_nb_total_sains_infectes.writerow(["temps","population totale","individus sains","individus infectés","pourcentage de la population infectée",
#                                      "virulence moyenne","taux de transmission guérison","taux de transmission"]) #header des données générales de la pop
#    def update_data_files(self,dt):
#        current_time = time.clock()
#        simulation_time = round(current_time - initial_time,4) 
#        nb_of_healthies = len(list_of_healthies) #liste des individus sains vivants
#        total_nb_of_parazites_alive = len(list_of_parazites) #liste des parasites vivants
#        total_population = nb_of_healthies +  total_nb_of_parazites_alive
#        if nb_of_healthies > 0 :
#            percentage_of_parazites_in_pop = round((float(total_nb_of_parazites_alive)/total_population)*100,2) #pourcentage de parasite dans la population totale
#        else :
#            percentage_of_parazites_in_pop = 0 # pour éviter division par zéro
#            
#        #inscription dans le fichier src/nb_sains_infectes.csv
#        csv_nb_total_sains_infectes.writerow([simulation_time,total_population,nb_of_healthies,
#                                              total_nb_of_parazites_alive,percentage_of_parazites_in_pop,self.mean_vir,self.mean_recov,self.mean_trans])
#        
#        #parcours les souches et met à jour le fichier "souche.csv" qui leur correspond
#        for strain_id in strain_dictionary:
#            total_nb_of_infections = len(strain_dictionary[strain_id][1]) #nombre total d'infection secondaires
#            nb_of_parazites_alive = 0 # nombre de parasites de cette souche en vie à l'instant t
#            for id_infected_by_this_strain in strain_dictionary[strain_id][1]:  # on parcours la liste des id qui ont été infectés par cette souche
#                if id_infected_by_this_strain in balls_dictionnary: #on prend la liste des id qui ont été inféctés par cette souche et on compare avec la liste des invidividus encore en vie
#                    nb_of_parazites_alive += 1    
#            
#            percentage_of_all_infections = round((float(nb_of_parazites_alive)/total_nb_of_parazites_alive) * 100, 2) #quelle importance a cette souche comparée au total des autres   
#       
#            if nb_of_parazites_alive > 0 :    #on contnu de mettre à jour le fichier csv seuelment si la souche est encore active ( au moins 1 parasite encore en vie)
#                    with open("data/" + strain_id + ".csv","a") as UpdateStrainFile:
#                        dico_of_strains_for_csv[strain_id] = csv.writer(UpdateStrainFile)
#                        dico_of_strains_for_csv[strain_id].writerow([simulation_time,strain_id,total_nb_of_infections,
#                                                            total_population,nb_of_parazites_alive, percentage_of_all_infections])
'''
