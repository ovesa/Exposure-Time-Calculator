
'''
Instrument efficiency:
This function should return some decimal value corresponding to the efficiency of the instrument.
'''

import astropy as ap
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

'''
AGILE

AGILE TRANSMISSION: DOES NOT REQUIRE ANY TELESCOPE OR CCD CORRECTION
Just return the value from getAGILE() given some wavelength.
'''

def getAGILE(lamda_inp, string_name_text_file):

    # Load AGILE data: Contains telescope torrection so this is all that needs to be done for AGILE other than
    # interpolation for a finer grid.

    Agile_wave, Agile_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
    
    nm_to_angs = 10.0
    Agile_auxilary = scipy.interpolate.interp1d(Agile_wave * nm_to_angs, Agile_transmission, fill_value='extrapolate') # interpolating array for Agile

    return Agile_auxilary(lamda_inp)

'''
NICFPS

Given: detector efficiency only.  The rest are assumed to be unity.  
Telescope correction must be performed for NICFPS.

NICFPS detector: The detector is a Rockwell Hawaii 1-RG 1024x1024 HgCdTe device with a 
0.273 arsec/pixel scale and 4.58 arcmin sqaure, unvignetted field, and sensitivity from 0.85 to 2.4 microns.

NICFPS Digitized using WebDigitizer: https://automeris.io/WebPlotDigitizer/
https://www.eso.org/sci/facilities/lasilla/instruments/sofi/inst/HawaiiDetector.html

The detector as tested by Rockwell demonstrates a mean quantum efficiency (QE) of 73.0% in J band and 81.9% in Ks band. 
H-band QE is approximately mid-way between these values on the typical H1RG.)
'''

def getNICFPS(lamda_inp, string_name_text_file):
    
    # Load NICFPS data (in microns, um)

    Nicfps_wave, Nicfps_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
    
    micron_to_angs = 10**4.0
    Nicfps_auxilary = scipy.interpolate.interp1d(Nicfps_wave * micron_to_angs, Nicfps_transmission, fill_value='extrapolate') # interpolating array for Agile

    return Nicfps_auxilary(lamda_inp) * 0.01



'''
ARCTIC

Given: CCD plot on ARCTIC page.  Other efficiencies set to unity.
Telescope correction must be performed on ARCTIC.
Digitized using: https://automeris.io/WebPlotDigitizer/
'''

def getARCTIC(lamda_inp, string_name_text_file):

    # Load ARCTIC data (in nm)

    Arctic_wave, Arctic_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])

    nm_to_angs = 10.0
    Arctic_auxilary = scipy.interpolate.interp1d(Arctic_wave * nm_to_angs, Arctic_transmission, fill_value='extrapolate')

    return Arctic_auxilary(lamda_inp) * 0.01 # %Transmission to decimal.


'''
ARCES

TK2048E 2048x2048 pixel CCD
QE Curve at :https://www.apo.nmsu.edu/arc35m/Instruments/SPICAM/spicamusersguide_contents.html

Two cross-dispersion UBK7 prisms at 45deg (we do not know what the tranmission is)

Diffraction grating: 31.6 grooves/mm, blaze angle b = 63.5 deg (nominal), or tan b = 2
incident angle = 69.5 deg

We also do not know the throughput of the grating


'''

def getARCES(lamda_inp, string_name_text_file):

    # Load ARCES data (in nm)

    Arces_wave, Arces_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
    
    nm_to_angs = 10.0
    Arces_auxilary = scipy.interpolate.interp1d(Arces_wave * nm_to_angs, Arces_transmission, fill_value='extrapolate') # interpolating array for Agile

    return Arces_auxilary(lamda_inp) * 0.01 # %QE to decimal


'''
DIS

Standard DIS III grating setup is either B400/R300 or B1200/R1200.

These are the diffractions gratings which are still in use (whose plots were provided)

Options: 5 gratings, 2 CCD's (red and blue)


'''

