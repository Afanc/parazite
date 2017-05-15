# -*- coding: utf-8 -*-                                                                                                
from random import *
seed(42)
#mode: 'theory_tester', 'war', 'all_night_long'
MODE = 'all_night_long'


#mode theory tester :
#pensez à ne mettre qu'un seul parasite au départ(NB_PARASITE= 1)
#choisisez la durée de chaque simulation
SIMULATION_TIME = 120

#mode all_night_long
#choisisez la natalité quand la population tombe en dessous de 50 et la mortalité quand elle est plus grande que 250
#les varaibles stock doivent être les mêmes que DYING PROB et REPRODUCTION_PROB
STOCK_DYING_PROB = 0.13
ROOF_DYING_PROB = 0.2
STOCK_REPRODUCTION_PROB = 0.13
BOTTOM_REPRODUCTION_PROB = 0.15

#GUI
DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100
BASE_COLOR = [0,0,1]

#MAIN
#Choisisez le type de trade_off. 

TRADE_OFF = 'leo'
NB_SAINS = 100
NB_PARASITE = 5
MAX_VELOCITY= 1
MAX_VIRULANCE= 1
MIN_SIZE_FOR_DATA = 40 * 1000  #pour avoir mesure en kb, à utiliser dans all_night_long et war

#INDIVIDUAL
DYING_PROB = 0.13    #max 0.5
REPRODUCTION_PROB = 0.13

#HEALTHY
TRANSMISSION_RESISTANCE = 0

#PARAZITE
BASE_FITNESS = 0.8
MAX_FITNESS = 1.8
MAX_FITNESS_CHANGE_ON_INFECTION = 0.2   #max 0.5
MAX_FITNESS_CHANGE_ON_NOTHING = 0.1   #max 0.5
MAX_FITNESS_CHANGE_ON_REPRODUCTION = 0.2 #max 0.5

#equations
compteur_id = 1
last_clock = 0
nb_coll = 0
mean_vir = 0
mean_trans = 0
mean_recov = 0
