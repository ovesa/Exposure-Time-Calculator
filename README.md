# Exposure Time Calculator

ETC Project


#### We’ll add any and all notes regarding the architecture here ####

Each little function is currently a directory because I don’t know how much baggage each thing will have.  Some will probably require deeper layers to structure things clearly but here is a basic outline.

Directory Structure (preliminary):

ETC (parent):
	
	README.txt (this document)
	
	>Functions	(subdirectories for functions)
		
		>atmLam	(atmospheric conditions at observation time) (Oana)
		
		>calcFlam	(calc the flux from an input mag/ return input spec on required wavelength grid)
		
		>detLam	(info about the detector for a given instrument) (Annie)
		
		>getColA	(given an observatory and telescope, returns collecting area) (Annie)
		
		>instLam	(info about throughput of instrument) (Ali)
		
		>instOverLam	(integrate count equation) (Kelly)
		
		>solveForExp	(get the S/N and exposure time)
		
		>telLam	(info about throughput of telescope)
		
		>filtLam	(info about throughput of filter) (Matt)