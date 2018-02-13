#!/usr/bin/env python3

import math
import matplotlib
matplotlib.use("Agg")
import pylab as plt
from sklearn.metrics import auc
import argparse
from random import shuffle

matplotlib.pylab.rcParams.update({
    'legend.fontsize': 'medium',
    'figure.figsize': (6, 6),
    'axes.labelsize': 'large',
    'axes.titlesize': 'x-large',
    'xtick.labelsize': 'medium',
    'ytick.labelsize': 'medium'
})


def main():
    realPaths = [
                    "real.cos.eval",
                    "real.l2.eval",
                    "real.tpw.eval",
                    "real.twe.eval",
                    "real.hybrid.eval",
                    "real.path.eval"
                ]
    fakePaths = [
                    "fake.cos.eval",
                    "fake.l2.eval",
                    "fake.tpw.eval",
                    "fake.twe.eval",
                    "fake.hybrid.eval",
                    "fake.path.eval"
                ]
    legend = {
                # 0: {
                    # 2: "({0:.3f}) CSim",
                    # 3: "({0:.3f}) BestCentrCSim"
                   # },
                # 1: {
                    # 2: "({0:.3f}) $L_2^{{-1}}$",
                    # 3: "({0:.3f}) BestCentr$L_2$"
                   # },
                # 2: {
                    # 2: "({0:.3f}) BestTopicPerWord"
                   # },
                # 3: {
                    # 2: "({0:.3f}) TopicCorr"
                   # },
                # 4: {
                    # 2: "({0:.3f}) PolyMultiple"
                   # },
                5: {
                    3: "({0:.3f}) NumHops",
                    4: "({0:.3f}) Average Path Length Through Topics",
                    5: "({0:.3f}) Average Query Word Betweenness",
                    6: "({0:.3f}) Average Path Betweenness Through Topics",
                    7: "({0:.3f}) Average Query Word Eigenvalue",
                    8: "({0:.3f}) Average Path Eigenvalue Through Topics",
                    9: "({0:.3f}) Clustering Coef",
                    10: "({0:.3f}) Modularity"
                   }
             }

    #dontReverse = {(1, 2), (4, 2), (5, 6), (5, 9)}
    dontReverse = {}

    fig = plt.figure()
#    fig.set_size_inches(8, 8)
#    fig.suptitle("", fontsize=16, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_title('ROC Published vs. Noise')
    ax = fig.add_subplot(111)

    legends = []
    areas = []

    colors = [
            'purple',
            'blue',
            'cyan',
            'green',
            'orange',
            'red',
            'brown',
            'slategrey',
            'black',
            'tomato',
            'aqua',
            'crimson'
            'indigo',
            'black',
             ]
    colorIdx = 0

    class Data:
        def __init__(self, area, tpf, fpf, legend):
            self.area = area
            self.tpf = tpf
            self.fpf = fpf
            self.legend = legend

        def __str__(self):
            return self.legend.format(self.area)

    plotData = []

    for pathIdx in range(len(realPaths)):
        realPath = realPaths[pathIdx]
        fakePath = fakePaths[pathIdx]
        print(realPath, fakePath)
        if pathIdx not in legend:
            continue
        for columnIdx, plotText in legend[pathIdx].items():

            print(plotText)
            data = []

            realData = []
            with open(realPath) as rFile:
                for line in rFile:
                    tokens = line.split()
                    realData.append((float(tokens[columnIdx]), 1))
            realData = [d for d in realData if not math.isnan(d[0]) and not math.isinf(d[0])]
            shuffle(realData)

            fakeData = []
            with open(fakePath) as fFile:
                for line in fFile:
                    tokens = line.split()
                    fakeData.append((float(tokens[columnIdx]), 0))
            fakeData = [d for d in fakeData if not math.isnan(d[0]) and not math.isinf(d[0])]
            shuffle(fakeData)

            size = min(len(realData), len(fakeData))
            realData = realData[1:size]
            fakeData = fakeData[1:size]

            data = realData + fakeData

            shuffle(data)
            shouldReverse = (pathIdx, columnIdx) not in dontReverse
            data.sort(key=lambda x: x[0], reverse=shouldReverse)

            ySum = [0 for d in data]
            nSum = [0 for d in data]
            fpf = [0 for d in data]
            tpf = [0 for d in data]

            totalY = sum([1 for d in data if d[1] == 1])
            totalN = sum([1 for d in data if d[1] == 0])

            if data[0][1] == 1:
                ySum[0] = 1
            else:
                nSum[0] = 1

            for i in range(1, len(data)):
                if data[i][1] == 1:
                    ySum[i] += 1
                else:
                    nSum[i] += 1
                ySum[i] += ySum[i-1]
                nSum[i] += nSum[i-1]

            for i in range(len(data)):
                fpf[i] = nSum[i] / totalN
                tpf[i] = ySum[i] / totalY

            area = auc(fpf, tpf)
            plotData.append(Data(area, tpf, fpf, plotText))
    print(plotData)
    plotData.sort(key=lambda x: x.area)
    for colorIdx, d in enumerate(plotData):
        print(colorIdx, d.legend, d.area)
        ax.plot(d.fpf, d.tpf, color=colors[colorIdx], linewidth=2)
        legends.append(d.legend.format(d.area))
    ax.set_xlabel("False Positive Fraction")
    ax.set_ylabel("True Positive Fraction")

    plt.tight_layout()
    box = ax.get_position()
    #ax.set_position([box.x0, box.y0 + box.height , box.width * 0.85, box.height * 0.85])

    # legArea = plt.legend(areas, loc="upper center",
                         # bbox_to_anchor=(0.5, -0.1),
                         # fancybox=True,
                         # title="Area",
                         # ncol=4)
    # ax.add_artist(legArea)
    plt.legend(legends, loc=4, title="(Area) Metric Name")
    #names = plt.legend(legends, loc="center left", bbox_to_anchor=(1, 0.5))
    #ax.add_artist(names)

    plt.savefig("published_roc.png")


if __name__ == "__main__":
    main()
