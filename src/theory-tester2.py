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
EFFECT = 0

#A CHANGER ICI
MAX_LEVEL = 10
STEP = 0.2

def launch() :
    filename = "effect_", str(EFFECT)
    
            
    os.system("python main.py "+ str(filename) + str(EFFECT)     #pas d'autre moyen parce que difficile de flush les objets en mémoire

    time.sleep(2)                                   #juste pour se donner du temps


#---- the tester
EFFECT = 0 # somme des argument 
while EFFECT < MAX_LEVEL :
    EFFECT += STEP
    launch()

        
