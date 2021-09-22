"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import GDE3, Problem, Real
import random
from random import randint
import pandas as pd
import numpy as np
import time
import corn_stover_processing_V as CS_processing

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import district level data
df_geo = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code 

districts = list(df_geo['STASD_N']) # list of ag_district code
land_costs = df_geo.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_geo['land_limits_ha'].values # county ag production area in acres
cost = list(df_geo['CG_cost_per_ha'])
C_yield = df_geo.iloc[:,8:].values  # Corn Grain yield as kg/ha

#specify grouping
groups = 20

#district-to-hub data
df_D2H = pd.read_excel('AgD2H_48_cb.xlsx',header=0, engine='openpyxl') # contains travel time and travel distance
c = list(df_D2H['STASD_N']) # list of ag_district code in filename excel sheet 

# Hub grouping information, distance look-up tables
dist_D2H = []
district_hubs = []
for d in districts:
    
    # distance from each district to pre-defined hub
    dist_D2H.append(df_D2H.loc[df_D2H['STASD_N']==d,'travel_dist_km'].values[0])
    
    # list of hubs assigned to each district
    district_hubs.append(df_D2H.loc[df_D2H['STASD_N']==d,'destinationID'].values[0]) # the whole corn belt divided 18 hubs abd this defines which ag_dist found under which hub

#hub-to-hub data
df_H2H =pd.read_excel('AgD_48g_H2H_cb.xlsx', header=0, engine='openpyxl')
hubs = list(df_H2H['OriginID'].unique()) # there is 18 hub 

years = range(1958,2021)
listyears =[]

for year in years :
    listyears.append(str(year))

########################################################################
#########        PRE-PROCESSING       ##################################
########################################################################

# put a number > 0 and < number of hubs if desired; if not, problem defaults to full list of hubs
num_refineries = 0
locations = hubs
    
################################
# Convert to function inputs

dist_map = np.zeros((len(hubs),len(locations))) #creating matrix for representing hub to hub distance as km

# convert look-up table to distance matrix
for i in range(0,len(hubs)):
    c1 = hubs[i]
    for j in range(0,len(locations)):
        c2 = locations[j]
        dist_map[i,j] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers'] 

map_D2H = np.zeros((len(districts), len(hubs))) # 107 district and 18 hubs 

# convert look-up table to distance matrix #when 50 is indexed 49 is not valid because of missing hubs
for i in range(0,len(districts)):
    h = hubs.index(int(district_hubs[i])) # int(county_hubs[i]) - 1
    map_D2H[i,h] = 1    # represnet which district located which hub 


# #########################################################
# # Identify quota as % of maximum theoretical production
# import multiyear_quota
# p=.05
# Q_min, Q_series = multiyear_quota.QD(districts,locations)
# quota = Q_min*p #quota in biomass in kilograms as opposed to ethanol

#########################################################
# Identify quota as % of maximum theoretical production
import deneme_quota
p=.05
quota, UB , v_test = deneme_quota.QD(districts,locations,p)
quota = quota[0]

#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################

