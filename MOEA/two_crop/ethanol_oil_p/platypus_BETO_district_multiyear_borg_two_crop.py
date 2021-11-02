"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import GDE3, Problem, Real
from pyborg import BorgMOEA
import random
from random import randint
import pandas as pd
import numpy as np
import time
import corn_grain_processing as CG_processing
import soybean_processing as SB_processing 


start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

df_geo_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code 

cost_corn = list(df_geo_corn['CG_cost_per_ha'])
cost_soy = list(df_geo_soy['SB_cost_per_ha'])
cost_soy_kg = list(df_geo_soy['SB_cost_per_kg'])
districts = list(df_geo_corn['STASD_N']) # list of ag_district code

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
        df_geo_corn = df_geo_corn.drop(index=idx) #deleting the rest of the ag_district code where is located out of corn belt

df_geo_corn = df_geo_corn.reset_index(drop=True) # fixing the index number because we drop some of them and the numbers are not going by orderly. 

for k in districts: # districts = whole list of ag_district 
    idxs = districts.index(k)
    if k in c: # c = ag_dist code only located in corn belt
        pass
    else:
        df_geo_soy = df_geo_soy.drop(index=idxs) #deleting the rest of the ag_district code where is located out of corn belt

df_geo_soy = df_geo_soy.reset_index(drop=True) # fixing the index number because we drop some of them and the numbers are not going by orderly. 

districts = list(df_geo_corn['STASD_N'])# new district list which is only contains corn belt ag_districts
land_costs = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_geo_corn['land_limits_ha'].values # county ag production area in acres
years = range(1960,2021)
listyears =[]

for year in years :
    listyears.append(str(year))

# Corn Grain yield
C_yield = df_geo_corn.iloc[:,13:].values  #yield in bushels per acre

# Soybean yield
S_yield = df_geo_soy.iloc[:,12:].values  #yield in bushels per acre


########################################################################
#########        PRE-PROCESSING       ##################################
########################################################################

################################
# Convert to function inputs

# Hub grouping information, distance look-up tables
dist_D2H = []
district_hubs = []
for d in districts:
    
    # idx = districts.index(d)
    
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
p=.05
Q_min, Q_series = multiyear_quota.QD(districts,locations)
quota = Q_min*p #quota in biomass in kilograms as opposed to ethanol


