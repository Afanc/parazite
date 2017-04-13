# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from individual import *    #on peut supposer qu'on aura besoin de tout, mais c'est pas joli
                            #à noter que le code écrit dans individual.py se lance désormais

class Healthy(Individual):  #est de type Individual
        
    #Constructeur
    def __init__(self,pos,speed):
        Individual.__init__(self,pos,speed)     #et donc quand je crée un healthy, je crée un individu
        Resistances = []    #c'est un attribut que seuls les healthys ont uniquement





print test.getSpeed()       #eh oui, ils existent et se partagent
test2 = Healthy(2,4)           #créons un mec sain

print isinstance(test2,Healthy)     #une fonction pratique, est-ce que a est un objet de type b ?
print isinstance(test2,Individual)  #c'est un individu sain
print isinstance(test, Healthy)     #c'est un individu non-sain
print test2.position                #et donc j'ai une position, comme un individu


from parazite1 import *     #voir commentaire dans parazite1.py
