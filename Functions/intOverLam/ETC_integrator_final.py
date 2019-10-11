#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 15:43:15 2017

@author: kellysanderson
===============================================================================
Simpson's Rule for Integration of the Count Equation:
    
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

def GetSprime(lambda_vals, phot_flux, atm_e, tel_e, inst_e, filt_e, det_e):
    
    h = 6.62e-27 #planck's constant ergs s
    c = 2.99e10 #speed of light cm s^-1
    kb = 1.38e-16 #Boltzmaaaan's con$tant ergs/K
    Y = np.array(phot_flux)*atm_e*tel_e*inst_e*filt_e*det_e #determine the integrand
    Sprime = integrate.simps(Y,lambda_vals, even='first') #Calls a Simpson Rule integrator to calculate Sprime
    return Sprime




