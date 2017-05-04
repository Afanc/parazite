# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    #on peut supposer qu'on aura besoin de tout, mais c'est pas joli
                            #à noter que le code écrit dans individual.py se lance désormais

class Healthy(Individual):  #est de type Individual
        
    #Constructeur
    def __init__(self,idd, res = []):
        Individual.__init__(self, idd)     #et donc quand je crée un healthy, je crée un individu
        self.resistances = res

    def __str__(self) :
        return 'ID : ' +str(self.idd) +'\nresistance : '+str(self.resistances)\


    def addResistance(self, idd) :
        if idd not in self.resistances:
            resistances.append(idd)

    def setResistance(self, res) :
        if res != [] and res not in self.resistances:
            self.resistances.append(res)

    def getResistances(self) :
        return self.resistances

    def isResistant(self, idd) :
        if idd in self.resistances:
            return True
        return False
