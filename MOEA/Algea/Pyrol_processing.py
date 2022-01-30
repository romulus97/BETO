# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 21:16:08 2021

@author: Ece Ari Akdemir
"""

import numpy as np
import pandas as pd

    
def sim(Feedstock_kg):
        
    # CONVERSIONS
    Electricity = 123.91 # MJ/kg Feedstock

    Feedstock_Energy = Feedstock_kg * Electricity
    
    return Feedstock_Energy  