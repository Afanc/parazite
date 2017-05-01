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
    def set_New_Vir(self,r) : 
        diff = r - self.getVir()
        
        if diff > 0 :       #recov goes up
            x = uniform(0, 1-self.getTransmRate())
            y = uniform(0, self.getRecovProb())
        if diff < 0 :
            x = -uniform(0, self.getTransmRate())
            y = -uniform(0, 1-self.getRecovProb())

        if x+y < diff:  #si ça dépasse notre limite
            norm = diff/(x+y)
            x *= norm
            y *= norm
        self.setTransmRate(self.getTransmRate() - x)
        self.setRecovProb(self.getRecovProb() - y)

        self.setVir(r)

    #if transm rate goes up, vir goes up, recov goes down
    def set_New_TransmRate(self, r) :
        diff = r - self.getTransmRate()
        
        if diff > 0 :       #recov goes up
            x = uniform(0, 1-self.getVir())
            y = uniform(0, self.getRecovProb())
        if diff < 0 :
            x = -uniform(0, self.getVir())
            y = -uniform(0, 1-self.getRecovProb())

        if x+y < diff:  #si ça dépasse notre limite
            norm = diff/(x+y)
            x *= norm
            y *= norm
        self.setVir(self.getVir() - x)
        self.setRecovProb(self.getRecovProb() - y)

        self.setTransmRate(r)

    #if recov rate goes up, vir goes down, transm rate goes down
    def set_New_RecovProb(self, r) :
        diff = r - self.getRecovProb()
        
        if diff > 0 :       #recov goes up - loss of advantage
            x = uniform(0, self.getVir())
            y = uniform(0, self.getTransmRate())

        if diff < 0 :       #recov goes down - gain of advantage
            x = uniform(0, 1-self.getVir())
            y = uniform(0, 1-self.getTransmRate())

        if (y - x) < - diff :
            norm = abs(diff)/(x-y)
            print 'before, x = ',x,'y =',y,'norm = ',norm
            x *= norm
            y *= norm
            print 'after, x=',x,'y=',y

        print 'x=',x,'y=',y

        if diff < 0 :
            self.setVir(self.getVir() + x)
            self.setTransmRate(self.getTransmRate() + y)

        if diff > 0 :
            self.setVir(self.getVir() - x)
            self.setTransmRate(self.getTransmRate() - y)

        self.setRecovProb(r)


    def getTotal(self) :
        return (1 - self.getVir()) + (1 - self.getRecovProb()) + self.getTransmRate()


test = Parazite(1,1, 0, 0, 1, 'ID23')
print 'before'
print test
print test.getTotal()
test.set_New_RecovProb(0.1)
print test
print test.getTotal()
#test.set_New_RecovProb(0.2)
#test.set_New_RecovProb(0.3)
#test.set_New_RecovProb(0.4)
#test.set_New_RecovProb(0.5)
#
#test.set_New_TransmRate(0.2)
#test.set_New_TransmRate(0.3)
#test.set_New_TransmRate(0.4)
#test.set_New_TransmRate(0.5)
#test.set_New_TransmRate(0.6)
#test.set_New_Vir(0.5)
#test.set_New_Vir(0.4)
#test.set_New_Vir(0.3)
#test.set_New_Vir(0.2)
#test.set_New_Vir(0.1)


    #idées
    #survie après mort/prob_transm/def_anti_para/taille/prob_manip/
