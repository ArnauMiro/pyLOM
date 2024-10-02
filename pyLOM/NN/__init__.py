#!/usr/bin/env python
#
# pyLOM - Python Low Order Modeling.
#
# NN Module
#
# Last rev: 02/11/2023

# Supress prints from tensorflow
import os, torch
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

from .wrapper       import tanh, relu, elu, sigmoid, leakyRelu, silu, VariationalAutoencoder, Autoencoder
from .architectures import Encoder2D, Decoder2D, Encoder3D, Decoder3D
from .callbacks     import EarlyStopper
from .utils         import Dataset, create_results_folder, select_device, betaLinearScheduler
from ..utils.plots  import plotSnapshot


del wrapper, os, torch
