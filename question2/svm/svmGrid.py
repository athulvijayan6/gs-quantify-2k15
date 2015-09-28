#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-26 02:16:55
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 13:00:29
from __future__ import division
import pandas as pd
import numpy as np
import os
import csv
import matplotlib.pyplot as plt
import scipy.stats
plt.style.use('ggplot')

trainData = np.load('../data/Initial_Training_Data.npy')
np.random.shuffle(trainData)
testData = np.load('../data/Initial_Test_Data.npy')
truth = trainData[:, 19].astype(int)
numClasses = max(truth) - min(truth) + 1

# No need to remove NaNs
trainFeatures = np.hstack((trainData[:, 1:19], trainData[:, 20:]))
testFeatures = testData[:, 1:]

# libsvm filenames
svm_train_data = 'svm_train_data'
resultFile = 'results/iter__grid_01'

# ============================= Train SVM Grid====================
print('scaling data')
command = './libsvm/svm-scale -l -1 -u 1 -s results/range {0} > {1}.scale'
command = command.format(svm_train_data, svm_train_data)
os.system(command)

svm_train_data += '.scale'

print('starting svm grid training')
s = 0
t = 2
d = 2
# g gamma : set gamma in kernel function (default 1/k)
r = 0
c = 1
b = 0
v = 5
command = 'python grid.py -log2c -5,5,1 -log2g -4,0,1 -v 5 -m 300 {0}'
command = command.format(svm_train_data)
os.system(command)