def simulate(
    
    
        vars, # cultivation hectares per county, hub-to-hub biomass flows
        LC = land_costs, # land costs per county
        C_Y = C_yield, # corn yield kg/ha
        LL = land_limits, # land limits
        CG_cost_per_ha = cost,  #corn grain cost per hectare 
        DM = dist_map, # hub to hub distances
        D2H_map = map_D2H, # binary matrix mapping counties (rows) to hubs (columns)
        D2H = dist_D2H, # county to hub distances
        locations = locations, #possible location of biorefineries,
        hubs = hubs,
        Q = quota
        
        ):
    
    num_c = np.size(LC) #size of land cost 
    num_h = np.size(hubs) #size of hubs
    num_l = np.size(locations) #size of the locations 
     
     # Empty parameters 
    CG_cultivation_capex = 0 #not as single scalars. they need to be either vectors, or empty sets
    CG_cultivation_opex = 0 #make them vectors of zeros
    CG_prod_total = np.zeros((len(years), 1))
    CG_ethanol_total = np.zeros((len(years),1))
    # CS_travel_opex = np.zeros((len(years, 1)))

    # Capital costs (need to expand)
    L = np.array(LC) #$/acre
    v = np.array(vars)
    # v = np.ones((num_c,1))*100
        
    CG_cultivation_capex += np.sum(v[0:num_c]*(L+5977.4)) #  ha*$/acre
    # (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(Y) #kg/ha # kg_stover_per_ha =CS_per_ha #output $ 
    
    CG_cultivation_opex += np.sum((v[0:num_c]*(CG_cost_per_ha))) #herbicide in per ha??
    Constraints = [] # constraints
    
    Z = []
    
    for year in years:
        i = years.index(year)
        Y = C_Y[:,i]

        CG_prod = np.sum(v[0:num_c]*Y)
        CG_prod_total[i] = CG_prod
        
        
        ###############################
        # Refinery
        
        # Ethanol produced at refinery at hub 'l'
        CG_ethanol = CS_processing.sim(CG_prod) #L
        CG_ethanol_total[i] = CG_ethanol
        
        if (Q - CG_ethanol) < 0:
       
            shortfall = 0
        
        else: 
            
            shortfall = Q - CG_ethanol
    
        Z.append(shortfall)
        
    Constraints.append(Q*0.5 - min(CG_ethanol_total))
    Constraints = list(Constraints)
        
    # Returns list of objectives, Constraints
    biomass_cost = CG_cultivation_capex + CG_cultivation_opex
    min_shortfall = max(Z)
    return [biomass_cost, min_shortfall], Constraints ##

####################################################################
#########           MOEA EXECUTION          ########################
####################################################################

# Number of variables, constraints, objectives
g = np.size(land_costs)
num_variables = g 
num_constraints = 1 #+ g   #must match to contraints
num_objs = 2

# problem = Problem(num_variables,num_objs,num_constraints)
# problem.types[0:g+1] = Real(0,max(reduced_land_limits))
# problem.types[g+1:] = Real(0,UB )
# problem.constraints[:] = "<=0"

problem = Problem(num_variables,num_objs,num_constraints)
for i in range(0,np.size(land_costs)):
    problem.types[i] = Real(0,land_limits[i]+5)
# problem.types[g:] = Real(0,UB+5)
# problem.types[g:] = Real(0,UB*100)
problem.constraints[:] = "<=0"

#What function?
problem.function = simulate

# What algorithm?
algorithm = GDE3(
    problem=problem,
    population_size=100,
    )

# Evaluate function # of times
algorithm.run(5000)

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
fn = 'Decision_Variables_' + version + '.csv'
df_D.to_csv(fn)

df_O = pd.DataFrame(O)
fn2 = 'Objective_functions_' + version + '.csv'
df_O.to_csv(fn2)


# # # find constraints that are violated
# import constraint_test

# df = pd.read_csv(fn,header=0,index_col=0)

# LC = land_costs # land costs per county
# C_Y = C_yield # corn yield per acre
# LL = land_limits # land limits
# DM = dist_map # hub to hub distances
# D2H_map = map_D2H # binary matrix mapping counties (rows) to hubs (columns)
# D2H = dist_D2H # county to hub distances
# locations = locations #possible location of biorefineries,
# hubs = hubs
# Q = quota

# violations = {}

# for i in range(0,len(df)):
#     DV = df.iloc[0,:] # take first solution
#     [CS_refinery_capex, CS_travel_opex], Constraints = constraint_test.test(DV, LC, C_Y, LL, DM, D2H_map, D2H, locations, hubs, Q)
#     C = []
#     for j in range(0,len(Constraints)):
#             if Constraints[j] > 0:
#                 C.append(j)
#     violations[i] = C
        
        
