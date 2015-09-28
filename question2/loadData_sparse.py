#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul Vijayan
# @Date:   2015-09-25 15:12:37
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 13:21:06
import csv
import pandas as pd
import numpy as np
import re
import scipy.io

months = {'jan':0, 'feb':1, 'mar':2, 'apr':3, 'may':4, 'jun':5, 'jul':6, 'aug':7, 'sep':8, 'oct':9, 'nov':10, 'dec':11}
trainDataFile = 'data/Initial_Training_Data.csv'
testDataFile = 'data/Initial_Test_Data.csv'

DataPd = [pd.read_csv(trainDataFile), pd.read_csv(testDataFile)]

featureNames = list(DataPd[0].columns.values)

data = [np.zeros((DataPd[0].shape[1]+4,)), np.zeros((DataPd[1].shape[1]+4,))]
for i in xrange(len(DataPd)):
    for row in DataPd[i].iterrows():
        temp = np.zeros((DataPd[i].shape[1]+4,))
        for f in xrange(DataPd[i].shape[1]):
            item = row[1][f]
            if pd.isnull(item):
                temp[f] = item
            else:
                # [0, 1, 2, 3, 5, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19]
                if f not in [4, 6, 7, 8, 12]:
                    # extract number
                    point = int(re.search('[0-9]+', item).group(0))
                    temp[f] = point
                elif f in [4, 6]:
                    # boolean field
                    if item == 'N':
                        temp[f] = 0
                    elif item == 'Y':
                        temp[f] = 1
                    else:
                        temp[f] = np.nan
                elif f == 7:
                    # Int field
                    temp[f] = item
        data[i] = np.vstack((data[i], temp))
    data[i] = data[i][1:]
trainData = data[0]
testData = data[1]
np.save('data/Initial_Training_Data', trainData)
np.save('data/Initial_Test_Data', testData)
scipy.io.savemat('data/DataFile', {'trainData':trainData, 'testData':testData})






