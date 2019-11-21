def atm_trans(wl,airmass,path):
    import numpy as np
    from astropy.io import fits
    from scipy import interpolate
    
    #put wl in an array if a single value is entered
    
    if type(wl) is float or type(wl) is int or type(wl) is list:
        wl = np.array([wl])
    
    #convert wl (entered in um) to nm since that's what the tranmission files use
    wl_nm = wl*1000
    
    #airmasses that we have transmissions at
    am_on_file = [1,1.5,2,2.5,3]
    trans = []
    lam = []
    interp = []
    for i in am_on_file:
        skytable = fits.open(path+'skytable_0_'+str(i)+'.fits') #open skytable fits file
        hdu = skytable[1].data #extract data
        trans.append(hdu['trans_ma']) #extract atmospheric transmission
        lam.append(hdu['lam']) #extract wavelength
        
        #create an interpolation at each airmass in case entered wavlength not contained in file
        interp.append(interpolate.interp1d(hdu['lam'],hdu['trans_ma']))

    trans_at_wl = [] #transmission at entered wavelength(s)
    #loop over wavelengths and interpolate the transmission (currently only takes one wl, so some uneccessary code still exists here)
    for j in wl_nm:
        holder = []
        for i in interp:
            holder.append(i(j))
        trans_at_wl.append(holder)
    
    #create interpolation of transmission at given wl as a function of airmass
    interp_am = []
    for i in trans_at_wl:
        interp_am.append(interpolate.interp1d(am_on_file,i))
    
    #get interpd transmission at one wl given an airmass
    trans_at_wl_am = []
    for i in np.arange(0,len(interp_am)):
        trans_at_wl_am.append(interp_am[i](airmass))
        
    #return transmission for that wavelength at that airmass
    return np.array(trans_at_wl_am)
