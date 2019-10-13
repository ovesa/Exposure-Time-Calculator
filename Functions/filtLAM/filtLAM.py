def filtLAM(filt,wl):
    '''Input:
    
        filt: Input filter being used as a string. Currently supports Johnson-Cousins ('jc') UBVRI, 
        Sloan Digital Sky Survey ('sdss') ugriz, and Mauna Kea Observatory JHK ('mko'). For example, 'jc_U', sdss_g',
        or 'mko_J' would all be valid inputs.
        
        wl: Wavelength(s) of interest in microns. Can input a single value or an array.
    
    Output:
    
        The transmission of the filter as a percentage at the given wavelength(s)'''
    
    import numpy as np
    from scipy import interpolate
    
    #read in the info for the selected filter. text files are two columns(wl, transmission) space delimited.
    f = open(filt+'.txt','r')
    lines = f.readlines()
    wavelength = np.array([])
    transmission = np.array([])
    for i in lines:
        wavelength = np.append(wavelength,float(i.split(' ')[0]))
        transmission = np.append(transmission,float(i.split(' ')[1]))
        
    ll = min(wavelength) #lower limit of wavelength for this filter
    ul = max(wavelength) #upper limit of wavelength for this filter
    
    #interpolation function if a given wl is not defined in the text files
    interp = interpolate.interp1d(wavelength,transmission)
    
    if type(wl) is float or type(wl) is int:
        wl = np.array([wl])
        
    #check that entered wavelengths fall within filter range
    if wl.any() < ll and wl.any() > ul:
            print('Error: one of your entered wavelengths is outside of the filter range.')
            print('Transmission data for '+ filt + ' exists from ' + str(ll) + 'um to ' + str(ul)+'um')
            
    #if all wavelengths check out ok, continue to transmission extraction
    else:
        print('Your selected wavelength range is ' + str(min(wl))+ 'um to '+str(max(wl))+'um')
        
        trans_vals = np.array([]) #empty array for transmission values to be returned
        
        #loop through entered wavelengths
        for i in np.arange(0,len(wl)):
            
            #check if entered wavelengths are an exact match to those already in the transmission files
            try:
                tv = transmission[np.argwhere(wavelength==wl[i])]
                trans_vals = np.append(trans_vals,tv[0][0])
            
            #if they are not an exact match, use the interpolation function to estimate a transmission at that wavelength
            except(IndexError):
                #print(str(wl[i]) + ' is not explicitly defined in the filter curve. Using interpolation.')
                new_trans = interp(wl[i]) #plug in to interpolation function
                trans_vals = np.append(trans_vals,new_trans)
        return trans_vals
