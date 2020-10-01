# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 13:22:20 2020

@author: jkern
"""

import pandas as pd
import numpy as np
import time
import corn_stover_cultivation as CS_cultivation
import corn_stover_processing as CS_processing

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import county level data
df_geo = pd.read_excel('geo.xlsx',sheet_name='counties',header=0)
fips = df_geo['fips'].values
counties = df_geo['name']
land_costs = df_geo.loc[:,'land_cost'].values # $ per ha
land_limits = df_geo['land_limit'].values # ha

# Corn Stover
bu_per_acre_C_yield = df_geo['C_yield'].values 

# import distance look-up table
df_dist = pd.read_excel('geo.xlsx',sheet_name='distance_lookup',header=0)
dist_map = np.zeros((len(counties),len(counties)))

# Simple refinery case (remove later)
refinery_idx = int(np.round(np.float(np.random.rand(1)*98),decimals=0))
 
# convert look-up table to matrix
for i in range(0,len(counties)):
    c1 = counties[i]
    for j in range(0,len(counties)):
        c2 = counties[j]
        if i != j:
            a = df_dist.loc[df_dist['county1']==c1]
            b = a.loc[df_dist['county2']==c2]
            dist_map[i,j] = (b['distance_m'].values)/1000
        else:
            dist_map[i,j] = 0
            

#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
lb_to_kg= 0.453515 # pounds to kilograms
kg_to_L_Ethanol = 1.273723
    
    
# simulation model (function to be evaluated by MOEA)
def simulate(
        variables, # planted corn stover in hectares
        LC = land_costs, # land costs per county
        C_Y = bu_per_acre_C_yield, # corn yield per acre
        LL = land_limits, # land limits
        DM = dist_map, # distance mapping
        R_idx = refinery_idx # location of refinery in simple case
        ):
    
    # Empty variables 
    CS_farm_kg = 0 # corn stover production in kg
    CS_cultivation_capex = 0 # total costs
    CS_cultivation_opex = 0
    CS_travel_opex = 0
    CS_flow_matrix = np.zeros((len(counties),len(counties)))
    CS_flow = 0
    CS_refinery_kg = 0
    CS_ethanol = np.zeros((len(counties),1))
    CS_refinery_opex = 0
    CS_refinery_capex = 0
    
    Constraints = [] # constraints
    
    ##############################
    # Cultivation and Harvesting
    for i in range(0,len(counties)):
        
        # Per ha values (need to expand)
        (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y[i])
        
        # kg CS produced in given county 'i'
        CS_farm_kg += CS_per_ha*variables[i]

        # Capital costs (need to expand)
        CS_cultivation_capex += variables[i]*LC[i]
        
        # Operating costs (need to expand)
        harvesting = 38.31*ha_to_acre # $ per ha
        CS_cultivation_opex += variables[i]*(seeds_per_ha*.00185 + fertilization_per_ha[0]*0.55 + fertilization_per_ha[1]*0.46 + fertilization_per_ha[2]*0.50 + lime_per_ha*0.01 + harvesting) #herbicide in per ha??
        
        ################################
        # Flow to refinery
        for j in range(0,len(counties)):
            
            # County to county mass transfer (kg of CS) (from county 'i' to county 'j')
            CS_flow_matrix[i,j] += variables[(i+1)*len(counties) + j]
        
            # Travel costs in bale-miles
            CS_travel_opex += DM[i,j]*CS_flow_matrix[i,j]*(lb_to_kg)*(1/1500)*0.50 
        
        # Transportation constraints (flow from county 'i' must be <= mass produced)
        CS_flow = sum(CS_flow_matrix[i,:])
        Constraints.append(CS_flow - CS_farm_kg)
        
        # Cultivation constraints (land limits)
        Constraints.append(variables[i] - LL[i])  
        
        
    ################################
    # Refinery
    for j in range(0,len(counties)):
        
        # Find total mass sent to refinery in county 'j'
        CS_refinery_kg = sum(CS_flow_matrix[:,j])
        
        # Ethanol produced at refinery in county 'j'
        CS_ethanol[j] = CS_processing.sim(CS_refinery_kg)
    
    # Refinery opex
    #ADD THIS        
        
        # Refinery capex
        if CS_refinery_kg > 0:
            scale = CS_refinery_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file
            CS_refinery_capex+= 400000000*(scale)**.6
    
        
    Constraints.append(1990000-sum(CS_ethanol))
    Constraints.append(sum(CS_ethanol) - 2010000)
    Constraints = list(Constraints)
    
    return [CS_refinery_capex, CS_travel_opex], Constraints

num_variables = len(counties) * len(counties) + len(counties)
variables = np.ones((num_variables,1))

a,b = simulate(variables)