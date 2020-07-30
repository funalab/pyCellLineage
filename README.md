# pyLineage
***
Used to create lineage of schnitzCell Data
Has three Main directories,
- LIAnalysis  
  Mainly used for analysing the lineage for cellular age and oscillation.
  It also prepares data for stochastic HMM Analysis and GPR.
  
- PDAnalysis  
  Mainly used for analysis on doubling time and cell size.

- lineageIO  
  Mainly used to create a custom Dataframe reading the schnitzcell lin.mat data.
  It can also load Ratio Imgs to calculate ATP concentration.
  Once the Dataframe has been created it can either plot 2D, 3D lineage renderations or create histograms of each time point.
  Visualize Lineages also makes it possible for segmented images to show tracked information.

An optional GUI is also provided,  
- Analysis_Gui
  Very Simple GUI to select which Samples you would like to Analyze and allows you to select Analysis Modes.  
  To start GUI enter;  
  ```zsh
  % cd /Path/To/pyLineage
  % python Analysis_Gui/Final\ All\ Samples\ Create\ Lineage.py
  ```
  The results that are created by these analyses are saved in the directory of the sample.  
  
Warnings:  
   For Experiments Analysis_Gui uses paths that are hardcoded in Analysis_Gui/Final\ All\ Samples\ Create\ Lineage.py  
   Also all functions depend on a certain directory structure. (See Sample Data Structure for details)  

The first three directories are part of the pyLineage Module,  
but the util directory also contains python or zsh programs that are useful in extracting schnitzcell prepared images from raw images,  
creating an automatic initSchnitz command unique to the experiment for MatLab and also creating Ratio images from the raw images.  

The last directory is used for GUI Analysis.  


## requirements  
- python 2.7
- numpy : 1.15.2
- pandas : 0.23.4
- matplotlib : 2.2.3
- scipy : 1.1.0
- scikit-image : 0.14.2_1
- networkx : 2.2  

## Additional requirements for GUI  
- kivy : 1.10.1_0

