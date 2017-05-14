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


#A CHANGER ICI
global  EFFECT

#A CHANGER ICI
MAX_LEVEL = 5.0
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
EFFECT = 1.8 # somme des argument 
while EFFECT < MAX_LEVEL :
    print " un tour"
    EFFECT += STEP
    launch(EFFECT)

        
