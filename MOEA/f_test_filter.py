"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""
from platypus import NSGAII, Problem, Real 
import random
from random import randint
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation_V as CS_cultivation
import corn_stover_processing_V as CS_processing
import matplotlib.pyplot as plt


#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import county level data
df_geo = pd.read_excel('geodata_total.xlsx',header=0, engine='openpyxl')
counties = list(df_geo['co_state'])

#specify grouping
groups = 20

#county-to-hub data
filename = 'C2H_' + str(groups) + '.xlsx'
df_C2H = pd.read_excel(filename,header=0, engine='openpyxl')
c = list(df_C2H['co_state'])

#eliminate and counties that don't appear in both lists
for i in counties:
    idx = counties.index(i)
    if i in c:
        pass
    else:
        df_geo = df_geo.drop(index=idx)

df_geo = df_geo.reset_index(drop=True)
fips = df_geo['fips'].values
counties = list(df_geo['co_state'])
land_costs = df_geo.loc[:,'land_cost_dpa'].values # $ per acre
land_limits = df_geo['land_limits_acre'].values # county ag production area in acres

# Corn Stover
bu_per_acre_C_yield = df_geo['yield_bpa'].values  #yield in bushels per acre

########################################################################
#########        PRE-PROCESSING       ##################################
########################################################################

###################################
# PROBLEM SIZE CONTROLS

# Limit # of counties under consideration
# put a number > 0 and < number of counties if desired; if not, problem defaults to full list of counties
num_counties = 0

reduced_counties = []
reduced_land_costs = []
reduced_land_limits = []
reduced_C_yield = []

if num_counties > 0:
    for i in range(0,num_counties):
        s = randint(0,len(counties)-1)
        if s in reduced_counties:
            pass
        else:
            reduced_counties.append(counties[s])
else:
    reduced_counties = counties
    

################################
# Convert to function inputs

# Hub grouping information, distance look-up tables
dist_C2H = []
county_hubs = []
for county in reduced_counties:
    
    idx = counties.index(county)
    
    reduced_land_costs.append(land_costs[idx])
    reduced_land_limits.append(land_limits[idx])
    reduced_C_yield.append(bu_per_acre_C_yield[idx])
    
    # distance from each county to pre-defined hub
    dist_C2H.append(df_C2H.loc[df_C2H['co_state']==county,'travel_dist_km'].values[0])
    
    # list of hubs assigned to each county
    county_hubs.append(df_C2H.loc[df_C2H['co_state']==county,'destinationID'].values[0])


# Pre-define location of refineries
# put a number > 0 and < number of hubs if desired; if not, problem defaults to full list of hubs
num_refineries = 0

#hub-to-hub data
filename = 'H2H_' + str(groups) + '.xlsx'
df_H2H = pd.read_excel(filename,header=0, engine='openpyxl')
hubs = list(df_H2H['OriginID'].unique())

locations = []

if num_refineries > 0:
    for i in range(0,num_refineries):
        s = random.choice(hubs) #randint(1,len(hubs))
        if s in locations:
            pass
        else:
            locations.append(s)
else:
    locations = hubs
    
################################
# Convert to function inputs

dist_map = np.zeros((len(hubs),len(locations)))

# convert look-up table to distance matrix
for i in range(0,len(hubs)):
    c1 = hubs[i]
    for j in locations: 
        c2 = j
        dist_map[i,locations.index(j)] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers']
    # for j in range(0, len(locations)):
    #     c2 = hubs[locations[j]-1]
    #     dist_map[i,j] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers']

map_C2H = np.zeros((len(reduced_counties), len(hubs)))

# convert look-up table to distance matrix #when 50 is indexed 49 is not valid because of missing hubs
for i in range(0,len(reduced_counties)):
    h = hubs.index(int(county_hubs[i])) # int(county_hubs[i]) - 1
    map_C2H[i,h] = 1  

df = pd.read_csv('Decision_Variables_scale_filter.csv',header=0,index_col=0)
DV = df.iloc[0,:].values # take first solution
# plt.figure()
# plt.scatter(reduced_land_limits,DV[0:len(reduced_land_limits)])
 
#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
lb_to_kg= 0.453515 # pounds to kilograms
kg_to_L_Ethanol = 1.273723