import multiyear_quota_soy
ps=.05
Q_S_min, Q_S_series = multiyear_quota_soy.QD(districts,locations)
quota_S = Q_S_min*ps #quota in biomass in kilograms as opposed to soy oil

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
        S_Y = S_yield,  # soybean yield per acre  
        LL = land_limits, # land limits
        CG_cost_per_ha = cost_corn,  #corn grain cost per hectare 
        SB_cost_per_ha = cost_soy, # soy bean cost per hectare 
        SB_cost_per_kg = cost_soy_kg, # soy bean cost per kg
        DM = dist_map, # hub to hub distances
        D2H_map = map_D2H, # binary matrix mapping counties (rows) to hubs (columns)
        D2H = dist_D2H, # county to hub distances
        locations = locations, #possible location of biorefineries,
        hubs = hubs,
        Q = quota,
        Q_S = quota_S
        
        ):
    
    num_c = np.size(LC) #size of land cost 
    num_h = np.size(hubs) #size of hubs
    num_l = np.size(locations) #size of the locations 
     
      # Empty parameters 
    CG_cultivation_capex = 0 #not as single scalars. they need to be either vectors, or empty sets
    SB_cultivation_capex = 0
    CG_cultivation_opex = 0 #make them vectors of zeros
    SB_cultivation_opex = 0
    CG_prod_total = np.zeros((len(years), 1))
    CG_ethanol_total = np.zeros((len(years),1))
    SB_prod_total = np.zeros((len(years), 1))
    SB_oil_total = np.zeros((len(years),1))

    # Capital costs (need to expand)
    L = np.array(LC) #$/acre
    vc = np.array(vars)/2
    vs = np.array(vars)/2
    # v = np.ones((num_c,1))*100
        
    CG_cultivation_capex += np.sum(vc[0:num_c]*(L+5977.4)) #  ha*$/acre (land cost+capital cost)*land usage
    SB_cultivation_capex += np.sum(vs[0:num_c]*(L+6817)) #  ha*$/acre land cost is not change for any feedstock
    # (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(Y) #kg/ha # kg_stover_per_ha =CS_per_ha #output $ 
    
    CG_cultivation_opex += np.sum((vc[0:num_c]*(CG_cost_per_ha))) #
    SB_cultivation_opex += np.sum((vs[0:num_c]*(SB_cost_per_ha)))
    Constraints = [] # constraints
    
    Z = []
    Z_S = []
    A = 0
    B = 0
    
    for year in years:
        i = years.index(year)
        Y = C_Y[:,i]
        S = S_Y[:,i]
        
        # Constraints = [] # constraints
        
        # Per ha values (need to expand) # this is where we would put in code from Jack 
        
        ##############################
        # Cultivation and Harvesting
    
        # Operating costs (need to expand)
        CG_prod = np.sum(vc[0:num_c]*Y)
        CG_prod_total[i] = CG_prod
        SB_prod = np.sum(vs[0:num_c]*S)
        SB_prod_total[i] = SB_prod
        
                
        # Ethanol and oil produced at refinery at hub 'l'
        CG_ethanol = CG_processing.sim(CG_prod) #L
        CG_ethanol_total[i] = CG_ethanol
        
        SB_oil = SB_processing.sim(SB_prod) #L
        SB_oil_total[i] = SB_oil
        
        if i > 0:
            A += abs(CG_ethanol_total[i] - CG_ethanol_total[i-1])
            
        if i > 0:
            B += abs(SB_oil_total[i] - SB_oil_total[i-1])
            
     
            
        
        if (Q - CG_ethanol) < 0:
       
            shortfall = 0
        
        else: 
            
            shortfall = Q - CG_ethanol
    
        Z.append(shortfall)
        
        
        
        if (Q_S - SB_oil) < 0:
       
            shortfall_soy = 0
        
        else: 
            
            shortfall_soy = Q_S - SB_oil
    
        Z_S.append(shortfall_soy)
        
    
    CG_cultivation_opex += np.sum((vc[0:num_c]*(CG_cost_per_ha))) #
    SB_cultivation_opex += np.sum(((vs[0:num_c]*(SB_cost_per_ha))) +((SB_prod_total*(SB_cost_per_kg))))
    
    
    # Constraints.append(Q*0.5 - min(CG_ethanol_total))
    Constraints.append(Q * 0.98 - np.mean(CG_ethanol_total)) #LB for corn
    Constraints.append(np.mean(CG_ethanol_total) - Q * 1.02 ) #UB for corn
    
    Constraints.append(Q_S * 0.98 - np.mean(SB_oil_total)) #LB for soy 
    Constraints.append(np.mean(SB_oil_total) - Q_S * 1.02 ) #UB for soy 
    
    Constraints = list(Constraints)
        
    # Returns list of objectives, Constraints
    biomass_cost_corn = CG_cultivation_capex + CG_cultivation_opex
    min_shortfall_corn = max(Z)
    biomass_cost_soy = SB_cultivation_capex + SB_cultivation_opex
    min_shortfall_soy = max(Z_S)
    return [biomass_cost_corn, min_shortfall_corn, A, biomass_cost_soy, min_shortfall_soy, B], Constraints ##
    
#return [biomass_cost,   np.sum(v[0:num_c]), np.sum(CS_refinery_capex), CS_travel_opex], Constraints



####################################################################
#########           MOEA EXECUTION          ########################
####################################################################

# Number of variables, constraints, objectives
g = np.size(land_costs)
num_variables = g 
num_constraints = 4 #+ g   #must match to contraints
num_objs = 6

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
algorithm = BorgMOEA(problem, epsilons=0.1)

# Evaluate function # of times
algorithm.run(100000)

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
fn = 'Decision_Variables_borg_two_crop' + version + '.csv'
df_D.to_csv(fn)

df_O = pd.DataFrame(O)
fn2 = 'Objective_functions_borg_two_crop' + version + '.csv'
df_O.to_csv(fn2)

        
        
