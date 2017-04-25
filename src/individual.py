# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

class Individual:

    #Constructeur, s'utilise : 'johnny = Individual(pos, vit, etc.)'
    def __init__(self, pos, speed, color = [0,0,0]):    #si color n'est pas donné : par défaut !
        self.position = pos 
        self.speed = speed 
        self.color = color #pas besoin de tout définir à la main (on peut aussi mettre par défaut...)

    def __str__(self):  #pseudo-overload
        return 'position : '+str(self.position)+'\ncouleur : '+str(self.color)

    def getPosition(self):  #oui, en python il faut spécifier dans la méthode que l'on se prend soi-même comme objet...
        return self.position

    def getSpeed(self):
        return self.speed

    def setPosition(self,pos): #pratique, à faire pour ~tous les attributs publiques
        self.position = pos


