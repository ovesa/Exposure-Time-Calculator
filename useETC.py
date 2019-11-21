import numpy as np
import math
from astropy.io import fits
import matplotlib.pyplot as plt

'''
all imports for functionality:
from folder.subfolder.file import function (input parameters)
'''

from Functions.instLam.getInstEfficiency import getAGILE #  (wave range, string for text file)
from Functions.instLam.getInstEfficiency import getNICFPS #  (wave range, string for text file)
from Functions.instLam.getInstEfficiency import getARCTIC #  (wave range, string for text file)
from Functions.instLam.getInstEfficiency import getARCES #  (wave range, string for text file)
from Functions.instLam.getInstEfficiency import getDIS #  (wave range, transmission for grating file, transmission channel file)
from Functions.instLam.getInstEfficiency import getTSPEC #  (wave range, transmission for grating file, 'everything else' file)

from Functions.telLam.telLam import telLam #  (primary dia, obstruction, dia, Al reflectivity)

from Functions.solveForExp.solve_expT import calc_expT # (SN,flux,back,seeing,tel)

from Functions.intOverLam.ETC_integrator_final import GetSprime #  (lambda_vals, phot_flux, atm_e, tel_e, filt_e, inst_e, det_e)

from Functions.filtLAM.filtLAM import filtLAM # (filt,wl)

from Functions.atmLam.final_atm import total_background_flux # (moonphase, airmass, wavelength)

from Functions.atm_trans.atm_trans import atm_trans # (wavelength, airmass, path)

from Functions.calcPhotFlux.calcPhotFlux import calcPhotFlux # (mag_sys,band,mag)

from Functions.intOverLam.ETC_integrator_final import GetSprime # (lambda_vals, phot_flux, atm_e, tel_e, inst_e, filt_e, det_e)


# instLam can now be fully called!
# telLam can now be called!
# solve_expT can be used!
# intOverLam can be used but needs completion
# all filters can now be used along with the instruments
# moonphases now works!

# some of the functions require files so these paths go to them!
instrument_path = 'Functions/instLam/Efficiencies/'
filter_path = 'Functions/filtLam/'
moonphase_path = 'Functions/atmLam/'
atmos_transmission_path = 'Functions/atm_trans/'

# print(atm_trans(0.55, 1.2))

# EXAMPLES OF WORKING SHIT:
# print(getAGILE(np.arange(0.5, 0.8, 0.01), instrument_path+'AGILE.txt'))
# print(getARCTIC(np.arange(0.5, 0.8, 0.01), instrument_path+'ARCTIC_CCD_QE.txt'))
# print(getDIS(np.arange(0.5, 0.8, 0.01), instrument_path+'DIS_R300.txt', instrument_path+'DIS_red_E2V-CCD42-20-1-D21.txt'))
# print(getNICFPS(np.arange(1.0, 2.0, 0.1), instrument_path+'NICFPS_Hawaii_QE.txt'))
# print(getARCES(np.arange(0.5, 0.8, 0.01), instrument_path+'ARCES.txt'))
# print(getTSPEC(np.arange(1.0, 2.0, 0.1), instrument_path+'tspec_grating_throughput.txt', instrument_path+'tspec_everythingelse.txt'))
# print(telLam(100.0,20.0,0.1)) 
# print(calc_expT(100., 23.5, 2.4, 1., 10000.))
# print(filtLAM(filter_path+'jc_V', np.arange(0.5, 0.8, 0.01)))
# print(atm_trans(0.5, 1.2, atmos_transmission_path))

# print(total_background_flux(moonphase_path+'45', 1.2, 0.55))
# print(calcPhotFlux('AB', 'g', 20.0))

# Main User Inputs:

instrument_list = '[AGILE, NICFPS, ARCTIC, T-SPEC, DIS, ARCES]'
filter_list = '[jc_U, jc_B, jc_V, jc_R, jc_I, mko_H, mko_J, mko_K, sdss_g, sdss_r, sdss_i, sdss_u, sdss_z]'
moonphase_list = '[0, 45, 90, 135, 180, 225, 270, 315]'
photometric_system = '[AB, Vega]'
bands_AB = '[u,g,r,i,z]'
bands_Vega = '[U,B,V,R,I,J,H,K]'


input_phot_sys = input('Photometric System Options: \n'+photometric_system+'\nSystem: ')
# print(input_phot_sys)
if input_phot_sys == 'AB':
    input_phot_band = input('Photometric Band Options: \n'+bands_AB+'\nBand: ')
elif input_phot_sys == 'Vega':
    input_phot_band = input('Photometric Band Options: \n'+bands_Vega+'\nBand: ')
else:
    print('\nChoose only from the options\n')
# print(input_phot_band)

input_magnitude = input('Enter magnitude of target: ')
input_magnitude = float(input_magnitude)
# print(input_magnitude)


input_instrument = input('Instrument Options:\n'+instrument_list+'\nInstrument: ')
if input_instrument == 'DIS':
    input_channel = input('R300 or B400? (Enter R or B): ')
    


