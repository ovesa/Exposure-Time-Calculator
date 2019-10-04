#code to calculate telescope throughput

import numpy as np

def telLam(d_p,d_ob,R):
	''' calculates telescope throughput given:
	d_p = telescope primary diameter, meters
	d_p = diameter of central obstruction, meters
	R = reflectance (of Aluminum)
	'''
	R_p = d_p/2
	R_ob = d_ob/2
	A_p = np.pi * R_p**2
	A_ob = np.pi * R_ob**2

	tp = (A_p - A_ob) * (R**3) #throughput = effective collecting area * R**3

	return tp


# print(telLam(3.5,0.3,0.97))