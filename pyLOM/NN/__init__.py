#!/usr/bin/env python
#
# pyLOM - Python Low Order Modeling.
#
# NN Module
#
# Last rev: 09/10/2024

# Supress prints from tensorflow
import os, torch
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

from .callbacks     import EarlyStopper
from .utils         import Dataset, create_results_folder, select_device, betaLinearScheduler, MinMaxScaler

from .architectures.mlp import MLP
from .architectures.autoencoders import Autoencoder, VariationalAutoencoder
from .architectures.encoders_decoders import Encoder2D, Decoder2D, Encoder3D, Decoder3D

from .optimizer import OptunaOptimizer
from .pipeline import Pipeline

## Wrapper of the activation functions
import torch.nn as nn
def tanh():
    return nn.Tanh()

def relu():
    return nn.ReLU()

def elu():
    return nn.ELU()

def sigmoid():
    return nn.Sigmoid()

def leakyRelu():
    return nn.LeakyReLU()

def silu():
    return nn.SiLU()

del os
