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
# df_yield = pd.read_excel('normalized_63_year_corn_yield.xlsx',header=0,engine='openpyxl') #contains yearly yield data for corn in each ag_district
df_geo = pd.read_excel('combined_pivot_excel_LNG.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
cost = list(df_geo['CG_cost_per_ha'])
districts = list(df_geo['STASD_N']) # list of ag_district code

#specify grouping
groups = 20

#district-to-hub data
filename = 'AgD2H_48_cb.xlsx' # contains travel time and travel distance - these are not changed with year
df_D2H = pd.read_excel(filename,header=0, engine='openpyxl')
c = list(df_D2H['STASD_N']) # list of ag_district code in filename excel sheet 

#eliminate districts that don't appear in both lists - (US_ag_district_geodata contains each ag_district code in the USA but we want to use only corn belt)
for i in districts: # districts = whole list of ag_district 
    idx = districts.index(i)
    if i in c: # c = ag_dist code only located in corn belt
        pass
    else:
        df_geo = df_geo.drop(index=idx) #deleting the rest of the ag_district code where is located out of corn belt

df_geo = df_geo.reset_index(drop=True) # fixing the index number because we drop some of them and the numbers are not going by orderly. 
# fips = df_geo['fips'].values
districts = list(df_geo['STASD_N'])# new district list which is only contains corn belt ag_districts
land_costs = df_geo.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_geo['land_limits_ha'].values # county ag production area in acres
years = range(1958,2021)
listyears =[]

for year in years :
    listyears.append(str(year))

# Corn Grain yield
C_yield = df_geo.iloc[:,6:].values  #yield in bushels per acre


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
    
    # distance from each district to pre-defined hub
    dist_D2H.append(df_D2H.loc[df_D2H['STASD_N']==d,'travel_dist_km'].values[0])
    
    # list of hubs assigned to each district
    district_hubs.append(df_D2H.loc[df_D2H['STASD_N']==d,'destinationID'].values[0]) # the whole corn belt divided 18 hubs abd this defines which ag_dist found under which hub


# Pre-define location of refineries
# put a number > 0 and < number of hubs if desired; if not, problem defaults to full list of hubs
num_refineries = 0

#hub-to-hub data
filename = 'AgD_48g_H2H_cb.xlsx'
df_H2H = pd.read_excel(filename,header=0, engine='openpyxl')
hubs = list(df_H2H['OriginID'].unique()) # there is 18 hub 

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

map_D2H = np.zeros((len(districts), len(hubs))) # I don't understand what we are trying to define 

# convert look-up table to distance matrix #when 50 is indexed 49 is not valid because of missing hubs
for i in range(0,len(districts)):
    h = hubs.index(int(district_hubs[i])) # int(county_hubs[i]) - 1
    map_D2H[i,h] = 1    


#########################################################
# Identify quota as % of maximum theoretical production
import multiyear_quota
p=.25
Q, Q_min= multiyear_quota.QD(districts,locations)
quota = np.mean(Q)*p #quota in biomass in kilograms as opposed to ethanol

# FIX QUOTA TO BE MULTIYEAR
 
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
    CG_cultivation_capex = np.zeros((len(years, 1))) #not as single scalars. they need to be either vectors, or empty sets
    CG_cultivation_opex = np.zeros((len(years, 1))) #make them vectors of zeros
    CG_prod_total = np.zeros((len(years, 1)))
    # CS_travel_opex = np.zeros((len(years, 1)))
    
    # CS_flow_matrix = np.zeros((len(hubs),len(locations)))
    # CS_D2H_prod = np.zeros((num_c,num_h))
    # CS_flow = 0
    # CS_refinery_kg = 0
    # CS_ethanol = np.zeros((num_l,1))
    # CS_refinery_capex = 0

    # Capital costs (need to expand)
    L = np.array(LC) #$/acre
    v = np.array(vars)
        
    CG_cultivation_capex += np.sum(v[0:num_c]*(L+5977.4)) #  ha*$/acre
    # (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(Y) #kg/ha # kg_stover_per_ha =CS_per_ha #output $ 
    
    CG_cultivation_opex += np.sum((v[0:num_c]*(CG_cost_per_ha))) #herbicide in per ha??
    Constraints = [] # constraints
    
    for year in years:
        i = years.index(year)
        Y = C_Y[:,i]
        
        # Constraints = [] # constraints
        
        # Per ha values (need to expand) # this is where we would put in code from Jack 
        
        ##############################
        # Cultivation and Harvesting
    
        # Operating costs (need to expand)
        #harvesting = 38.31*ha_to_acre # $ per ha
        
        # d2h_map = np.array(D2H_map)
        # Automatic flow to pre-processing hub
        # CS_D2H_prod = d2h_map * np.transpose(np.array([(CS_per_ha * v[0:num_c])]*num_h)) #kg = kg*ha/ha
        CG_prod = np.sum(v[0:num_c]*Y)
        CG_prod_total[i] = CG_prod
        
        # CS_cultivation_opex += np.sum(CS_per_ha*v[0:num_c]*(lb_to_kg)*(1/1500)*0.50*D2H)
       
        # Cultivation constraints (land limits) #PUT OUTSIDE OF LOOP 
        # for i in range(0,len(LC)):
        #     Constraints.append(vars[i] - LL[i] - 5) #allow some slack in DVs
            
        # LL_cons = np.subtract(np.subtract(v[0:len(LC)], LL), 5)
        # Constraints.extend(LL_cons.tolist())
       
        ################################
            
        # ref = (len(LC) + (len(hubs) - 1)*len(locations) + (len(locations) - 1)) + 1
       
        # # Mass transfer (1Ms kg of CS) from hub 'j' to hub 'k'
        # CS_flow_matrix = v[num_c:].reshape((num_h,num_l)) #kg
        
        # Travel costs in bale-miles
        # CS_travel_opex = np.sum(DM*CS_flow_matrix*((lb_to_kg)*(1/1500)*0.50)) # km*kg*
        
        # #Flow to refinery
        # for j in range(0,len(hubs)):
            
        #     for k in range(0,len(locations)):
            
        #         # Mass transfer (1Ms kg of CS) from hub 'j' to hub 'k'
        #         CS_flow_matrix[j,k] = CS_flow_matrix[j,k] + vars[len(LC) + j*len(locations) + k] 
                
        #         # Travel costs in bale-miles
        #         CS_travel_opex += DM[j,k]*CS_flow_matrix[j,k]*(lb_to_kg)*(1/1500)*0.50 
    
        #for j in range(0,len(hubs)):
        # P = np.array(CS_C2H_prod)
        # F = np.array(CS_flow_matrix)
       
        # Hubs collect biomass from counties
        # CS_hub_kg = np.sum(CS_D2H_prod, axis=0) #kg
        
        # Transportation constraints (all delivery from hub 'j' must be <= mass produced)
        # CS_flow = np.sum(CS_flow_matrix, axis=1) #kg
        # flow_constraints = CS_flow - CS_hub_kg - 5 #allow some slack in DVs #kg
        
        # for j in range(0,len(hubs)):
        #     Constraints.append(flow_constraints[j]) 
        
        # Constraints.extend(flow_constraints.tolist())
        
        ###############################
        # Refinery
       
        #for k in range(0,len(locations)):
              
        # Find total mass received at hub 'l'
        # CS_refinery_kg = np.sum(CS_flow_matrix, axis=0) #kg
        
        # # Only allow plants above certain scale
        # filter_flows = np.array(list(map(int,(CS_refinery_kg/(5563*142))>1000)))
        # new_kg = filter_flows*CS_refinery_kg
        # scale = filter_flows*(CS_refinery_kg/(5563*142))
                
        # Ethanol produced at refinery at hub 'l'
        CG_ethanol = CS_processing.sim(CG_prod) #L
        # scale = CS_refinery_kg/(5563*142)
        
        # for k in range(0,len(locations)):
            # if scale[k] < 1000:
            #     CS_refinery_capex += 25000000*scale[k]
            # elif scale[k] >= 1000 and scale[k] < 5000:
            #     CS_refinery_capex += 12500000*scale[k]
            # elif scale[k] >= 5000 and scale[k] < 10000:
            #     CS_refinery_capex += 7500000*scale[k]    
            # else:
            #     CS_refinery_capex += 500000*scale[k] 
            
    
        # CS_refinery_capex = 400000000*(scale)**.6
        
        # Sets ethanol production quota (L)
        # Constraints.append(Q - np.sum(CS_ethanol)-5) #L
        # Constraints.append(sum(CS_ethanol)[0] - Q*1.05) #remove upper contraint 
        
        Z = []
        if (Q - CG_ethanol[year]) < 0:
       
            shortfall = 0
        
        else: 
            
            shortfall = Q - CG_ethanol[year] 
    
        Z.append(sum(shortfall))
        
    Constraints.append(Q*0.5 - sum(CG_prod))
    Constraints = list(Constraints)
        
    # Returns list of objectives, Constraints
    biomass_cost = (CG_cultivation_capex + CG_cultivation_opex*len(years))
    
    return [biomass_cost, np.sum(v[0:num_c])], Z, Constraints ##
    
#return [biomass_cost,   np.sum(v[0:num_c]), np.sum(CS_refinery_capex), CS_travel_opex], Constraints



# ####################################################################
# #########           MOEA EXECUTION          ########################
# ####################################################################

# # Number of variables, constraints, objectives
# g = np.size(land_costs)
# num_variables = g 
# num_constraints = 1 #+ g   #must match to contraints
# num_objs = 3

# # problem = Problem(num_variables,num_objs,num_constraints)
# # problem.types[0:g+1] = Real(0,max(reduced_land_limits))
# # problem.types[g+1:] = Real(0,UB )
# # problem.constraints[:] = "<=0"

# problem = Problem(num_variables,num_objs,num_constraints)
# for i in range(0,np.size(land_costs)):
#     problem.types[i] = Real(0,land_limits[i]+5)
# # problem.types[g:] = Real(0,UB+5)
# # problem.types[g:] = Real(0,UB*100)
# problem.constraints[:] = "<=0"

# #What function?
# problem.function = simulate

# # What algorithm?
# algorithm = GDE3(
#     problem=problem,
#     population_size=250,
#     )

# # Evaluate function # of times
# algorithm.run(5000)

# stop = time.time()
# elapsed = (stop - start)/60
# mins = str(elapsed) + ' minutes'
# print(mins)


# #####################################################################
# ##########           OUTPUTS                 ########################
# #####################################################################

# # solutions = [s for s in algorithm.result]

# solutions = [s for s in algorithm.result if s.feasible]

# D = np.zeros((len(solutions),num_variables))
# O = np.zeros((len(solutions),num_objs))

# for s in solutions:
    
#     idx = solutions.index(s)
#     # ax.scatter(s.objectives[0]/1000,s.objectives[1],s.objectives[2]*-1, c = 'red',alpha=0.5)

#     #record solution information
#     for i in range(0,num_variables):
#         D[idx,i] = s.variables[i]
#     for j in range(0,num_objs):
#         O[idx,j] = s.objectives[j]

# df_D = pd.DataFrame(D)
# fn = 'Decision_Variables_' + version + '.csv'
# df_D.to_csv(fn)

# df_O = pd.DataFrame(O)
# fn2 = 'Objective_functions_' + version + '.csv'
# df_O.to_csv(fn2)


# # # # find constraints that are violated
# # import constraint_test

# # df = pd.read_csv(fn,header=0,index_col=0)

# # LC = land_costs # land costs per county
# # C_Y = C_yield # corn yield per acre
# # LL = land_limits # land limits
# # DM = dist_map # hub to hub distances
# # D2H_map = map_D2H # binary matrix mapping counties (rows) to hubs (columns)
# # D2H = dist_D2H # county to hub distances
# # locations = locations #possible location of biorefineries,
# # hubs = hubs
# # Q = quota

# # violations = {}

# # for i in range(0,len(df)):
# #     DV = df.iloc[0,:] # take first solution
# #     [CS_refinery_capex, CS_travel_opex], Constraints = constraint_test.test(DV, LC, C_Y, LL, DM, D2H_map, D2H, locations, hubs, Q)
# #     C = []
# #     for j in range(0,len(Constraints)):
# #             if Constraints[j] > 0:
# #                 C.append(j)
# #     violations[i] = C
        
        