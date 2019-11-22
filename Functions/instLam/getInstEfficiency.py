'''
This function returns a decimal value corresponding to the efficiency of the instrument at a given wavelenth.

----------------------------
---------------------------- 

AGILE

AGILE transmission does not require any telescope or CCD correction.

----------------------------
----------------------------  

NICFPS

Given: detector efficiencies only.  The rest are assumed to be unity.  
Telescope correction must be performed for NICFPS in the parent function.

NICFPS detector: The detector is a Rockwell Hawaii 1-RG 1024x1024 HgCdTe device with a 
0.273 arsec/pixel scale and 4.58 arcmin sqaure, unvignetted field, and sensitivity from 0.85 to 2.4 microns.

NICFPS Digitized using WebDigitizer: https://automeris.io/WebPlotDigitizer/
https://www.eso.org/sci/facilities/lasilla/instruments/sofi/inst/HawaiiDetector.html

The detector as tested by Rockwell demonstrates a mean quantum efficiency (QE) of 73.0% in J band and 81.9% in Ks band. 
H-band QE is approximately mid-way between these values on the typical H1RG).

----------------------------
----------------------------

ARCTIC

Given: CCD plot on ARCTIC page.  Other efficiencies set to unity.
Telescope correction must be performed on ARCTIC.
Digitized using: https://automeris.io/WebPlotDigitizer/

----------------------------
----------------------------

ARCES

TK2048E 2048x2048 pixel CCD
QE Curve at :https://www.apo.nmsu.edu/arc35m/Instruments/SPICAM/spicamusersguide_contents.html

Two cross-dispersion UBK7 prisms at 45deg (we do not know what the tranmission is)

Diffraction grating: 31.6 grooves/mm, blaze angle b = 63.5 deg (nominal), or tan b = 2
incident angle = 69.5 deg

Grating throughput unknown.

----------------------------
----------------------------

DIS

Standard DIS III grating setup is either B400/R300 or B1200/R1200.

These are the diffractions gratings which are still in use (whose plots were provided)

Options: 5 gratings, 2 CCD's (red and blue)

----------------------------
----------------------------

TRIPLE SPEC

TripleSpec is a cross-dispersed near-infrared spectrograph that provides simultaneous continuous wavelength 
coverage from 0.95-2.46um (0.95 - 2.460 um) in five spectral orders.

The primary configuration of the instrument delivers a spectral resolution of R=3500 in a 1.1 arcsecond 
slit at 2.1 pixels per slit on the spectrograph array. Slits with 0.7", 1.5", and 1.7" are also available.

Gratings: all in same file.
'Everything else' file are all efficiency sources other than gratings (detector, optics, etc.).

----------------------------
----------------------------
'''

import astropy as ap
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate

nm_to_mic = 1E-3
angstrom_to_microns = 1E-4




def getAGILE(lamda_inp, string_name_text_file):

    '''   
    Inputs: 

        wavelength : float or float array.

        file_name : string for instrument efficiency textfile.


    output:
        
        Percent efficiency in decimal format at a given wavelenght or wavelength range.
    '''

    # Load AGILE data: Contains telescope torrection so this is all that needs to be done for AGILE other than
    # interpolation for a finer grid.

    Agile_wave, Agile_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])
    
    Agile_auxilary = scipy.interpolate.interp1d(Agile_wave * nm_to_mic, Agile_transmission, fill_value='extrapolate') # interpolating array for Agile

    return Agile_auxilary(lamda_inp)



def getNICFPS(lamda_inp, string_name_text_file):
    
    '''
    Inputs: 

        wavelength : float or float array.

        file_name : string for instrument efficiency textfile.


    output:
        
        Percent efficiency in decimal format at a given wavelenght or wavelength range.
    '''
    
    # Load NICFPS data (in microns, um)

    Nicfps_wave, Nicfps_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])
    
    Nicfps_auxilary = scipy.interpolate.interp1d(Nicfps_wave, Nicfps_transmission, fill_value='extrapolate')

    return Nicfps_auxilary(lamda_inp) * 0.01





def getARCTIC(lamda_inp, string_name_text_file):

    '''   
    Inputs: 

        wavelength : float or float array.

        file_name : string for instrument efficiency textfile.


    output:
        
        Percent efficiency in decimal format at a given wavelenght or wavelength range.
    '''

    # Load ARCTIC data (in nm)

    Arctic_wave, Arctic_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])

    Arctic_auxilary = scipy.interpolate.interp1d(Arctic_wave * nm_to_mic, Arctic_transmission, fill_value='extrapolate')

    return Arctic_auxilary(lamda_inp) * 0.01 # %Transmission to decimal.




