"""
Author: Joel Nakatani
Overview:

Parameters:
"""

from pyCellLineage.lineageIO.annotateLineageIdx import annotateLineageIdx as annt
from pyCellLineage.PDAnalysis.calcGEL import constructTimeRef
from pyCellLineage.PDAnalysis.calcGEL import CalcGEL
from pyCellLineage.PDAnalysis.calcEL import CalcEL
from pyCellLineage.PDAnalysis.calcRetro import RetrospectiveSampling as RS
import pyCellLineage as myPackage

import pandas as pd
import os
import argparse
import pickle
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from scipy.stats import mannwhitneyu as npTtest
from scipy.stats import ttest_ind as tTest


def argParser():
    parser = argparse.ArgumentParser(
        description="Run CalcEL and CalcGL on data")

    parser.add_argument(
        "-g",
        "--general",
        dest="gel",
        action="store_true",
        default=False,
        help="For Generalized Euler-Lotka analysis",
    )
    parser.add_argument(
        "-e",
        "--euler",
        dest="el",
        action="store_true",
        default=False,
        help="For Euler-Lotka analysis",
    )
    parser.add_argument(
        "-r",
        "--retro",
        dest="retro",
        action="store_true",
        default=False,
        help="For retrospective analysis",
    )
    parser.add_argument(
        "-p",
        "--plot",
        dest="plot",
        action="store_true",
        default=False,
        help="For Plotting All",
    )

    return parser


def shapeData(data):
    X, Y = data
    dy = list()

    for i, y in enumerate(Y):
        if i > 0:
            dy.append(abs(y - Y[i - 1]))
    index = np.argmax(dy) + 1

    return np.array(X[index:]), np.array(Y[index:])


def expFunc(x, a, b, c):
    return a * np.exp(-b * x) + c


def curveFit(data):
    x, y = shapeData(data)
    popt, pcov = curve_fit(expFunc,
                           x,
                           y,
                           sigma=np.repeat(0.001, len(x)),
                           bounds=([-1, 0, 0], 1))
    popt = tuple(popt)
    print(f'A={popt[0]:.2f}, B={popt[1]:.2f}, C={popt[2]:.2f}')

    return x, expFunc(x, *popt), popt


def plot(x, y, xLabel, yLabel, save):
    plt.cla()
    plt.clf()
    plt.scatter(x, y, label='data')
    fitX, fitY, popt = curveFit((x, y))
    print(fitX, fitY)
    plt.plot(fitX,
             fitY,
             'r-',
             label=f'fit A={popt[0]:.2f}, B={popt[1]:.2f}, C={popt[2]:.2f}')
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend()
    plt.savefig(save)

    return popt[2]


