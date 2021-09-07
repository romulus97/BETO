# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 14:55:57 2021

@author: Ece Ari Akdemir
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
# def simulate(
    
    
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

num_c = np.size(LC) #size of land cost 
num_h = np.size(hubs) #size of hubs
num_l = np.size(locations) #size of the locations 
 
 # Empty parameters 
CG_cultivation_capex = np.zeros((len(years), 1)) #not as single scalars. they need to be either vectors, or empty sets
CG_cultivation_opex = np.zeros((len(years), 1)) #make them vectors of zeros
CG_prod_total = np.zeros((len(years), 1))

# Capital costs (need to expand)
L = np.array(LC) #$/acre
v = np.array(vars)
    
CG_cultivation_capex += np.sum(v[0:num_c]*(L+5977.4)) #  ha*$/acre

CG_cultivation_opex += np.sum((v[0:num_c]*(CG_cost_per_ha))) #herbicide in per ha??
Constraints = [] # constraints

for year in years:
    i = years.index(year)
    Y = C_Y[:,i]
    
    CG_prod = np.sum(v[0:num_c]*Y)
    CG_prod_total[i] = CG_prod
            
    # Ethanol produced at refinery at hub 'l'
    CG_ethanol = CS_processing.sim(CG_prod) #L
    
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
shortfall_cost = Z

# return [biomass_cost, np.sum(v[0:num_c])], Z, Constraints ##
    
#return [biomass_cost,   np.sum(v[0:num_c]), np.sum(CS_refinery_capex), CS_travel_opex], Constraints