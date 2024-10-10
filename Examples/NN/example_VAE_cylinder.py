#!/usr/bin/env python
#
# Example of 2D-VAE.
#
# Last revision: 24/09/2024
from __future__ import print_function, division

import mpi4py
mpi4py.rc.recv_mprobe = False

import os, numpy as np
import pyLOM


## Set device
device = pyLOM.NN.select_device("cpu") # Force CPU for this example, if left in blank it will automatically select the device


## Specify autoencoder parameters
nlayers     = 5
channels    = 64
lat_dim     = 5
beta        = 0
beta_start  = 0
beta_wmup   = 0
kernel_size = 4
nlinear     = 512
padding     = 1
activations = [pyLOM.NN.tanh(), pyLOM.NN.tanh(), pyLOM.NN.tanh(), pyLOM.NN.tanh(), pyLOM.NN.tanh(), pyLOM.NN.tanh(), pyLOM.NN.tanh()]


## Load pyLOM dataset and set up results output
BASEDIR = './DATA/'
CASESTR = 'CYLINDER'
DSETDIR = os.path.join(BASEDIR,f'{CASESTR}.h5')
RESUDIR = 'vae_beta_%.2e_ld_%i' % (beta, lat_dim)
pyLOM.NN.create_results_folder(RESUDIR)


## Mesh size (HARDCODED BUT MUST BE INCLUDED IN PYLOM DATASET)
n0h = 449
n0w = 199
nh  = 448
nw  = 192


## Create a torch dataset
m    = pyLOM.Mesh.load(DSETDIR)
d    = pyLOM.Dataset.load(DSETDIR,ptable=m.partition_table)
u_x  = d['VELOX'][:,0]
time = d.get_variable('time')[0]
td   = pyLOM.NN.Dataset((u_x,), (n0h, n0w))
td.crop(nh, nw)


## Set and train the variational autoencoder
betasch    = pyLOM.NN.betaLinearScheduler(0., beta, beta_start, beta_wmup)
encoder    = pyLOM.NN.Encoder2D(nlayers, lat_dim, nh, nw, td.num_channels, channels, kernel_size, padding, activations, nlinear, vae=True)
decoder    = pyLOM.NN.Decoder2D(nlayers, lat_dim, nh, nw, td.num_channels, channels, kernel_size, padding, activations, nlinear)
model      = pyLOM.NN.VariationalAutoencoder(lat_dim, (nh, nw), td.num_channels, encoder, decoder, device=device)
early_stop = pyLOM.NN.EarlyStopper(patience=5, min_delta=0.02)

pipeline = pyLOM.NN.Pipeline(
    train_dataset = td,
    test_dataset  = td,
    model=model,
    training_params={
        "batch_size": 1,
        "epochs": 500,
        "lr": 1e-4,
        "betasch": betasch
    },
)
pipeline.run()


## Reconstruct dataset and compute accuracy
rec = model.reconstruct(td)
rd  = pyLOM.NN.Dataset((rec,), (nh, nw))
rd.pad(n0h, n0w)
td.pad(n0h, n0w)
d.add_field('urec',1,rd[0,0,:,:].numpy().reshape((n0w*n0h,)))
d.add_field('utra',1,td[0,0,:,:].numpy().reshape((n0w*n0h,)))
pyLOM.io.pv_writer(m,d,'reco',basedir=RESUDIR,instants=[0],times=[time],vars=['urec', 'VELOX', 'utra'],fmt='vtkh5')
pyLOM.NN.plotSnapshot(m,d,vars=['urec'],instant=0,component=0,cmap='jet',cpos='xy')
pyLOM.NN.plotSnapshot(m,d,vars=['utra'],instant=0,component=0,cmap='jet',cpos='xy')


pyLOM.cr_info()
