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

INFECTION_CHANCE, CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION, PARAZITE_FIGHT_CHANCE,TRANSMISSION_OF_RESISTANCE_PROB, BASE_CHANCE_OF_HEALING = 0.4,0.0,0.0,0.0,0.5,1,0.1

list_of_names = ['INFECTION_CHANCE', 'CHANCE_OF_MUTATION_ON_INFECTION', 'CHANCE_OF_MUTATION_ON_NOTHING','CHANCE_OF_MUTATION_ON_REPRODUCTION', 'PARAZITE_FIGHT_CHANCE','TRANSMISSION_OF_RESISTANCE_PROB', 'BASE_CHANCE_OF_HEALING']

list_of_param = [INFECTION_CHANCE, CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION, PARAZITE_FIGHT_CHANCE,TRANSMISSION_OF_RESISTANCE_PROB, BASE_CHANCE_OF_HEALING]

#A CHANGER ICI
sub_list_of_param = [CHANCE_OF_MUTATION_ON_INFECTION, CHANCE_OF_MUTATION_ON_NOTHING,CHANCE_OF_MUTATION_ON_REPRODUCTION]

#A CHANGER ICI
MAX_LEVEL = 0.3
STEP = 0.1

def launch() :
    filename = 'inf'+str(list_of_param[0])+'_infmut'+str(list_of_param[1])+'_notmut'+str(list_of_param[2])+'_repmut'+str(list_of_param[3])+'_fight'+str(list_of_param[4])+'_restransm'+str(list_of_param[5])+'_heal'+str(list_of_param[6])
    
    #A CHANGER ICI
    list_of_param[1] = sub_list_of_param[0]
    list_of_param[2] = sub_list_of_param[1]
    list_of_param[3] = sub_list_of_param[2]

    with open('CHANGING_CONST.py', 'w') as f:
        f.write('#!/usr/bin/python\n\n')
        for inx, it in enumerate(list_of_param) :
            f.write(str(list_of_names[inx])+' = '+str(list_of_param[inx])+'\n')
    os.system("python main.py "+str(filename))      #pas d'autre moyen parce que difficile de flush les objets en mémoire

    time.sleep(2)                                   #juste pour se donner du temps

def increment_difficulty(l, j=1) :
    if j > len(l) :
        return

    sub_list_of_param = l
    launch()

    if l[-j] >= MAX_LEVEL :
        l[-j] = 0.0
        j += 1
        increment_difficulty(l, j)
    else :
        l[-j] = round(l[-j]+STEP, 1)

#---- the tester
sum_l = 0
while sum_l < MAX_LEVEL*len(sub_list_of_param) :
    sum_l = 0
    increment_difficulty(sub_list_of_param)
    for a in sub_list_of_param :
        sum_l += a