# # simulation model (function to be evaluated by MOEA)
def test(DV,reduced_land_costs,reduced_C_yield,reduced_land_limits,dist_map,map_C2H,dist_C2H,locations,hubs):
    
    
    variables = DV # cultivation hectares per county, hub-to-hub biomass flows
    LC = reduced_land_costs, # land costs per county
    C_Y = reduced_C_yield, # corn yield per acre
    LL = reduced_land_limits, # land limits
    DM = dist_map, # hub to hub distances
    C2H_map = map_C2H, # binary matrix mapping counties (rows) to hubs (columns)
    C2H = dist_C2H, # county to hub distances
    locations = locations, #possible location of biorefineries,
    hubs = hubs,
    
    h = np.size(hubs)
    l = np.size(locations)
    c = np.size(LC)
    
    # Empty parameters 
    CS_cultivation_capex = 0 
    CS_cultivation_opex = 0
    CS_travel_opex = 0
    # CS_flow_matrix = np.zeros((len(hubs),len(locations)))
    CS_C2H_prod = np.zeros((c,h))
    CS_flow = 0
    CS_refinery_kg = 0
    CS_ethanol = np.zeros((l,1))
    CS_refinery_capex = 0
    
    Constraints = [] # constraints
    
    # Per ha values (need to expand)
    (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y) #kg/ha
    
    # Capital costs (need to expand)
    L = np.array(LC) #$/acre
    v = np.array(variables)
    
    CS_cultivation_capex += np.sum(v[0:c]*L) #  ha*$/acre
    
    ##############################
    # Cultivation and Harvesting
    
    # Operating costs (need to expand)
    harvesting = 38.31*ha_to_acre # $ per ha
    CS_cultivation_opex += np.sum((v[0:c]*(seeds_per_ha*.00185 + fertilization_per_ha[0]*0.55 + fertilization_per_ha[1]*0.46 + fertilization_per_ha[2]*0.50 + lime_per_ha*0.01 + harvesting))) #herbicide in per ha??
       
    c2h_map = np.array(C2H_map)
    # Automatic flow to pre-processing hub
    CS_C2H_prod = c2h_map * np.transpose(np.array([(CS_per_ha * v[0:c])]*h)) #kg = kg*ha/ha
    
    CS_cultivation_opex += np.sum(CS_per_ha*v[0:c]*(lb_to_kg)*(1/1500)*0.50*C2H)
       
    # Cultivation constraints (land limits) #PUT OUTSIDE OF LOOP 
    # for i in range(0,len(LC)):
    #     Constraints.append(vars[i] - LL[i] - 5) #allow some slack in DVs
        
    # LL_cons = np.subtract(np.subtract(v[0:len(LC)], LL), 5)
    # Constraints.extend(LL_cons.tolist())
       
    ################################
        
    # ref = (len(LC) + (len(hubs) - 1)*len(locations) + (len(locations) - 1)) + 1
       
    # # Mass transfer (1Ms kg of CS) from hub 'j' to hub 'k'
    CS_flow_matrix = v[c:].reshape((h,l)) #kg
    
    # Travel costs in bale-miles
    CS_travel_opex = np.sum(DM*CS_flow_matrix*((lb_to_kg)*(1/1500)*0.50)) # km*kg*
       
    # Hubs collect biomass from counties
    CS_hub_kg = np.sum(CS_C2H_prod, axis=0) #kg
    
    # Transportation constraints (all delivery from hub 'j' must be <= mass produced)
    CS_flow = np.sum(CS_flow_matrix, axis=1) #kg
    flow_constraints = CS_flow - CS_hub_kg - 5 #allow some slack in DVs #kg
    
    
    Constraints.extend(flow_constraints.tolist())
    
    ###############################
    # Refinery
       
    #for k in range(0,len(locations)):
          
    # Find total mass received at hub 'l'
    CS_refinery_kg = np.sum(CS_flow_matrix, axis=0) #kg
    
    # Only allow plants above certain scale
    filter_flows = np.array(list(map(int,(CS_refinery_kg/(5563*142))>1000)))
    new_kg = filter_flows*CS_refinery_kg
    scale = filter_flows*(CS_refinery_kg/(5563*142))
            
    # Ethanol produced at refinery at hub 'l'
    CS_ethanol = CS_processing.sim(new_kg) #L
    
    #for k in range(0,len(locations)):
        # Refinery capex
        #if CS_refinery_kg[k] > 5:   #skip or remove
    # scale = CS_refinery_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file
    CS_refinery_capex = 400000000*(scale)**.6


    return [np.sum(CS_refinery_capex), CS_travel_opex]

a = test(DV,reduced_land_costs,reduced_C_yield,reduced_land_limits,dist_map,map_C2H,dist_C2H,locations,hubs)