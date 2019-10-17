def atm_trans(wl,airmass, path):
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

    
    ll = min(lam[0]) #lower limit of wavelength
    ul = max(lam[0]) #upper limit of wavelength
    
    
    trans_at_wl = [] #transmission at entered wavelength(s)
    for i in interp:
        trans_at_wl.append(i(wl_nm)[0]) #might need to add [0]? weird for single value vs loops. Right now works for loops.
    
    #print(trans_at_wl)
    
    #interpolation of transmission at given wl as a function of airmass
    interp_am = interpolate.interp1d(am_on_file,trans_at_wl)
    
    #return transmission for that wavelength at that airmass
    return interp_am(airmass)
