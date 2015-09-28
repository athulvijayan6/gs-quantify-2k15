#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-28 13:04:41
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 13:30:25
from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import mixture
from sklearn.neighbors import KNeighborsClassifier
from sklearn.lda import LDA
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

#  ============================= Train GMM =======================
gmmModels = []
for cls in xrange(numClasses):
    classFeatures = trainFeatures[truth==cls, :]
    numGaussians = 14
    gmmModels.append(mixture.GMM(n_components=numGaussians))
    gmmModels[cls].fit(classFeatures)

# ====================== test GMM ===========================
gmmScores = np.zeros((testData.shape[0], numClasses))
for cls in xrange(numClasses):
    gmmScores[:, cls] = gmmModels[cls].score(testFeatures)

# =========================== KNN model =======================
knnModel = KNeighborsClassifier(n_neighbors=5)
knnModel.fit(trainFeatures, truth)
knnScores = knnModel.predict_proba(testFeatures)

# =========================== FDA model =======================
fdaModel = LDA()
fdaModel.fit(trainFeatures, truth)
fdaScores = fdaModel.predict_proba(testFeatures)

# ======================== Build hybrid =======================
scores = np.log(gmmScores) + np.log(knnScores) + np.log(fdaScores)
targetScores = np.amax(scores, axis = 1)
targetClass = np.argmax(scores, axis = 1)

outFile = 'output.csv'
with open(outFile, 'w') as f:
    f.write('ISIN, Risk_Stripe\n')
    for i in xrange(testData.shape[0]):
        line = 'ISIN{0},Stripe {1}\n'
        line = line.format(int(testData[i, 0]), int(targetClass[i]))
        f.write(line)
f.close()

