#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-26 15:40:20
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-26 16:26:05
from __future__ import division
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import scipy.stats
import cPickle, gzip
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

trainFeatures = np.hstack((trainData[:, 1:19], trainData[:, 20:]))
testFeatures = np.hstack((testData[:, 1:19], testData[:, 20:]))

trainDataFile = 'data/traindata_01.pkl.gz'
testDataFile = 'data/testdata_01.pkl.gz'

with gzip.open(trainDataFile, 'wb') as pfile:
    cPickle.dump((trainFeatures, truth), pfile)

with gzip.open(testDataFile, 'wb') as pfile:
    cPickle.dump((testFeatures, testData[:, 19].astype(int)), pfile)

# ====================== Make dnn model ====================
command = 'python pdnn/cmds/run_DNN.py --train-data "{0},random=true" --valid-data "{1},random=true" --nnet-spec "{2}:128:128:16" --wdir ./ --param-output-file dnn.mdl'
command = command.format(trainDataFile, testDataFile, trainFeatures.shape[1])
os.system(command)

