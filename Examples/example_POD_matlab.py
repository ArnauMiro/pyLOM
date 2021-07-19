#!/usr/bin/env python
#
# Example of POD following the MATLAB script.
#
# Last revision: 19/07/2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import pyLOM


## Data loading
UALL = np.load('DATA/UALL.npy')
X    = UALL
N = 151

## Compute POD after subtracting mean (i.e., do PCA)
Uavg = pyLOM.POD.temporal_mean(X)
X_m  = pyLOM.POD.subtract_mean(X,Uavg)
Y    = X_m

PSI,S,V = pyLOM.POD.svd(Y)
# PSI are POD modes
'''
Guardar tot això amb matlab i comparar amb el seu codi
'''

# Plot accumulative S
plt.figure()#size=(8,6),dpi=100)

#n_snaps = 1:N;
accumulative_S = np.zeros((1,N));
diag_S = np.diag(S);

for i in range(N):
    accumulative_S[0, i] = np.linalg.norm(diag_S[i:N],2)/np.linalg.norm((diag_S),2);
plt.semilogy(np.linspace(1, N, N), np.transpose(accumulative_S), 'bo')
plt.ylabel('varepsilon1')
plt.xlabel('Truncation size')
plt.title('Tolerance')
plt.ylim((0, 1))

## Show and print timings
pyLOM.cr_info()
plt.show()
