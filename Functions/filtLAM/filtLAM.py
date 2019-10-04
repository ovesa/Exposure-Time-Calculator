def filtLAM(filt,**kwargs):
    import numpy as np
    '''filt: Input filter being used as a string. Currently supports Johnson-Cousins ('jc') UBVRI, 
    Sloan Digital Sky Survey ('sdss') ugriz, and Mauna Kea Observatory JHK ('mko'). For example, 'sdss_g'.
    
    kwargs: wl_1 = float and wl_2 = float (optional). Input a wavelength of interest or a range of wavelengths in microns 
    to get the corresponding tranmission(s). If no range is input, will return entire filter transmission.'''
    
    global wavelength,transmission,transmission_rng
    
    #extract the keyword arguments that define a wavelength range (if given)
    wl_1 = kwargs.get('wl_1')
    wl_2 = kwargs.get('wl_2')
    
    #read in the info for the selected filter
    f = open(filt+'.txt','r')
    lines = f.readlines()
    wavelength = np.array([])
    transmission = np.array([])
    for i in lines:
        wavelength = np.append(wavelength,float(i.split(' ')[0]))
        transmission = np.append(transmission2,float(i.split(' ')[1]))
    
    try:
        #return the transmission in the given wl range (if given)
        if wl_1 == True and wl_2 == True:
            transmission_rng = transmission[np.argwhere(wavelength==wl_1)[0][0]:np.argwhere(wavelength==wl_2)[0][0]]
            return transmission_rng
    
    except(NameError,IndexError):
        #if no range given or if wl given does not fall within filter, return entire transmission
        print('Wavelength not in range of selected filter or no range selected. Returning full transmission.')
        return transmission
