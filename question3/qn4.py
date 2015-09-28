#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Athul
# @Date:   2015-09-28 13:30:51
# @Last Modified by:   Athul
# @Last Modified time: 2015-09-28 13:49:15

# 5,1,0.424831822644,0.3,0.05,0.03,0.04,0.08,0.01,0.35,0.03,0.35,0.02,0.1,0.01,0.01,0.01,0.001,0.001,0.001,0.001,0.2 
import numpy as np
x0 = np.array([0.02,0.25,0.35,0.05,0.03,0.35,0.4,0.15,0.07])
sigma = np.array([0.001,0.001,0.001,0.01,0.001,0.001,0.1,0.01,0.1])
T = 0.1
P = 0.48950563524
K = 0.01

A = np.zeros(x0.size, dtype=np.float64)
b = np.zeros(x0.size, dtype=np.float64)
for i in xrange(len(x0)):
    A[i] = x0[i]*np.exp((-1/2)*T*sigma[i]**2)
    b[i] = sigma[i]*np.sqrt(T)

R1 = R2 = 0
for i in xrange(len(x0)):
    for j in xrange(len(x0)):
        if i == j:
            R1 += b[i]**2
        else:
            R2 += b[i]*b[j]
rho = (2*np.log(P+K) - 2*np.sum(np.log(A)) - R1)/R2
print(rho)

