"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import os
import sys
import cv2 as cv
from pyCellLineage.lineageIO.atpCalib import atpCalib
import numpy as np
import pandas as pd
import glob
import pyCellLineage.lineageIO as myPackage

def createRatioFS(path,atp_path=None,raw=False):
    if atp_path == None:
        atp_path = os.path.join(os.path.dirname(myPackage.__file__),"atp_calib.csv")

    atp_df = pd.read_csv(atp_path)
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
        dirLen = len(glob.glob(os.path.join(baseDir,'*')))
        for i in range(dirLen):
            fname = "img_"+str(i).zfill(9)+"_"+basename+"_000.tif"
            imgfile = os.path.join(path ,basename,fname)
            if os.path.isfile(imgfile):
                tmpImg = cv.imread(imgfile,cv.IMREAD_GRAYSCALE).astype(np.float32)
                Imgs[basename].append(tmpImg)
    for i in range(dirLen):
        Imgs['Ratio'].append(np.divide(Imgs['405'][i],Imgs['488'][i]))
    counter = 0
    for img in Imgs['Ratio']:
        fname = "405-g-"+str(counter).zfill(3)+".tif"
        print("Doing image " + fname + " in RatioFS\n")
        atpImg = np.zeros(img.shape)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                tmp = atpCalib(img[i,j],emax=emax,d=d,EC50=EC50)
                if np.isnan(tmp) or np.isinf(tmp):
                    atpImg[i,j] = 0
                    img[i,j] = 0
                else:
                     atpImg[i,j] = tmp
                                        
                    
        atpImg = atpImg.astype(np.float32)
        savePath =os.path.join(saveDir,fname)
        if not raw:
            cv.imwrite(savePath,atpImg)
        else:
            cv.imwrite(savePath,img)
        counter = counter + 1


if __name__ == "__main__":
    for path in sys.argv:
        if os.path.isdir(path):
            createRatioFS(path)
