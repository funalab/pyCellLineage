import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import pyLineage as myPackage

root = os.path.join(os.path.dirname(myPackage.__file__),"Data")

# coding: utf-8
conds = ['glc_rich', 'glc_poor']

def tskew (DF):
    skewlist = list()
    tList = list()
    for i in range(max(DF['Z'])+1):
        vals = tmp[tmp['Z']==i]['intensity']
        if len(vals) > 3:
            tList.append(str(i))
            skewlist.append(tmp[tmp['Z']==i]['intensity'].skew())
    return dict(zip(tList,skewlist))
    
def ageCV (DF):
    tmp = DF[DF['Z']==max(DF['Z'])]
    CVlist = list()
    maxAge = int(max(tmp['Age']))
    ageList = list()
    for i in range(1,maxAge+1):
        vals = tmp[tmp['Age']==i]['intensity']
        if len(vals) > 3:
            ageList.append(str(i))
            CVlist.append(np.std(vals)/np.mean(vals))
    return dict(zip(ageList,CVlist))

def ageClass (DF):
    Classlist = {}
    for name in ['high','low']:
        tmp = DF[DF['Z']==max(DF['Z'])]
        tmp = tmp[tmp['ATP_Class']==name]
        Classlist[name] = list(tmp[tmp ['Age']>0]['Age'])
    return Classlist
    
def AgeSkew (DF):
    tmp = DF[DF['Z']==max(DF['Z'])]
    skewlist = list()
    maxAge = int(max(tmp['Age']))
    ageList = list()
    for i in range(1,maxAge+1):
        vals = tmp[tmp['Age']==i]['intensity']
        if len(vals) > 3:
            ageList.append(str(i))
            skewlist.append(tmp[tmp['Age']==i]['intensity'].skew())
    return dict(zip(ageList,skewlist))
    

allDFs = {} 
for cond in conds: 
    sampleDFs = {} 
    for i in range(1,4): 
        dfPath = os.path.join(root,cond,"sample"+str(i),"CellDF_wAge.csv") 
        dfPath2 = os.path.join(root,cond,"sample"+str(i),"CellDF.csv")
        if os.path.isfile(dfPath2):
            tmp = pd.read_csv(dfPath)
            tmp2 = pd.read_csv(dfPath2)
            tmp['ATP_Class'] = tmp2['ATP_Class']
            sampleDFs["sample"+str(i)] = tmp
    allDFs[cond] = sampleDFs
   
valDict = {}
for cond in conds:
    tmpDict = {}
    for i in range(1,4):
        sname = "sample"+str(i)
        tmp = allDFs[cond][sname]
        tmpDict[sname] = ageClass(tmp)
    valDict[cond] = tmpDict
   
AllmergeDict = {}
for cond in conds:
    mergeDict = {}
    for i in range(1,4):
        tmp = valDict[cond]["sample"+str(i)]
        for key,value in tmp.items():
            if i == 1:
                mergeDict[key] = value
            else:
                mergeDict[key].extend(value)
    AllmergeDict[cond] = mergeDict
   
for cond in conds:
    tmp = AllmergeDict[cond]
    x = list()
    y = list()
    for key,values in tmp.items():
        for value in values:
            print(x,y)
            x.append(key)
            y.append(value)
    plt.boxplot([tmp['high'],tmp['low']],labels=['high','low'])
    r,p = stats.mannwhitneyu(tmp['high'],tmp['low'])
    plt.title('r:'+str(r)+'p:'+str(p))
    plt.xlabel('ATP Class')
    plt.ylabel('Cellular Age')
    plt.ylim((0,8))
    plt.savefig(os.path.join(root,'Total',cond+"_AgeClass.pdf"))
    plt.show()
    