# input_filter = input('Filter Options:\n'+filter_list+'\nFilter: ')


input_StoN = input('Please enter S/N: ')
StoN = float(input_StoN)

# input_wave_range = input('Enter wavelength range as beginning,end,wave_step_size (comma-separated): ')
# input_wave_range = input_wave_range.split(',')
# input_wave_range = [float(input_wave_range[i]) for i in range(len(input_wave_range))]
# HERE IS THE WAVELENGTH RANGE WE WILL USE:
# wave_range = np.arange(input_wave_range[0], input_wave_range[1], input_wave_range[2])
input_wave_range = input('Enter desired wavelength range as a 2 element np.array: ')
w1 = eval(input_wave_range)[0]
w2 = eval(input_wave_range)[1]
wavelength = np.arange(w1,w2,.0001) #eval(input_wave_range)

if input_instrument == 'AGILE' or input_instrument == 'ARCTIC' or input_instrument == 'NICFPS':
    input_filter = input('Filter Options:\n'+filter_list+'\nFilter: ')
    # filter efficiency
    filter_eff,bandpass = filtLAM(filter_path+input_filter, wavelength)
else:
    filter_eff = 1.0
    bandpass = 1


moonphase = input('Moon-Sun Angle Options:\n'+moonphase_list+'\nMoon Phase: ')

input_airmass = input('Please enter airmass: ')
airmass = float(input_airmass)


'''
Now use the inputs to get parameters for final exposure time calculation.

There are the parameter we have:

input_instrument (string)
input_channel (string)
input_filter (string)
input_phot_sys (string)
StoN (float)
wavelength (float)
moonphase (string)
airmass (float)

'''

print('**************')
print('Starting Exposure Time Calculation')
print('**************')

#  MAIN CALLS WITH PARAMETERS:


# get efficiency of chosen instrument, at the given wavelenght:
if input_instrument == 'AGILE':
    inst_eff = getAGILE(wavelength, instrument_path+'AGILE.txt')
elif input_instrument == 'NICFPS':
    inst_eff = getNICFPS(wavelength, instrument_path+'NICFPS_Hawaii_QE.txt')
elif input_instrument == 'ARCTIC':
    inst_eff = getARCTIC(wavelength, instrument_path+'ARCTIC_CCD_QE.txt')
elif input_instrument == 'T-SPEC':
    inst_eff = getTSPEC(wavelength, instrument_path+'tspec_grating_throughput.txt', instrument_path+'tspec_everythingelse.txt')
elif input_instrument == 'ARCES':
    inst_eff = getARCES(wavelength, instrument_path+'ARCES.txt')
elif input_instrument == 'DIS':
    if input_channel == 'R':
        inst_eff = getDIS(wavelength, instrument_path+'DIS_R300.txt', instrument_path+'DIS_red_E2V-CCD42-20-1-D21.txt')
    elif input_channel == 'B':
        inst_eff = getDIS(wavelength, instrument_path+'DIS_B400.txt', instrument_path+'DIS_blue_Marconi-CCD42-20-0-310.txt')
else:
    print('\nAdhere to options, please.\n')


print('inst_eff: ', inst_eff)

# get telescope area
Tel_Collect_Area = telLam(340.0, 47.0, 0.97) # APO VALUES HARD CODED HERE... in cm^2
print('Tel_Collect_Area: ', Tel_Collect_Area)

# filter_eff got called earlier.  Only called if imager is chosen.  Otherwise set to 1.0
print('filter_eff: ', filter_eff)
print('bandpass: ',bandpass)

# background flux
back_flux = total_background_flux(moonphase_path+moonphase, airmass, wavelength)
print('back_flux: ', back_flux)

# get atmos transmission
atmos_transmission = atm_trans(wavelength, airmass, atmos_transmission_path)
print('atmos_transmission: ', atmos_transmission)


# get photon flux
phot_flux = calcPhotFlux(input_phot_sys, input_phot_band, input_magnitude)
print('phot_flux: ', phot_flux)

# GetSprime(lambda_vals, phot_flux, atm_e, tel_e, inst_e, filt_e, det_e)
S_prime = GetSprime(bandpass, phot_flux, atmos_transmission, 1.0, inst_eff, filter_eff, 1.0) # tel_e = 1.0, det_e = 1.0
print('Sprime is: ', S_prime*Tel_Collect_Area)

# GetSprime(lambda_vals, phot_flux, atm_e, tel_e, inst_e, filt_e, det_e)
B_prime = GetSprime(bandpass, back_flux, atmos_transmission, 1.0, inst_eff, filter_eff, 1.0) # tel_e = 1.0, det_e = 1.0
print('Bprime is: ', B_prime)

# Final exposure time result!
Exposure_time = calc_expT(StoN, S_prime, B_prime, 1.0, Tel_Collect_Area) # calc_expT(SN,flux,back,seeing,tel)
print()
print('Exposure time: ', Exposure_time)

plt.plot(wavelength,Exposure_time)
plt.xlabel('Wavelength(um)')
plt.ylabel('Exposure Time (s)')
plt.show()



