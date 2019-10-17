
# coding: utf-8

# In[1]:


from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate


# In[257]:


def atm_trans(wl,airmass):
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
        skytable = fits.open('skytable_0_'+str(i)+'.fits') #open skytable fits file
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
    return trans_at_wl_am[0]


# In[258]:


test = atm_trans(1.4,2)
test*2


# In[218]:


wl = [.4]
for i in wl:
    print(atm_trans(i,2))
    


# In[76]:


hdu_main = fits.open('skytable_0_1.5.fits')
header = hdu_main[1].header
hdu = hdu_main[1].data
#header = hdu[0].header
atm_trans = hdu['trans_ma']
#am = header['comment skymodel.target.airmass']


# In[73]:


plt.plot(hdu['lam'],atm_trans)
#plt.xlim(13000,20000)
plt.show()


# In[77]:


for i in range(len(header['COMMENT'])):
    if 'AIRMASS' in header['COMMENT'][i]:
        print(header['COMMENT'][i],i)


# In[43]:


header['COMMENT'][37]


# In[58]:


a = hdu_main[0].data


# In[272]:


atm_trans(.3,2)


# In[80]:


hdu['lam'][0:100]


# In[143]:


a = np.array([1])


# In[147]:


if a.any() > 1:
    print('hi')


# In[226]:


am_floats = [1.0,1.5,2.0,2.5,3.0]
b = [4,5,6,7,8]
interpolate.interp1d(a,b)


# In[234]:


taw


# In[165]:


a = [1,2,3]
b = np.array([4,5,6])


# In[43]:


a = np.array(a)


# In[44]:


a


# In[167]:


b