def getARCES(lamda_inp, string_name_text_file):
    
    '''   
    Inputs: 

        wavelength : float or float array.

        file_name : string for instrument efficiency textfile.


    output:
        
        Percent efficiency in decimal format at a given wavelenght or wavelength range.
    '''

    # Load ARCES data (in nm)

    Arces_wave, Arces_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])
    
    Arces_auxilary = scipy.interpolate.interp1d(Arces_wave * nm_to_mic, Arces_transmission, fill_value='extrapolate') # interpolating array for Agile

    return Arces_auxilary(lamda_inp) * 0.01 # %QE to decimal




def getDIS(lamda_inp, string_name_text_file, ccd_string):
    
    '''
    Inputs:

        wavelength : float or float array.

        file_name : string for instrument efficiency textfile.

        ccd_string : path to detector efficiencies for Red or Blue in DIS


    output:
        
        Percent efficiency in decimal format at a given wavelenght or wavelength range.=
    '''

    # load DIS diffraction throughput:

    Dis_wave, Dis_transmission = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])

    Dis_wave_CCD, Dis_CCD = np.loadtxt(ccd_string, unpack=True, usecols=[0,1])
    
    
    Dis_auxilary = scipy.interpolate.interp1d(Dis_wave * angstrom_to_microns, Dis_transmission, fill_value='extrapolate')


    Dis_CCD_auxilary = scipy.interpolate.interp1d(Dis_wave_CCD * nm_to_mic, Dis_CCD, fill_value='extrapolate')

    # the 1e-04 factor is due to (1/100)^2 since both terms are in %QE
    return Dis_auxilary(lamda_inp) * Dis_CCD_auxilary(lamda_inp) * 1e-04





def getTSPEC(lamda_inp, string_name_text_file, ee_string):
    
    '''
    Inputs:

        wavelength : float or float array.

        file_name : string for instrument efficiency textfile.

        ee_string : path to sources of efficiencies other than gratings.


    output:
        
        Percent efficiency in decimal format at a given wavelenght or wavelength range.=
    '''

    # load TSPEC data in microns:

    Tspec_wave_grat, Tspec_transmission_grat = np.loadtxt(string_name_text_file, unpack=True, usecols=[0,1])
    Tspec_wave_other, Tspec_transmission_other = np.loadtxt(ee_string, unpack=True, usecols=[0,1])


    Tspec_aux_grat = scipy.interpolate.interp1d(Tspec_wave_grat, Tspec_transmission_grat, fill_value='extrapolate')
    Tspec_aux_other = scipy.interpolate.interp1d(Tspec_wave_other, Tspec_transmission_other, fill_value='extrapolate')

    return Tspec_aux_grat(lamda_inp) * Tspec_aux_other(lamda_inp)







if __name__ == "__main__":
    
    local_path = 'Efficiencies/'

    instruments = '[AGILE, NICFPS, ARCTIC, T-SPEC, DIS, ARCES]'
    user_input = input('Enter Instrument From List: [AGILE, NICFPS, ARCTIC, T-SPEC, DIS, ARCES]: ')
    lamda_para = input('Enter wavelength range in um in the form begin,end,resolution: ')
    lamda_para = lamda_para.split(',')
    lamda_para = [float(lamda_para[i]) for i in range(len(lamda_para))]
    lamda_inp = np.arange(lamda_para[0], lamda_para[1], lamda_para[2])

    if user_input == 'AGILE':
        output = getAGILE(lamda_inp, local_path+'AGILE.txt')
        print(output)

    elif user_input == 'NICFPS':
        output = getNICFPS(lamda_inp, local_path+'NICFPS_Hawaii_QE.txt')
        print(output)

    elif user_input == 'ARCTIC':
        output = getARCTIC(lamda_inp, local_path+'ARCTIC_CCD_QE.txt')
        print(output)

    elif user_input == 'T-SPEC':
        output = getTSPEC(lamda_inp, local_path+'tspec_grating_throughput.txt', local_path+'tspec_everythingelse.txt')
        print(output)

    elif user_input == 'DIS':
        red_or_blue = input('R300 or B400? Enter R or B: ')
        if red_or_blue == 'B':
            output = getDIS(lamda_inp, local_path+'DIS_B400.txt', local_path+'DIS_blue_Marconi-CCD42-20-0-310.txt')
            print(output)
        elif red_or_blue == 'R':
            output = getDIS(lamda_inp, local_path+'DIS_R300.txt', local_path+'DIS_red_E2V-CCD42-20-1-D21.txt')
            print(output)
        

    elif user_input == 'ARCES':
        output = getARCES(lamda_inp, local_path+'ARCES.txt')
        print(output)

    else:
        print('\nPlease adhere to the given format and choose from the list (no quotes):\n'+instruments)
