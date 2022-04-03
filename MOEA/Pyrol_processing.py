# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 21:16:08 2021

@author: Ece Ari Akdemir
"""

import numpy as np
import pandas as pd

    
def sim(Feedstock_kg):
        
    # CONVERSIONS
    Biocrude_constant = 0.25 # kg/kg Feedstock

    Biocrude = Feedstock_kg * Biocrude_constant
    
    return Biocrude  