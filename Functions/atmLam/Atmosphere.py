#!/usr/bin/env python
# coding: utf-8



import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits




# Defining the Moon phases by their Moon-Sun separation angle
# NM = New Moon; WxC = Waxing Crescent; FQ = First Quarter
# WxG = Waxing Gibbous; FM = Full Moon; WnG = Waning Gibbous
# TQ = Third Quarter; WnC = Waning Crescent
NM,WxC,FQ,WxG,FM,WnG,TQ,WnC  = 0,45,90,135,180,225,270,315


def load_fits(moon_phase):
    ''' This code loads in the associated sky table corresponding to the inputted 
    moon phase and outputs the wavlength and flux
    
    Input:
    moon_phase = phase of moon desired. Currently just uses initials

    Output:
    wav = wavelength (nm)
    flux = flux in (ph/s/m^2/micron/arcsec^2) for that moon phase.'''
    
 
    moon_file = 'skytable_' + str(moon_phase) +'.fits'
    sky = fits.open(moon_file)
    sky = sky[1].data 
    
    wav = sky['lam'].data
    flux = sky['flux'].data
    
    return wav,flux



# loading in the sky table
wav,flux = load_fits(TQ)


plt.figure()
plt.title('Sky Flux')
plt.xlabel('Wavelength [nm]')
plt.ylabel('Flux (ph/s/m^2/micron/arcsec^2)')
plt.plot((wav),np.log10(flux), color='k',linewidth=.5)
plt.show()


