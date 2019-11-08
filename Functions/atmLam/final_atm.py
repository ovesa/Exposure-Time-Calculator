#!/usr/bin/env python
# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from scipy import interpolate


# Defining the Moon phases by their Moon-Sun separation angle
# NM = New Moon; WxC = Waxing Crescent; FQ = First Quarter
# WxG = Waxing Gibbous; FM = Full Moon; WnG = Waning Gibbous
# TQ = Third Quarter; WnC = Waning Crescent
NM,WxC,FQ,WxG,FM,WnG,TQ,WnC  = 0,45,90,135,180,225,270,315

def load_flux(moon_phase):
    ''' This code loads in the associated sky table corresponding to the inputted 
    moon phase. Moon phases can be entered by their initials or by their respective 
    Moon-Sun separation. Npz is a zipped dictionary-like archive of the sky tables 
    downloaded from the ESO Sky Calculator  
    (https://www.eso.org/observing/etc/bin/gen/form?INS.MODE=swspectr+INS.NAME=SKYCALC). 
    Each one holds 5 different fluxes and wavelengths, each corresponding to a 
    different initial airmass (X = 1.0, 1.5, 2.0, 2.5, and 3.0). This 
    function is referenced in the total_background_flux function.
    
    
    Input:
    moon_phase = phase of moon desired; currently just uses initials and/or Sun-Moon separation

    Output:
    sky = loads in the sky spectra. '''
 

    moon_file = str(moon_phase) +'.npz'
    sky = np.load(moon_file)

    return sky



def air_mass(X,moon_phase):
    '''This function returns the flux array and its associated index in the .npz file
    that best corresponds closely to the chosen airmass. The flux arrays chosen depend 
    on the sky spectrum downloaded from the ESO sky calculator. Downloaded sky spectrums were
    for initial airmasses for 1.0, 1.5, 2.0, 2.5, and 3.0. While the code can be more involved,
    it calculates the respective flux for a given airmass by approximating the inputted airmass
    to one of the nearest airmasses corresponding to the sky spectrums  downloaded 
    (X = 1.0, 1.5, 2.0, 2.5, and 3.0). This function is referenced in the total_background_flux function. 
    
    Input:
    X = airmass
    moon_phase =  phase of moon desired; currently just uses initials and/or Sun-Moon separation
                The input comes from the load_flux function.
                
    Output:
    flux = flux array
    index = index of the flux array in the .npz file. Used in the cal_bg_photon function.'''
    
    
    # loads in the load_flux function
    sky = load_flux(moon_phase)
    # airmass array
    airmass_array = np.array([1.0,1.5,2.0,2.5,3.0])
   

    if X < 1 or X > 3:
        # raises error if X = airmass is below 1 or above 3
        raise Exception('Airmass should be between 1 and 3. The value of X was: {}'.format(X)) 
    
    # finds the index of the value best corresponding to the inputted X value
    airmass_index = [np.abs(airmass_array - X).argmin()]
    # retrieves the number corresponding to that index
    airmass_value = airmass_array[airmass_index]
    
    return airmass_value,airmass_index



def cal_bg_photon(wav,X,airmass_index,moon_phase):
    '''This function calculates the final background photon flux for a given wavelength, moon phase, and 
    airmass. This function is referenced in the total_background_flux function. 
    
    Input:
    wav = wavelength
    X = airmass
    index = index of the flux array in the .npz file. Used in the cal_bg_photon function
    moon_phase = phase of moon desired; currently just uses initials and/or Sun-Moon separation
    
    
    Output:
    bg_photon_flux = the final background photon flux (ph/s/m^2/micron/arcsec^2)
    '''
    
    
    # loads in the load_flux function
    sky = load_flux(moon_phase)
    
    
    # raises an error if the inputted wavelength is not within the range of 300 nm to 1200 nm
    # each wavelength array is the same; so, it doesn't matter which one is called
    # changing it to microns which is what the user input is
    if wav < min(sky['wav_X_1']*0.001) or wav > max(sky['wav_X_1']*0.001):
        raise Exception('Chosen wavelength out of range (0.3 - 2.5 microns). The wavelength entered was: {} µm'.format(wav))
    else:
        # each wavelength array is the same; so, it doesn't matter which one is called
        # only the flux changes at different airmasses
        # interpolates the wavelength vs the fluxes of the different airmasses
        # the array names correpsond to the airmass associated with them
        interp_flux = interpolate.interp1d(sky['wav_X_1']*0.001,[sky['flux_X_1'],sky['flux_X_1_5'],sky['flux_X_2'],sky['flux_X_2_5'],sky['flux_X_3']])
        # this gives the flux at that chosen wavelength for a particular airmass
        bg_photon_flux = interp_flux(wav)[airmass_index]
            
       
        
    return bg_photon_flux



def total_background_flux(moon_phase,X,wav):
    '''This function contains all of the other functions previously defined for the atmosphere module
    and prints out the final background photon flux.
    
    Input:
    moon_phase = phase of moon desired; currently just uses initials and/or Sun-Moon separation
    X = airmass
    wav = wavelength (nm)
    
    Output:
    bg_photon_flux = the final background photon flux (ph/s/m^2/micron/arcsec^2)
    '''
    
    
    sky = load_flux(moon_phase)
    airmass_value,airmass_index = air_mass(X,moon_phase)
    bg_photon_flux = cal_bg_photon(wav,airmass_value,airmass_index,moon_phase)[0]
    return bg_photon_flux # (ph/s/m^2/micron/arcsec^2)






