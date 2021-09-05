# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 15:42:38 2021

@author: Ece Ari Akdemir
"""

import numpy as np
import pandas as pd

# read in data; treat first column as index
df_TEALCA = pd.read_excel('Cost_excel_Jack_JK.xlsx',header=0,index_col=0)
inputs = list(df_TEALCA.index.values)
df_district = pd.read_excel('combined_pivot_excel_LNG.xlsx',header=0,index_col=0)
districts = list(df_district['STASD_N'])

# def sim(bu_per_acre):
    
# ###################################
# # CONVERSIONS
# # B = np.array(bu_per_acre)
# ha_to_acre = 2.47105 # 1 Hectares = 2.47105 Acres  (acrage/hectare)
# lb_to_kg= 0.453515 # pounds to kilograms
# one_inch_to_gal = 27154
# gal_to_kg = 0.003785 #m^3 water/gal
# bushels_corn_to_kg = 25.4


#######################################################################
# Uniform annual per ha costs (don't change in space, occur every year)

uniform_per_ha = 0

for i in inputs:
    
    j = i.replace(" ", "_")

    locals()[j] = df_TEALCA.loc[i,'Input']*df_TEALCA.loc[i,'Per Unit Cost']

    uniform_per_ha += locals()[j]
    
    
###############################################
# Non-Uniform annual per ha costs (do change in space)    
    
# read in district information as data frame (df_district)
# define list or districts

district_per_ha_cultivation = []
    
for d in districts: #list of districts
     
    ag_dist = df_district.loc[df_district['STASD_N']==d]
    dist_electricity = ag_dist['Electricity Price $/MWh'].values[0]
    
    # calculate electricity cost
    electricity_cost = df_TEALCA.loc['Electricity','Input']*dist_electricity
    
    ag_dist = df_district.loc[df_district['STASD_N']==d]
    dist_LNG = ag_dist['NG Price($/MWh)'].values[0]
    
    # calculate natural gas cost
    LNG_cost = df_TEALCA.loc['LNG','Input']*dist_LNG
    
    non_uniform_per_ha = uniform_per_ha + electricity_cost + LNG_cost
    
    district_per_ha_cultivation.append(non_uniform_per_ha)
    

# district_per_ha_cultivation = pd.DataFrame(np.zeros((107,3)))
# dist_cost = []

    
# for d in districts: #list of districts
     
#     ag_dist = df_district.loc[df_district['STASD_N']==d]
#     dist_electricity = ag_dist['Electricity Price $/MWh'].values[0]
    
#     # calculate electricity cost
#     electricity_cost = df_TEALCA.loc['Electricity','Input']*dist_electricity
    
#     ag_dist = df_district.loc[df_district['STASD_N']==d]
#     dist_LNG = ag_dist['NG Price($/MWh)'].values[0]
    
#     # calculate natural gas cost
#     LNG_cost = df_TEALCA.loc['LNG','Input']*dist_LNG
    
#     non_uniform_per_ha = uniform_per_ha + electricity_cost + LNG_cost
#     dist_cost.append(non_uniform_per_ha)
    
# for state in df_district['State'].unique():
    
#     filtered_df_geo = df_district.loc[df_district['State']==state].copy()
        
#     for STASD in filtered_df_geo['STASD_N'].unique():
            
#         stasd_ind = districts.index(STASD)
            
#         filtered_STASD_N = filtered_df_geo.loc[filtered_df_geo['STASD_N']==STASD].copy()
#         del filtered_STASD_N['State']
        
#         district_per_ha_cultivation.iloc[stasd_ind,0] = state # sadece sayi yazabilirsin - index de sayi zaten - iloc daha cok index ozaman
#         district_per_ha_cultivation.iloc[stasd_ind,1] = filtered_STASD_N #stasd_ind =row 1:4 olan column ona gore belirliyor nereye koyacagini 
#         district_per_ha_cultivation.iloc[:,2] = dist_cost
             
# column_names = ['State', 'STASD_N', 'cost']
# district_per_ha_cultivation.columns = column_names

# district_per_ha_cultivation.to_excel('cost.xlsx')

















# Note: district_per_ha_cultivation should be list of $/ha/year values, one for each district, that /
# represents annual cultivation cost, but does not include capital or land costs (one time expenses)

# Then return this list to the main MOEA function

#120 - Irrigation
# gals_h2o_per_ha = ((1/17.4)*B + 8.2221) * one_inch_to_gal * ha_to_acre # H2O per acre
# m3_h2o_per_yr = gals_h2o_per_ha*arable_land * gal_to_kg
# Rain_water_per_yr = rain_water_blue_water * arable_land

# #130 - Fertilizers (N, P, K)
# kg_fert_per_ha = fertilizer_per_ha  # Converting the fertilization requirment from lb/acre to kg/ha
# fertilization_per_yr = kg_fert_per_ha * arable_land # Total fertilizer required for the arable lands

# #140 - Soil pH managment
# lime_per_yr = lime_treatment * arable_land

# #160 - Herbicide 
# herbicide_per_yr = herbicide_atrazibe * arable_land

# #170 - Crop Operations
# L_deisel_per_yr= L_diesel_per_ha * arable_land # kg/yr
# Natural_gas_per_yr = Gas * arable_land # kg/yr
# Electricity_per_yr = Electricity * arable_land  # kg/yr
# Labor_per_yr = labor * arable_land # $/yr

#180 - Harvest Yield
# kg_corn_grain_per_ha = B * bushels_corn_to_kg * ha_to_acre #kg/ha
# corn_stover_per_ha = kg_corn_grain_per_ha * 0.8867 #kg/ha
# kg_stover_per_ha = corn_stover_per_ha * arable_land * 0.5

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

    # return kg_stover_per_ha, corn_seed, fertilization_per_yr, lime_treatment
