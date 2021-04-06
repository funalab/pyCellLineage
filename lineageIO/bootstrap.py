import numpy as np
from scipy.stats import skew


def bootstrap(data,itr=100000):
    data = data.dropna()
    orgSkew = data.skew()
    mean = float(data.mean())
    std = float(data.std())
    leng = len(data)
    skewList = list()
    for i in range(itr):
        #print mean,std,leng
        tmpData = np.random.normal(mean,std,leng)
        skewList.append(skew(tmpData))

    p = float(sum(i > orgSkew for i in skewList)) / float(itr)
    return p
