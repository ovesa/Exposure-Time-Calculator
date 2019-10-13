
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

    Agile_wave, Agile_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
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

    Nicfps_wave, Nicfps_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
    Nicfps_auxilary = scipy.interpolate.interp1d(Nicfps_wave, Nicfps_transmission, fill_value='extrapolate') # interpolating array for Agile

    Nicfps_wave_High_Res = np.arange(0.8, 2.601, 0.001) # 0.8 um - 2.6 um in 10nm steps (0.001 um)
    Nicfps_transmission_High_Res = Nicfps_auxilary(Nicfps_wave_High_Res) # Transmission at every nanometer
    return Nicfps_transmission_High_Res



'''
ARCTIC

Given: CCD plot on ARCTIC page.  Other efficiencies set to unity.
Telescope correction must be performed on ARCTIC.
Digitized using: https://automeris.io/WebPlotDigitizer/
'''

def getARCTIC(string_name_text_file):

    # Load ARCTIC data (in nm)

    Arctic_wave, Arctic_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
    Arctic_auxilary = scipy.interpolate.interp1d(Arctic_wave, Arctic_transmission, fill_value='extrapolate') # interpolating array for Agile

    Arctic_wave_High_Res = np.arange(300., 1005., 5.0) # 320nm - 1000nm array with 1nm resolution
    Arctic_transmission_High_Res = Arctic_auxilary(Arctic_wave_High_Res) * 0.01 # %Transmission to decimal.
    return Arctic_transmission_High_Res


'''
ARCES

TK2048E 2048x2048 pixel CCD
QE Curve at :https://www.apo.nmsu.edu/arc35m/Instruments/SPICAM/spicamusersguide_contents.html

Two cross-dispersion UBK7 prisms at 45deg (we do not know what the tranmission is)

Diffraction grating: 31.6 grooves/mm, blaze angle b = 63.5 deg (nominal), or tan b = 2
incident angle = 69.5 deg

We also do not know the throughput of the grating


'''

def getARCES(string_name_text_file):

    # Load ARCES data (in nm)

    Arces_wave, Arces_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
    Arces_auxilary = scipy.interpolate.interp1d(Arces_wave, Arces_transmission, fill_value='extrapolate') # interpolating array for Agile

    Arces_wave_High_Res = np.arange(350., 1080., 5.0) # 350nm - 1080nm array with 5nm resolution
    Arces_transmission_High_Res = Arces_auxilary(Arces_wave_High_Res) * 0.01 # %QE to decimal
    return Arces_transmission_High_Res


'''
DIS

Standard DIS III grating setup is either B400/R300 or B1200/R1200.

These are the diffractions gratings which are still in use (whose plots were provided)

Options: 5 gratings, 2 CCD's (red and blue)


'''

def getDIS(string_name_text_file):

    # load DIS diffraction throughput:

    Dis_wave, Dis_transmission = np.loadtxt('Efficiencies/'+string_name_text_file, unpack=True, usecols=[0,1])
    Dis_wave = Dis_wave / 10.0
    Dis_wave_blue_CCD, Dis_blue_CCD = np.loadtxt('Efficiencies/DIS_blue_Marconi-CCD42-20-0-310.txt', unpack=True, usecols=[0,1])
    Dis_wave_red_CCD, Dis_red_CCD = np.loadtxt('Efficiencies/DIS_red_E2V-CCD42-20-1-D21.txt', unpack=True, usecols=[0,1])
    Dis_blue_CCD = 0.01 * Dis_blue_CCD # from %QE to decimal
    
    Dis_auxilary = scipy.interpolate.interp1d(Dis_wave, Dis_transmission, fill_value='extrapolate') # interpolating array for Agile

    Dis_wave_High_Res = np.arange(300., 996.3, 5.0) # 350nm - 1080nm array with 5nm resolution
    Dis_transmission_High_Res = Dis_auxilary(Dis_wave_High_Res) * 0.01 # %QE to decimal
    # return Dis_transmission_High_Res, Dis_wave_blue_CCD, Dis_blue_CCD, Dis_wave_red_CCD, Dis_red_CCD
    return Dis_wave_blue_CCD, Dis_blue_CCD, Dis_wave_red_CCD, Dis_red_CCD



'''
TRIPLE SPEC

TripleSpec is a cross-dispersed near-infrared spectrograph that provides simultaneous continuous wavelength 
coverage from 0.95-2.46um (950 - 2460 nm) in five spectral orders.

The primary configuration of the instrument delivers a spectral resolution of R=3500 in a 1.1 arcsecond 
slit at 2.1 pixels per slit on the spectrograph array. Slits with 0.7", 1.5", and 1.7" are also available.

Gratings: all in same file.
Everything else: ...everything else! (detector, optics, etc.)

'''

def getTSPEC(string_name_text_file):

    # load TSPEC data:

    Tspec_wave_grat, Tspec_transmission_grat = np.loadtxt('tspec_stuff/'+string_name_text_file, unpack=True, usecols=[0,1])
    Tspec_wave_other, Tspec_transmission_other = np.loadtxt('tspec_stuff/tspec_everythingelse.txt', unpack=True, usecols=[0,1])


    return Tspec_wave_grat, Tspec_transmission_grat, Tspec_wave_other, Tspec_transmission_other



instruments = ['AGILE', 'NICFPS', 'ARCTIC', 'T-SPEC', 'DIS', 'ARCES']
user_input = input('Enter Instrument From List: [AGILE, NICFPS, ARCTIC, T-SPEC, DIS, ARCES]: ')

if user_input == instruments[0]:
    output = getAGILE('AGILE.txt')

elif user_input == instruments[1]:
    output = getAGILE('NICFPS_Hawaii_QE.txt')

elif user_input == instruments[2]:
    output = getAGILE('ARCTIC_CCD_QE.txt')

elif user_input == instruments[3]:
    wave_grat, tran_grat, wave_other, trans_other = getTSPEC('tspec_grating_throughput.txt')
    plt.plot(wave_grat, tran_grat, 'g')
    plt.plot(wave_other, trans_other, 'r')
    plt.show()
    print('T-SPEC still under development')

elif user_input == instruments[4]:
    # input_DIS_blue = input('Enter DIS Blue channel from list: [B400, B1200_BH]: ')
    # input_DIS_red = input('')
    # print('DIS under development')
    # op1, op2, op3, op4, op5 = getDIS('DIS_B400.txt')
    op2, op3, op4, op5 = getDIS('DIS_B400.txt')
    print('DIS still under development')
    # plt.plot(np.arange(300., 996.3, 5.0), op1, 'g:')
    plt.plot(op2, op3, 'b')
    plt.plot(op4, op5, 'r')
    plt.show()
    

elif user_input == instruments[5]:
    output = getARCES('ARCES.txt')

else:
    print('\nPlease adhere to the given format and choose from the list (no quotes):')
    print(instruments)


# Arces_wave, Arces_transmission = np.loadtxt('ARCES.txt', unpack=True, usecols=[0,1])

# plt.plot(np.arange(350., 1080., 5.0), output, 'b')
# plt.plot(Arces_wave, Arces_transmission*0.01, 'r:')

# plt.show()
