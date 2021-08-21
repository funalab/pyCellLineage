# coding: utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import linear_model

import statistics
import os
import pyLineage as myPackage


modes = ['last']
conds = ['glc_rich', 'glc_poor']
root = os.path.join(os.path.dirname(myPackage.__file__),"Data")
setlimFreq = 250
setlimAmp = 25
atpmax = 10
thr = {
    "glc_poor":{
        "sample1":3.46927206,
        "sample2":3.46927206,
        "sample3":3.46927206,
    },
    "glc_rich":{
        "sample1":3.46927206,
        "sample2":3.46927206,
        "sample3":3.46927206,
    }
}

allAmps = {}
allFreqs = {}
allCAmps = {}
allCfreqs = {}

for cond in conds:
    sampleDFs = {}
    sampleDFs2 = {}
    for i in range(1,4):
        dfPath = os.path.join(root,cond,"sample"+str(i),"atpAmp.csv")
        dfPath2 = os.path.join(root,cond,"sample"+str(i),"atpFreq.csv")
        print(dfPath)
        if os.path.isfile(dfPath) and os.path.isfile(dfPath2):
            print(dfPath)
            sampleDFs["sample"+str(i)] = pd.read_csv(dfPath)
            
            sampleDFs2["sample"+str(i)] = pd.read_csv(dfPath2)
    allAmps[cond] = sampleDFs        
    allFreqs[cond] = sampleDFs2



for mode in modes:        
    for cond in conds:
        condAmp = None
        tmp = allAmps[cond]
        atpClass = []
        for sample in sorted(tmp.keys()):
            if sample == 'sample1':
                condAmp = tmp[sample].copy()
            else:
                condAmp = pd.concat([condAmp,tmp[sample]])
            for atp in tmp[sample][mode+'ATP']:
                if atp >= thr[cond]["sample"+str(i)]:
                    name = "high"
                else:
                    name = "low"
                atpClass.append(name)

        condAmp['ClassATP'] = atpClass
        maxmed = abs(condAmp['maxATP']-condAmp['medianATP'])
        minmed = abs(condAmp['minATP']-condAmp['medianATP'])
        condAmp['diffATP'] = pd.DataFrame(np.where(maxmed > minmed, maxmed, minmed))
        print ([maxmed,minmed,condAmp[mode+'ATP']])
    
    
        condFreq = None
        tmp = allFreqs[cond]
        for sample in sorted(tmp.keys()):
            if sample == 'sample1':
                condFreq = tmp[sample].copy()
            else:
                condFreq = pd.concat([condFreq,tmp[sample]])
        condFreq['diffATP'] = condAmp[mode+'ATP']
        condFreq['ClassATP'] = condAmp['ClassATP']
                
        #plt.scatter(condAmp['ClassATP'],condAmp['maxAmp'])
        plt.boxplot([condAmp[condAmp['ClassATP'] == "high"]['maxAmp'],condAmp[condAmp['ClassATP']=="low"]['maxAmp']],labels=['high','low'])
        r,pvalue = stats.mannwhitneyu(condAmp[condAmp['ClassATP'] == "high"]['maxAmp'],condAmp[condAmp['ClassATP']=="low"]['maxAmp'],alternative='two-sided')
        plt.title(cond+" p: "+str(pvalue))
        plt.ylim((0,setlimAmp))
        plt.xlabel('ATP Class')
        plt.ylabel('Maximum Amplitude')
        plt.savefig(os.path.join(root,'Total',cond+"_"+mode+"ClassAmp.pdf"))
        plt.show()
        
        #plt.scatter(condFreq['ClassATP'],condFreq['maxFreq'])
        plt.boxplot([condFreq[condFreq['ClassATP'] == "high"]['maxFreq'],condFreq[condFreq['ClassATP']=="low"]['maxFreq']],labels=['high','low'])
        r,pvalue = stats.mannwhitneyu(condFreq[condFreq['ClassATP'] == "high"]['maxFreq'],condFreq[condFreq['ClassATP']=="low"]['maxFreq'],alternative='two-sided')
        plt.title(cond+" p: "+str(pvalue))
        plt.ylim((0,setlimFreq))
        plt.xlabel('ATP Class')
        plt.ylabel('Maximum Frequency')

        plt.savefig(os.path.join(root,'Total',cond+"_"+mode+"ClassFreq.pdf"))
        plt.show()

