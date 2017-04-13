# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

class Individual(object):

    #Constructeur, s'utilise : 'johnny = Individual(pos, vit, etc.)'
    def __init__(self, pos, speed):
        self.position = pos 
        self.speed = speed 

    def getPosition(self):  #oui, en python il faut spécifier dans la méthode que l'on se prend soi-même comme objet...
        return self.position

    def getSpeed(self):
        return self.speed

    def setPosition(self,pos): #pratique, à faire pour ~tous les attributs publiques
        self.position = pos


#s'utilise ainsi
test = Individual(2,3)
print test.getPosition()
