# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    #on peut supposer qu'on aura besoin de tout, mais c'est pas joli
                            #à noter que le code écrit dans individual.py se lance désormais

class Healthy(Individual):  #est de type Individual
        
    #Constructeur
    def __init__(self,idd):
        Individual.__init__(self, idd)     #et donc quand je crée un healthy, je crée un individu
        Resistances = []    #c'est un attribut que seuls les healthys ont uniquement

    def addResistance(self, idd) :
        if idd not in self.Resistances:
            Resistances.append(idd)

    def getResistances(self) :
        return self.Resistances

    def isResistant(self, idd) :
        if idd in self.Resistances:
            return True
        return False
