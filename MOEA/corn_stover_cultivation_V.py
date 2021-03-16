
"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

import numpy as np
import pandas as pd


def sim(bu_per_acre):
    
    ###################################
    # CONVERSIONS
    B = np.array(bu_per_acre)
    ha_to_acre = 2.47105 # Hectares to Acres
    gal_to_acre_feet = 3.07e-6 # Gallons to Acre-feet
    lb_to_kg= 0.453515 # pounds to kilograms
    bushels_corn_to_kg = 25.4
    miles_to_km = 1.60934
    kWh_to_MJ = 3.6
    gal_to_L = 3.78541
    kg_to_ton = 0.00110231
    ton_to_bu = 35.71428571
    
    
    ###################################
    # INPUTS
    # bu_per_acre = 175 # Bushels Corn per Acre
    seeds_per_acre = 3000 # Seeds per Acre
    seeds_per_ha = seeds_per_acre*ha_to_acre # Seeds per Hectare
    fertilizer_per_acre = np.array([144, 64, 82]) # lb N , P2O5 , K2O per acre
    lime_treatment = 183.04 # kg of lime per acre
    herbicide_atrazibe = 1.082 #lb of Atrezine per acre 
    hours_per_ha_labor = 2.965
    L_diesel_per_ha = 56.124
    
    field_to_biorefinary = 10 # miles
    truck_capacity = 20 #tonnes
    
    comminution_energy = 0.1404 # MJ per kg stover
    percent_to_hammer_mill = 97 # percent of corn stover goes into hammer mill is comminuted 
    
    ###################################
    # AGRICULTURE 100s
    
    #110 - Land dedication and seeding
    arable_land = 1 #ha
    seeded_land = arable_land
    
    #120 - Irrigation
    h2o_per_acre = (1/17.4)*B + 8.2221 # H2O per acre
    gals_h2o_per_acre = h2o_per_acre*27154 # 
    gals_h2o_per_ha = gals_h2o_per_acre*ha_to_acre
    
    #130 - Fertilizers (N, P, K)
    fert_per_ha = fertilizer_per_acre * lb_to_kg * ha_to_acre # Converting the fertilization requirment from lb/acre to kg/ha
    fertilization_per_ha = fert_per_ha * arable_land # Total fertilizer required for the arable lands
    
    #140 - Soil pH managment
    lime_per_ha = lime_treatment * ha_to_acre
    
    #160 - Herbicide 
    herbicide_per_ha = herbicide_atrazibe * ha_to_acre * lb_to_kg
    
    #170 - Crop Operations
    labor_h_per_ha = hours_per_ha_labor
    L_deisel= L_diesel_per_ha
    
    #180 - Harvest Yield
    kg_corn_grain_per_ha = B * bushels_corn_to_kg * ha_to_acre #kg/ha
    corn_stover_per_ha = kg_corn_grain_per_ha * 0.8867 #kg/ha
    kg_stover_per_ha = corn_stover_per_ha * arable_land * 0.5
        
    return kg_stover_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha
