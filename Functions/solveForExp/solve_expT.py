#code to solve for exposure time, given S/N

import numpy as np

def calc_expT(SN,flux,back,seeing,tel):

	''' returns exposure time given inputs:
		S/N, 
		photon flux from source (counts/s/cm^2/A), 
		background SB (counts/s/m^2/micron/arcsec^2), 
		seeing (arcsec),
		telescope collecting area (cm^2)
	'''
	back_area = np.pi * seeing**2 #background area
	bgr = back*1e8 #convert background SB to units of counts/s/cm^2/A/arcsec^2
	count = flux * 1e4
	expT = (((bgr*back_area*tel) + count)/count**2)*(SN**2) #from noise equation
	return expT
