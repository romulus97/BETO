"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""
# from platypus import NSGAII, Problem, Real 
import random
from random import randint
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation_V as CS_cultivation
import corn_stover_processing_V as CS_processing
import matplotlib.pyplot as plt

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import district level data
df_geo = pd.read_csv('US_ag_district_geodata.csv',header=0)
districts = list(df_geo['STASD_N'])

#specify grouping
groups = 20

#district-to-hub data
filename = 'AgD2H_48_cb.csv'
df_D2H = pd.read_csv(filename,header=0)
c = list(df_D2H['STASD_N'])

#eliminate districts that don't appear in both lists
for i in districts:
    idx = districts.index(i)
    if i in c:
        pass
    else:
        df_geo = df_geo.drop(index=idx)

df_geo = df_geo.reset_index(drop=True)
# fips = df_geo['fips'].values
districts = list(df_geo['STASD_N'])
land_costs = df_geo.loc[:,'land_costs'].values # $ per acre
land_limits = df_geo['land_limits_acres'].values # county ag production area in acres

# Corn Stover
C_yield = df_geo['yield_bpa'].values  #yield in bushels per acre

########################################################################
#########        PRE-PROCESSING       ##################################
########################################################################

################################
# Convert to function inputs

# Hub grouping information, distance look-up tables
dist_D2H = []
district_hubs = []
for d in districts:
    
    idx = districts.index(d)
    
    # distance from each county to pre-defined hub
    dist_D2H.append(df_D2H.loc[df_D2H['STASD_N']==d,'travel_dist_km'].values[0])
    
    # list of hubs assigned to each county
    district_hubs.append(df_D2H.loc[df_D2H['STASD_N']==d,'destinationID'].values[0])


# Pre-define location of refineries
# put a number > 0 and < number of hubs if desired; if not, problem defaults to full list of hubs
num_refineries = 0

#hub-to-hub data
filename = 'AgD_48g_H2H_cb.csv'
df_H2H = pd.read_csv(filename,header=0)
hubs = list(df_H2H['OriginID'].unique())

locations = hubs
    
################################
# Convert to function inputs

dist_map = np.zeros((len(hubs),len(locations)))

# convert look-up table to distance matrix
for i in range(0,len(hubs)):
    c1 = hubs[i]
    for j in range(0,len(locations)):
        c2 = locations[j]
        dist_map[i,j] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers']

map_D2H = np.zeros((len(districts), len(hubs)))

# convert look-up table to distance matrix #when 50 is indexed 49 is not valid because of missing hubs
for i in range(0,len(districts)):
    h = hubs.index(int(district_hubs[i])) # int(county_hubs[i]) - 1
    map_D2H[i,h] = 1    


#########################################################
# Identify quota as % of maximum theoretical production
import determine_quota_V_district
p=.05
quota, UB , v_test = determine_quota_V_district.QD(districts,locations,p)
quota = quota[0]
  

df = pd.read_csv('Decision_Variables_district.csv',header=0,index_col=0)
DV = df.iloc[0,:].values # take first solution
plt.figure()
plt.scatter(land_limits,DV[0:len(land_limits)])
 
#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
lb_to_kg= 0.453515 # pounds to kilograms
kg_to_L_Ethanol = 1.273723

# # simulation model (function to be evaluated by MOEA)
# def test(variables,LC,C_Y,LL,DM,C2H_map,C2H,locations,hubs,Q):
    
    
variables = DV # cultivation hectares per county, hub-to-hub biomass flows
LC = land_costs # land costs per county
C_Y = C_yield # corn yield per acre
LL = land_limits # land limits
DM = dist_map # hub to hub distances
D2H_map = map_D2H # binary matrix mapping counties (rows) to hubs (columns)
D2H = dist_D2H # county to hub distances
locations = locations #possible location of biorefineries,
hubs = hubs
Q = quota
        

# Empty parameters 
CS_cultivation_capex = 0 
CS_cultivation_opex = 0
CS_travel_opex = 0
CS_flow_matrix = np.zeros((len(hubs),len(locations)))
CS_D2H_prod = np.zeros((len(LC),len(hubs)))
CS_refinery_kg = 0
CS_ethanol = np.zeros((len(locations),1))
CS_refinery_capex = 0

