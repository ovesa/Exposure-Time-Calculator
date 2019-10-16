

import numpy as np
import math


# import sys
# sys.path.insert(0, 'Functions/instLam/getInstEfficiency.py')
from Functions.instLam.getInstEfficiency import *

# this formulation works: will be worked on further.
print(getAGILE(np.arange(0.5, 0.8, 0.01), 'Functions/instLam/Efficiencies/AGILE.txt'))
print()
print(getARCTIC(np.arange(0.5, 0.8, 0.01), 'Functions/instLam/Efficiencies/ARCTIC_CCD_QE.txt'))

# print(getInstEfficiency.getAGILE(0.55, 'AGILE.txt'))

# instrument_list = '[AGILE, NICFPS, ARCTIC, T-SPEC, DIS, ARCES]'
# filter_list = '[jc_U, jc_B, jc_V, jc_R, jc_I, mko_H, mko_J, mko_K, sdss_g, sdss_r, sdss_i, sdss_u, sdss_z]'

# input_instrument = input('Please choose instrument from the list:\n'+instrument_list+'\nInstrument: ')
# if input_instrument == 'DIS':
#     input_channel = input('R300 or B400? (Enter R or B): ')

# input_filter = input('Please enter filter from the list:\n'+filter_list+'\nfilter: ')

# input_StoN = input('Please enter S/N: ')
# input_StoN = float(input_StoN)

# input_wave_range = input('Enter the range of wavelength beginning, end, and resolution (comma separated): ')
# input_wave_range = input_wave_range.split(',')
# input_wave_range = [float(input_wave_range[i]) for i in range(len(input_wave_range))]

# input_airmass = input('Please enter airmass: ')
# input_airmass = float(input_airmass)

start, stop, res = 0.55, 0.60, 0.01

wave_range = np.arange(start, stop, res)
# wave_range = np.arange(input_wave_range[0], input_wave_range[1], input_wave_range[2])
