#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-26 06:06:47
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-26 06:26:30
from __future__ import division
import pandas as pd
import numpy as np
import os
from sklearn import svm
import matplotlib.pyplot as plt
import scipy.stats
plt.style.use('ggplot')

trainData = np.load('../data/Initial_Training_Data.npy')
np.random.shuffle(trainData)
testData = trainData[int(trainData.shape[0]*0.8):,:]
trainData = trainData[:int(trainData.shape[0]*0.8),:]
# testData = np.load('../data/Initial_Test_Data.npy')
truth = trainData[:, 19].astype(int)

# Remove NaNs from traindata
col_mean = scipy.stats.nanmean(trainData, axis=0)
ids = np.where(np.isnan(trainData))
trainData[ids] = np.take(col_mean, ids[1]) 

# Remove NaNs from testdata
col_mean = scipy.stats.nanmean(testData, axis=0)
ids = np.where(np.isnan(testData))
testData[ids] = np.take(col_mean, ids[1]) 

trainFeatures = np.hstack((trainData[:, 1:19], trainData[:, 20:]))
testFeatures = np.hstack((testData[:, 1:19], testData[:, 20:]))

# ============================= Train SVM ====================
print('starting svm training')
model = svm.SVC()
model.fit(trainFeatures, truth)
# # ============================== Test svm model===============
print('starting svm testing')
targetClass = model.predict(testFeatures)
trueClass = testData[:, 19].astype(int)

miss = np.count_nonzero(trueClass - targetClass)
accuracy = model.score(testFeatures, trueClass)
print('Number of misses '+str(miss)+' in '+str(testData.shape[0])+' trials')
print('Accuracy = '+str(accuracy))
