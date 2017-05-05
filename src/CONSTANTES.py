# resistance = 

#GUI
DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100
BASE_COLOR = [0,0,1]
SPEC_BASE_COLOR = [0,0.5,.5]

#MAIN
NB_SAINS = 200
NB_PARASITE = 20
MAX_VELOCITY= 1
MAX_VIRULANCE= 1

#INDIVIDUAL
DYING_PROB = 0.13    #max 0.5
REPRODUCTION_PROB = 0.12

#HEALTHY
TRANSMISSION_OF_RESISTANCE_PROB = 1

#PARAZITE
BASE_FITNESS = 0.8
MAX_FITNESS = 1.8
INFECTION_CHANCE = 0.1  #max 0.5 ! else : troubles
BASE_CHANCE_OF_HEALING = 0.05
CHANCE_OF_MUTATION_ON_INFECTION = 0.1
MAX_FITNESS_CHANGE_ON_INFECTION = 0.2   #max 0.5
CHANCE_OF_MUTATION_ON_NOTHING = 0.01
MAX_FITNESS_CHANGE_ON_NOTHING = 0.1   #max 0.5
CHANCE_OF_MUTATION_ON_REPRODUCTION = 0.2
MAX_FITNESS_CHANGE_ON_REPRODUCTION = 0.2 #max 0.5
PARAZITE_FIGHT_CHANCE = 1
