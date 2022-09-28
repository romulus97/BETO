# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:03:00 2021

@author: Ece Ari Akdemir
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
import Pyrol_processing as G_processing 
import Algal_Oil as A_processing

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_corn_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae = pd.read_excel('combined_pivot_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   

df_geo_corn_GHG= pd.read_excel('Corn_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from corn
df_geo_soy_GHG = pd.read_excel('Soy_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from soy
df_geo_grass_GHG = pd.read_excel('Switchgrass_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from grass
df_geo_algae_GHG = pd.read_excel('Algae_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from algae

df_geo_corn_MFSP = pd.read_excel('Corn_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from corn
df_geo_soy_MFSP = pd.read_excel('Soy_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from soy
df_geo_grass_MFSP = pd.read_excel('Switchgrass_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from grass
df_geo_algae_MFSP = pd.read_excel('Algae_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from algae


# #Emission 
# # Corn
# Corn_emission= df_geo_corn_GHG.loc[:,1998:2013].values  #gCO2/MJ
# Corn_cost= df_geo_corn_MFSP.loc[:,1998:2013].values  #$/MJ

# # Soybean
# Soy_emission = df_geo_soy_GHG.loc[:,1998:2013].values  #gCO2/MJ
# Soy_cost = df_geo_soy_MFSP.loc[:,1998:2013].values    #$/MJ

# # Switchgrass
# Grass_emission = df_geo_grass_GHG.loc[:,1998:2013].values  #gCO2/MJ
# Grass_cost = df_geo_grass_MFSP.loc[:,1998:2013].values    #$/MJ

# # Algae
# Algae_emission = df_geo_algae_GHG.loc[:,1998:2013].values  #gCO2/MJ
# Algae_cost = df_geo_algae_MFSP.loc[:,1998:2013].values    #$/MJ

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
marginal_land_costs = df_geo_grass.loc[:,'land_costs-$/ha'].values # $ per ha
marginal_land_limits = df_geo_grass['land_limits_ha'].values # county ag production area in acres


years = range(1998,2014)
listyears =[]

for year in years :
    listyears.append(str(year))

# Corn Grain yield
C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algae yield
A_yield = df_geo_algae.loc[:,1998:2013].values  #yield in kg/ha


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
import multiyear_quota_energy
p=.1
Q_min, Q_series = multiyear_quota_energy.QD(districts,locations)
quota = Q_min*p #quota in biomass in kilograms as opposed to ethanol

# FIX QUOTA TO BE MULTIYEAR
 
#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################   

def simulate(
 
        vars, # cultivation hectares per county for corn, hub-to-hub biomass flows
        LC = land_costs, # land costs per county
        MLC = marginal_land_costs,
        C_Y = C_yield, # corn yield per acre
        S_Y = S_yield,  # soybean yield per acre  
        G_Y = G_yield,
        A_Y = A_yield,
        LL = land_limits, # land limits
        MLL = marginal_land_limits, 
        DM = dist_map, # hub to hub distances
        D2H_map = map_D2H, # binary matrix mapping counties (rows) to hubs (columns)
        D2H = dist_D2H, # county to hub distances
        locations = locations, #possible location of biorefineries,
        hubs = hubs,
        Q = quota
        
        ):
    
    num_c = np.size(LC) #size of land cost 
    # num_h = np.size(hubs) #size of hubs
    # num_l = np.size(locations) #size of the locations 
     
    CG_prod_nt_d = np.zeros((len(years),107))
    SB_prod_nt_d = np.zeros((len(years),107))
    G_prod_nt_d = np.zeros((len(years),107))
    A_prod_nt_d = np.zeros((len(years),107))
    
    CG_ethanol_nt_d = np.zeros((len(years),107))
    SB_oil_nt_d = np.zeros((len(years),107))
    G_energy_nt_d = np.zeros((len(years),107))
    A_energy_nt_d = np.zeros((len(years),107))
    
    GHG_emission_corn_yearly = np.zeros((len(years),107))
    GHG_emission_soy_yearly = np.zeros((len(years),107))
    GHG_emission_grass_yearly = np.zeros((len(years),107))
    GHG_emission_algae_yearly = np.zeros((len(years),107))
    
    MFSP_corn_yearly = np.zeros((len(years),107))
    MFSP_soy_yearly = np.zeros((len(years),107))
    MFSP_grass_yearly = np.zeros((len(years),107))
    MFSP_algae_yearly = np.zeros((len(years),107))
     
    CG_prod_total = np.zeros((len(years), 1))
    CG_ethanol_total = np.zeros((len(years),1))
    SB_prod_total = np.zeros((len(years), 1))
    SB_oil_total = np.zeros((len(years),1))
    G_prod_total = np.zeros((len(years), 1))
    G_energy_total = np.zeros((len(years),1))
    A_prod_total = np.zeros((len(years), 1))
    A_energy_total = np.zeros((len(years),1))
    
    
    Energy_total = np.zeros((len(years),1))

    # L = np.array(LC) #$/acre
    # ML = np.array(MLC)
    vc = (np.array(vars[0:num_c]))/2
    vs = (np.array(vars[0:num_c]))/2
    vg = (np.array(vars[num_c:2*num_c])) 
    va = (np.array(vars[num_c*2:]))      # planted agricultural areas (ha)
    
    
    Constraints = [] # constraints
    
    Z = []
    A = 0
    
    for year in years:
        i = years.index(year)
        Y = C_Y[:,i]   # corn yield kg/ha
        S = S_Y[:,i]   # soy yield kg/ha
        G = G_Y[:,i]   # grass yield kg/ha
        Al = A_Y[:,i]   # algae yield kg/ha
        
        ##############################
        # Cultivation and Harvesting
    
        # Operating costs (need to expand)
        CG_prod_nt = (vc[0:num_c]*Y)
        CG_prod_nt_d[i] = CG_prod_nt       # corn kg bipmass production for each district and each year
        
        CG_prod = np.sum(vc[0:num_c]*Y)   
        CG_prod_total[i] = CG_prod         # total corn biomass production (kg)
        
        SB_prod_nt = (vs[0:num_c]*S)
        SB_prod_nt_d[i] = SB_prod_nt       # soy kg bipmass production for each district and each year
        
        SB_prod = np.sum(vs[0:num_c]*S)
        SB_prod_total[i] = SB_prod         # total soy biomass production (kg)    
        
        G_prod_nt = (vg[0:num_c]*G)
        G_prod_nt_d[i] = G_prod_nt       # soy kg bipmass production for each district and each year
        
        G_prod = np.sum(vg[0:num_c]*G)
        G_prod_total[i] = G_prod           # total grass biomass production (kg)
        
        A_prod_nt = (va[0:num_c]*Al)
        A_prod_nt_d[i] = A_prod_nt       # soy kg bipmass production for each district and each year        
        
        A_prod = np.sum(va[0:num_c]*Al)
        A_prod_total[i] = A_prod           # total algae biomass production (kg)
                
        # Ethanol and oil produced at refinery at hub 'l'
        CG_ethanol_nt = CG_processing.sim(CG_prod_nt)
        CG_ethanol_nt_d[i] = CG_ethanol_nt
        
        CG_ethanol = CG_processing.sim(CG_prod) #kg ethanol
        CG_ethanol_total[i] = CG_ethanol
        
        SB_oil_nt = CG_processing.sim(SB_prod_nt)
        SB_oil_nt_d[i] = SB_oil_nt
        
        SB_oil = SB_processing.sim(SB_prod)  #kg soy oil
        SB_oil_total[i] = SB_oil
        
        G_energy_nt = CG_processing.sim(G_prod_nt)
        G_energy_nt_d[i] = G_energy_nt
        
        G_energy = G_processing.sim(G_prod) # kg biocrude 
        G_energy_total[i] = G_energy
        
        A_energy_nt = CG_processing.sim(A_prod_nt)
        A_energy_nt_d[i] = A_energy_nt
        
        A_energy = A_processing.sim(A_prod) # kg algae oil
        A_energy_total[i] = A_energy
        
        Energy =(29.7 * CG_ethanol + 39.6 * SB_oil + 21* G_energy + 22 * A_energy)   # Ethanol * 29.7 MJ/kg + Soy Oil * 39.6 MJ/kg + biocrude * 21 MJ/kg + algae oil * 22 MJ/kg
        Energy_total[i] = Energy   # total energy MJ/yr
        
        
        corn_GHG = df_geo_corn_GHG[i]
        soy_GHG = df_geo_soy_GHG[i]
        grass_GHG = df_geo_grass_GHG[i]
        algae_GHG = df_geo_algae_GHG[i]
        
        GHG_emission_corn = corn_GHG*CG_ethanol_nt
        GHG_emission_corn_yearly[i] = GHG_emission_corn
        
        GHG_emission_soy = soy_GHG*SB_oil_nt
        GHG_emission_soy_yearly[i] = GHG_emission_soy
        
        GHG_emission_grass = grass_GHG*G_energy_nt
        GHG_emission_grass_yearly[i] = GHG_emission_grass
        
        GHG_emission_algae = algae_GHG*A_energy_nt
        GHG_emission_algae_yearly[i] = GHG_emission_algae
        
        GHG_impact = GHG_emission_corn + GHG_emission_soy + GHG_emission_grass +GHG_emission_algae
        
        corn_MFSP = df_geo_corn_MFSP[i]
        soy_MFSP = df_geo_soy_MFSP[i]
        grass_MFSP = df_geo_grass_MFSP[i]
        algae_MFSP = df_geo_algae_MFSP[i]
        
        MFSP_corn = corn_MFSP*CG_ethanol_nt
        MFSP_corn_yearly[i] = MFSP_corn
        
        MFSP_soy = soy_MFSP*SB_oil_nt
        MFSP_soy_yearly[i] = MFSP_soy
        
        MFSP_grass = grass_MFSP*G_energy_nt
        MFSP_grass_yearly[i] = MFSP_grass
        
        MFSP_algae = algae_MFSP*A_energy_nt
        MFSP_algae_yearly[i] = MFSP_algae
        
        MFSP_total = MFSP_corn + MFSP_soy + MFSP_grass +MFSP_algae
        
        
        if i > 0:
            A += abs(Energy_total[i] - Energy_total[i-1])
            
  
        if (Q - Energy) < 0:
     
            shortfall = 0
        
        else: 
            
            shortfall = Q - Energy
    
        Z.append(shortfall)
        
    
    # CG_prod_max_total = np.zeros((len(districts)))
    # SB_prod_max_total = np.zeros((len(districts)))
    # G_prod_max_total = np.zeros((len(districts)))
    # A_prod_max_total = np.zeros((len(districts)))
    
    
    # for i in districts: # districts = whole list of ag_district 
    #     idx = districts.index(i)
    #     Y_max = max(C_Y[idx,:]) # max corn yield kg/ha
    #     S_max = max(S_Y[idx,:] )  # soy yield kg/ha
    #     G_max = max(G_Y[idx,:])   # grass yield kg/ha
    #     Al_max = max(A_Y[idx,:])   # algae yield kg/ha
        
    #     CG_prod_max= np.sum(vc[idx]*Y_max) # max corn biomass (kg)
    #     SB_prod_max = np.sum(vs[idx]*S_max) # max soy biomass (kg)
    #     G_prod_max = np.sum(vg[idx]*G_max) # max grass biomass (kg)
    #     A_prod_max = np.sum(va[idx]*Al_max) # max algae biomass (kg)

    #     CG_prod_max_total[idx] = CG_prod_max * (0.284774923 + 0.02565) # corn max biomass * (capital cost + labor)
    #     SB_prod_max_total[idx] = SB_prod_max * (0.357131479 + 0.008339832) # soy max biomass * (capital cost + labor)
    #     G_prod_max_total[idx] = G_prod_max * (0.92) # grass max biomass * (capital cost)
    #     A_prod_max_total[idx] = A_prod_max * (1.6233249 + 0.0083398) # algae max biomass * (capital cost + labor)
        
    Constraints.append(Q * 0.98 - np.mean(Energy_total)) #LB 
    Constraints.append(np.mean(Energy_total) - Q * 1.02 ) #UB
    
    vt = vg[0:num_c] + va[0:num_c] - MLL[0:num_c]
    b = [0 if abc <=0 else 1 for abc in vt]
    c = sum(b)

    # # do boolean 
    # vg[0:num_c] + va[0:num_c] - MLL[0:num_c] #compare those element to element wise basis  
    
    
    Constraints.append(c)
    
    # Returns list of objectives, Constraints
    Constraints = list(Constraints)
    
        
    min_GHG = min(GHG_impact)
    min_shortfall = max(Z)
    min_MSFP = min(MFSP_total)
     
    ## just use cost as total 
    return [min_MSFP, min_shortfall, min_GHG], Constraints ##biomass cost unit $ - min shortfall unit MJ - min_GHG g CO2e
    
#return [biomass_cost,   np.sum(v[0:num_c]), np.sum(CS_refinery_capex), CS_travel_opex], Constraints

df_total_cost = pd.read_excel('total_land_cost.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
total_land_cost = list(df_total_cost['land_costs-$/ha'])
total_land_limit = list(df_total_cost['land_limits_ha'])


####################################################################
#########           MOEA EXECUTION          ########################
####################################################################

# Number of variables, constraints, objectives
g = np.size(total_land_cost)
num_variables = g # + np.size(marginal_land_costs)
num_constraints = 3 #+ g   #must match to contraints
num_objs = 3

# problem = Problem(num_variables,num_objs,num_constraints)
# problem.types[0:g+1] = Real(0,max(reduced_land_limits))
# problem.types[g+1:] = Real(0,UB )
# problem.constraints[:] = "<=0"

problem = Problem(num_variables,num_objs,num_constraints)

for i in range(0,np.size(total_land_cost)):
    problem.types[i] = Real(0,total_land_limit[i]+5)
# problem.types[g:] = Real(0,UB+5)
# problem.types[g:] = Real(0,UB*100)
problem.constraints[:] = "<=0"


#What function?
problem.function = simulate

# What algorithm?
algorithm = BorgMOEA(problem, epsilons=0.1)

# Evaluate function # of times
algorithm.run(10000)

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
fn = 'Decision_Variables_borg_two_crop_trial' + version + '.csv'
df_D.to_csv(fn)

df_O = pd.DataFrame(O)
fn2 = 'Objective_functions_borg_two_crop_trial' + version + '.csv'
df_O.to_csv(fn2)


        
        