Constraints = [] # constraints

# Per ha values (need to expand)
(CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y) #kg/ha

# Capital costs (need to expand)
L = np.array(LC) #$/acre
v = variables

CS_cultivation_capex += np.sum(v[0:len(LC)]*L) #  ha*$/acre

##############################
# Cultivation and Harvesting

# Operating costs (need to expand)
harvesting = 38.31*ha_to_acre # $ per ha
CS_cultivation_opex += np.sum((v[0:len(LC)]*(seeds_per_ha*.00185 + fertilization_per_ha[0]*0.55 + fertilization_per_ha[1]*0.46 + fertilization_per_ha[2]*0.50 + lime_per_ha*0.01 + harvesting))) #herbicide in per ha??
   
d2h_map = np.array(D2H_map)

# Automatic flow to pre-processing hub
CS_D2H_prod = d2h_map * np.transpose(np.array([(CS_per_ha * v[0:len(LC)])])) #kg = kg*ha/ha

CS_cultivation_opex += np.sum(CS_per_ha*variables[0:len(LC)]*(lb_to_kg)*(1/1500)*0.50*D2H)
   
# Cultivation constraints (land limits) #PUT OUTSIDE OF LOOP 
# for i in range(0,len(LC)):
#     Constraints.append(variables[i] - LL[i] - 5) #allow some slack in DVs
    
# LL_cons = np.subtract(np.subtract(v[0:len(LC)], LL), 5)
# Constraints.extend(LL_cons.tolist())
   
################################
    
# ref = (len(LC) + (len(hubs) - 1)*len(locations) + (len(locations) - 1)) + 1
   
# # Mass transfer (1Ms kg of CS) from hub 'j' to hub 'k'
CS_flow_matrix = v[len(LC):].reshape((len(hubs),len(locations))) #kg

# Travel costs in bale-miles
CS_travel_opex = np.sum(DM*CS_flow_matrix*((lb_to_kg)*(1/1500)*0.50)) # km*kg*

# #Flow to refinery
# for j in range(0,len(hubs)):
    
#     for k in range(0,len(locations)):
    
#         # Mass transfer (1Ms kg of CS) from hub 'j' to hub 'k'
#         CS_flow_matrix[j,k] = CS_flow_matrix[j,k] + variables[len(LC) + j*len(locations) + k] 
        
#         # Travel costs in bale-miles
#         CS_travel_opex += DM[j,k]*CS_flow_matrix[j,k]*(lb_to_kg)*(1/1500)*0.50 

#for j in range(0,len(hubs)):
# P = np.array(CS_C2H_prod)
# F = np.array(CS_flow_matrix)
   
# Hubs collect biomass from counties
CS_hub_kg = np.sum(CS_D2H_prod, axis=0) #kg

# Transportation constraints (all delivery from hub 'j' must be <= mass produced)
CS_flow = np.sum(CS_flow_matrix, axis=1) #kg
flow_constraints = CS_flow - CS_hub_kg - 5 #allow some slack in DVs #kg

# for j in range(0,len(hubs)):
#     Constraints.append(flow_constraints[j]) 

Constraints.extend(flow_constraints.tolist())

###############################
# Refinery
   
#for k in range(0,len(locations)):
      
# Find total mass received at hub 'l'
CS_refinery_kg = np.sum(CS_flow_matrix, axis=0) #kg
        
# Ethanol produced at refinery at hub 'l'
CS_ethanol = CS_processing.sim(CS_refinery_kg) #L

#for k in range(0,len(locations)):
    # Refinery capex
    #if CS_refinery_kg[k] > 5:   #skip or remove
scale = CS_refinery_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file
CS_refinery_capex = 400000000*(scale)**.6

# Sets ethanol production quota (L)
Constraints.append(Q - np.sum(CS_ethanol) - 5) #L
#Constraints.append(sum(CS_ethanol)[0] - Q*1.05) #remove upper contraint 

Constraints = list(Constraints)

a = np.sum(CS_refinery_capex)
b = CS_travel_opex

print([a,b])

# Returns list of objectives, Constraints
# return np.sum(CS_refinery_capex), CS_travel_opex, np.sum(CS_ethanol)
