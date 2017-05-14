# -*- coding: utf-8 -*-
#!/usr/bin/python

from main import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import  Builder
import kivy.factory_registers 
import time
import sys
import os

global INFECTION_CHANCE, CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION, PARAZITE_FIGHT_CHANCE, TRANSMISSION_OF_RESISTANCE_PROB, BASE_CHANCE_OF_HEALING

INFECTION_CHANCE, CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION, PARAZITE_FIGHT_CHANCE,TRANSMISSION_OF_RESISTANCE_PROB, BASE_CHANCE_OF_HEALING = 0.4,0,0,0,0.5,1,0.1

list_of_names = ['INFECTION_CHANCE', 'CHANCE_OF_MUTATION_ON_INFECTION', 'CHANCE_OF_MUTATION_ON_NOTHING','CHANCE_OF_MUTATION_ON_REPRODUCTION', 'PARAZITE_FIGHT_CHANCE','TRANSMISSION_OF_RESISTANCE_PROB', 'BASE_CHANCE_OF_HEALING']
list_of_param = [INFECTION_CHANCE, CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION, PARAZITE_FIGHT_CHANCE,TRANSMISSION_OF_RESISTANCE_PROB, BASE_CHANCE_OF_HEALING]


#A CHANGER ICI
global  EFFECT

#A CHANGER ICI
MAX_LEVEL = 10
STEP = 0.2

def launch(eff) :
    filename = "effect_"  + str(eff)
    
    eff = str(eff)
    print "------------------------------------------------"
    print float(eff)
    os.system("python main.py "+ str(filename) + " " + str(eff))     #pas d'autre moyen parce que difficile de flush les objets en mémoire
    print "avant le sleep"
    time.sleep(2)                                   #juste pour se donner du temps
    print "après le sleep"

#---- the tester
EFFECT = 0 # somme des argument 
while EFFECT < MAX_LEVEL :
    print " un tour"
    EFFECT += STEP
    launch(EFFECT)

        
