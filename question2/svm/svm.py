#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-26 02:16:55
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 13:58:13
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
svm_train_data = 'results/svm_train_data'
svm_test_data = 'results/svm_test_data'
modelfile = 'results/svm_model_data_01.model'
resultFile = 'results/iter_01'

with open(svm_train_data, 'w') as f:
    for i in xrange(trainFeatures.shape[0]):
        d = {}
        for j in xrange(trainFeatures[i].size):
            if not np.isnan(trainFeatures[i, j]):
                d[j+1] = trainFeatures[i, j]
        line = str(truth[i]+1)
        for index, value in d.iteritems():
            line += ' '+str(index)+':'+str(value)
        line += '\n'
        f.write(line)
    f.close()

with open(svm_test_data, 'w') as f:
    for i in xrange(testFeatures.shape[0]):
        d = {}
        for j in xrange(testFeatures[i].size):
            if not np.isnan(testFeatures[i, j]):
                d[j+1] = testFeatures[i, j]
        line = str(1)
        for index, value in d.iteritems():
            line += ' '+str(index)+':'+str(value)
        line += '\n'
        f.write(line)
    f.close()

# ============================= Train SVM ====================
print('scaling data')
command = './libsvm/svm-scale -l -1 -u 1 -s results/range {0} > {1}.scale'
command = command.format(svm_train_data, svm_train_data)
os.system(command)

command = './libsvm/svm-scale -r results/range {0} > {1}.scale'
command = command.format(svm_test_data, svm_test_data)
os.system(command)

svm_train_data += '.scale'
svm_test_data += '.scale'


print('starting svm training')
s = 0
t = 2
d = 2
g = 0.0625
r = 0
c = 1
b = 0
v = 5
command = './libsvm/svm-train {8} {9} -s {0} -t {1} -d {2} -g {3} -r {4} -c {5} -b {6} -v {7}'
command = command.format(s, t, d, g, r, c, b, v, svm_train_data, modelfile)
os.system(command)

# # ============================== Test svm model===============
print('starting svm testing')
b = 0
command = './libsvm/svm-predict -b {0} {1} {2} {3}'
command = command.format(b, svm_test_data, modelfile, resultFile)
os.system(command)

# =========================== Make output file ==================
outFile = 'output.csv'
with open(outFile, 'w') as f:
    f.write('ISIN, Risk_Stripe\n')
    res = open(resultFile, 'rb')
    for i in xrange(testFeatures.shape[0]):
        cls = int(res.readline())
        line = 'ISIN{0},Stripe {1}\n'
        line = line.format(int(testData[i, 0]), cls)
        f.write(line)
f.close()
res.close()



