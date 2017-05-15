# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python
"""
    Important pour bien comprendre :
    un rectangle est décrit par 4 directions : les bords gauche/droite/bas/haut.
    C'est donc un vecteur à 1 dimension : [gauche, droite, bas, haut]
"""

import math
from random import *
from datetime import datetime
from collision import *

class Quadtree:
    
    MAX_SIZE = 5
    MAX_LEVEL = 4

    objects = []               #ce qu'il contient
    box = []
    actual_level = None
    space = None

    def __init__(self, lev, space):     #space est un int, space une liste des 4 coins (coordonnées)
        self.actual_level = lev                         #niveau actuel (0 = top)
        self.space = space                              #espace total à dispo
        self.objects = []
        self.box = []

    def add_object(self,obj,idd):
        self.objects.append([obj,idd])

    def remove_object(self, obj, idd): 
        self.objects.remove([obj,idd])

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

        return object_level

    def insert(self,obj,idd):
        object_level = self.index(obj)

        try :
            if self.box and object_level != -1:                 #s'il y a un gosse et que ça fit
                self.box[object_level].insert(obj,idd)              #on descend encore
                return                                          #jusqu'au max, puis on sort

            self.add_object(obj,idd)                                #on met l'objet - c'est bien le seul moment où on n'utilise pas la récursive !
            
        except :
            print "could not fit object in quadtree"

        try : 
            if len(self.objects) > self.MAX_SIZE and self.actual_level < self.MAX_LEVEL :     #si on atteint la limite d'objets, qu'on peut descendre
                if not self.box :
                    self.split()
                for child in list(self.objects) :                             #et dans cec cas, faut mettre tous les enfants dans leurs cases aussi - aussi : on fait une copie !
                    child_level = self.index(child[0])
                    if child_level != -1 :                              #s'ils fittent plus bas
                        self.box[child_level].insert(child[0],child[1])             #on les place plus bas
                        #self.objects.remove([child[0],child[1]])                      
                        self.remove_object(child[0], child[1])#et pas oublier de les enlever du parent (à la liste originale, on itère sur une copie !)

        except :
            print "could not split and fit children"


    def fetch(self,obj,idd):

        object_level = self.index(obj)
        potential_collisions = []

        if object_level != -1 and self.box :                           #s'il y a enfant ! sinon, c'est moi
            potential_collisions = self.box[object_level].fetch(obj,idd)
        
        potential_collisions.extend(self.objects)                      #arrivé au bon niveau, on charge

        for pairs in potential_collisions:
            if pairs[1] == idd :
                potential_collisions.remove([obj,idd])                               #on en profite pour enlever l'objet lui-même
        #if idd in potential_collisions :

        return potential_collisions                                    #pas trouvé de méthode sans créer de nouvelle variable :S



# ---------------- testing -----------------------
"""
def random_balls(n) :
    dic = {}
    letter = 'a'
    for i in range(0,n) :
        x = uniform(0, 10)
        y = uniform(0,10)
        dic[letter]=[x, x+1, y, y+1]
        letter = chr(ord(letter) + 1)
    
    return dic

test_quad = Quadtree(0, [0,10,0,10])              #on crée un quadtree au niveau 0, limites : [0,10,0,10]
#lui peut rester toujours vivant
#on mets quelques objets tests (leurs tailles) : (ils sont tous dans le 1e cadran)
a = [8.8,9.8,3.7,4.7]
b = [8.0,9.0,4.2,5.2]
c = [8.5,9.5,8.2,9.2]
d = [1.7,2.7,8.1,9.1]
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
test_obj = {'a':a,'b':b,'c':c,'d':d, 'e':e,'f':f,'g':g,'h':h,'i':i,'j':j,'k':k,'l':l,'m':m,'n':n,'o':o,'p':p, 'q':q, 'r':r,'s':s,'t':t}
seed(30)
test_obj = random_balls(150)
#et à chaque dt :
for i in test_obj.keys() :         #donc là ça fait n
    test_quad.insert(test_obj[i],i)

print 'au niveau 0, on a ', test_quad.objects
print '\nau niveau 1, on a', test_quad.box[0].objects,'\n',test_quad.box[1].objects,'\n',test_quad.box[2].objects,'\n',test_quad.box[3].objects

b = 0

for i in test_obj.keys():  
    temp_balls = test_quad.fetch(test_obj[i],i)
    temp_keys = [k[1] for k in temp_balls]
    potential_collisions = {key:test_obj[key] for key in temp_keys}


    #print '\n ------ On teste ', i, test_obj[i], 'contre ', potential_collisions, '\n'

    for j in potential_collisions.keys() :
        dx = test_obj[i][0] - potential_collisions[j][0]
        dy = test_obj[i][2] - potential_collisions[j][2]

        dist = math.hypot(dx, dy)
        if dist < (test_obj[i][1]-test_obj[i][0])/2 + (potential_collisions[j][1] - potential_collisions[j][0])/2 :
            print 'boom', test_obj[i], 'contre', potential_collisions[j]
            b += 1

print b


"""