def getDIS(lamda_inp, string_name_text_file):

    # load DIS diffraction throughput:

    Dis_wave, Dis_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])

    Dis_wave_blue_CCD, Dis_blue_CCD = np.loadtxt('Efficiencies/DIS_blue_Marconi-CCD42-20-0-310.txt', unpack=True, usecols=[0,1])
    Dis_wave_red_CCD, Dis_red_CCD = np.loadtxt('Efficiencies/DIS_red_E2V-CCD42-20-1-D21.txt', unpack=True, usecols=[0,1])
    
    # only red_CCD is ion decimals so convert back to % and convert back the total for output
    Dis_red_CCD = 100.0 * Dis_red_CCD # to %QE

    
    Dis_auxilary = scipy.interpolate.interp1d(Dis_wave, Dis_transmission, fill_value='extrapolate')

    nm_to_angs = 10.0

    Dis_blue_CCD_auxilary = scipy.interpolate.interp1d(Dis_wave_blue_CCD * nm_to_angs, Dis_blue_CCD, fill_value='extrapolate')
    Dis_red_CCD_auxilary = scipy.interpolate.interp1d(Dis_wave_red_CCD * nm_to_angs, Dis_red_CCD, fill_value='extrapolate')

    # the 1e-06 factor is due to (1/100)^3 since all 3 terms are in %
    return Dis_auxilary(lamda_inp) * Dis_blue_CCD_auxilary(lamda_inp) * Dis_red_CCD_auxilary(lamda_inp) * 1e-06



'''
TRIPLE SPEC

TripleSpec is a cross-dispersed near-infrared spectrograph that provides simultaneous continuous wavelength 
coverage from 0.95-2.46um (950 - 2460 nm) in five spectral orders.

The primary configuration of the instrument delivers a spectral resolution of R=3500 in a 1.1 arcsecond 
slit at 2.1 pixels per slit on the spectrograph array. Slits with 0.7", 1.5", and 1.7" are also available.

Gratings: all in same file.
Everything else: ...everything else! (detector, optics, etc.)

'''

def getTSPEC(lamda_inp, string_name_text_file):

    # load TSPEC data:

    Tspec_wave_grat, Tspec_transmission_grat = np.loadtxt('tspec_stuff/'+string_name_text_file, unpack=True, usecols=[0,1])
    Tspec_wave_other, Tspec_transmission_other = np.loadtxt('tspec_stuff/tspec_everythingelse.txt', unpack=True, usecols=[0,1])

    micron_to_angs = 10**4.0

    Tspec_aux_grat = scipy.interpolate.interp1d(Tspec_wave_grat * micron_to_angs, Tspec_transmission_grat, fill_value='extrapolate')
    Tspec_aux_other = scipy.interpolate.interp1d(Tspec_wave_other * micron_to_angs, Tspec_transmission_other, fill_value='extrapolate')

    return Tspec_aux_grat(lamda_inp) * Tspec_aux_other(lamda_inp)



instruments = ['AGILE', 'NICFPS', 'ARCTIC', 'T-SPEC', 'DIS', 'ARCES']
user_input = input('Enter Instrument From List: [AGILE, NICFPS, ARCTIC, T-SPEC, DIS, ARCES]: ')
lamda_inp = input('Enter wavelength (angstrom): ')
lamda_inp = float(lamda_inp)

if user_input == instruments[0]:
    output = getAGILE(lamda_inp, 'AGILE.txt')
    print(output)

elif user_input == instruments[1]:
    output = getNICFPS(lamda_inp, 'NICFPS_Hawaii_QE.txt')
    print(output)

elif user_input == instruments[2]:
    output = getARCTIC(lamda_inp, 'ARCTIC_CCD_QE.txt')
    print(output)

elif user_input == instruments[3]:
    output = getTSPEC(lamda_inp, 'tspec_grating_throughput.txt')
    print(output)

elif user_input == instruments[4]:
    output = getDIS(lamda_inp, 'DIS_B400.txt')
    print(output)
    

elif user_input == instruments[5]:
    output = getARCES(lamda_inp, 'ARCES.txt')
    print(output)

else:
    print('\nPlease adhere to the given format and choose from the list (no quotes):')
    print(instruments)