if __name__ == "__main__":
    parser = argParser()
    args = parser.parse_args()
    root = os.path.join(os.path.dirname(myPackage.__file__), 'Data')
    TotalDf = {}

    for cond in ['poor', 'rich']:
        TotalDf[cond] = {}

        for smpl in range(1, 4):
            target = os.path.join(root, f'glc_{cond}', f'sample{smpl}')
            fName = os.path.join(target, 'CellDf.csv')
            df = pd.read_csv(fName)
            tag = f'{cond}_{smpl}'
            refName = os.path.join(target, f'timeFrame_{tag}.bin')

            if not os.path.isfile(refName):
                timeRef = constructTimeRef(df)
                with open(refName, 'wb') as f:
                    pickle.dump(timeRef, f)
            else:
                with open(refName, 'rb') as f:
                    timeRef = pickle.load(f)
            figDir = os.path.join(target, 'FiguresGR')

            if not os.path.isdir(figDir):
                os.mkdir(figDir)

            if args.gel:
                maxDiv = max([len(i) for i in timeRef])
                minDiv = min([len(i) for i in timeRef])
                print(minDiv, maxDiv)
                vals = list()
                x = list()
                samples = list()

                for i in range(2, maxDiv):
                    try:
                        res = CalcGEL(df,
                                      timeRef=timeRef,
                                      linCutOff=maxDiv,
                                      lin_gel=i)
                    except ZeroDivisionError or ValueError:
                        pass

                    if res != None:
                        vals.append(res)
                        x.append(i)
                        samples.append(len([j for j in timeRef if len(j) > i]))

                    if i > max(x) + 5:
                        break

                # plot(x,
                #      samples,
                #      'divisions',
                #      '# of independent lineages',
                #      os.path.join(target,'FiguresGR',f'div_num_{tag}.pdf')
                #      )
                A = plot(
                    x, vals, 'divisions', 'Growth Rate',
                    os.path.join(target, 'FiguresGR', f'div_gr_{tag}.pdf'))
                # plot(vals,
                #      samples,
                #      'Growth Rate',
                #      '# of independent lineages',
                #      os.path.join(target,'FiguresGR',f'gr_num_{tag}.pdf')
                #      )
                with open(os.path.join(target, f'GEL_{tag}.log'), 'w') as f:
                    f.write(str(A))

            if args.el:
                minDiv = min([len(i) for i in timeRef])
                B = CalcEL(
                    df,
                    timeRef=timeRef,
                    linCutOff=minDiv,
                )
                with open(os.path.join(target, f'EL_{tag}.log'), 'w') as f:
                    f.write(str(B))

            if args.retro:
                retroSmpl = RS(
                    df,
                    timeRef=timeRef,
                )
                minT = retroSmpl.minT
                maxT = retroSmpl.getMaxT(df)

                if minT == maxT:
                    minT = 5
                print(maxT)
                print(minT)

                gr = list()

                for i in range(minT, maxT):
                    retroSmpl.minT = i
                    val = retroSmpl.calculate(
                        mode='reCount',
                        timeRef=timeRef,
                    )
                    gr.append(val)
                    print(i, val)
                C = plot(range(minT, maxT), gr, 'considered last timepoint',
                         'Growth Rate',
                         os.path.join(target, 'FiguresGR/RS_{tag}.pdf'))
                name = f'RS_{tag}.log'
                with open(os.path.join(target, name), 'w') as f:
                    f.write(str(C))

    if args.plot:
        conds = ['poor', 'rich']
        samples = range(1, 4)
        suffix = ['GEL']
        tags = []

        for cond in conds:
            for smpl in samples:
                tags.append(f'{cond}_{smpl}')
        vals = dict.fromkeys(tags)

        for key in vals.keys():
            vals[key] = dict.fromkeys(suffix)

        for s in suffix:
            for t in tags:
                cond, smpl = t.split('_')
                fName = os.path.join(root, f'glc_{cond}', f'sample{smpl}',
                                     f'{s}_{t}.log')

                if os.path.isfile(fName):
                    with open(fName, 'r') as f:
                        val = float(f.read())

                    vals[t][s] = val

        poorDict = dict([(key, vals[key]) for key in vals if 'poor' in key])
        richDict = dict([(key, vals[key]) for key in vals if 'rich' in key])
        x = [poorDict[key]['GEL'] for key in poorDict]
        y = [richDict[key]['GEL'] for key in richDict]
        i, p = npTtest(x, y)
        fName = os.path.join(os.path.dirname(myPackage.__file__), 'Data',
                             'GrowthRate', f'p_value.txt')
        with open(fName, 'w') as f:
            f.write(str(p))

        for i, condDict in enumerate([poorDict, richDict]):
            for key in condDict.keys():
                plt.scatter(condDict[key].keys(),
                            condDict[key].values(),
                            label=key)
            plt.legend()
            plt.savefig(
                os.path.join(os.path.dirname(myPackage.__file__), 'Data',
                             'GrowthRate', f'Result_{i}.pdf'))
            plt.cla()
            plt.clf()
        sumList = [x, y]

        for i, cond in enumerate(['poor', 'rich']):
            plt.scatter([cond] * len(sumList[i]), sumList[i])
        plt.ylabel('Growth Rate($\Lambda$)')
        plt.savefig(
            os.path.join(os.path.dirname(myPackage.__file__), 'Data',
                         'GrowthRate', 'Result_3.pdf'))
        plt.cla()
        plt.clf()
