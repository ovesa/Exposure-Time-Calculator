#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue. Oct, 11 2019

@author: kellysanderson
===============================================================================
Simpson's Rule for Integration of the Count Equation:
    
    Function that approximates the integral of a the count equation
    Input:
        All inputs should be functions of lambda, 
        lambda_vals: single value or array of lambda values as indicated by user input
        phot_flux: source flux in units of photons per area per time
        atm_e: single value of array of atm transmission values corresponding to user input wavelengths
        tel_e: single value or array of telescope transmission values corresponding to user input wavlengths
        filt_e: single value or array of filter transmission values corresponding to user input wavelengths
        ints_e: single value or array of instruments transmission values corresponding to user input wavelengths
        det_e: single value or array of detector transmission values corresponding to user input wavelengths
    Output:
        approximate integral of function 
===============================================================================
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from astropy.table import Table, Column
from scipy import integrate

def GetSprime(lambda_val, phot_flux, atm_e, tel_e, inst_e, filt_e, det_e):

    if type(lambda_val) is float or type(lambda_val) is int:
        Y = phot_flux*atm_e*tel_e*inst_e*filt_e*det_e*lambda_val
        return Y
    else: 
        Y = np.array(phot_flux)*atm_e*tel_e*inst_e*filt_e*det_e #determine the integrand
        Sprime = integrate.simps(Y,lambda_val, even='first') #Calls a Simpson Rule integrator to calculate Sprime
        return Sprime




