from parazite1 import *
from random import uniform, sample
def trade_off(para_i):
    qui = sample(range(1,4), 1)
    new_vir = 0
    new_recov = 0
    new_transmission = 0
    R0 = uniform(0,10):
    new_vir = 
    
    if qui[0] == 1:
        new_vir = uniform(0,1)
        new_transmission = (1-new_vir)/2
        new_recov = (1-new_vir)/2
    
    if qui[0] == 2:
        new_transmission = uniform(0,1)
        new_recov = new_transmission
        new_vir = 1- 2*(new_transmission)
    
    if qui[0] == 3:
        new_recov = uniform(0,1)
        new_transmission = new_recov
        new_vir = 1- 2*(new_recov)
        
    para_i.setVir(new_vir)
    para_i.setTransmRate(new_transmission)
    para_i.setRecovProb(new_recov)

test = Parazite(0.7, 0.1, 0, 'ID23')    
trade_off(test)
print test.getVir()
print test.getTransmRate()
print test.getRecovProb()    