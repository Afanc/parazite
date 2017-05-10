from parazite1 import *
from random import uniform, sample
import matplotlib.pyplot as plt

def trade_off(para_i = None):
    if isinstance(para_i, Parazite):
        new_vir = 0
        new_recov = 0
        new_transmission = 0
        effect = uniform(0,10)
        new_vir = 1/(1+exp(-(effect/1.1-5)))
        new_transmission = -0.1 * effect + 1
        new_recov = 0.1 * effect 
        para_i.setVir(new_vir)
        para_i.setTransmRate(new_transmission)
        para_i.setRecovProb(new_recov)
    else : 
        new_vir = 0
        new_recov = 0
        new_transmission = 0
        effect = uniform(0,10)
        new_vir = 1/(1+exp(-(effect/1.1-5)))
        new_transmission = -0.1 * effect + 1
        new_recov = 0.1 * effect 
        return [new_vir,new_transmission,new_recov]
    '''
new_vir = []    
for effect in range(0,10,1):
    new_vir.append(1/(1+exp(-(effect/1.1-5))))
plt.scatter(range(0,10,1 ),new_vir)
plt.show()
'''    

    
'''
test = Parazite(0.7, 0.1, 0, 'ID23')    
trade_off(test)
print test.getVir()
print test.getTransmRate()
print test.getRecovProb()'''