#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-27 16:15:39
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 11:16:38
from __future__ import division
import pandas as pd
import numpy as np
import os
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import scipy.stats
plt.style.use('ggplot')

trainData = np.load('data/Initial_Training_Data.npy')
testData = np.load('data/Initial_Test_Data.npy')
truth = trainData[:, 19].astype(int)
numClasses = 16

# Remove NaNs
for cls in xrange(numClasses):
    col_mean = scipy.stats.nanmean(trainData[truth==cls, :], axis=0)
    ids = np.where(np.isnan(trainData[truth==cls, :]))
    trainData[ids] = np.take(col_mean, ids[1]) 

col_mean = scipy.stats.nanmean(trainData, axis=0)
ids = np.where(np.isnan(testData))
testData[ids] = np.take(col_mean, ids[1])

trainFeatures = np.hstack((trainData[:, 1:19], trainData[:, 20:]))
testFeatures = testData[:, 1:]

# ============================== Do PCA   ========================
if False:
    pca = PCA(n_components=5)
    pca.fit(trainFeatures)
    trainFeatures = pca.transform(trainFeatures)
    testFeatures = pca.transform(testFeatures)

    print('variance captured by PCA = '+str(np.sum(pca.explained_variance_ratio_)))
    plt.figure()
    ax = plt.subplot(111, projection='3d')
    colors = iter(cm.rainbow(np.linspace(0, 1, 16)))
    for i in xrange(16):
        clsData = trainFeatures[truth==i, :]
        ax.plot(clsData[:, 0], clsData[:, 1], clsData[:, 2], linestyle='None', marker='o', markersize=5,alpha=0.6, color= next(colors), label='class '+str(i))
    plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=8, bbox_to_anchor=(0, 0))

    df = pd.DataFrame(trainFeatures, columns=[str(i) for i in xrange(trainFeatures.shape[1])])
    axes = pd.tools.plotting.scatter_matrix(df, alpha=0.2)
    plt.tight_layout()
# ===================== hISTOGRAM =========================
if False:
    for i in xrange(trainFeatures.shape[1]):
        fig, ax = plt.subplots()
        hist, bins = np.histogram(trainFeatures[truth==1, i], bins=50)
        width = 0.7 * (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.title('Histogram of feature number '+str(i))


# ********************** Plot correlation heat map *********
if True:
    corrMat = np.corrcoef(np.transpose(trainFeatures))
    fig, ax = plt.subplots()
    ax.pcolor(corrMat, cmap=plt.cm.Blues, alpha=0.8)
    # Format
    fig = plt.gcf()
    fig.set_size_inches(8, 11)
    # turn off the frame
    ax.set_frame_on(False)
    ax.grid(False)
    plt.title('Correlation heatmap')
plt.show()
