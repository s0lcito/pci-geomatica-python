# pci-geomatica-python

This repository contains scripts utilizing PCI Geomatics libraries for satellite imagery processing. These projects demonstrate practical applications of atmospheric correction, mosaicking, clipping, and other remote sensing techniques.

## Scripts Overview

### 1. **Kyushu, Japan**
**Purpose**: Automate the mosaicking, atmospheric correction, and color balancing of multiple Landsat 8 scenes for the Kyushu region.  
**Key Features**:  
- Haze removal and atmospheric correction.
- Mosaic generation.
- Exporting cutlines for visualization.  

**Data Requirements**:  
- Download the following Landsat 8 scenes:
  - `LC81130382020226LGN00`
  - `LC81130372020242LGN00`
  - `LC81120382020219LGN00`
  - `LC81120372019216LGN00`

### 2. **Montreal, Canada**
**Purpose**: Clip a Landsat 8 scene to the boundaries of Montreal Island and perform principal component analysis (PCA).  
**Key Features**:  
- Clipping satellite imagery to a specified shapefile.
- Adding new channels to clipped images.
- Generating PCA components for analysis.  

**Data Requirements**:  
- Download the following Landsat 8 scene: `LC80150282021293LGN00`
- Montreal Island Borders shapefile: [Download Here](https://donnees.montreal.ca/ville-de-montreal/limites-terrestres)

## Prerequisites
- **Software**:  
  - PCI Geomatica with Python API.  
- **Libraries**:  
  - Standard PCI libraries (e.g., `pci.masking`, `pci.hazerem`, `pci.clip`).
- **System**:  
  - Scripts tested on Windows OS.

## Disclaimer
These scripts are for educational purposes and were developed as part of coursework for REMS 6023. For professional use, please ensure compliance with licensing requirements and verify the accuracy of results.


