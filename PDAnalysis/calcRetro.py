"""
Author: Joel Nakatani
Overview:

Parameters:
"""

from ..lineageIO.getIndependentLineage import getIndependentLineage
from .calcGEL import constructTimeRef
import numpy as np


class RetrospectiveSampling():
    CellDF = object()  # Cellular DF
    indiLineage = list()  # List of Indepedent Lineages
    ForwardDist = list()  # Forward Distribution
    BackwardDist = list()  # Backward Distribution
    diviList = list()  # List of number of Divisions
    minT = int()

    m = 2  # number of offspring

    def __init__(self, CellDF, T=None, timeRef=None):
        self.CellDF = CellDF
        self.indiLineage = getIndependentLineage(CellDF, mode='parallel')

        if T is None:
            self.minT = self.getMinT(self.CellDF)
        else:
            self.minT = T
        self.diviList = self.countDivi(self.CellDF, timeRef)

    def countDivi(self, CellDF, timeRef=None):
        # Transform to cutoff lin
        j = 0

        if self.indiLineage is not list():
            # typical analysis will fall here
            diviList = list()

            for lin in self.indiLineage:
                linSlice = lin.iloc[:self.minT]

                if len(linSlice) == self.minT:
                    diviList.append(
                        len(linSlice[(linSlice['daughter2ID'] == -3)
                                     | (linSlice['daughter2ID'] > 0)]) - 1)
        else:
            if timeRef == None:
                timeRef = constructTimeRef(CellDF)
            tmp = [[] for i in range(len(timeRef))]

            for lin in timeRef:
                timeTot = 0
                i = 0

                while timeTot < self.minT and i < len(timeRef[j]):
                    timeTot += timeRef[j][i]
                    # This has room for bugs because the timeRef skips the time it took for the first division
                    tmp[j].append(timeRef[j][i])
                    i += 1
                j += 1
                diviList = [len(lin) - 1 for lin in tmp]

        return diviList

    def getMinT(self, CellDF):
        if self.indiLineage is list():
            lins = getIndependentLineage(CellDF)
        else:
            lins = self.indiLineage
        minVal = np.min([len(lin) for lin in lins])

        return minVal

    def getMaxT(self, CellDF):
        if self.indiLineage is list():
            lins = getIndependentLineage(CellDF)
        else:
            lins = self.indiLineage
        maxVal = np.max([len(lin) for lin in lins])

        return maxVal

    def calculate(self, mode=None, timeRef=None):
        if mode == None:
            attrs = self.diviList
        elif mode == 'reCount':
            attrs = self.countDivi(self.CellDF, timeRef)
        attrs = [i for i in attrs if i > 0]  ## remove 0

        if len(attrs) > 0:
            tau_mean = np.mean([self.minT / k for k in attrs])
            vals_div, bins_div = np.histogram(
                attrs,
                bins=np.arange(np.min(attrs),
                               np.max(attrs) + 1.5) - 0.5,
                density=True)

            self.ForwardDist = self.forwardSampling(vals_div, bins_div)
            self.BackwardDist = attrs

            two_to_div = [self.m**k for k in attrs]

            GrowthRate = np.log(np.mean(two_to_div)) / self.minT
            # Arthur's code does not consider the last value in the two_to_div array; tis a bug

        else:
            GrowthRate = float('Inf')

        return GrowthRate

    def forwardSampling(self, vals_div, bins_div):
        # Distribution weighted by m^K
        vals_div_dom = [
            vals_div[i] * np.exp(bins_div[i] * np.log(self.m))
            for i in range(len(vals_div))
        ]

        # Normalization of this 'distrib'
        surf = 0

        for i in range(len(vals_div_dom)):
            surf += vals_div_dom[i]

        vals_div_dom_norm = [x / surf for x in vals_div_dom]

        return vals_div_dom_norm


def calcRetro(CellDF):
    lineage = RetrospectiveSampling(CellDF)

    return lineage.calculate()


if __name__ == "__main__":
    import pyCellLineage.lineageIO.annotateLineageIdx as annt
    CellDF = annt.annotateLineageIdx(
        tanauchi=
        '/Users/ryonakatani/LAB/labrot/BCU/lineageData/Tanauchi/MC4100_37C/')
    print(calcRetro(CellDF))
