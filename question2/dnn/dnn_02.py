#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-28 15:11:59
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 16:02:24
from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import mixture
import scipy.stats
import cPickle, gzip
import cnn.cnn as cnn
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
trainFeatures = trainFeatures[:, 11:18]
valFeatures = trainFeatures[:int(trainFeatures.shape[0]/8)]
valLabels = truth[:int(trainFeatures.shape[0]/8)]
testFeatures = trainFeatures[int(7*trainFeatures.shape[0]/8):]
testLabels = truth[int(7*trainFeatures.shape[0]/8):]

# ============================= Make pickle files ==================
datafile = 'qn2_data.pkl.gz'
with gzip.open(datafile, 'wb') as f:
    data = ((trainFeatures, truth), (valFeatures, valLabels), (testFeatures, testLabels))
    cPickle.dump(data, f)
print('created pickle file as ' + datafile)

# ============================ Apply model ===========================
cnn.evaluate_lenet5(dataset=datafile, batch_size=100)