# -*- coding: utf-8 -*-                                                                                                
#!/usr/bin/env python

from parazite1 import *
from healthy import *

nb_sains = 5
nb_parasite = 3

def start(nb_sains, nb_parasite):
    indi = []
    heal = []
    para = []
    for i in range(nb_sains):
        heal.append(Healthy(200, 200)) # créer des individus
    for a in heal:
        indi.append(a)
    for i in range(nb_parasite):
        para.append(Parazite(5,6,1))
    for i in range(1,10):
        indi.append(i)
    print len(heal)
        

def main():
    print 'le programme de sa mère\n'
    start(nb_sains, nb_parasite)
    
main()