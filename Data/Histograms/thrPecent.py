"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import pandas as pd
import os
import pyCellLineage as myPackage
from pyCellLineage.lineageIO.createHist import makeHistFromRawImage

thr = 3.46927206


def calcPercent():
    samples = ['Control', 'GlucosePoor']

    for SampleName in samples:
        tots = []
        root = os.path.join(os.path.dirname(myPackage.__file__),
                            'Data/Histograms', SampleName,
                            'MergedSamples(N=3)/Pos0')
        saveimgDir = os.path.join(root, 'saveimg')
        RatioFSDir = os.path.join(root, 'RatioFS')
        DF = makeHistFromRawImage(os.path.join(saveimgDir,
                                               os.listdir(saveimgDir)[0],
                                               "405/segmentation/"),
                                  RatioFSDir,
                                  atpInten=8)

        percent = len([val for val in DF if val > thr]) / len(DF)
        with open('thrPercentResult.txt', 'a') as f:
            f.write(f'{root}\n')
            f.write(f'{percent}\n')


if __name__ == "__main__":
    calcPercent()
