# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 17:54:50 2021

@author: tlpac
"""

from platypus import GDE3, Problem, Real 
import random
from random import randint
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation_V as CS_cultivation
import corn_stover_processing_V as CS_processing

start = time.time()
version = 'scale_filter_district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import district level data
df_geo = pd.read_excel('US_ag_district_geodata.xlsx',header=0, engine='openpyxl')
districts = list(df_geo['STASD_N'])

#specify grouping
groups = 20

#district-to-hub data
filename = 'AgD2H_48_cb.xlsx'
df_D2H = pd.read_excel(filename,header=0, engine='openpyxl')
c = list(df_D2H['STASD_N'])
AgD2H_flow = df_D2H['destinationID'].to_list()

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
filename = 'AgD_48g_H2H_cb.xlsx'
df_H2H = pd.read_excel(filename,header=0, engine='openpyxl')
hubs = list(df_H2H['OriginID'].unique())

r_idx = np.array(hubs) - 1
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


########################################################
# Identify quota as % of maximum theoretical production
import determine_quota_V_district
p=.05
quota, UB , v_test = determine_quota_V_district.QD(districts,locations,p)
quota = quota[0]
 
#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
lb_to_kg= 0.453515 # pounds to kilograms
kg_to_L_Ethanol = 1.273723

# NOTE: MAKE SURE OF CONVERSIONS BELOW -- VALUES ABOVE NOW APPEAR ALL IN ACRES
    
# # test function
# import f_test
# obj1,obj2,product = f_test.test(v,reduced_land_costs,reduced_C_yield,reduced_land_limits, dist_map,map_C2H,dist_C2H,locations,hubs,quota)

# simulation model (function to be evaluated by MOEA)
def simulate(
    
    
        vars, # cultivation hectares per county, hub-to-hub biomass flows
        LC = land_costs, # land costs per county
        C_Y = C_yield, # corn yield per acre
        LL = land_limits, # land limits
        DM = dist_map, # hub to hub distances
        D2H_map = map_D2H, # binary matrix mapping counties (rows) to hubs (columns)
        D2H = dist_D2H, # county to hub distances
        locations = locations, #possible location of biorefineries,
        hubs = hubs,
        Q = quota
        
        ):
    
    num_c = np.size(LC)
    num_h = np.size(hubs)
    num_l = np.size(locations)
    
    # Empty parameters 
    CS_cultivation_capex = 0 
    CS_cultivation_opex = 0
    CS_travel_opex = 0
    # CS_flow_matrix = np.zeros((len(hubs),len(locations)))
    CS_D2H_prod = np.zeros((num_c,num_h))
    CS_flow = 0
    CS_refinery_kg = 0
    CS_ethanol = np.zeros((num_l,1))
    CS_refinery_capex = 0
    
    Constraints = [] # constraints
    
    # Per ha values (need to expand)
    (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y) #kg/ha

    # Capital costs (need to expand)
    L = np.array(LC) #$/acre
    v = np.array(vars)
    
    CS_cultivation_capex += np.sum(v[0:num_c]*L) #  ha*$/acre
    
    ##############################
    # Cultivation and Harvesting

    # Operating costs (need to expand)
    harvesting = 38.31*ha_to_acre # $ per ha
    CS_cultivation_opex += np.sum((v[0:num_c]*(seeds_per_ha*.00185 + fertilization_per_ha[0]*0.55 + fertilization_per_ha[1]*0.46 + fertilization_per_ha[2]*0.50 + lime_per_ha*0.01 + harvesting))) #herbicide in per ha??
   
    d2h_map = np.array(D2H_map)
    # Automatic flow to pre-processing hub
    CS_D2H_prod = d2h_map * np.transpose(np.array([(CS_per_ha * v[0:num_c])]*num_h)) #kg = kg*ha/ha
    
    kg_stover = CS_per_ha*v[0:num_c]
    
    CS_travel_opex_d2h = pd.DataFrame(kg_stover*(lb_to_kg)*(1/1500)*0.50*D2H)
    
    CS_travel_opex_d2h['hub'] = AgD2H_flow
    
    CS_travel_opex_ih = CS_travel_opex_d2h.groupby(['hub']).agg({0: sum}).reset_index()
    
    flow_map = np.zeros((len(hubs), len(hubs))) #full matrix for hub to refinery  

    flow_map = np.array(dist_map)

    hub_dist = np.min(np.where(flow_map==0, flow_map.max(), flow_map), axis=1) #distance from each hub to closest refinery

    hub_dist[r_idx] = 0 #hubs that are choosen go to stay don't transfer

    df_hub_dist = pd.DataFrame(hub_dist) #dataframe of hub_dist

    hub_flow = np.argmin(np.where(flow_map==0, flow_map.max(), flow_map), axis=1) #index of closest refinery to hub   

    hub_flow[r_idx] = r_idx #hubs that are choosen don't transfer

    if num_refineries == 1: #argmin messes up at 1 refinery but this fixes it
        hub_flow[np.where(hub_flow == 0)] = r_idx
    else:
        pass
    
    
    
    AgD_c = pd.DataFrame(kg_stover)
    
    AgD_c['hub'] = AgD2H_flow #add list of closest hubs

    h_c_sum = AgD_c.groupby(['hub']).agg({0: sum}).reset_index() #amount of cultivation that is at each hub  

    hub_sum = h_c_sum.drop(columns=['hub']) #drop hub column
    
    
    CS_travel_opex_h2h = hub_sum*(lb_to_kg)*(1/1500)*0.50*np.array(df_hub_dist)
    
    CS_travel_opex = np.sum(np.array(CS_travel_opex_ih) + np.array(CS_travel_opex_h2h))
    
    ###############################
    CS_hub_kg = np.sum(CS_D2H_prod, axis=0) #kg
       
    ###############################
         
    # Ethanol produced at refinery at hub 'l'
    CS_ethanol = CS_processing.sim(CS_hub_kg) #L
    scale = CS_hub_kg/(5563*142)
    CS_refinery_capex = 400000000*((scale)**.6)
        
    # Sets ethanol production quota (L)
    Constraints.append(Q - np.sum(CS_ethanol)-5) #L
     
    Constraints = list(Constraints)
    
    # Returns list of objectives, Constraints
    return [np.sum(CS_refinery_capex), CS_travel_opex], Constraints


#####################################################################
##########           MOEA EXECUTION          ########################
#####################################################################

# Number of variables, constraints, objectives
g = np.size(land_costs)
num_variables = g #+ np.size(hubs) * np.size(locations)
num_constraints =  1 #+ np.size(hubs) + g   #must match to contraints
num_objs = 2

# problem = Problem(num_variables,num_objs,num_constraints)
# problem.types[0:g+1] = Real(0,max(reduced_land_limits))
# problem.types[g+1:] = Real(0,UB )
# problem.constraints[:] = "<=0"

problem = Problem(num_variables,num_objs,num_constraints)
for i in range(0,np.size(land_costs)):
    problem.types[i] = Real(0,land_limits[i]+5)
# problem.types[g:] = Real(0,UB+5)
#problem.types[g:] = Real(0,UB*100)
problem.constraints[:] = "<=0"

#What function?
problem.function = simulate

# What algorithm?
algorithm = GDE3(
    problem=problem,
    population_size=250,
    )

# Evaluate function # of times
algorithm.run(5000000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

# solutions = [s for s in algorithm.result]

solutions = [s for s in algorithm.result if s.feasible]

D = np.zeros((len(solutions),num_variables))
O = np.zeros((len(solutions),num_objs))

for s in solutions:
    
    idx = solutions.index(s)
    # ax.scatter(s.objectives[0]/1000,s.objectives[1],s.objectives[2]*-1, c = 'red',alpha=0.5)

    #record solution information
    for i in range(0,num_variables):
        D[idx,i] = s.variables[i]
    for j in range(0,num_objs):
        O[idx,j] = s.objectives[j]

df_D = pd.DataFrame(D)
fn = 'Decision_Variables_' + version + '_test.csv'
df_D.to_csv(fn)

df_O = pd.DataFrame(O)
fn2 = 'Objective_functions_' + version + '_test.csv'
df_O.to_csv(fn2)
