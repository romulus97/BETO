# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 21:30:22 2023

@author: eari
"""

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

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# Yields and land limits : contains State - STASD_N - land_limits_ha - yields (1998-2013)
df_geo_corn = pd.read_excel('combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
df_geo_soy = pd.read_excel('combined_pivot_Soy.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG = pd.read_excel('combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML = pd.read_excel('combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG = pd.read_excel('combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl')   
df_geo_algae_ML = pd.read_excel('combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl')  


# Greenhouse gas emission : contains State - STASD_N - greenhouse gas emission (gCO2/MJ) (1998-2013)
df_geo_corn_GHG= pd.read_excel('Corn_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_soy_GHG = pd.read_excel('Soy_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_grass_AG_GHG = pd.read_excel('Switchgrass_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML_GHG = pd.read_excel('Switchgrass_ML_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG_GHG = pd.read_excel('Algae_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_GHG = pd.read_excel('Algae_ML_GHG.xlsx',header=0, engine='openpyxl')


# Minimum fuel selling price (MFSP) : contains State - STASD_N - MFSP ($/MJ) (1998-2013)
df_geo_corn_MFSP = pd.read_excel('Corn_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_soy_MFSP = pd.read_excel('Soy_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG_MFSP = pd.read_excel('Switchgrass_AG_MFSP.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML_MFSP = pd.read_excel('Switchgrass_ML_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG_MFSP = pd.read_excel('Algae_AG_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_MFSP = pd.read_excel('Algae_ML_MFSP.xlsx',header=0, engine='openpyxl')



# # Districts (list of district as STASD_N code)
# districts = list(df_geo_corn['STASD_N'])

# Land limits (list of land limits for each district) as hectare
agricultural_land_limits = df_geo_corn['land_limits_ha'].values
marginal_land_limits_grass = df_geo_grass_ML['land_limits_ha'].values
marginal_land_limits_algae = df_geo_algae_ML['land_limits_ha'].values

# Year range from 1998 to 2013 
years = range(1998,2014)
listyears =[]

for year in years :
    listyears.append(str(year))


# Corn Grain values 
C_yield = df_geo_corn.loc[:,1998:2013].values  #kg/ha
Corn_emission= df_geo_corn_GHG.loc[:,1998:2013].values  #gCO2/MJ
Corn_cost= df_geo_corn_MFSP.loc[:,1998:2013].values  #$/MJ

# Soybean values
S_yield = df_geo_soy.loc[:,1998:2013].values  #kg/ha
Soy_emission = df_geo_soy_GHG.loc[:,1998:2013].values  #gCO2/MJ
Soy_cost = df_geo_soy_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass values for marginal lands 
G_yield_AG = df_geo_grass_AG.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission_AG = df_geo_grass_AG_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost_AG = df_geo_grass_AG_MFSP.loc[:,1998:2013].values    #$/MJ

# Grass yield
G_yield_ML = df_geo_grass_ML.loc[:,1998:2013].values  #yield in kg/ha
Grass_emission_ML = df_geo_grass_ML_GHG.loc[:,1998:2013].values  #gCO2/MJ
Grass_cost_ML = df_geo_grass_ML_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield
A_yield_AG = df_geo_algae_AG.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission_AG = df_geo_algae_AG_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost_AG = df_geo_algae_AG_MFSP.loc[:,1998:2013].values    #$/MJ

# Algae yield
A_yield_ML = df_geo_algae_ML.loc[:,1998:2013].values  #yield in kg/ha
Algae_emission_ML = df_geo_algae_ML_GHG.loc[:,1998:2013].values  #gCO2/MJ
Algae_cost_ML = df_geo_algae_ML_MFSP.loc[:,1998:2013].values    #$/MJ


#####################################################################
##########     DESIRED ENERGY CALCULATION    ########################
##################################################################### 

bg = 15 ## We will try 0, 3, 6, 9, 12, 15, 18, 20   biofuel gallon 
bgg =  bg*10**9  # conversion to billion  
con = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons   ## jet fuels conversion
quota = bgg*con  ## energy as MJ/yr


#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################   

def simulate(
 
        vars, # cultivation hectares per county for corn, hub-to-hub biomass flows (ha)
        C_Y = C_yield,
        S_Y = S_yield,  
        G_Y_AG = G_yield_AG,
        G_Y_ML = G_yield_ML,
        A_Y_AG = A_yield_AG,
        A_Y_ML = A_yield_ML,
        C_emission = Corn_emission,
        S_emission = Soy_emission,
        G_emission_AG = Grass_emission_AG,
        G_emission_ML = Grass_emission_ML,
        A_emission_AG = Algae_emission_AG,
        A_emission_ML = Algae_emission_ML,
        C_cost = Corn_cost,
        S_cost = Soy_cost,
        G_cost_AG = Grass_cost_AG,
        G_cost_ML = Grass_cost_ML,
        A_cost_AG = Algae_cost_AG,
        A_cost_ML = Algae_cost_ML,
        LL = agricultural_land_limits, # land limits
        MLLg = marginal_land_limits_grass,
        MLLa = marginal_land_limits_algae, 
        Q = quota  
        ):
    
    num_c = np.size(LL) #size of land limit 
    
    GHG_emission_corn_yearly = np.zeros((len(years),num_c))
    GHG_emission_soy_yearly = np.zeros((len(years),num_c))
    GHG_emission_grass_yearly_AG = np.zeros((len(years),num_c))
    GHG_emission_grass_yearly_ML = np.zeros((len(years),num_c))
    GHG_emission_algae_yearly_AG = np.zeros((len(years),num_c))
    GHG_emission_algae_yearly_ML = np.zeros((len(years),num_c))

    MFSP_corn_yearly = np.zeros((len(years),num_c))
    MFSP_soy_yearly = np.zeros((len(years),num_c))
    MFSP_grass_yearly_AG = np.zeros((len(years),num_c))
    MFSP_grass_yearly_ML = np.zeros((len(years),num_c))
    MFSP_algae_yearly_AG = np.zeros((len(years),num_c))
    MFSP_algae_yearly_ML = np.zeros((len(years),num_c))

    Energy_total = np.zeros((len(years),1))
    GHG_impact_yearly = np.zeros((len(years),num_c))
    MFSP_total_yearly = np.zeros((len(years),num_c))

    vc = (np.array(vars[0:num_c]))/2
    vs = (np.array(vars[0:num_c]))/2
  
    vg_ML = (np.array(vars[num_c:2*num_c]))  
    va_ML = (np.array(vars[num_c*2:3*num_c]))      
        
    
    vg_AG = (np.array(vars[num_c*3:4*num_c]))
    va_AG = (np.array(vars[num_c*4:5*num_c]))      
    
    
    Constraints = [] # constraints
    
    Z = []
    GHG=[]
    MFSP=[]
    Energy_f=[]
    
    for year in years:
        i = years.index(year)
        
        #yield kg/ha
        Y = C_Y[:,i]
        S = S_Y[:,i]   
        G_AG = G_Y_AG[:,i]   
        G_ML = G_Y_ML[:,i]   
        Al_AG = A_Y_AG[:,i]   
        Al_ML = A_Y_ML[:,i]   
        
        # gco2/MJ
        corn_GHG = C_emission[:,i]  
        soy_GHG = S_emission[:,i]
        grass_GHG_AG = G_emission_AG[:,i]
        grass_GHG_ML = G_emission_ML[:,i]
        algae_GHG_AG = A_emission_AG[:,i]
        algae_GHG_ML = A_emission_ML[:,i]
        
        #$/MJ
        corn_MFSP = C_cost[:,i]  
        soy_MFSP = S_cost[:,i]
        grass_MFSP_AG = G_cost_AG[:,i]
        grass_MFSP_ML = G_cost_ML[:,i]
        algae_MFSP_AG = A_cost_AG[:,i]
        algae_MFSP_ML = A_cost_ML[:,i]
        
        ##############################
        # Cultivation and Harvesting
        #biomass production from used land for each district as kg  
        CG_prod = vc[0:num_c]*Y
        SB_prod = vs[0:num_c]*S
        G_prod_ML = vg_ML[0:num_c]*G_ML
        A_prod_ML = va_ML[0:num_c]*Al_ML         
        G_prod_AG = vg_AG[0:num_c]*G_AG   
        A_prod_AG = va_AG[0:num_c]*Al_AG  
        
        
        # MJ conversion from kg biomass 
        Energy =sum((9.42 * CG_prod) + (8.02 * SB_prod) + (8.35* G_prod_ML) + (20.82* A_prod_ML) + (8.35* G_prod_AG) + (20.82*A_prod_AG))   
        Energy_total[i] = Energy   # total energy MJ/yr
        Energy_f.append(Energy)
        
        # Greenhouse gas emission calculation 
        GHG_emission_corn = np.sum(corn_GHG * (9.42 * CG_prod))
        GHG_emission_corn_yearly[i] = GHG_emission_corn
        
        GHG_emission_soy = np.sum(soy_GHG * (8.02 * SB_prod))
        GHG_emission_soy_yearly[i] = GHG_emission_soy
        
        GHG_emission_grass_ML = np.sum(grass_GHG_ML * (8.35* G_prod_ML))
        GHG_emission_grass_yearly_ML[i] = GHG_emission_grass_ML
        
        GHG_emission_algae_ML = np.sum(algae_GHG_ML * (20.82* A_prod_ML))
        GHG_emission_algae_yearly_ML[i] = GHG_emission_algae_ML
        
        GHG_emission_grass_AG = np.sum(grass_GHG_AG * (8.35* G_prod_AG))
        GHG_emission_grass_yearly_AG[i] = GHG_emission_grass_AG

        GHG_emission_algae_AG = np.sum(algae_GHG_AG * (20.82* A_prod_AG))
        GHG_emission_algae_yearly_AG[i] = GHG_emission_algae_AG
        
        GHG_impact = (GHG_emission_corn + GHG_emission_soy + GHG_emission_grass_ML + GHG_emission_algae_ML + GHG_emission_grass_AG + GHG_emission_algae_AG)
        GHG_impact_yearly[i] = GHG_impact
        
        GHG.append(GHG_impact)
        
        MFSP_corn = np.sum(corn_MFSP * (9.42 * CG_prod))
        MFSP_corn_yearly[i] = MFSP_corn
        
        MFSP_soy = np.sum(soy_MFSP * (8.02 * SB_prod))
        MFSP_soy_yearly[i] = MFSP_soy
        
        MFSP_grass_ML = np.sum(grass_MFSP_ML * (8.35* G_prod_ML))
        MFSP_grass_yearly_ML[i] = MFSP_grass_ML
        
        MFSP_algae_ML = np.sum(algae_MFSP_ML * (20.82* A_prod_ML))
        MFSP_algae_yearly_ML[i] = MFSP_algae_ML
        
        MFSP_grass_AG = np.sum(grass_MFSP_AG * (8.35* G_prod_AG))
        MFSP_grass_yearly_AG[i] = MFSP_grass_AG
        
        MFSP_algae_AG = np.sum(algae_MFSP_AG * (20.82* A_prod_AG))
        MFSP_algae_yearly_AG[i] = MFSP_algae_AG
        
        MFSP_total = (MFSP_corn + MFSP_soy + MFSP_grass_ML + MFSP_algae_ML + MFSP_grass_AG + MFSP_algae_AG)
        MFSP_total_yearly[i] = MFSP_total
        
        MFSP.append(MFSP_total)
    
        # Shortfall definition             
        if (Q - Energy) < 0:    # if produced energy higher than the quota set shortfall as 0 
     
            shortfall = 0
        
        else:                   # if produced energy lower than the quota set shortfall as deficit energy 
            
            shortfall = Q - Energy
    
        Z.append(shortfall)


    ### Constraints    
    Constraints.append(Q * 0.98 - np.mean(Energy_total)) #LB for energy production
    Constraints.append(np.mean(Energy_total) - Q * 1.02 ) #UB for energy production

    # Agricultural land usage limit
    v_AG = vc[0:num_c] + vs[0:num_c] + vg_AG[0:num_c] + va_AG[0:num_c] - LL[0:num_c]
    b = [0 if abc <=0 else 1 for abc in v_AG]
    c = sum(b)
    Constraints.append(c)

    # Rotation of corn soy on agricultural land  
    v_CS = vc[0:num_c] - vs[0:num_c] 
    k = [0 if abc ==0 else 1 for abc in v_CS]
    l = sum(k)
    Constraints.append(l)
    
    # Marginal land usage limit for switchgrass   
    v_ML_g = vg_ML[0:num_c] + va_ML[0:num_c]- MLLg[0:num_c] 
    z = [0 if abc <=0 else 1 for abc in v_ML_g]
    t = sum(z)
    Constraints.append(t)
 
    # Marginal land usage limit for algae      
    v_ML_a = va_ML[0:num_c] - MLLa[0:num_c] 
    za = [0 if abc <=0 else 1 for abc in v_ML_a]
    ta = sum(za)
    Constraints.append(ta)
    
    # Returns list of objectives, Constraints
    Constraints = list(Constraints)
    min_MSFP = sum(MFSP)/sum(Energy_f)
    min_shortfall = max(Z)
    min_GHG = sum(GHG)/sum(Energy_f)

    return [min_MSFP, min_shortfall, min_GHG], Constraints # $/MJ , MJ, gco2/MJ, MJ

df_total_cost = pd.read_excel('total_land_limit.xlsx',header=0, engine='openpyxl') 
total_land_limit = list(df_total_cost['land_limits_ha'])

####################################################################
#########           MOEA EXECUTION          ########################
####################################################################

# Number of variables, constraints, objectives
g = np.size(total_land_limit)
num_variables = g # + np.size(marginal_land_costs)
num_constraints = 6 #+ g   #must match to contraints
num_objs = 3

problem = Problem(num_variables,num_objs,num_constraints)

for i in range(0,np.size(total_land_limit)):
    problem.types[i] = Real(0,total_land_limit[i]+5)
problem.constraints[:] = "<=0"

#What function?
problem.function = simulate

# What algorithm?
algorithm = BorgMOEA(problem, epsilons=0.001)

# Evaluate function # of times
algorithm.run(1000000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)

#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

solutions = [s for s in algorithm.result if s.feasible]

D = np.zeros((len(solutions),num_variables))
O = np.zeros((len(solutions),num_objs))

for s in solutions:
    
    idx = solutions.index(s)

    #record solution information
    for i in range(0,num_variables):
        D[idx,i] = s.variables[i]
    for j in range(0,num_objs):
        O[idx,j] = s.objectives[j]

df_D = pd.DataFrame(D)
fn = 'Decision_Variables_borg_crops_GHG15_1000000_0.001' + version + '.csv'
df_D.to_csv(fn)

df_O = pd.DataFrame(O)
fn2 = 'Objective_functions_borg_crops_GHG15_1000000_0.001' + version + '.csv'
df_O.to_csv(fn2)


        
        