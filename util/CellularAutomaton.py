# coding: utf-8
import numpy as np
import random
import matplotlib.pyplot as plt

def findIndexes(a,res,patch=3):
    for j in range(a.shape[0]):
        for k in range(a.shape[1]):
            if np.array_equal(a[j:j+patch, k:k+patch],res):
                return j,k
            
def cellAutomaton(simSize=20,patch = 3,rememberence=4):
    a = np.random.randint(2,size=(simSize,simSize))
    c = np.random.randint(2,size=(simSize,simSize))
    remList = list(a)
    while True:
        b = np.copy(a)
        result = [a[j:j+patch, k:k+patch] for j in range(a.shape[0]) for k in range(a.shape[1])]
        for res in result:
            if len(res) == 3 and len(res[0]) == 3:
                j,k = findIndexes(a,res)
                if sum(np.delete(res,5)) < 4:
                    b[j+1,k+1] = 0
                # elif sum(np.delete(res,5)) != 4:
                #     b[j+1,k+1] = 0
        for array in remList:
            if np.array_equal(b,array):
                return b
        else:
            if len(remList) < rememberence:
                remList.append(b)
            else:
                del remList[0]
                remList.append(b)
        a = np.copy(b)
    return a
                
def measureSamePheno(a,patch=3):
    phenoList = list()
    result = [a[j:j+patch, k:k+patch] for j in range(a.shape[0]) for k in range(a.shape[1])]
    for res in result:
        if len(res) == 3 and len(res[0]) == 3:
            j,k = findIndexes(a,res)
            pheno = a[j+1,k+1]
            if pheno == 0:
                phenoList.append((8 - sum(np.delete(res,5))) / float(8))
            else:
                phenoList.append(sum(np.delete(res,5)) / float(8))
    return sum(phenoList)/len(phenoList)

def randomizationTest(a,expValue,iterations = 1000):
    randPhenoList = list()
    for itr in range(iterations):
        b = np.copy(a)
        random.shuffle(b)
        randPhenoList.append(measureSamePheno(b))
    return sum(float(num) > expValue for num in randPhenoList) / float(iterations) , randPhenoList

if __name__ == "__main__":
    a = cellAutomaton(simSize=40)
    print a
    fig = plt.figure()
    plt.imshow(a,cmap='hot',interpolation='none')
    fig.savefig("Heatmap.pdf")
    plt.cla()
    plt.clf()
    p, phenoList= randomizationTest(a,measureSamePheno(a))
    print "P-value,ExpValue"
    print p, measureSamePheno(a)
    print "Randomized Values"
    print phenoList
    
    fig = plt.figure()
    plt.hist(phenoList)
    fig.savefig("phenoHist.pdf")
