def filtLAM(filt,**kwargs):
    '''input:
    
    filt: Input filter being used as a string. Currently supports Johnson-Cousins ('jc') UBVRI, 
    Sloan Digital Sky Survey ('sdss') ugriz, and Mauna Kea Observatory JHK ('mko'). For example, 'sdss_g'.
    
    kwargs: wl_1 = float and wl_2 = float (optional). Input a wavelength of interest or a range of wavelengths in microns 
    to get the corresponding tranmission(s). If no range is input, will return entire filter transmission.
    
    output:
    
    The transmission of the filter in decimal form. Depending on inputs will return the entire filter transmission,
    the transmission in a range of wavelengths, or the transmission at a single wavelength.'''
    
    import numpy as np
    
    #extract the keyword arguments that define a wavelength range (if given)
    wl_1 = kwargs.get('wl_1')
    wl_2 = kwargs.get('wl_2')
    
    #read in the info for the selected filter. text files are two columns(wl, transmission) space delimited.
    f = open(filt+'.txt','r')
    lines = f.readlines()
    wavelength = np.array([])
    transmission = np.array([])
    for i in lines:
        wavelength = np.append(wavelength,float(i.split(' ')[0]))
        transmission = np.append(transmission,float(i.split(' ')[1]))
    
    #return the transmission in the given wl range (if given)
    if wl_1 and wl_2:
        print('Your selected wavelength range is ' + str(wl_1)+ 'um to '+str(wl_2)+'um')
        transmission_rng = transmission[np.argwhere(wavelength==wl_1)[0][0]:np.argwhere(wavelength==wl_2)[0][0]]
        return transmission_rng
    
    #return the transmission at wl_1
    elif wl_1 and not wl_2:
        print('Your selected wavelength is ' + str(wl_1)+ 'um')
        transmission_val = transmission[np.argwhere(wavelength==wl_1)]
        return transmission_val[0][0]
    
    #not needed? return the transmission at wl_2
    elif wl_2 and not wl_1:
        print('Your selected wavelength is ' + str(wl_2)+ 'um')
        transmission_val = transmission[np.argwhere(wavelength==wl_2)]
        return transmission_val[0][0]
    
    #if no range given or if wl given does not fall within filter, return entire transmission 
    else:
        print('Wavelength not in range of selected filter or no wavelength(s) selected. Returning full transmission.')
        return transmission
