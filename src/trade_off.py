# -*- coding: utf-8 -*-        
from parazite1 import *
from random import uniform, sample
import matplotlib.pyplot as plt
from CONSTANTES import *
from CHANGING_CONST import *

def trade_off(para_i = None, effect_arg = None):
    if effect_arg != None:
        new_vir = 0
        new_recov = 0
        new_transmission = 0
        effect = effect_arg
        new_vir = (effect**2)/100
        new_transmission = 1/(1+exp(-(effect/1.1-5)))
        new_recov =  0.1 + 1/effect
        if new_recov > 1:
            new_recov = 1
        return [new_vir,new_transmission,new_recov]
    if isinstance(para_i, Parazite):
        new_vir = 0
        new_recov = 0
        new_transmission = 0
        effect = (para_i.getVir()*100)**0.5
        effect += uniform(-2,2)
        compteur = 0
        while effect > 10 or effect <0 and compteur < 3:
            effect = (para_i.getVir()*100)**0.5
            effect += uniform(-2,2)
            compteur += 1
        if effect > 10 or effect <0: 
            effect = (para_i.getVir()*100)**0.5
        new_vir = (effect**2)/100
        new_transmission = 1/(1+exp(-(effect/1.1-5)))
        new_recov =  0.1 + 1/effect
        if new_recov > 1:
            new_recov = 1
        para_i.setVir(new_vir)
        para_i.setTransmRate(new_transmission)
        para_i.setRecovProb(new_recov)
    else : 
        new_vir = 0
        new_recov = 0
        new_transmission = 0
        effect = uniform(0,10)
        new_vir = (effect**2)/100
        new_transmission = 1/(1+exp(-(effect/1.1-5)))
        new_recov =  0.1 + 1/effect
        if new_recov > 1:
            new_recov = 1
        
        return [new_vir,new_transmission,new_recov]


print trade_off(effect_arg = 2.6)
  
y = []
x = []
R0 = 0
for i in arange(0.1,10.0,0.1):
    x.append(i)
    effect = i
    new_vir = (effect**2)/100
    new_transmission = 1/(1+exp(-(effect/1.1-5)))
    new_recov =  0.1 + 1/effect
    if new_recov > 1:
        new_recov = 1
    R0num = (200 * (1+new_transmission)*0.4)
    R0den = ((1+new_vir)*DYING_PROB + (1+new_recov)*BASE_CHANCE_OF_HEALING)
    R0 = R0num/R0den
    y.append(R0)

plt.scatter(x,y)

plt.show()


#print trade_off(effect_arg = 7.0) #correspond à une virulance de 0.49
'''    
new_vir = []    
for effect in range(0,10,1):
    new_vir.append(1/(1+exp(-(effect/1.1-5))))
plt.scatter(range(0,10,1 ),new_vir)
plt.show()
  
new_recov =  1- (effect**2)/150
    

test = Parazite(0.7, 0.1, 0, 'ID23')    
trade_off(test)
print test.getVir()
print test.getTransmRate()
print test.getRecovProb()
'''