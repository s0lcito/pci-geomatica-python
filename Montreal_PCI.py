####################################################################
## Purpose: Clipping a Landsat 8 Imagery of to a shapefile of the ##
##           extent of Montreal.                                  ##
## Author: s0lcito                                                ##
## Date: March 2nd 2022                                           ##
## Disclaimer: This code is for educational purposes only.        ##
####################################################################

# IMPORTING LIBRARIES 
import os
import pci
from pci.exceptions import *
from pci.fexport import fexport # to export the files
from pci.clip import * # used for the clip function
from pci.pcimod import pcimod # used to add the channels 
from pci.pca import pca # used for the principal component analysis
from pci.nspio import * # used for the report


# SETTING WORKING DIRECTORY
## This is where the imagery is located
working_dir = r'D:\MontrealQC'

## Final Shapefile output folder
output_dir = r'D:\MontrealQC\output'

## If any of the previous folder does not exist, 
##  the following will create any missing folder:
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

## Letting the user know the working directories for the code
print ('Working directory: ', working_dir)
print ('Output directory: ', output_dir)

# CLIPPING THE LANDSAT 8 IMAGERY TO THE MONTREAL SHAPEFILE
fili = r'D:\MontrealQC\LC08_L1TP_015028_20211020_20211026_01_T1.tar\LC08_L1TP_015028_20211020_20211026_01_T1_MTL.txt-MS'
dbic= [1,2,3,4,5,6,7]
dbsl = []
sltype = 'VEC'
filo = r'D:\MontrealQC\output\Montreal.pix'
ftype = 'PIX'
foptions = ''
clipmeth = 'LAYERVEC'
clipfil = r'D:\MontrealQC\Montreal\terre_shp.shp'
cliplay = [1]
laybnds = 'SHAPES'
coordtyp = ''
clipul = ''
cliplr = ''
clipwh = ''
initvalu = [0]
setnodat = 'Y'
oclipbdy = 'Y'
     
clip (fili, dbic, dbsl, sltype, filo, ftype, foptions, clipmeth, clipfil, cliplay, laybnds, coordtyp, clipul, cliplr, clipwh, initvalu, setnodat, oclipbdy )

# ADDING NEW CHANNELS TO THE CLIPPED PIX FILE 
clip_file = os.path.join(output_dir,'Montreal.pix')
channels = [0,0,3,0]

pcimod(file=clip_file, pciop="ADD", pcival=channels)

# PCA
## Setting up Report file
rep_file = r'D:\MontrealQC\output\report.txt'

## Opening the text file
try:
    Report.clear()
    enableDefaultReport(rep_file)
    
    ## Running the PCA function
    file = os.path.join(output_dir,'Montreal.pix') # clipped imagery
    dbic = [1,2,3,4,5,6,7] # bands used in the pca
    eign =	[1,2,3]	# eigenchannels retained for output
    dboc =	[8,9,10]	# output to channel 6,7,8
    midpoint =	[]	# no midpoint
    devrange =	[]	# 3 standard deviations
    mask =	[]	# force full sampling
    rtype =	'LONG'	# type of the report 

    pca( file, dbic, eign, dboc, midpoint, devrange, mask, rtype )

    rep_file = r'D:\output\report.txt' # points to the report file you want to write the report info to

# Closing the text file
finally:
    enableDefaultReport('term')
   
# END OF THE PROGRAM
print ('\n End of the Program')
