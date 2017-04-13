# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

class Quadtree:
    
    MAX_IND = 10
    MAX_LEV = 5

    objects = []               #ce qu'il contient
    box = []                   #les 4 sous-niveaux
    actual_level = None
    space = None

    def __init__(self, lev, space):     #space est un int, space une liste des 4 coins (coordonnées)
        self.actual_level = lev                         #niveau actuel (0 = top)
        self.space = space                              #espace total à dispo
        self.box = [Quadtree(i) for i in xrange(4)]     #une liste de 4 quadtree, nous sous-trees

    def reset(self):
        del self.objects[:]      #permet de supprimer les références également, objects = [] sinon
        for i in self.box:
            i.reset()

    def split(self):
        #space[i] est du type [gauche_bas,droite_bas,gauche_haut,droite_haut], chacun un [x,y]
        midHeight_y = self.space[3][1] / 2      #on calcule les milieux
        midWidth_x = self.space[1][0] / 2
        
        #on attribue de gauche à droite, et de bas en haut
        box[0] = Quadtree(self.actuel + 1, [ self.space[0], [midWidth_x,self.space[0][1]], [self.space[0][0],midHeight_y],[midWidth_x, midHeight_y] ])
        box[1] = Quadtree(self.actuel + 1, [ [midWidth_x,self.space[0][1]], self.space[1], [midWidth_x, midHeight_y], [self.space[1][0],midHeight_y] ])
        box[2] = Quadtree(self.actuel + 1, [ self.space[0], [self.space[0[0], midHeight_y], [midWidth_x, midHeight_y], self.space[2], [midWidth_x, self.space[2][1]]] ])
        box[3] = Quadtree(self.actuel + 1, [ [midWidth_x, midHeight_y], [self.space[1][0], midHeight_y], [midWidth_x, self.space[2][1]], self.space[3] ])

        

