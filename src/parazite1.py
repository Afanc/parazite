# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    

class Parazite(Individual): 
        
    #Constructeur
    def __init__(self,pos,speed,vir):
        Individual.__init__(self,pos,speed) 
        self.virulance = vir

    def getVir(self):
        return self.virulance

