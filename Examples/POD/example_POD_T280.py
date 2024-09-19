#!/usr/bin/env python
#
# Example of POD.
#
# Last revision: 19/07/2021
from __future__ import print_function, division

import mpi4py
mpi4py.rc.recv_mprobe = False

import numpy as np
import pyLOM


## Parameters
DATAFILE = './DATA/Tensor_re280.h5'
VARIABLE = 'VELOC'


## Data loading
m = pyLOM.Mesh.load(DATAFILE)
d = pyLOM.Dataset.load(DATAFILE,ptable=m.partition_table)
X = d[VARIABLE]
t = d.get_variable('time')


## Run POD
PSI,S,V = pyLOM.POD.run(X,remove_mean=False) # PSI are POD modes
if pyLOM.utils.is_rank_or_serial(root=0): pyLOM.POD.plotResidual(S)
# Truncate according to a residual
PSI,S,V = pyLOM.POD.truncate(PSI,S,V,r=5e-6)
pyLOM.POD.save('results.h5',PSI,S,V,d.partition_table,nvars=3,pointData=d.point)
# Reconstruct the flow
X_POD = pyLOM.POD.reconstruct(PSI,S,V)
# Compute RMSE
rmse = pyLOM.math.RMSE(X_POD,X)
pyLOM.pprint(0,'RMSE = %e'%rmse)


## Dump to ParaView
d.add_field('spatial_modes_U',6,pyLOM.POD.extract_modes(PSI,1,len(d),modes=[1,4,6,2,5,3]))
d.add_field('spatial_modes_V',6,pyLOM.POD.extract_modes(PSI,2,len(d),modes=[1,4,6,2,5,3]))
d.add_field('spatial_modes_W',6,pyLOM.POD.extract_modes(PSI,3,len(d),modes=[1,4,6,2,5,3]))
pyLOM.io.pv_writer(m,d,'modes',basedir='out/modes',instants=[0],times=[0.],vars=['spatial_modes_U','spatial_modes_V','spatial_modes_W'],fmt='vtkh5')
pyLOM.POD.plotSnapshot(m,d,vars=['spatial_modes_U'],instant=0,component=0,cmap='jet')

# Temporal evolution
d.add_field('VELOR',3,X_POD)
pyLOM.io.pv_writer(m,d,'flow',basedir='out/flow',instants=np.arange(t.shape[0],dtype=np.int32),times=t,vars=['VELOC','VELOR'],fmt='vtkh5')
pyLOM.POD.plotSnapshot(m,d,vars=['VELOR'],instant=0,component=0,cmap='jet')


## Plot POD mode
if pyLOM.utils.is_rank_or_serial(0):
	# 0 - module, 1,2 - components
	_,ax = pyLOM.POD.plotMode(V,t,modes=[1,3])
	ax[0][1].set_xlim([0,0.5])
	ax[1][1].set_xlim([0,0.5])


## Show and print timings
pyLOM.cr_info()
pyLOM.show_plots()