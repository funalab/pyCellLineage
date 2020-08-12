# coding: utf-8
import numpy as np
from sklearn.mixture import GaussianMixture as gmm

def findBestBIC(data):
    f = np.ravel(data.dropna()).astype(np.float)
    f = f .reshape(-1,1)
    
    bestBIC = np.inf
    bestThr = 0
    for i in range(2,len(f)-1):
        tmpData = sorted(f)
        x1 = np.ravel(tmpData[:i]).astype(np.float)
        x2 = np.ravel(tmpData[i:]).astype(np.float)
        x1 = x1.reshape(-1,1)
        x2 = x2.reshape(-1,1)
        x1fit = gmm()
        x2fit = gmm()
        x1fit.fit(X=x1)
        x2fit.fit(X=x2)
        currBIC = (x1fit.bic(x1) + x2fit.bic(x2))
        if bestBIC > currBIC:
            bestBIC = currBIC
            bestThr = tmpData[i]
    return bestThr
