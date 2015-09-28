#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul Vijayan
# @Date:   2015-09-25 22:38:46
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 11:49:18
from __future__ import division
import pandas as pd
import numpy as np
import re
import scipy.io
import matplotlib.pyplot as plt
from scipy.cluster.vq import whiten, vq, kmeans
from sklearn import mixture
from sklearn.decomposition import PCA
import scipy.stats
plt.style.use('ggplot')

trainData = np.load('../data/Initial_Training_Data.npy')
np.random.shuffle(trainData)
testData = np.load('../data/Initial_Test_Data.npy')
truth = trainData[:, 19].astype(int)
numClasses = max(truth) - min(truth) + 1

# Remove NaNs
for cls in xrange(numClasses):
    classData = trainData[truth==cls, :]
    col_mean = scipy.stats.mode(classData, axis=0)
    ids = np.where(np.isnan(classData))
    classData[ids] = np.take(col_mean, ids[1])
    trainData[truth==cls, :] = classData

col_mean = scipy.stats.mode(trainData, axis=0)
ids = np.where(np.isnan(testData))
testData[ids] = np.take(col_mean, ids[1])

trainFeatures = np.hstack((trainData[:, 1:19], trainData[:, 20:]))
testFeatures = testData[:, 1:]

# ============================== Do PCA   ========================
pca = PCA(n_components='mle')
pca.fit(trainFeatures)
trainFeatures = pca.transform(trainFeatures)
testFeatures = pca.transform(testFeatures)

#  ============================= Train GMM =======================
models = []
for cls in xrange(numClasses):
    classFeatures = trainFeatures[truth==cls, :]
    numGaussians = 14
    models.append(mixture.GMM(n_components=numGaussians))
    models[cls].fit(classFeatures)

# ====================== test GMM ===========================
scores = np.zeros((testData.shape[0], numClasses))
for cls in xrange(numClasses):
    scores[:, cls] = models[cls].score(testFeatures)
targetScores = np.amax(scores, axis = 1)
targetClass = np.argmax(scores, axis = 1)

outFile = 'output.csv'
with open(outFile, 'w') as f:
    f.write('ISIN, Risk_Stripe\n')
    for i in xrange(testData.shape[0]):
        line = 'ISIN{0},Stripe {1}\n'
        line = line.format(int(testData[i, 0]), targetClass[i])
        f.write(line)
f.close()