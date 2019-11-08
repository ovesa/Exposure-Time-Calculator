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
	back_area = np.pi * seeing**2.0 #background area
	bgr = back * 1e4 #convert background SB to units of counts/s/cm^2/A/arcsec^2
	# expT = (((bgr*back_area*tel) + flux)/flux**2.0)*(SN**2.0) #from noise equation
	expT = ((bgr*back_area + flux) / (flux**2)) * (SN**2) / tel
	return expT
