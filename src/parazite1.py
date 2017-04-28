# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    

class Parazite(Individual): 
        
    #Constructeur
    def __init__(self,pos,speed, vir, h_mod, p_manip, idd):
        Individual.__init__(self,pos,speed, idd) 
        self.virulance = vir
        self.hourglass_modificator = h_mod
        self.prob_manip = p_manip

    def getVir(self):
        return self.virulance
    
    def setVir(self, v) :
        self.virulance = v

    def size_mod(self):
        new_radius = 1 - (1 - p)**NUM_PAR
        return new_radius**(1/2)
    
    def trade_off_calculator(self) :
        print('yay')



    #idées
    #survie après mort/prob_transm/def_anti_para/taille/prob_manip/
