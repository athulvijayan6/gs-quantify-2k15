#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul Vijayan
# @Date:   2015-09-25 22:38:46
# @Last Modified by:   Athul Vijayan
# @Last Modified time: 2015-09-26 02:01:11
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
testData = trainData[int(trainData.shape[0]*0.8):,:]
trainData = trainData[:int(trainData.shape[0]*0.8),:]
# testData = np.load('../data/Initial_Test_Data.npy')
truth = trainData[:, 19]

# Remove NaNs
col_mean = scipy.stats.nanmean(trainData, axis=0)
ids = np.where(np.isnan(trainData))
trainData[ids] = np.take(col_mean, ids[1]) 

col_mean = scipy.stats.nanmean(testData, axis=0)
ids = np.where(np.isnan(testData))
testData[ids] = np.take(col_mean, ids[1])

# ============================== Do PCA   ========================
pca = PCA(n_components='mle')
features = np.hstack((trainData[:, 1:19], trainData[:, 20:]))
pca.fit(features)
features = pca.transform(features)

#  ============================= Train GMM =======================
numClasses = int(max(truth) - min(truth) + 1)
models = []
for cls in xrange(numClasses):
    classData = features[trainData[:, 19].astype(int) == cls]
    numGaussians = 28
    models.append(mixture.GMM(n_components=numGaussians))
    models[cls].fit(classData)

# ====================== test GMM ===========================
testFeatures = np.hstack((testData[:, 1:19], testData[:, 20:]))
testFeatures = pca.transform(testFeatures)
scores = np.zeros((testFeatures.shape[0], numClasses))
for cls in xrange(numClasses):
    sc = models[cls].score(testFeatures)
    scores[:, cls] = sc
targetScores = np.amax(scores, axis = 1)
targetClass = np.argmax(scores, axis = 1)
trueClass = testData[:, 19].astype(int)

miss = np.count_nonzero(trueClass - targetClass)
accuracy = 1-(miss/testData.shape[0])
print('variance captured by PCA = '+str(np.sum(pca.explained_variance_ratio_)))
print('Number of misses '+str(miss)+' in '+str(testData.shape[0])+' trials')
print('Accuracy = '+str(accuracy))