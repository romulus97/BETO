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
df_geo_grass_L = pd.read_excel('combined_pivot_land_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae_L = pd.read_excel('combined_pivot_land_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   
df_geo_algae = pd.read_excel('combined_pivot_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   

df_geo_corn_GHG= pd.read_excel('Corn_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from corn
df_geo_soy_GHG = pd.read_excel('Soy_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from soy
df_geo_grass_L_GHG = pd.read_excel('Switchgrass_L_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from grass
df_geo_grass_GHG = pd.read_excel('Switchgrass_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from grass
df_geo_algae_L_GHG = pd.read_excel('Algae_L_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from algae
df_geo_algae_GHG = pd.read_excel('Algae_GHG_power_sector.xlsx',header=0, engine='openpyxl') #yearly ghg emission as gCO2/MJ from algae

df_geo_corn_MFSP = pd.read_excel('Corn_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from corn
df_geo_soy_MFSP = pd.read_excel('Soy_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from soy
df_geo_grass_L_MFSP = pd.read_excel('Switchgrass_L_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from grass
df_geo_grass_MFSP = pd.read_excel('Switchgrass_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from grass
df_geo_algae_L_MFSP = pd.read_excel('Algae_L_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from algae
df_geo_algae_MFSP = pd.read_excel('Algae_MFSP.xlsx',header=0, engine='openpyxl') #yearly cost as $/MJ from algae


districts = list(df_geo_corn['STASD_N']) # list of ag_district code

# #specify grouping
# groups = 20

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

# land_costs = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_geo_corn['land_limits_ha'].values # county ag production area in acres
# marginal_land_costs = df_geo_grass.loc[:,'land_costs-$/ha'].values # $ per ha
marginal_land_limits_g = df_geo_grass['land_limits_ha'].values # county ag production area in acres
marginal_land_limits_a = df_geo_algae['land_limits_ha'].values # county ag production area in acres


years = range(1998,2014)
listyears =[]

for year in years :
    listyears.append(str(year))


# Corn Grain yield
C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha
Corn_emission= df_geo_corn_GHG.loc[:,1998:2013].values  #gCO2/MJ
Corn_cost= df_geo_corn_MFSP.loc[:,1998:2013].values  #$/MJ

# Soybean yield
S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha
Soy_emission = df_geo_soy_GHG.loc[:,1998:2013].values  #gCO2/MJ
Soy_cost = df_geo_soy_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass yield
G_yield_L = df_geo_grass_L.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission_L = df_geo_grass_L_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost_L = df_geo_grass_L_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission = df_geo_grass_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost = df_geo_grass_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield
A_yield_L = df_geo_algae_L.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission_L = df_geo_algae_L_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost_L = df_geo_algae_L_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield
A_yield = df_geo_algae.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission = df_geo_algae_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost = df_geo_algae_MFSP.loc[:,1998:2013].values    #$/MJ


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

#####################################################################
##########     DESIRED ENERGY CALCULATION    ########################
##################################################################### 

bg = 3 ## We will try 0, 3, 6, 9, 12, 15, 18, 20
bgg =  bg*10**9
con = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons
quota = bgg*con  ## energy as MJ/yr


#########################################################
# Identify quota as % of maximum theoretical production
# import multiyear_quota_energy
# p=.1
# Q_min, Q_series = multiyear_quota_energy.QD(districts,locations)
# quota = Q_min*p #quota in biomass in kilograms as opposed to ethanol



# FIX QUOTA TO BE MULTIYEAR
 
#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################   

def simulate(
 
        var, # cultivation hectares per county for corn, hub-to-hub biomass flows (ha)
        # LC = land_costs, # land costs per county ($/ha)
        # MLC = marginal_land_costs, # marginal land cost per county ($/ha)
        C_Y = C_yield, # corn yield per acre
        S_Y = S_yield,  # soybean yield per acre  
        G_Y_L = G_yield_L,
        G_Y = G_yield,
        A_Y_L = A_yield_L,
        A_Y = A_yield,
        C_emission = Corn_emission,
        S_emission = Soy_emission,
        G_emission_L = Grass_emission_L,
        G_emission = Grass_emission,
        A_emission_L = Algae_emission_L,
        A_emission = Algae_emission,
        C_cost = Corn_cost,
        S_cost = Soy_cost,
        G_cost_L = Grass_cost_L,
        G_cost = Grass_cost,
        A_cost_L = Algae_cost_L,
        A_cost = Algae_cost,
        LL = land_limits, # land limits
        MLLg = marginal_land_limits_g,
        MLLa = marginal_land_limits_a, 
        DM = dist_map, # hub to hub distances
        D2H_map = map_D2H, # binary matrix mapping counties (rows) to hubs (columns)
        D2H = dist_D2H, # county to hub distances
        locations = locations, #possible location of biorefineries,
        hubs = hubs,
        Q = quota
        
        ):
    
    num_c = np.size(LL) #size of land limit 
    # num_h = np.size(hubs) #size of hubs
    # num_l = np.size(locations) #size of the locations 
     
    CG_prod_nt_d = np.zeros((len(years),107))
    SB_prod_nt_d = np.zeros((len(years),107))
    G_prod_nt_d_L = np.zeros((len(years),107))
    G_prod_nt_d = np.zeros((len(years),107))
    A_prod_nt_d_L = np.zeros((len(years),107))
    A_prod_nt_d = np.zeros((len(years),107))
    
    CG_ethanol_nt_d = np.zeros((len(years),107))
    SB_oil_nt_d = np.zeros((len(years),107))
    G_energy_nt_d_L = np.zeros((len(years),107))
    G_energy_nt_d = np.zeros((len(years),107))
    A_energy_nt_d_L = np.zeros((len(years),107))
    A_energy_nt_d = np.zeros((len(years),107))
    
    GHG_emission_corn_yearly = np.zeros((len(years),107))
    GHG_emission_soy_yearly = np.zeros((len(years),107))
    GHG_emission_grass_yearly_L = np.zeros((len(years),107))
    GHG_emission_grass_yearly = np.zeros((len(years),107))
    GHG_emission_algae_yearly_L = np.zeros((len(years),107))
    GHG_emission_algae_yearly = np.zeros((len(years),107))
    GHG_impact_yearly = np.zeros((len(years),107))
    
    MFSP_corn_yearly = np.zeros((len(years),107))
    MFSP_soy_yearly = np.zeros((len(years),107))
    MFSP_grass_yearly_L = np.zeros((len(years),107))
    MFSP_grass_yearly = np.zeros((len(years),107))
    MFSP_algae_yearly_L = np.zeros((len(years),107))
    MFSP_algae_yearly = np.zeros((len(years),107))
    MFSP_total_yearly = np.zeros((len(years),107))

    Energy_total = np.zeros((len(years),1))

    vc = (np.array(var[0:num_c]))/2
    vs = (np.array(var[0:num_c]))/2
    vg_L = (np.array(var[0:num_c]))
    va_L = (np.array(var[0:num_c]))     
    vg = (np.array(var[num_c:2*num_c]))  
    va = (np.array(var[num_c*2:]))      # planted agricultural areas (ha)
    
    
    Constraints = [] # constraints
    
    Z = []
    GHG=[]
    MFSP=[]
    Energy_f=[]
    A = 0
    
    for year in years:
        i = years.index(year)
        Y = C_Y[:,i]   # corn yield kg/ha
        S = S_Y[:,i]   # soy yield kg/ha
        G_L = G_Y_L[:,i]   # grass yield kg/ha
        G = G_Y[:,i]   # grass yield kg/ha
        Al_L = A_Y_L[:,i]   # algae yield kg/ha
        Al = A_Y[:,i]   # algae yield kg/ha
        
        corn_GHG = C_emission[:,i]  # gco2/MJ
        soy_GHG = S_emission[:,i]
        grass_GHG_L = G_emission_L[:,i]
        grass_GHG = G_emission[:,i]
        algae_GHG_L = A_emission_L[:,i]
        algae_GHG = A_emission[:,i]
        
                
        corn_MFSP = C_cost[:,i]
        soy_MFSP = S_cost[:,i]
        grass_MFSP_L = G_cost_L[:,i]
        grass_MFSP = G_cost[:,i]
        algae_MFSP_L = A_cost_L[:,i]
        algae_MFSP = A_cost[:,i]
        
        ##############################
        # Cultivation and Harvesting
    
        # Operating costs (need to expand)
        CG_prod_nt = vc[0:num_c]*Y
        CG_prod_nt_d[i] = CG_prod_nt       # corn kg bipmass production for each district and each year
        
        
        SB_prod_nt = vs[0:num_c]*S
        SB_prod_nt_d[i] = SB_prod_nt       # soy kg bipmass production for each district and each year
        
        
        G_prod_nt_L = vg_L[0:num_c]*G_L
        G_prod_nt_d_L[i] = G_prod_nt_L       # grass kg bipmass production for each district and each year
        
        
        G_prod_nt = vg[0:num_c]*G
        G_prod_nt_d[i] = G_prod_nt       # grass kg bipmass production for each district and each year
        
        
        A_prod_nt_L = va_L[0:num_c]*Al_L
        A_prod_nt_d_L[i] = A_prod_nt_L       # algae kg bipmass production for each district and each year    
        
        
        A_prod_nt = va[0:num_c]*Al
        A_prod_nt_d[i] = A_prod_nt       # algae kg bipmass production for each district and each year        
        
                
        # Ethanol and oil produced at refinery at hub 'l'
        CG_ethanol_nt = CG_processing.sim(CG_prod_nt) #kg ethanol for a year for each district 
        CG_ethanol_nt_d[i] = CG_ethanol_nt
        

        SB_oil_nt = SB_processing.sim(SB_prod_nt) #kg soy oil for a year for each district 
        SB_oil_nt_d[i] = SB_oil_nt
        

        
        G_energy_nt_L = G_processing.sim(G_prod_nt_L) #kg biocrude for a year for each district 
        G_energy_nt_d_L[i] = G_energy_nt_L
        
        
        G_energy_nt = G_processing.sim(G_prod_nt) #kg biocrude for a year for each district 
        G_energy_nt_d[i] = G_energy_nt
        

        
        A_energy_nt_L = A_processing.sim(A_prod_nt_L)  #kg algae oil for a year for each district 
        A_energy_nt_d_L[i] = A_energy_nt_L
        

        
        A_energy_nt = A_processing.sim(A_prod_nt)  #kg algae oil for a year for each district 
        A_energy_nt_d[i] = A_energy_nt
        

        
        Energy =sum((29.7 * CG_ethanol_nt) + (39.6 * SB_oil_nt) + (21* G_energy_nt_L) + (21* G_energy_nt) + (22 * A_energy_nt_L) + (22 * A_energy_nt))   # Ethanol * 29.7 MJ/kg + Soy Oil * 39.6 MJ/kg + biocrude * 21 MJ/kg + algae oil * 22 MJ/kg
        Energy_total[i] = Energy   # total energy MJ/yr
        Energy_f.append(Energy)
        
        GHG_emission_corn = np.sum(corn_GHG * (29.7 * CG_ethanol_nt))
        GHG_emission_corn_yearly[i] = GHG_emission_corn
        
        GHG_emission_soy = np.sum(soy_GHG * (39.6 * SB_oil_nt))
        GHG_emission_soy_yearly[i] = GHG_emission_soy
        
        GHG_emission_grass_L = np.sum(grass_GHG_L * (21* G_energy_nt_L))
        GHG_emission_grass_yearly_L[i] = GHG_emission_grass_L
        
        GHG_emission_grass = np.sum(grass_GHG * (21* G_energy_nt))
        GHG_emission_grass_yearly[i] = GHG_emission_grass
        
        GHG_emission_algae_L = np.sum(algae_GHG_L * (22 * A_energy_nt_L))
        GHG_emission_algae_yearly_L[i] = GHG_emission_algae_L
        
        GHG_emission_algae = np.sum(algae_GHG * (22 * A_energy_nt))
        GHG_emission_algae_yearly[i] = GHG_emission_algae
        
        GHG_impact = (GHG_emission_corn + GHG_emission_soy + GHG_emission_grass_L + GHG_emission_grass + GHG_emission_algae_L + GHG_emission_algae)/Energy
        GHG_impact_yearly[i] = GHG_impact
        
        GHG.append(GHG_impact)
        
        MFSP_corn = np.sum(corn_MFSP* (29.7 * CG_ethanol_nt))
        MFSP_corn_yearly[i] = MFSP_corn
        
        MFSP_soy = np.sum(soy_MFSP* (39.6 * SB_oil_nt))
        MFSP_soy_yearly[i] = MFSP_soy
        
        MFSP_grass_L = np.sum(grass_MFSP_L* (21* G_energy_nt_L))
        MFSP_grass_yearly_L[i] = MFSP_grass_L
        
        MFSP_grass = np.sum(grass_MFSP* (21* G_energy_nt))
        MFSP_grass_yearly[i] = MFSP_grass
        
        MFSP_algae_L = np.sum(algae_MFSP_L* (22 * A_energy_nt_L))
        MFSP_algae_yearly_L[i] = MFSP_algae_L
        
        MFSP_algae = np.sum(algae_MFSP* (22 * A_energy_nt))
        MFSP_algae_yearly[i] = MFSP_algae
        
        MFSP_total = (MFSP_corn + MFSP_soy + MFSP_grass_L + MFSP_grass + MFSP_algae_L + MFSP_algae)/Energy
        MFSP_total_yearly[i] = MFSP_total
        
        MFSP.append(MFSP_total)
        
        
        # if i > 0:
        #     A += abs(Energy_total[i] - Energy_total[i-1])
            
  
        if (Q - Energy) < 0:
     
            shortfall = 0
        
        else: 
            
            shortfall = Q - Energy
    
        Z.append(shortfall)


        
    Constraints.append(Q * 0.98 - np.mean(Energy_total)) #LB 
    Constraints.append(np.mean(Energy_total) - Q * 1.02 ) #UB

    
    vt = vc[0:num_c] + vs[0:num_c] + vg_L[0:num_c] + va_L[0:num_c] - LL[0:num_c]
    b = [0 if abc <=0 else 1 for abc in vt]
    c = sum(b)
    
    Constraints.append(c)
    
    vk = vc[0:num_c] - vs[0:num_c] 
    k = [0 if abc <=0 else 1 for abc in vk]
    l = sum(k)

    
    Constraints.append(l)
    
    # Returns list of objectives, Constraints
    Constraints = list(Constraints)
    
    min_MSFP = sum(MFSP)/len(MFSP)   
    min_shortfall = max(Z)
    min_GHG = sum(GHG)/len(GHG)
    min_energy = sum(Energy_f)/len(Energy_f)
    
    
     
    ## just use cost as total 
    return [min_MSFP, min_shortfall, min_GHG, min_energy], Constraints ##biomass cost unit $ - min shortfall unit MJ - min_GHG g CO2e
    
#return [biomass_cost,   np.sum(v[0:num_c]), np.sum(CS_refinery_capex), CS_travel_opex], Constraints

df_total_cost = pd.read_excel('total_land_limit.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
# total_land_cost = list(df_total_cost['land_costs-$/ha'])
total_land_limit = list(df_total_cost['land_limits_ha'])


####################################################################
#########           MOEA EXECUTION          ########################
####################################################################

# Number of variables, constraints, objectives
g = np.size(total_land_limit)
num_variables = g # + np.size(marginal_land_costs)
num_constraints = 4 #+ g   #must match to contraints
num_objs = 4

# problem = Problem(num_variables,num_objs,num_constraints)
# problem.types[0:g+1] = Real(0,max(reduced_land_limits))
# problem.types[g+1:] = Real(0,UB )
# problem.constraints[:] = "<=0"

problem = Problem(num_variables,num_objs,num_constraints)

for i in range(0,np.size(total_land_limit)):
    problem.types[i] = Real(0,total_land_limit[i]+5)
# problem.types[g:] = Real(0,UB+5)
# problem.types[g:] = Real(0,UB*100)
problem.constraints[:] = "<=0"


#What function?
problem.function = simulate

# What algorithm?
algorithm = BorgMOEA(problem, epsilons=0.1)

# Evaluate function # of times
algorithm.run(1)

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
fn = 'Decision_Variables_borg_crops_GHG_0.98' + version + '.csv'
df_D.to_csv(fn)

df_O = pd.DataFrame(O)
fn2 = 'Objective_functions_borg_crops_GHG_0.98' + version + '.csv'
df_O.to_csv(fn2)


        
        