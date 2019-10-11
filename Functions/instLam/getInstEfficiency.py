
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

def getAGILE(string_name_text_file):

    # Load AGILE data: Contains telescope torrection so this is all that needs to be done for AGILE other than
    # interpolation for a finer grid.

    Agile_wave, Agile_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])
    Agile_auxilary = scipy.interpolate.interp1d(Agile_wave, Agile_transmission, fill_value='extrapolate') # interpolating array for Agile

    Agile_wave_High_Res = np.arange(320., 1001., 1.0) # 320nm - 1000nm array with 1nm resolution
    Agile_transmission_High_Res = Agile_auxilary(Agile_wave_High_Res) # Transmission at every nanometer
    return Agile_transmission_High_Res

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

def getNICFPS(string_name_text_file):
    
    # Load NICFPS data (in microns, um)

    Nicfps_wave, Nicfps_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])
    Nicfps_auxilary = scipy.interpolate.interp1d(Nicfps_wave, Nicfps_transmission, fill_value='extrapolate') # interpolating array for Agile

    Nicfps_wave_High_Res = np.arange(0.8, 2.601, 0.001) # 320nm - 1000nm array with 1nm resolution
    Nicfps_transmission_High_Res = Nicfps_auxilary(Nicfps_wave_High_Res) # Transmission at every nanometer
    return Nicfps_transmission_High_Res



'''
ARCTIC

Given: CCD plot on ARCTIC page.  Other efficiencies set to unity.
Telescope correction must be performed on ARCTIC.
Digitized using: https://automeris.io/WebPlotDigitizer/
'''

def getARCTIC(string_name_text_file):

    # Load ARCTIC data (in microns, nm)

    Arctic_wave, Arctic_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])
    Arctic_auxilary = scipy.interpolate.interp1d(Arctic_wave, Arctic_transmission, fill_value='extrapolate') # interpolating array for Agile

    Arctic_wave_High_Res = np.arange(300., 1005., 5.0) # 320nm - 1000nm array with 1nm resolution
    Arctic_transmission_High_Res = Arctic_auxilary(Arctic_wave_High_Res) * 0.01 # Transmission at every nanometer
    return Arctic_transmission_High_Res


