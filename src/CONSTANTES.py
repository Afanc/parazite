#GUI
DELTA_TIME = 1.0 / 60.0
MAX_BALL_SPEED = 100
BASE_COLOR = [0,0,1]

#MAIN
NB_SAINS = 5                                                                                                           
NB_PARASITE = 3
INFECTION_CHANCE = 0.3  #max 0.5 ! else : troubles
CONTAINER_HEIGHT= 200
CONTAINER_WIDTH= 300
MAX_VELOCITY= 1
MAX_VIRULANCE= 1

#INDIVIDUAL
DYING_PROB = 0.12    #max 0.5
REPRODUCTION_PROB = 0.1

#PARAZITE
BASE_FITNESS = 0.5
NUM_PAR = 100
MAX_FITNESS = 1
CHANCE_OF_MUTATION_ON_INFECTION = 0.1
MAX_FITNESS_CHANGE_ON_INFECTION = 0.2   #max 0.5
CHANCE_OF_MUTATION_ON_REPRODUCTION = 0.1
MAX_FITNESS_CHANGE_ON_REPRODUCTION = 0.2 #max 0.5
