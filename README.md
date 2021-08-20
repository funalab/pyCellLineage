# pyLineage
===
Ryo J. Nakatani:nakatani@fun.bio.keio.ac.jp
Date:

## License
Copyright (c) 2021 Funahashi Lab., Keio University.
Modifications Copyright (c)

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program.
If not, see http://www.gnu.org/licenses/.

## Introduction

This software allows users to analyze ATP heterogeneity among single cell populations grown in a 2-dimensional surface using time-lapse fluorescent images.
This software allows users to do the following analyses on these images.
- Analysis of stochastic state switching using hidden markov models(HMM).
- Analysis of periodic oscillation using Gaussian Process Regression(GPR) and Fourier Transform.
- Analysis of cellular age using cellular lineages and spatial information.

Regarding previously reported programs such as Schnitzcells(Young et al. 2012), and cellular transmission analysis (van Vliet et al. 2018) they are not included in pyLineage for license purposes.
The user must download the above codes on their own.

## Installation

The software is implemented as a combination of Python and R scripts.
To use this software you must have Python 3.7.10 and R 3.4.3.
The software has been tested on Mac OS X High Sierra.

## Quick start usage
The software can be executed to generate figures and csv files used in the paper as follows.
  ```zsh
  # In terminal
  % cd /Path/To/pyLineage
  % python3 Analysis_Gui/Final\ All\ Samples\ Create\ Lineage.py  
  
  # -or on ipython-  
  
  from pyLineage.Analysis_Gui import SampleAnalysesGui
  SampleAnalysesGui.run()
  
  ```
Once the software has started to run you will need to select the following modes via GUI to generate results.
All data used to make figures is saved in a cell Data Frame that can be imported by pandas.

### GUI explanation
1. Sample Selection:
Select all samples.

2. Lineage Plots:
Allow plotting of 3d lineages and 2d lineages.
If there are no preferences in saving select show.
Select 3d for 3-dimensional lineage, defaults to 2-dimensional.

3. Data Frames:
Allow saving of constructed cell data frame.
Contains cell uIDs and relationship with other cells.
Also contains information on size, position, intensity of each individual.

4. Oscillatory Analysis:
Allows analysis for Fourier Free Transform (fft).
If data directory is prepared for use, select fft.

5. Histograms:
None are used to plot histograms used in the paper.

6. Hidden Markov Model Analysis (6,7,8th screens):
Select hmmPrep totalATP gmmPoor for results used in paper.
Select hmmPrep class 2D for plot of classified lineage.

### Cell DataFrame Explanation
|Variable Name|Contents|
|-|-|
| ID |unique ID within single image for individuals| 
| uID | unique ID within whole lineage| 
| motherID|ID of mother Cell| 
| daughter1ID| ID of one daughter cell| 
| daughter2ID| ID of other daughter cell| 
| cenX| centroid x position| 
| cenY| centroid y position| 
| Z| time frame| 
| cellNo| ID used in Schnitzcells| 
| intensity|Intensity of Individual in image| 
| area|Area of individual| 
| ATP|intracellular ATP concentration when input image is raw ratio image| 
| linIdx|ID of lineage; depends on how many cell there are in first image| 
|...|Other variables can be appended using pandas| 


## All code and how to use
***
This software can be used to create lineage of schnitzCell Data.  
The software consists of three main directories,
- LIAnalysis  
  Mainly used for analysing the lineage for cellular age and oscillation.
  It also prepares data for HMM Analysis and GPR.
  
- PDAnalysis  
  Mainly used for analysis on doubling time and cell size.

- lineageIO  
  Mainly used to create a custom Dataframe reading the schnitzcell lin.mat data.
  It can also load Ratio Imgs to calculate ATP concentration. (Look at below warnings)  
  Once the Dataframe has been created it can either plot 2D, 3D lineage renderations or create histograms of each time point.
  Visualize Lineages also makes it possible for segmented images to show tracked information.

An optional GUI is also provided,  
- Analysis_Gui  
  This is a very Simple GUI to select which Samples you would like to Analyze and allows you to select Analysis Modes.  
  To start GUI enter;  
  ```zsh
  # In terminal
  % cd /Path/To/pyLineage
  % python Analysis_Gui/Final\ All\ Samples\ Create\ Lineage.py  
  
  # -or on ipython-  
  
  from pyLineage.Analysis_Gui import SampleAnalysesGui
  SampleAnalysesGui.run()
  
  ```
  The results that are created by these analyses are saved in the directory of the sample.  
  
Warnings:  
   For Experiments Analysis_Gui uses paths that are hardcoded in pyLineage/Analysis_Gui/pathParms.py
   Also all functions depend on a certain directory structure. (See Sample Data Structure for details)

   Another point to keep in mind is that when calculating atp concentration pyLineage looks for a file named "atp_calib.csv" in the lineageIO directory. It is a simple CSV file with the below contents. Please updated the file on your own whenever you redraw the caliburation curve.  
   
   ```
   parameter,value
   Emax,4.9474
   EC50,5.8325
   d,0.6521

   ```

The first three directories are part of the pyLineage Module,  
but the util directory also contains python or zsh programs that are useful in extracting schnitzcell prepared images from raw images,  
creating an automatic initSchnitz command unique to the experiment for MatLab and also creating Ratio images from the raw images.

### About utils
arrangeFiles.sh   
Arranges files to schnitz readable directory format.

ex)
```zsh
% arrangeFiles.sh ./Pos0
```
imagesToSchnitz.py
Makes image file names to schnitz readable format.

ex)
```zsh
% imagesToSchnitz.py ./405
```

initschnitzmaker.py
Makes initial initschnitz command for Schnitzcells based on current Directory. (Directory must be schnitz readable format)

```zsh
% python initschnitzmaker.py #at directory that has been prepared for schnitz
```

CreateRatioFS.py   
Make ATP images from raw images.

## GUI
The last directory is used for GUI Analysis.

# Update Information and News
pyLineage27 has been removed from the main branch.


## requirements  
- python 3.7
- numpy : 1.15.2
- pandas : 0.23.4
- matplotlib : 2.2.3
- scipy : 1.1.0
- scikit-image : 0.14.2_1
- networkx : 2.2
- opencv : 3.4.10  

## Additional GUI
- kivy 2.0.0
