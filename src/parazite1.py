# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from __future__ import division         #seriously - python 2 has no true division ?!
from individual import *    

class Parazite(Individual): 
        
    #Constructeur
    def __init__(self,pos,speed, vir, rate, rec, idd):
        Individual.__init__(self,pos,speed, idd) 
        self.virulance = vir        #high is bad    -> we sum 1-x
        self.transm_rate = rate     #high is good   -> we sum x
        self.recovery_prob = rec    #high is bad    -> we sum 1-x

    def __str__(self) :
        return 'ID : ' +str(self.idd) + '\nposition : '+str(self.position)+'\ncouleur : '+str(self.color)\
            +'\nvirulance : '+str(self.virulance) + '\ntransmission rate : '+str(self.transm_rate)\
            +'\nrecovery prob : '+str(self.recovery_prob)

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
    def set_New_Vir(self,v) : 
        diff = 1 - ((1-v)**2 + self.getTransmRate()**2 + (1-self.getRecovProb())**2)    #vir up -> diff < 0
        x = randint(0, 100*diff)/100
        self.setTransmRate(self.getTransmRate + x)
        self.setRecovProb(self.getRecovProb() - (diff - x))
        self.setVir(v)

    #if transm rate goes up, vir goes up, recov goes down
    def set_New_TransmRate(self, r) :
        diff = 1 - (r**2 + (1-self.getVir())**2 + (1-self.getRecovProb())**2)    #vir up -> diff < 0
        x = randint(0, 100*diff)/100
        self.setVir(self.getVir + x)
        self.setRecovProb(self.getRecovProb() - (diff - x))
        self.setTransmRate(r)

    #if recov rate goes up, vir goes down, transm rate goes down
    def set_New_RecovProb(self, r) :
        diff = 1 - ((1-r)**2 + self.getTransmRate()**2 + (1-self.getVir())**2)    #vir up -> diff < 0
        x = randint(0, 100*diff)/100
        self.setVir(self.getVir() - x)
        self.setTransmRate(self.getTransmRate() - (diff - x))
        self.setRecovProb(r)


test = Parazite(1,1, 1, 0, 0, 'ID23')
print test
test.set_New_RecovProb(1)
print test


    #idées
    #survie après mort/prob_transm/def_anti_para/taille/prob_manip/
