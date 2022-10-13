# coding: utf-8
import numpy as np
import random
import matplotlib.pyplot as plt
import os

# Magic Numbers
glcmM = 0.1  # mM
eAtpmM = 5  # mM (eATP / Cell * D)
w = 1  # weight


def findIndexes(a, res, patch=3):
    for j in range(a.shape[0]):
        for k in range(a.shape[1]):
            if np.array_equal(a[j : j + patch, k : k + patch], res):
                return j, k


def cellAutomaton(
    simSize=20,
    patch=3,
    rememberence=4,
    randomExchange=0,
    maxitr=None,
    saveAll=False,
    savePath="",
    rule1Rate=None,
    rule2Rate=None,
):
    a = np.random.randint(2, size=(simSize, simSize))
    c = np.random.randint(2, size=(simSize, simSize))
    remList = list(a)
    num = 0
    neighbors = patch**2 - 1
    center = int(patch / 2.0)
    centerIdx = patch * center + center + 1
    if rule1Rate != None and rule2Rate == None:
        rule2Rate = 1.0 - rule1Rate

    # default fig
    fig = plt.figure()
    plt.imshow(a, cmap="hot", interpolation="none")
    plt.axis("off")
    fig.savefig(os.path.join(savePath, "Heatmap" + str(num) + ".png"))
    num += 1
    plt.cla()
    plt.clf()
    plt.close()
    np.random.seed(seed=1)
    rng = np.random.default_rng()

    while maxitr != 0:
        b = np.copy(a)
        result = [
            a[j : j + patch, k : k + patch]
            for j in range(a.shape[0])
            for k in range(a.shape[1])
        ]
        for res in result:
            if len(res) == patch and len(res[0]) == patch:
                j, k = findIndexes(a, res, patch=patch)
                if rule1Rate != None and rule2Rate != None:
                    if sum(np.delete(res, centerIdx)) > int(neighbors * rule1Rate):
                        b[j + center, k + center] = 1  # rule 1 moore neighbor
                    elif sum(np.delete(res, centerIdx)) < int(neighbors * rule2Rate):
                        b[j + center, k + center] = 0  # rule 2 moore neighbor
                    prob = sum(np.delete(res, centerIdx)) / float(patch**2 - 1)
                else:
                    prob = glcmM / (
                        glcmM + w * (sum(np.delete(res, centerIdx)) * eAtpmM)
                    )
                if rng.uniform() > prob:
                    b[j + center, k + center] = 0
                else:
                    b[j + center, k + center] = 1
        for i in range(randomExchange):
            j = rng.integers(simSize)
            k = rng.integers(simSize)
            b[j, k] = 0

        for array in remList:
            if np.array_equal(b, array):
                return b
        else:
            if len(remList) < rememberence:
                remList.append(b)
            else:
                if saveAll:
                    fig = plt.figure()
                    plt.imshow(b, cmap="hot", interpolation="none")
                    plt.axis("off")
                    fig.savefig(os.path.join(savePath, "Heatmap" + str(num) + ".png"))
                    num += 1
                    plt.cla()
                    plt.clf()
                    plt.close()
                del remList[0]
                remList.append(b)
        if maxitr != None:
            maxitr = maxitr - 1
        a = np.copy(b)

    return a


def measureSamePheno(a, patch=3):
    phenoList = list()
    result = [
        a[j : j + patch, k : k + patch]
        for j in range(a.shape[0])
        for k in range(a.shape[1])
    ]
    for res in result:
        if len(res) == 3 and len(res[0]) == 3:
            j, k = findIndexes(a, res, patch=patch)
            pheno = a[j + 1, k + 1]
            if pheno == 0:
                phenoList.append((8 - sum(np.delete(res, 5))) / float(8))
            else:
                phenoList.append(sum(np.delete(res, 5)) / float(8))
    return sum(phenoList) / len(phenoList)


def randomizationTest(a, expValue, iterations=1000):
    randPhenoList = list()
    for itr in range(iterations):
        b = np.copy(a)
        random.shuffle(b)
        randPhenoList.append(measureSamePheno(b))
    return (
        sum(float(num) > expValue for num in randPhenoList) / float(iterations),
        randPhenoList,
    )


if __name__ == "__main__":
    simSize = 40
    rem = cellAutomaton(
        simSize=simSize,
        patch=3,
        saveAll=True,
        maxitr=30,
        savePath="/users/nakatani/Desktop/heatmap",
    )
    p, phenoList = randomizationTest(rem, measureSamePheno(rem), iterations=1000)
    print("P-value,ExpValue")
    print(p, measureSamePheno(rem))
    print("Randomized Values")
    print(phenoList)

    fig = plt.figure()
    plt.hist(phenoList)
    fig.savefig("phenoHist.pdf")
