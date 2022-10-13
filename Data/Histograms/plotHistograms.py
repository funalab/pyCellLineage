"""
Author: Joel Nakatani
Overview:

Parameters:
"""

 from pyCellLineage.lineageIO import createHist
 import pyCellLineage as myPackage


def plotHists():
    samples = ['ATP',  'Control',  'GlucosePoor',  'Glycerol',  'Supernatant']

    for SampleName in samples:
        root = os.path.join(os.path.dirname(myPackage.__file__),'Data/Histograms',SampleName,'MergedSamples(N=3)/Pos0')
        saveimgDir = os.path.join(root,'saveimg')
        RatioFSDir = os.path.join(root,'RatioFS')
        createHist.makeHistFromRawImage(os.path.join(saveimgDir,os.listdir(saveimgDir)[0],"405/segmentation/"),RatioFSDir,atpInten=8)



if __name__ == "__main__":
    plotHists()
