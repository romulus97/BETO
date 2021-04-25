"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
from random import randint
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation as CS_cultivation
import corn_stover_processing as CS_processing

   
#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
lb_to_kg= 0.453515 # pounds to kilograms
kg_to_L_Ethanol = 1.273723

# NOTE: MAKE SURE OF CONVERSIONS BELOW -- VALUES ABOVE NOW APPEAR ALL IN ACRES
    
    
# simulation model (function to be evaluated by MOEA)
def test(DV, LC, C_Y, LL, DM, C2H_map, C2H, locations, hubs, Q):
       
    # Empty parameters 
    CS_cultivation_capex = 0 
    CS_cultivation_opex = 0
    CS_travel_opex = 0
    CS_flow_matrix = np.zeros((len(hubs),len(locations)))
    CS_C2H_prod = np.zeros((len(LC),len(hubs)))
    CS_flow = 0
    CS_refinery_kg = 0
    CS_ethanol = np.zeros((len(locations),1))
    CS_refinery_capex = 0
    
    Constraints = [] # constraints
    
    ##############################
    # Cultivation and Harvesting
        
    for i in range(0,len(LC)):
        
        # Per ha values (need to expand)
        (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y[i])
    
        # Capital costs (need to expand)
        CS_cultivation_capex += DV[i]*LC[i]
        
        # Operating costs (need to expand)
        harvesting = 38.31*ha_to_acre # $ per ha
        CS_cultivation_opex += DV[i]*(seeds_per_ha*.00185 + fertilization_per_ha[0]*0.55 + fertilization_per_ha[1]*0.46 + fertilization_per_ha[2]*0.50 + lime_per_ha*0.01 + harvesting) #herbicide in per ha??
        
        # Automatic flow to pre-processing hub
        CS_C2H_prod[i,:] = C2H_map[i,:]*CS_per_ha*DV[i]

        CS_cultivation_opex += CS_per_ha*DV[i]*(lb_to_kg)*(1/1500)*0.50*C2H[i]
        
        # # Cultivation constraints (land limits)
        # Constraints.append(DV[i] - LL[i] - 5) #allow some slack in DVs
        
    ################################
        
    # Flow to refinery
    for j in range(0,len(hubs)):
        
        for k in range(0,len(locations)):
        
            # Mass transfer (1Ms kg of CS) from hub 'j' to hub 'k'
            CS_flow_matrix[j,k] = CS_flow_matrix[j,k] + DV[i + 1 + j*len(locations) + k]
            
            # Travel costs in bale-miles
            CS_travel_opex += DM[j,k]*CS_flow_matrix[j,k]*(lb_to_kg)*(1/1500)*0.50 

    for j in range(0,len(hubs)):
        
        # Hubs collect biomass from counties
        CS_hub_kg = sum(CS_C2H_prod[:,j])
    
        # Transportation constraints (all delivery from hub 'j' must be <= mass produced)
        CS_flow = sum(CS_flow_matrix[j,:])
        Constraints.append(CS_flow - CS_hub_kg - 5) #allow some slack in DVs

        
    ###############################
    # Refinery
    for k in range(0,len(locations)):
          
        # Find total mass received at hub 'l'
        CS_refinery_kg = sum(CS_flow_matrix[:,k])
        
        # Ethanol produced at refinery at hub 'l'
        CS_ethanol[k] = CS_processing.sim(CS_refinery_kg)
        
        # Refinery capex
        if CS_refinery_kg > 5:
            scale = CS_refinery_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file
            CS_refinery_capex+= 400000000*(scale)**.6
    
    # Sets ethanol production quota (L)
    Constraints.append(Q - np.sum(CS_ethanol) - 5)

    Constraints = list(Constraints)
    
    # Returns list of objectives, Constraints
    return [CS_refinery_capex, CS_travel_opex], Constraints


