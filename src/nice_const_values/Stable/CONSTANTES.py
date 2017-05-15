# -*- coding: utf-8 -*-                                                                                                
from random import *
seed(42)
#mode: 'theory_tester', 'war', 'all_night_long'
MODE = 'all_night_long'

#mode theory tester :
SIMULATION_TIME = 120
TEST_THEORY = 0

#all_night_long
#ALL_NIGHT_LONG = 0
#HEALTHY_ROOF = 1
STOCK_DYING_PROB = 0.13
ROOF_DYING_PROB = 0.2
STOCK_REPRODUCTION_PROB = 0.15
BOTTOM_REPRODUCTION_PROB = 0.15

#GUI
DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100
BASE_COLOR = [0,0,1]

#MAIN
TRADE_OFF = 'dariush'
NB_SAINS = 120
NB_PARASITE = 10
MAX_VELOCITY= 1
MAX_VIRULANCE= 1
MIN_SIZE_FOR_DATA = 40 * 1000  #pour avoir mesure en kb, à utiliser dans all_night_long et war

#INDIVIDUAL
DYING_PROB = 0.12    #max 0.5
REPRODUCTION_PROB = 0.14

#HEALTHY
TRANSMISSION_RESISTANCE = 1

#PARAZITE
BASE_FITNESS = 0.8
MAX_FITNESS = 1.8
MAX_FITNESS_CHANGE_ON_INFECTION = 0.2   #max 0.5
MAX_FITNESS_CHANGE_ON_NOTHING = 0.05   #max 0.5
MAX_FITNESS_CHANGE_ON_REPRODUCTION = 0.2 #max 0.5

#equations
compteur_id = 1
last_clock = 0
nb_coll = 0
mean_vir = 0
mean_trans = 0
mean_recov = 0
