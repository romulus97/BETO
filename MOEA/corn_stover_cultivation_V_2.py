# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 15:42:38 2021

@author: Ece Ari Akdemir
"""

import numpy as np
import pandas as pd

df_TEALCA = pd.read_excel('Cost_excel_Jack.xlsx',header=0)
def sim(bu_per_acre):
    
    ###################################
    # CONVERSIONS
    B = np.array(bu_per_acre)
    ha_to_acre = 2.47105 # 1 Hectares = 2.47105 Acres  (acrage/hectare)
    lb_to_kg= 0.453515 # pounds to kilograms
    one_inch_to_gal = 27154
    gal_to_kg = 0.003785 #m^3 water/gal
    bushels_corn_to_kg = 25.4
    
    ###################################
    # INPUTS
    # bu_per_acre = 175 # Bushels Corn per Acre
    corn_seed = df_TEALCA.iloc[4:5,2:3].values[0][0] # kg seeds/ha/yr
    fertilizer_per_ha = np.array([df_TEALCA.iloc[6:7,2:3].values[0][0], df_TEALCA.iloc[7:8,2:3].values[0][0], df_TEALCA.iloc[8:9,2:3].values[0][0]]) # N , P2O5 , K2O kg/ha/yr
    lime_treatment = df_TEALCA.iloc[9:10,2:3].values[0][0] # kg of ag lime/ha/yr
    herbicide_atrazibe = df_TEALCA.iloc[10:11,2:3].values[0][0] # kg of Atrezine/ha/yr
    labor = df_TEALCA.iloc[3:4,2:3].values[0][0] # dollar/ha/yr
    L_diesel_per_ha = df_TEALCA.iloc[15:16,2:3].values[0][0] # kg/ha/yr
    rain_water_blue_water = df_TEALCA.iloc[14:15,2:3].values[0][0] # m3/ha/yr
    Gas = df_TEALCA.iloc[18:19,2:3].values[0][0] # MJ/ha/yr 
    Electricity = df_TEALCA.iloc[19:20,2:3].values[0][0] # MJ/ha/yr
    
    Land_capital_cost = df_TEALCA.iloc[1:2,2:3].values[0][0]
    capital_cost = df_TEALCA.iloc[2:3,2:3].values[0][0]
    
    ##cost of inputs 
    corn_seed_cost = df_TEALCA.iloc[11:12,18:19].values[0][0] # $/kg seeds/yr
    fertilizer_per_ha_cost = np.array([df_TEALCA.iloc[28:29,18:19].values[0][0], df_TEALCA.iloc[29:30,18:19].values[0][0], df_TEALCA.iloc[30:31,18:19].values[0][0]]) # $/N , P2O5 , K2O kg/yr
    lime_treatment_cost = df_TEALCA.iloc[24:25,18:19].values[0][0] # $/kg/yr
    herbicide_atrazibe_cost = df_TEALCA.iloc[21:22,18:19].values[0][0] # $/kg/yr
    L_diesel_per_cost = df_TEALCA.iloc[43:44,18:19].values[0][0] # $/kg/yr
    Electricity_cost = df_TEALCA.iloc[44:45,18:19].values[0][0] # $/MJ/yr
    # natural gas price is empty in the excel 
    
    field_to_biorefinary = 10 # miles
    truck_capacity = 20 #tonnes
    
    comminution_energy = 0.1404 # MJ per kg stover
    percent_to_hammer_mill = 97 # percent of corn stover goes into hammer mill is comminuted 
    
    ###################################
    # AGRICULTURE 100s
    
    #110 - Land dedication and seeding
    arable_land = 1 #ha
    
    Seed = arable_land * corn_seed # kg seeds/yr
    
    #120 - Irrigation
    gals_h2o_per_ha = ((1/17.4)*B + 8.2221) * one_inch_to_gal * ha_to_acre # H2O per acre
    m3_h2o_per_yr = gals_h2o_per_ha*arable_land * gal_to_kg
    Rain_water_per_yr = rain_water_blue_water * arable_land
    
    #130 - Fertilizers (N, P, K)
    kg_fert_per_ha = fertilizer_per_ha  # Converting the fertilization requirment from lb/acre to kg/ha
    fertilization_per_yr = kg_fert_per_ha * arable_land # Total fertilizer required for the arable lands
    
    #140 - Soil pH managment
    lime_per_yr = lime_treatment * arable_land
    
    #160 - Herbicide 
    herbicide_per_yr = herbicide_atrazibe * arable_land
    
    #170 - Crop Operations
    L_deisel_per_yr= L_diesel_per_ha * arable_land # kg/yr
    Natural_gas_per_yr = Gas * arable_land # kg/yr
    Electricity_per_yr = Electricity * arable_land  # kg/yr
    Labor_per_yr = labor * arable_land # $/yr
    
    #180 - Harvest Yield
    kg_corn_grain_per_ha = B * bushels_corn_to_kg * ha_to_acre #kg/ha
    corn_stover_per_ha = kg_corn_grain_per_ha * 0.8867 #kg/ha
    kg_stover_per_ha = corn_stover_per_ha * arable_land * 0.5
    
    # #190 -One time Cost
    # land_capital_cost_total = Land_capital_cost * arable_land # $
    # capital_cost_total = capital_cost * arable_land # $
    
    # #200 - Yearly Cost
    # seed_cost = Seed * corn_seed_cost  # $
    # fertilization_cost = fertilization_per_yr * fertilizer_per_ha_cost
    # lime_cost = lime_per_yr * lime_treatment_cost
    # herbicide_cost = herbicide_per_yr * herbicide_atrazibe_cost 
    # diesel_cost = L_deisel_per_yr * L_diesel_per_cost
    # Elect_cost = Electricity_per_yr * Electricity_cost
    # Labor_cost = Labor_per_yr

    return kg_stover_per_ha, corn_seed, fertilization_per_yr, lime_treatment
