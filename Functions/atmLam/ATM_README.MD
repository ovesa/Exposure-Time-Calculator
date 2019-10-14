The sky tables are in a .npz format which is a numpy zipped dictionary-like archive. Each one corresponds to a different moon phase, 
and within each .npz file, there are different fluxes depending on the airmass desired. This module is comprised of
4 different functions (load_flux, air_mass_to_flux, cal_bg_photon, and total_background_flux). The total_background_flux function
is the main functions that calls the other three and computes the total background photon flux in units of ph/s/m^2/micron/arcsec^2. 
It requires an user input of wavelength, airmass, and moon phase. The wavelength range is 300-1200 nm, the airmass range is between 1 and 3 
(corresponds to what airmasses were available from ESO Sky Calculator), and the moon phase input can either be the initials of the
moon phase desired or the Sun-Moon separation angle.

For instance,the numbers correspond to the Sun-Moon separation angle
0 = New Moon (NM)
45 = Waxing Crescent (WxC)
90 = First Quarter (FQ)
135 = Waxing Gibbous (WxG)
180 =Full Moon (FM)
225 = Waning Gibbous (WnG)
270 = Third Quarter (TQ)
315 = Waning Crescent (WnC)
With these, the background photon flux needs to be calculated.