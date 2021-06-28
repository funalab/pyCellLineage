# pyLineage
***
Used to create lineage of schnitzCell Data.  
Has three Main directories,
- LIAnalysis  
  Mainly used for analysing the lineage for cellular age and oscillation.
  It also prepares data for stochastic HMM Analysis and GPR.
  
- PDAnalysis  
  Mainly used for analysis on doubling time and cell size.

- lineageIO  
  Mainly used to create a custom Dataframe reading the schnitzcell lin.mat data.
  It can also load Ratio Imgs to calculate ATP concentration. (Look at below warnings)  
  Once the Dataframe has been created it can either plot 2D, 3D lineage renderations or create histograms of each time point.
  Visualize Lineages also makes it possible for segmented images to show tracked information.

An optional GUI is also provided,  
- Analysis_Gui  
  Very Simple GUI to select which Samples you would like to Analyze and allows you to select Analysis Modes.  
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
