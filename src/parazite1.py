# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    
from healthy import *       #attention risque de dépendance cyclique : ici parazite dépend de healthy ->
                            #il ne faut importer parazite dans healthy. Il moyen de faire ça pour plus tard
                            #mais je m'en souviens plus comment. Plus tard
                            #nvm, il suffit d'importer parazite1 à la fin du code de healthy, ça reste ultra fragile
                            #pour le moment, on pourra faire mieux après. Juste pour vous montrer.

class Parazite(Individual): 
        
    #Constructeur
    def __init__(self,pos,speed,vir):
        Individual.__init__(self,pos,speed) 
        self.virulance = vir

    def getVir(self):
        return self.virulance


test3 = Parazite(5,6,1)
print test3.getVir()

#imaginons maintenant que notre individu sain se fasse paraziter
test4 = Parazite(test2.getPosition(), test2.getSpeed(), 1)
#et que notre parazite se fasse maintenant soigner
test5 = Healthy(test4.getPosition(), test4.getSpeed)  #eh oui, getPosition et getSpeed ne sont pas à redéfinir non plus

print isinstance(test5, Parazite)   #je suis soigné !
print isinstance(test5, Healthy)    #je confirme !

""" à faire mieux : faire vivre tous ces objets en les mettant dans des listes (cf code à bastien), de façon à pouvoir détruire l'ancien objet (comme test4) en le faisant popper de la liste - pas de merde qui traine, et rajouter le nouveau dans la bonne liste et tout.
liste gérée dans main.py du coup
"""
