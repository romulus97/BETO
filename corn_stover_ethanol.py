# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

import numpy as np
import pandas as pd
import Land_Dedication_Seeding
import Irrigation

###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
gal_to_acre_feet = 3.07e-6 # Gallons to Acre-feet


###################################
# INPUTS
bu_per_acre = 175 # Bushels Corn per Acre
seeds_per_acre = 3000 # Seeds per Acre
seeds_per_ha = seeds_per_acre*ha_to_acre # Seeds per Hectare


###################################
# AGRICULTURE 100s

#110 - Land dedication and seeding
arable_land = 1 #ha
seeded_land = Land_Dedication_Seeding.LDS(arable_land) # Seeded land in hectares

#120 - Irrigation
h2o_per_acre = Irrigation.Irr(bu_per_acre) # H2O per acre
gals_h2o_per_acre = h2o_per_acre*27154 # ASK JACK AND EVAN ???
gals_h2o_per_ha = gals_h2o_per_acre*ha_to_acre








###################################
# LIFE CYCLE ASSESSMENT




