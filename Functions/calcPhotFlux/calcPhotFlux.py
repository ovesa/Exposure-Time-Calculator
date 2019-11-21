#!/usr/bin/env python
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt


h = 6.626*10**-27 #erg s
c = 2.998*10**14 #um/s




def ABFlux(band,mag):
    
    '''
    Calculates flux density if photometric_system = "AB" is input
    
    Inputs: 
    -band = "u","g","r","i","z"
    -mag = magnitude of source
    
    Outputs: 
    -F = flux density at wavelength lam [erg/cm^2/s/um]
    -lam = wavelength in microns
    
    '''
    
    lam_cen_list = np.asarray([0.354,0.475,0.622,0.763,0.905]) #microns
    if band == "u":
        lam = lam_cen_list[0]
    elif band == "g":
        lam = lam_cen_list[1]
    elif band == "r":
        lam = lam_cen_list[2]
    elif band == "i":
        lam = lam_cen_list[3]
    elif band == "z":
        lam = lam_cen_list[4]
    else:
        print('band not included')
    F_nu_0 = 3.63*10**-20 #erg/cm^2/s/Hz
    F_nu_obj = F_nu_0*10**(-mag/2.5) #erg/cm^2/s/Hz
    F = F_nu_obj*(c/(lam)**2)
    return F, lam

def VegaFlux(band,mag):
    
    '''
    Calculates flux density if photometric_system = "Vega" is input
    
    Inputs: 
    -band = "U","B","V","R","I","J","H","K"
    -mag = magnitude of source
    
    Outputs: 
    -F = flux density at wavelength lam [erg/cm^2/s/um]
    -lam = wavelength in microns
    
    '''
    
    lam_cen_list = np.asarray([0.354,0.442,0.540,0.647,0.7865,1.250,1.635,2.200]) #microns
    f_lam_list = np.asarray([417.5,632,363.1,217.7,112.6,31.47,11.38,3.961])*10**-11 #erg cm^-2 s^-1 A^-1
    if band == "U":
        Flam = f_lam_list[0]
        lam = lam_cen_list[0]
    elif band == "B":
        Flam = f_lam_list[1]
        lam = lam_cen_list[1]
    elif band == "V":
        Flam = f_lam_list[2]
        lam = lam_cen_list[2]
    elif band == "R":
        Flam = f_lam_list[3]
        lam = lam_cen_list[3]
    elif band == "I":
        Flam = f_lam_list[4]
        lam = lam_cen_list[4]
    elif band == "J":
        Flam = f_lam_list[5]
        lam = lam_cen_list[5]
    elif band == "H":
        Flam = f_lam_list[6]
        lam = lam_cen_list[6]
    elif band == "K":
        Flam = f_lam_list[7]
        lam = lam_cen_list[7]
    else:
        print('band not included')
    Flam_mic = Flam*(1/(10**-4)) #convert to per micron (1A/10^-4um)                     
    F = Flam_mic*10**(-mag/2.5) #convert to vega mag to flux [ergs cm^-2 s^-1 um^-1]
    return F, lam


#will be evaluated at central wavelength of band
def calcPhotFlux(mag_sys,band,mag):
    
    '''
    Calculates photon flux.
    
    Inputs: 
    -mag_sys = "AB" or "Vega"
    -band = "AB": "u","g","r","i","z"; "Vega":"U","B","V","R","I","J","H","K"
    -mag = magnitude of source
    
    Outputs: S (Photon Flux) [photons/cm^2/s/um]

    '''
    
    if mag_sys == 'AB':
        F,lam = ABFlux(band,mag)
    elif mag_sys == 'Vega':
        F,lam = VegaFlux(band,mag) #F [ergs cm^-2 s^-1 um^-1], lam [um]
    else:
        print('Magnitude system is not compatible')
    S = (F*lam)/(h*c)
    return S



