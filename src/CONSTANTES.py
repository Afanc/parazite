# resistance = 

#GUI
DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100
BASE_COLOR = [0,0,1]
SPEC_BASE_COLOR = [0,0.5,.5]
POS_X = 0
POS_Y = 0

#MAIN
NB_SAINS = 100
NB_PARASITE = 3
MAX_VELOCITY= 1
MAX_VIRULANCE= 1
ALL_NIGHT_LONG = 1
HEALTHY_ROOF = 1

#INDIVIDUAL
DYING_PROB = 0.13    #max 0.5
STOCK_DYING_PROB = 0.13
ROOF_DYING_PROB = 0.15
REPRODUCTION_PROB = 0.13
STOCK_REPRODUCTION_PROB = 0.13
BOTTOM_REPRODUCTION_PROB = 0.15
TRADE_OFF = 'leo'
#HEALTHY
TRANSMISSION_OF_RESISTANCE_PROB = 1
GENERATION_RESISTANCE = 1

#PARAZITE
BASE_FITNESS = 0.8
MAX_FITNESS = 1.8
INFECTION_CHANCE = 0.1  #max 0.5 ! else : troubles
BASE_CHANCE_OF_HEALING = 0.07
CHANCE_OF_MUTATION_ON_INFECTION = 0.1
MAX_FITNESS_CHANGE_ON_INFECTION = 0.2   #max 0.5
CHANCE_OF_MUTATION_ON_NOTHING = 0.1
MAX_FITNESS_CHANGE_ON_NOTHING = 0.1   #max 0.5
CHANCE_OF_MUTATION_ON_REPRODUCTION = 0.2
MAX_FITNESS_CHANGE_ON_REPRODUCTION = 0.2 #max 0.5
PARAZITE_FIGHT_CHANCE = 0.2

#equations
compteur_id = 1
last_clock = 0
nb_coll = 0
mean_vir = 0
mean_trans = 0
mean_recov = 0
