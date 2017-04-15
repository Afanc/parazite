# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python
"""
    Important pour bien comprendre :
    un rectangle est décrit par 4 directions : les bords gauche/droite/bas/haut.
    C'est donc un vecteur à 1 dimension : [gauche, droite, bas, haut]
"""

import math
from datetime import datetime

class Quadtree:
    
    MAX_SIZE = 5
    MAX_LEVEL = 3

    objects = []               #ce qu'il contient
    box = []
    actual_level = None
    space = None

    def __init__(self, lev, space):     #space est un int, space une liste des 4 coins (coordonnées)
        self.actual_level = lev                         #niveau actuel (0 = top)
        self.space = space                              #espace total à dispo
        self.objects = []
        self.box = []

    def add_object(self,obj):
        self.objects.append(obj)

    def reset(self):
        try :
            del self.objects[:]      #permet de supprimer les références également, objects = [] sinon
            for i in self.box:
                i.reset()
            del self.box[:]
        except :
            print "could not reset quadtree"

    def split(self):
        #space[i] est rectangle du type [gauche, droite, bas, haut] décrivant chacun les valeurs limites
        midWidth_x = self.space[1] / 2
        midHeight_y = self.space[3] / 2      #on calcule les milieux

        #on attribue de gauche à droite, et de bas en haut
        self.box.append(Quadtree(self.actual_level + 1, [ self.space[0], midWidth_x, self.space[2], midHeight_y]))
        self.box.append(Quadtree(self.actual_level + 1, [ midWidth_x, self.space[1], self.space[2], midHeight_y]))
        self.box.append(Quadtree(self.actual_level + 1, [ self.space[0], midWidth_x, midHeight_y, self.space[3]]))
        self.box.append(Quadtree(self.actual_level + 1, [ midWidth_x, self.space[2], midHeight_y, self.space[3]]))

    def index(self,obj):         #obj est un rectangle
        midWidth_x = self.space[1] / 2
        midHeight_y = self.space[3] / 2

        object_level = -1       #à quel niveau l'objet appartient

        fit_left = obj[1] < midWidth_x       #est-ce l'objet est (complètement) à gauche ?
        fit_right = obj[0] > midWidth_x      #ou à droite ?

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

        #print obj, object_level
        return object_level

    def insert(self,obj):
        object_level = self.index(obj)

       # print '\nOn rajoute un objet ! Level ', self.actual_level, 'objet : ', obj, 'contenu : ', self.objects
#        try :
        if self.box and object_level != -1:                 #s'il y a un gosse et que ça fit
            #print obj, 'déjà un enfant !'
            self.box[object_level].insert(obj)              #on descend encore
            return                                          #jusqu'au max, puis on sort

        self.add_object(obj)                                #on met l'objet - c'est bien le seul moment où on n'utilise pas la récursive !
            
#        except :
        #print "could not fit object in quadtree"
        #try : 
        if len(self.objects) > self.MAX_SIZE and self.actual_level < self.MAX_LEVEL :     #si on atteint la limite d'objets, qu'on peut descendre
            #print 'split', self.actual_level, obj
            if not self.box :
                self.split()
            for child in list(self.objects) :                             #et dans cec cas, faut mettre tous les enfants dans leurs cases aussi
                child_level = self.index(child)
                #print 'distribue child', child, "à l'index", child_level, '\n'
                if child_level != -1 :                              #s'ils fittent plus bas
                    self.box[child_level].insert(child)             #on les place plus bas
                #    print 'child inséré', self.box[child_level].objects , 'et les parents ont', self.objects
                    self.objects.remove(child)                      #et pas oublier de les enlever du parent (à la liste originale, on itère sur une copie !)
                #    print 'on enlève le gosse aux parents', self.objects

        #except :
        #print "could not split and fit children"


    def fetch(self,obj):
        #print '\nje reçois', obj, 'niveau', self.actual_level

        object_level = self.index(obj)
        potential_collisions = []

        if object_level != -1 and self.box :                           #s'il y a enfant ! sinon, c'est moi
            potential_collisions = self.box[object_level].fetch(obj)
        
        potential_collisions.extend(self.objects)                      #arrivé au bon niveau, on charge

        #print obj, 'je trouve', potential_collisions, 'niveau', self.actual_level

        if obj in potential_collisions :
        #    print "j'enlève", obj
            potential_collisions.remove(obj)                               #on en profite pour enlever l'objet lui-même
        #    print "je m'enlève", potential_collisions

        #print obj,'je sors', potential_collisions, 'niveau', self.actual_level

        return potential_collisions                                    #pas trouvé de méthode sans créer de nouvelle variable :S



# ---------------- testing -----------------------
"""
startTime = datetime.now()
test_quad = Quadtree(0, [0,10,0,10])              #on crée un quadtree au niveau 0, limites : [0,10,0,10]
#lui peut rester toujours vivant
#on mets quelques objets tests (leurs tailles) : (ils sont tous dans le 1e cadran)
a = [6.8,7.8,2.7,3.7]
b = [8.0,9.0,5.2,6.2]
c = [8.5,9.5,3.2,4.2]
d = [4.7,5.7,7.1,8.1]
e = [7.2,8.2,4.5,5.5]
f = [3.5,4.5,7.0,8.0]
g = [9.0,10.0,1.2,2.2]
h = [6.2,7.3,5.4,6.4]
i = [5.0,6.0,5.0,6.0]
j = [7.9,8.9,4.0,5.0]
k = [8.2,9.2,5.0,6.0]
l = [1.1,2.1,2.0,3.0]
m = [2.3,3.3,8.3,9.3]
n = [5.5,6.5,4.0,5.0]
o = [8.5,9.5,8.0,9.0]
p = [1.5,2.5,4.0,5.0]
q = [2.0,3.0,7.3,8.3]
r = [7.2,8.2,6.3,7.3]
s = [4.0,5.0, 3.0,4.0]
t = [3.3,4.3,5.6,6.6]
test_obj = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t]
#et à chaque dt :
test_quad.reset()
for i in test_obj :         #donc là ça fait n
    test_quad.insert(i)   

#print 'au niveau 0, on a ', test_quad.objects
#print '\nau niveau 1, on a', test_quad.box[0].objects,'\n',test_quad.box[1].objects,'\n',test_quad.box[2].objects,'\n',test_quad.box[3].objects

for i in test_obj:          #eh oui, faut attendre que chaque objet ait été inséré, on n'a pas tous les index sinon ! Donc on a encore n
    potential_collisions = test_quad.fetch(i)

    print '\n ------ On teste ', i, 'contre ', potential_collisions, '\n'
    for j in potential_collisions:                          #et là ça fait m = min(MAX_SIZE,len(potential_collisions))
        
        #calcul de la distance entre le centre des particules
        dx = i[0] - j[0]
        dy = i[2] - j[2]
        dist = math.hypot(dx, dy)
    
    # comportement physique des particules en cas de collision
        if dist <= float(i[1]-i[0])/2 + float(j[1] - j[0])/2 :             #on suppose que c'est sphérique ici
            print "collision ! entre ", i, j
             Et après on détermine le rest
            tangent = math.atan2(dy, dx)
            angle = 0.5 * math.pi + tangent

            self.angle -= 2 * tangent
            p2.angle -= 2 * tangent

            angle = 0.5 * math.pi + tangent

            #self.x += math.sin(angle)
            #self.y -= math.cos(angle)
            self.velocity_x += math.sin(angle)
            self.velocity_y -= math.cos(angle)
            p2.velocity_x -= math.sin(angle)                                                                           
            p2.velocity_y += math.cos(angle)
            
print datetime.now() - startTime
"""
