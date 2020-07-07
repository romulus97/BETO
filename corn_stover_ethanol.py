# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

import numpy as np
import pandas as pd
import Land_Dedication_Seeding
import Irrigation
import Fertilization
import Available_Corn_Stover
import Truck
import Comminution

###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
gal_to_acre_feet = 3.07e-6 # Gallons to Acre-feet
lb_to_kg= 0.453515 # pounds to kilograms
Bushels_corn_to_kg = 25.4
Miles_to_km = 1.60934


###################################
# INPUTS
bu_per_acre = 175 # Bushels Corn per Acre
seeds_per_acre = 3000 # Seeds per Acre
seeds_per_ha = seeds_per_acre*ha_to_acre # Seeds per Hectare

fertilizer_per_acre = np.array([144, 64, 82]) # lb N , P2O5 , K2O per acre

Lime_tretment = 183.04 # kg of lime per acre

Herbicide_Atrazibe = 1.082 #lb of Atrezine per acre 

hours_per_ha_laber = 2.965
L_diesel_per_ha = 56.124

field_to_biorefinary = 10 # miles
Truck_Capasity = 20 #tonnes

Comminution_energy = 0.1404 # MJ per kg stover
Percent_to_hammer_mill = 97 # percent of corn stover goes into hammer mill is comminuted 
###################################
# AGRICULTURE 100s

#110 - Land dedication and seeding
arable_land = 1 #ha
seeded_land = Land_Dedication_Seeding.LDS(arable_land) # Seeded land in hectares

#120 - Irrigation
h2o_per_acre = Irrigation.Irr(bu_per_acre) # H2O per acre
gals_h2o_per_acre = h2o_per_acre*27154 # ASK JACK AND EVAN ???
gals_h2o_per_ha = gals_h2o_per_acre*ha_to_acre

#130 - Fertilizers (N, P, K)
fert_per_ha = fertilizer_per_acre * lb_to_kg * ha_to_acre # Converting the fertilization requirment from lb/acre to kg/ha
fertilizer_per_ha = Fertilization.Frt (fert_per_ha, arable_land) # Total fertilizer required for the arable lands

#140 - Soil pH managment
Lime_per_ha = Lime_tretment * ha_to_acre

#160 - Herbicide 
Herbicide_per_ha = Herbicide_Atrazibe * ha_to_acre * lb_to_kg

#170 - Crop Operations
Laber_h_per_ha = hours_per_ha_laber
L_deisel= L_diesel_per_ha

#180 - Harvest Yeild 
kg_corn_grain_per_ha = bu_per_acre * Bushels_corn_to_kg * ha_to_acre
corn_stover_per_ha = kg_corn_grain_per_ha * 0.8867
kg_stover_per_ha = Available_Corn_Stover.Stover(corn_stover_per_ha, arable_land)

#190 - Storage and Transportation
transportation = field_to_biorefinary * Miles_to_km #km
num_of_trucks = Truck.TRK (kg_stover_per_ha, Truck_Capasity)

###################################

# BIOPROCESS NAD CONVERSION 200 - 600
 
# 200 - Size Reduction Process - Comminution 
comm = Comminution.COMM (kg_stover_per_ha , Comminution_energy , Percent_to_hammer_mill)
Comminution_Electricity = comm [1] #MJ/ha
kg_comm_stover_ha = comm [0] # kg comminuted stover per ha

# 300 - Dilute acid hydrolysis 


###################################
# LIFE CYCLE ASSESSMENT




