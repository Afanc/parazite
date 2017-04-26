# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    #on peut supposer qu'on aura besoin de tout, mais c'est pas joli
                            #à noter que le code écrit dans individual.py se lance désormais

class Healthy(Individual):  #est de type Individual
        
    #Constructeur
    def __init__(self,pos,speed):
        Individual.__init__(self,pos,speed)     #et donc quand je crée un healthy, je crée un individu
        Resistances = []    #c'est un attribut que seuls les healthys ont uniquement

