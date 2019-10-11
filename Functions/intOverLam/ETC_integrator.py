#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:43:15 2017

@author: kellysanderson
===============================================================================
Simpson's Rule for Integration:
    
    Function that approximates the integral of a function
    Input:
        function of x, a initial value in function range, b final value in function range, 
        h increment length 
    Output:
        approximate integral of function 
===============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from astropy.table import Table, Column
from scipy import integrate


h = 6.62e-27 #planck's constant ergs s
c = 2.99e10 #speed of light cm s^-1
kb = 1.38e-16 #Boltzmaaaan's con$tant ergs/K
def bb_photflux(lam,T):
    A = 2.0*h*c*c

    B = lam**5.0

    D = []
    for i in range(len(lam)):
        C = (h*c)/(lam[i]*kb*T)

        D.append(math.exp(C)-1.0)

    E = (A)/(B*D)

    return E


lambda_vals = (np.linspace(4000.0, 100000.0, 40000))*(1.0e-8) #lambda values in cm
print(lambda_vals)

T = 10000.0 #K; temperature of hot hot boi
phot_flux = bb_photflux(np.array(lambda_vals),T)

atm_e = [1.0]*len(lambda_vals)
tel_e = [1.0]*len(lambda_vals)
inst_e = [1.0]*len(lambda_vals)
filt_e = [1.0]*len(lambda_vals)
det_e = [1.0]*len(lambda_vals)

Y = np.array(phot_flux)*atm_e*tel_e*inst_e*filt_e*det_e*(lambda_vals/(h*c))
print(integrate.simps(Y,lambda_vals, even='first'))
Sprime = integrate.simps(Y,lambda_vals, even='first')
plt.loglog(lambda_vals,Y)
plt.show()



