"""
Author: Joel Nakatani
Overview:

Parameters:
"""

import pyCellLineage as myPackage
import os
import pandas as pd
import matplotlib.pyplot as plt


def plotGCMS():
    root = os.path.join(os.path.dirname(myPackage.__file__),'Data/GC:MS')
    resultDF = pd.read_csv(os.path.join(root,'result.csv'),index_col=0)
    resultDF = resultDF.fillna(0)
    for chemical in resultDF.index.values:
        plt.cla()
        plt.clf()
        tmp = resultDF.loc[chemical]
        plt.bar(tmp.keys(),tmp.values)
        plt.title(chemical)
        plt.savefig(os.path.join(root,chemical+'.pdf'))


if __name__ == "__main__":
    plotGCMS()
