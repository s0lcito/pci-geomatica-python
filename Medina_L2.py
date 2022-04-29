####################################################################
## Purpose: Automati mosaicking, atmospheric correction and color ##
##          balancing of multiple satellite imagery. Here we will ##
##          be working with LandSat8 Imagery of Kyushu, Japan.    ##
## Author: s0lcito                                                ##
## Date: February 2nd 2022                                        ##
## Disclaimer: This code is for educational purposes only.        ##
####################################################################

# IMPORTING LIBRARIES 
import os
import fnmatch
import time
import pci
from pci.fimport import fimport
from pci.exceptions import *
from pci.masking import masking
from pci.hazerem import hazerem
from pci.mosprep import mosprep
from pci.mosrun import mosrun
from pci.pansharp import pansharp
from pci.atcor import atcor
from pci.pcimod import pcimod
from pci.mosdef import mosdef
from pci.mosrun import mosrun
from pci.fexport import fexport



# SETTING WORKING DIRECTORY
## This is where the imagery is located
working_dir = r'C:\Medina_L2'

## Main output directory with sub folders
output_dir = r'C:\Medina_L2\output'

## Haze removal output folder
haze_dir = r'C:\Medina_L2\output\haze_removal'

## Atmospheric correction output folder
atm_dir = r'C:\Medina_L2\output\atm_correction'

## Mosaic output folder
mosaic_dir = r'C:\Medina_L2\output\mosaic'

## Final Shapefile output folder
final_dir = r'C:\Medina_L2\output\mosaic\final'

## If any of the previous folder does not exist, 
##  the following will create any missing folder:
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
    
if not os.path.isdir(haze_dir):
    os.mkdir(haze_dir)
    
if not os.path.isdir(atm_dir):
    os.mkdir(atm_dir)
    
if not os.path.isdir(mosaic_dir):
    os.mkdir(mosaic_dir)
    
if not os.path.isdir(final_dir):
    os.mkdir(final_dir)

## Letting the user know the working directories for the code
print ("Working directory:", working_dir)
print ("Output directory: ", output_dir)


# SETTING SATELLITE IMAGERY PATH
start = time.time()

## Empty list created to store the pathnames of _MTL.txt files
input_files = []

## Retrieving the pathname of each _MTL.txt file with for loop
### 3 variables: r = main directory, d = .tar folder and f = _MTL.txt file
for r, d, f in os.walk(working_dir):
    for inFile in fnmatch.filter(f, '*_MTL.txt'):
        input_files.append(os.path.join(r, inFile))

# FOR LOOP: HAZE REMOVAL AND ATMOSPHERIC CORRECTION
print ("\n Starting Haze Removal and Atmospheric Correction")

for image in input_files:
    print(f"\n Now treating: {os.path.basename(image)} ({input_files.index(image)+1}/{len(input_files)})")
    
# HAZE REMOVAL
    ## Two input files
    ms_image = os.path.join('-'.join([image, 'MS']))
    pan_image = os.path.join('-'.join([image, 'PAN']))
    
    ## Four output files
    masks = os.path.join(haze_dir, '_MASK.'.join([os.path.basename(image).split('_MTL')[0], 'pix']))
    haze_ms = os.path.join(haze_dir, '_HAZE_MS..'.join([os.path.basename(image).split('_MTL')[0], 'pix']))
    haze_pan = os.path.join(haze_dir, '_HAZE_PAN.'.join([os.path.basename(image).split('_MTL')[0], 'pix']))

    ## Create cloud, water and haze masks
    masking(fili=ms_image,
            hazecov=[70],
            clthresh=[18,22,1],
            filo=masks)
        
    ## Remove the haze from both the multispectral and panchromatic bands
    hazerem(fili=ms_image,
            fili_pan=pan_image,
            maskfili=masks,
            hazecov=[70],
            filo=haze_ms,
            filo_pan=haze_pan)
    
# ATMOSPHERIC CORRECTION
    ## Output file in atm_dir
    atcor_ms = os.path.join(atm_dir, '_ATM.'.join([os.path.basename(image).split('_MTL')[0], 'pix']))

    ## Atmospheric correction for pansharpened multispectral image.
    atcor(fili=haze_ms, maskfili=masks, filo=atcor_ms)
    
# SELECTING DESIRED BANDS (COMPOSITE 562)
    ## Pix file with atmospheric corrections used
    pix_file = atcor_ms
    
    ## Specifying channels to delete
    channels = [1, 3, 4, 7, 8]
    
    ## Deleting channels from pix_file 
    pcimod(file=pix_file, pciop="DEL", pcival=channels)

# MOSAICKING 
print ("\n Creating Mosaic")

# Using corrected files in atm_dir
corrected = atm_dir
src_img_file = os.path.join(mosaic_dir, "mosaic.mos")

# Create Mosaic Definition XML file to
mosdef_file = os.path.join(mosaic_dir, "mosdef.xml")

## Mosaic Preparation
mosprep(mfile=corrected, silfile=src_img_file)
mosdef(silfile=src_img_file, mdfile=mosdef_file, dbic=[2,3,1])

# Create full resolution mosaic
mosrun(silfile=src_img_file, mdfile=mosdef_file, outdir=final_dir)

end = time.time()    
print (f"\n Mosaic Completed")

# EXPORTING CUTLINES
## Input files
pix_file = os.path.join(mosaic_dir,"mosaic\misc\mosaic_cutline_topology.pix")

shp_file = os.path.join(final_dir, "cutline.shp")

## Exporting cutlines as shapefile into ...\mosaic\final folder
fexport(fili=pix_file, filo=shp_file, dbvs=[2], ftype="shp")
    
# END OF THE PROGRAM
end = time.time()
print (f"\n Program Completed in {end-start} seconds")
print ("\n End of the Program")
