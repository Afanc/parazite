# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python
"""
    Important pour bien comprendre :
    un rectangle est décrit par 4 directions : les bords gauche/droite/bas/haut.
    C'est donc un vecteur à 1 dimension : [gauche, droite, bas, haut]
"""

class Quadtree:
    
    MAX_SIZE = 10
    MAX_LEVEL = 5

    objects = []               #ce qu'il contient
    box = []                   #les 4 sous-niveaux
    actual_level = None
    space = None

    def __init__(self, lev, space):     #space est un int, space une liste des 4 coins (coordonnées)
        self.actual_level = lev                         #niveau actuel (0 = top)
        self.space = space                              #espace total à dispo
        self.box = [Quadtree(i) for i in xrange(4)]     #une liste de 4 quadtree, nous sous-trees

    def add_object(self,obj):
        self.objects.append(obj)

    def reset(self):
        del self.objects[:]      #permet de supprimer les références également, objects = [] sinon
        for i in self.box:
            i.reset()

    def split(self):
        #space[i] est rectangle du type [gauche, droite, bas, haut] décrivant chacun les valeurs limites
        midWidth_x = self.space[1] / 2
        midHeight_y = self.space[3] / 2      #on calcule les milieux
        
        #on attribue de gauche à droite, et de bas en haut
        self.box[0] = Quadtree(self.actuel + 1, [ self.space[0], midWidth_x, self.space[2], midHeight_y])
        self.box[1] = Quadtree(self.actuel + 1, [ midWidth_x, self.space[1], self.space[2], midHeight_y])
        self.box[2] = Quadtree(self.actuel + 1, [ self.space[0], midWidth_x, midHeight_y, self.space[3]])
        self.box[3] = Quadtree(self.actuel + 1, [ midWidth_x, self.space[2], midHeight_y, self.space[3]])

        
    def fit_obj_in_space(self,obj):         #obj est un rectangle
        midWidth_x = self.space[1] / 2
        midHeight_y = self.space[3] / 2

        object_level = -1       #à quel niveau l'objet appartient

        fit_left = obj[1] < midWidth_x       #est-ce l'objet est (complètement) à gauche ?
        fit_right = obj[2] > midWidth_x      #ou à droite ?

        if (obj[3] < midHeight_y):   #s'il est en bas
            if fit_left :               #et à gauche
                object_level = 0            #1e cadran
            elif fit_right :
                object_level = 1            #2e cadran

        if (obj[2] > midHeight_y):   #s'il est en haut
            if fit_left :               #et à gauche
                object_level = 2            #3e cadran
            elif fit_right :
                object_level = 3            #4e cadran

        return object_level

    def insert(self,obj):
        object_level = self.fit_obj_in_space(obj)
        try :                                       #obj ne fit nulle part (division impossible)! -> rajoute ojb au level actuel
            if object_level == -1 :
                self.add_object(obj)
                return
            
        except :
            print "could not fit into parent"

        try :                                       #sinon, on le rajoute au niveau correspondant
            self.objects[object_level].add_object(obj)

            if len(self.object_level[object_level]) > MAX_SIZE and level < MAX_LEVEL:
                if 
                

        except :
            print "could not fit into child"

        




