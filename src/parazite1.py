# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from __future__ import division         #seriously - python 2 has no true division ?!
from individual import *    
from numpy import *

class Parazite(Individual): 
       
    #Constructeur
    def __init__(self,pos,speed, vir, rate, rec, idd):
        Individual.__init__(self,pos,speed, idd) 
        self.virulance = vir        #high is bad    -> we sum 1-x
        self.transm_rate = rate     #high is good   -> we sum x
        self.recovery_prob = rec    #high is bad    -> we sum 1-x

    def __str__(self) :
        return 'ID : ' +str(self.idd) + '\nposition : '+str(self.position)+'\ncouleur : '+str(self.color)\
            +'\nvirulance : '+str(1-self.virulance) + '\ntransmission rate : '+str(self.transm_rate)\
            +'\nrecovery prob : '+str(1-self.recovery_prob)+'\nTotal Fitness :'+str(self.getTotalFitness())

    def getVir(self):
        return self.virulance

    def getTransmRate(self):
        return self.transm_rate

    def getRecovProb(self):
        return self.recovery_prob
    
    def setVir(self, v) :
        self.virulance = v

    def setTransmRate(self,r) : 
        self.transm_rate = r

    def setRecovProb(self,r) :
        self.recovery_prob = r

    #if vir goes up, transm rate goes up, recov goes down
    def set_New_Vir(self,r) : 
        new_fitness = self.getTransmRate() + self.getRecovProb() + r

        diff = r - self.getVir()
        s = sign(diff)

        x = 0
        y = 0

        while(new_fitness > MAX_FITNESS) :
	    
	    max_x = (1 - s)/2 + s*self.getTransmRate()
	    max_y = (1 - s)/2 + s*self.getRecovProb()

            x = uniform(0, max_x) 	#on définit des pertes/gains aléatoires
            y = uniform(0, max_y) 

	    if r + self.getTransmRate()-s*x + self.getRecovProb()-s*y > MAX_FITNESS : 
		norm = r/(x + y) 	#on essaie de normaliser
		x = min(norm*x, max_x) 	#au cas où on dépasse la valeur max avec la normalisation
		y = min(norm*y, max_y)

	    new_fitness = r + self.getTransmRate()-x*s + self.getRecovProb()-y*s

	self.setVir(r)
        self.setTransmRate(self.getTransmRate() - s*x)
        self.setRecovProb(self.getRecovProb() - s*y)

    #if transm rate goes up, vir goes up, recov goes down
    def set_New_TransmRate(self, r) :
        new_fitness = self.getVir() + self.getRecovProb() + r

        diff = r - self.getTransmRate()
        s = sign(diff)

        x = 0
        y = 0

        while(new_fitness > MAX_FITNESS) :
	    
	    max_x = (1 - s)/2 + s*self.getVir()
	    max_y = (1 - s)/2 + s*self.getRecovProb()

            x = uniform(0, max_x) 	#on définit des pertes/gains aléatoires
            y = uniform(0, max_y) 

	    if r + self.getVir()-s*x + self.getRecovProb()-s*y > MAX_FITNESS : 
		norm = r/(x + y) 	#on essaie de normaliser
		x = min(norm*x, max_x) 	#au cas où on dépasse la valeur max avec la normalisation
		y = min(norm*y, max_y)

	    new_fitness = r + self.getVir()-x*s + self.getRecovProb()-y*s

	self.setTransmRate(r)
        self.setVir(self.getVir() - s*x)
        self.setRecovProb(self.getRecovProb() - s*y)


    #if recov rate goes up, vir goes down, transm rate goes down
    def set_New_RecovProb(self, r) :
        new_fitness = self.getVir() + self.getTransmRate() + r

        diff = r - self.getRecovProb()
        s = sign(diff)
        
        x = 0
        y = 0

        while(new_fitness > MAX_FITNESS) :
	    
	    max_x = (1 - s)/2 + s*self.getVir()
	    max_y = (1 - s)/2 + s*self.getTransmRate()

            x = uniform(0, max_x) 	#on définit des pertes/gains aléatoires
            y = uniform(0, max_y) 

	    if r + self.getVir()-s*x + self.getTransmRate()-s*y > MAX_FITNESS : #si on ne compense pas le gain de fitness
		norm = r/(x + y) 	#on essaie de normaliser
		x = min(norm*x, max_x) 	#au cas où on dépasse la valeur max avec la normalisation
		y = min(norm*y, max_y)

	    new_fitness = r + self.getVir()-x*s + self.getTransmRate()-y*s

	self.setRecovProb(r)
        self.setVir(self.getVir() - s*x)
        self.setTransmRate(self.getTransmRate() - s*y)

    def getTotalFitness(self) :
        return self.getVir() + self.getRecovProb() + self.getTransmRate()


test = Parazite(1,1, 0.7, 0.1, 0, 'ID23')
print 'before'
print test
print test.getTotalFitness()
test.set_New_RecovProb(0.9)
print test
print test.getTotalFitness()
test.set_New_RecovProb(0.2)
test.set_New_RecovProb(0.3)
test.set_New_RecovProb(0.4)
test.set_New_RecovProb(0.5)
print test
print test.getTotalFitness()

test.set_New_TransmRate(0.2)
test.set_New_TransmRate(0.3)
test.set_New_TransmRate(0.4)
test.set_New_TransmRate(0.5)
test.set_New_TransmRate(0.6)
test.set_New_Vir(0.5)
test.set_New_Vir(0.4)
test.set_New_Vir(0.3)
test.set_New_Vir(0.2)
test.set_New_Vir(0.1)
print test
print test.getTotalFitness()


    #idées
    #survie après mort/prob_transm/def_anti_para/taille/prob_manip/
