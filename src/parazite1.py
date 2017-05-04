# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from __future__ import division         #seriously - python 2 has no true division ?!
from individual import *    
from numpy import *

class Parazite(Individual): 
       
    #Constructeur
    def __init__(self, vir, rate, rec, idd, par=[]):
        Individual.__init__(self, idd) 
        self.virulance = vir        #high is bad    -> we sum 1-x
        self.transm_rate = rate     #high is good   -> we sum x
        self.recovery_prob = rec    #high is bad    -> we sum 1-x
        self.parenty = par
        
    def __str__(self) :
        return 'ID : ' +str(self.idd) +'\ncouleur : '+str(self.color)\
            +'\nvirulance : '+str(1-self.virulance) + '\ntransmission rate : '+str(self.transm_rate)\
            +'\nrecovery prob : '+str(1-self.recovery_prob)+'\nTotal Fitness : '+str(self.getTotalFitness())\
            +'\nparenty : ' + str(self.parenty)

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

    def getPar(self):
        return self.parenty
        
        
    #if vir goes up, transm rate goes up, recov goes down
    def set_New_Vir(self,r) : 
        new_fitness = self.getTransmRate() + self.getRecovProb() + r

        diff = r - self.getVir()
        s = sign(diff)

        x = 0
        y = 0

        for i in range(0,5) :
            if(new_fitness > MAX_FITNESS):
       
                max_x = (1 - s)/2 + s*self.getTransmRate()
                max_y = (1 - s)/2 + s*self.getRecovProb()

                x = uniform(0, max_x) 	#on définit des pertes/gains aléatoires
                y = uniform(0, max_y) 

                new_fitness = r + self.getTransmRate()-x + self.getRecovProb()-y
            else :
                break

        if new_fitness > MAX_FITNESS:
            return
	self.setVir(r)

        self.setTransmRate(self.getTransmRate() - x)
        self.setRecovProb(self.getRecovProb() - y)
    #if transm rate goes up, vir goes up, recov goes down
    def set_New_TransmRate(self, r) :
        new_fitness = self.getVir() + self.getRecovProb() + r

        diff = r - self.getTransmRate()
        s = sign(diff)

        x = 0
        y = 0

        for i in range(0,5) :
            if(new_fitness > MAX_FITNESS):
                max_x = (1 - s)/2 + s*self.getVir()
                max_y = (1 - s)/2 + s*self.getRecovProb()

                x = uniform(0, max_x) 	#on définit des pertes/gains aléatoires
                y = uniform(0, max_y) 

                new_fitness = r + self.getVir()-x + self.getRecovProb()-y
            else :
                break

        if new_fitness > MAX_FITNESS: 
            return
	self.setTransmRate(r)

        self.setVir(self.getVir() - x)
        self.setRecovProb(self.getRecovProb() - y)

    #if recov rate goes up, vir goes down, transm rate goes down
    def set_New_RecovProb(self, r) :
        new_fitness = self.getVir() + self.getTransmRate() + r

        diff = r - self.getRecovProb()
        s = sign(diff)
        
        x = 0
        y = 0

        #while(new_fitness > MAX_FITNESS) :
        for i in range(0,5) :
            if(new_fitness > MAX_FITNESS):
                max_x = (1 - s)/2 + s*self.getVir()
                max_y = (1 - s)/2 + s*self.getTransmRate()

                x = uniform(0, max_x) 	#on définit des pertes/gains aléatoires
                y = uniform(0, max_y) 

                new_fitness = r + self.getVir()-x + self.getTransmRate()-y
            else :
                break

        if new_fitness > MAX_FITNESS :
            return 
	self.setRecovProb(r)

        self.setVir(self.getVir() - x)
        self.setTransmRate(self.getTransmRate() - y)

    def getTotalFitness(self) :
        return self.getVir() + self.getRecovProb() + self.getTransmRate()

test = Parazite(0.7, 0.1, 0, 'ID23')
print 'before'
print test
print test.getTotalFitness()
for i in range(0,500) :
    test.setVir(uniform(0,1))
    test.setTransmRate(uniform(0,1))
    test.setRecovProb(uniform(0,1))
print test


    #idées
    #survie après mort/prob_transm/def_anti_para/taille/prob_manip/
