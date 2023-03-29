#!/bin/env python
#
# Extract DATASET for POD using pyAlya
#
# Last rev: 28/10/2021
from __future__ import print_function, division

import os, numpy as np
import pyAlya, pyLOM


BASEDIR        = '../'
DSETDIR        = './'
CASESTR        = 'channel'
VARLIST        = ['VELOC','PRESS']
START, DT, END = 500000, 500, 1000000

# In case of restart, load the previous data
listOfInstants = [ii for ii in range(START,END,DT)]
ni = len(listOfInstants)


## Load pyAlya mesh
mesh = pyAlya.Mesh.read(CASESTR,basedir=BASEDIR,read_commu=False,read_massm=False)
pyAlya.pprint(0,'Run (%d instants)...' % len(listOfInstants),flush=True)


## Create POD dataset
m = pyLOM.Mesh.from_pyAlya(mesh)
p = pyLOM.PartitionTable.from_pyAlya(mesh.partition_table,has_master=True)
d = pyLOM.Dataset(ptable=p, mesh=m, time=np.zeros((ni,),dtype=np.double))
d.save('%s_a.h5'%CASESTR,append=True,nopartition=True) 


## Build dataset from the instants
ntime = 100
ibuff = 0
X_PRESS = np.zeros((mesh.nnod,ntime),dtype=np.double) # POD matrix, VELOC and PRESS
X_VELOX = np.zeros((mesh.nnod,ntime),dtype=np.double) # POD matrix, VELOC and PRESS
X_VELOY = np.zeros((mesh.nnod,ntime),dtype=np.double) # POD matrix, VELOC and PRESS
X_VELOZ = np.zeros((mesh.nnod,ntime),dtype=np.double) # POD matrix, VELOC and PRESS
for ii,instant in enumerate(listOfInstants):
	if ii%100 == 0: pyAlya.pprint(1,'Processing instant %d...'%instant,flush=True)
	# Read data
	field, header = pyAlya.Field.read(CASESTR,VARLIST,instant,mesh.xyz,basedir=BASEDIR)
	# Store time
	d.time[ii] = header.time
	# Store the POD matrix
	X_PRESS[:,ibuff] = field['PRESS']
	X_VELOX[:,ibuff] = field['VELOC'][:,0]
	X_VELOY[:,ibuff] = field['VELOC'][:,1]
	X_VELOZ[:,ibuff] = field['VELOC'][:,2]
	ibuff += 1
	# Append POD matrix
	if ntime == ibuff:
		pyAlya.pprint(1,'Printing instant %d...'%instant,flush=True)
		d.add_variable('PRESS',True,1,X_PRESS)
		d.add_variable('VELOX',True,1,X_VELOX)
		d.add_variable('VELOY',True,1,X_VELOY)
		d.add_variable('VELOZ',True,1,X_VELOZ)
		d.save('%s_a.h5'%CASESTR,append=True,nopartition=True)
		# Reset counters
		ibuff  = 0


pyAlya.cr_info()
pyLOM.cr_info()

