#!/usr/bin/env python
#
# Example of SVD utility so that it returns
# the same output as MATLAB.
#
# Last revision: 09/07/2021
from __future__ import print_function, division

import numpy as np
import pyLOM


## Define matrix A 4x2
A = np.array([[1,2],[3,4],[5,6],[7,8]],dtype=np.double,order='C')


## Run SVD from numpy
pyLOM.cr_start('SVD numpy',0)
U, S, V = np.linalg.svd(A,full_matrices=False)
print('Numpy:')
print(U.shape,U)
print(S.shape,S)
print(V.shape,V)
pyLOM.cr_stop('SVD numpy',0)


## Run SVD from POD
pyLOM.cr_start('SVD pyLOM',0)
U, S, V = pyLOM.math.svd(A)
print('POD:')
print(U.shape,U)
print(S.shape,S)
print(V.shape,V)
pyLOM.cr_stop('SVD pyLOM',0)

pyLOM.cr_start('TSQR_SVD pyLOM',0)
U, S, V = pyLOM.math.tsqr_svd(A)
print('POD:')
print(U.shape,U)
print(S.shape,S)
print(V.shape,V)
pyLOM.cr_stop('TSQR_SVD pyLOM',0)


pyLOM.cr_info()