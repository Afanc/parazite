# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from CONSTANTES import *
 
class Individual(object):   #object afin d'avoir des 'nouvelles' classes

    #Constructeur, s'utilise : 'johnny = Individual(pos, vit, etc.)'
    def __init__(self, idd, res = [], color = [0,0,0]):    #si color n'est pas donné : par défaut !
        self.color = color #pas besoin de tout définir à la main (on peut aussi mettre par défaut...)
        self.idd = idd
        self.resistances = res
        
    def __str__(self):  #pseudo-overload
        return 'ID : ' +str(self.idd) + "\n Resistances : " + str(self.resistances)
    
    def __del__(self):
        pass
        #print "Individual détruit"
        
    def getPosition(self):  #oui, en python il faut spécifier dans la méthode que l'on se prend soi-même comme objet...
        return self.position

    def getSpeed(self):
        return self.speed

    def getIdd(self):
        return self.idd
     
    def setIdd(self, a):
        self.idd = a
        
    def addResistance(self, idd) :
        if idd not in self.resistances:
            temp_res = list(self.resistances)
            temp_res.append(idd)
            self.resistances = temp_res
            
    def getResistances(self) :
        return self.resistances

