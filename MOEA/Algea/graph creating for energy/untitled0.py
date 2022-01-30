# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 10:19:41 2021

@author: Ece Ari Akdemir
"""

from libpysal.weights import lat2W
from esda.moran import Moran
import numpy as np

# Use your matrix here, instead of this random one
Z = np.random.rand(200,150)

# Create the matrix of weigthts 
w = lat2W(Z.shape[0], Z.shape[1])

# Crate the pysal Moran object 
mi = Moran(Z, w)

# Verify Moran's I results 
print(mi.I) 
print(mi.p_norm)