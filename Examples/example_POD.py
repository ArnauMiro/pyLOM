#!/usr/bin/env python
#
# Example of POD.
#
# Last revision: 19/07/2021
from __future__ import print_function, division

import numpy as np
import matplotlib.pyplot as plt

import pyLOM


## Data loading
UALL = np.load('DATA/UALL.npy') # Data must be in C order
X    = UALL
N    = 151


## Compute POD after subtracting mean (i.e., do PCA)
pyLOM.cr_start('example',0)
PSI,S,V = pyLOM.POD.run(X)
# PSI are POD modes
pyLOM.cr_stop('example',0)


# Plot accumulative S
plt.figure(figsize=(8,6),dpi=100)

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
