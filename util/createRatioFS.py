"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import os
import sys
import cv2 as cv
from pyLineage.lineageIO.atpCalib import atpCalib
import numpy as np
import pandas as pd

def createRatioFS(path):
    atp_df = pd.read_csv("/Users/nakatani/git/pyLineage/lineageIO/atp_calib.csv")
    emax = float(atp_df[atp_df['parameter'] == 'Emax']['value'])
    d = float(atp_df[atp_df['parameter'] == 'd']['value'])
    EC50 = float(atp_df[atp_df['parameter'] == 'EC50']['value'])

    saveDir = os.path.join(path,"RatioFS")
    if not os.path.isdir(saveDir):
            os.mkdir(saveDir)

    Imgs405 = list()
    Imgs488 = list()
    ImgsRatio = list()
    
    Imgs ={
        '405':Imgs405,
        '488':Imgs488,
        'Ratio':ImgsRatio
    }

    basenames=['405','488']
    for basename in basenames:
        baseDir = os.path.join(path, basename)
        dirLen = len(os.listdir(baseDir))
        for i in range(dirLen):
            fname = "img_"+str(i).zfill(9)+"_"+basename+"_000.tif"
            imgfile = os.path.join(path ,basename,fname)
            if os.path.isfile(imgfile):
                tmpImg = cv.imread(imgfile,cv.IMREAD_GRAYSCALE).astype(np.float32)
                Imgs[basename].append(tmpImg)
            
    for i in range(dirLen):
        Imgs['Ratio'].append(Imgs['405'][i] / Imgs['488'][i])
        
        counter=0
        for img in Imgs['Ratio']:
            fname = "405-g-"+str(counter).zfill(3)+".tif"
            atpImg = np.zeros(img.shape)
            for i in range(img.shape[0]):
                for j in range(img.shape[1]):
                    if not pd.isna(img[i,j]):
                        atpImg[i,j] = atpCalib(img[i,j],emax=emax,d=d,EC50=EC50)
                    else:
                        atpImg[i,j] = 0

            atpImg = atpImg.astype(np.float32)
            savePath =os.path.join(saveDir,fname)
            cv.imwrite(savePath,atpImg)
            counter = counter + 1


if __name__ == "__main__":
    for path in sys.argv:
        if os.path.isdir(path):
            createRatioFS(path)