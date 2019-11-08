#code to solve for exposure time, given S/N

import numpy as np

def calc_expT(SN,flux,back,seeing,tel):

    ''' returns exposure time given inputs:
    S/N,
    photon flux from source (counts/s/cm^2/um),
    background SB (counts/s/m^2/arcsec^2),
    seeing (arcsec),
    telescope collecting area (cm^2)
    '''
    back_area = np.pi * seeing**2 #background area
    bgr = back#*(10**4) #convert background SB to units of counts/s/cm^2/arcsec^2
    #expT = (((bgr*back_area*tel) + flux)/flux**2)*SN**2 #from noise equation
    expT = ((SN/(flux*tel**.5))*(flux+back_area*bgr)**.5)**2
    return expT
