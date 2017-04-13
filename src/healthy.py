# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    #on peut supposer qu'on aura besoin de tout, mais c'est pas joli
                            #à noter que le code écrit dans individual.py se lance désormais

class Healthy(Individual):  #prend en argument un individu, il en hérite !
        
    #Constructeur
    def __init__(self,pos,speed):
        Individual.__init__(self,pos,speed)     #et donc quand je crée un healthy, je crée un individu

print test.getSpeed()       #eh oui, ils existent et se partagent
test2 = Healthy(test.getPosition(), test.getSpeed()) #la bonne façon de faire, ne pas accéder directement les attributs

print isinstance(test2,Healthy)     #une fonction pratique, est-ce que a est un objet de type b ?
print isinstance(test2,Individual)  #c'est un individu sain
print isinstance(test, Healthy)     #c'est un individu non-sain
