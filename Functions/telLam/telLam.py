#code to calculate telescope throughput

import numpy as np

def telLam(d_p,d_ob,R):
    
	''' calculates telescope throughput given:
	d_p = telescope primary diameter, cm
	d_p = diameter of central obstruction, cm
	R = reflectance of Aluminum
	'''
	
	r_p = d_p/2
	r_ob = d_ob/2
	A_p = np.pi * r_p**2
	A_ob = np.pi * r_ob**2

	tp = (A_p - A_ob) * (R**3) #throughput = effective collecting area * R**3, in cm^2

	return tp
