import numpy as np
import os
import pandas as pd


def nineFivePercentile(cellDFWP,attr='ATP'):
    dataset = np.array(cellDFWP[attr].dropna())
    return np.percentile(dataset,95)
