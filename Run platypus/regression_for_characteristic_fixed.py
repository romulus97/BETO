# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 12:57:15 2022

@author: eari
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import statsmodels.formula.api as smf
import scipy

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare
df_reg = pd.read_excel('combined_excel_regression.xlsx',header=0, engine='openpyxl')
df_reg_R2 = pd.read_excel('combined_regression_r2.xlsx',header=0, engine='openpyxl')

df_yield_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code with corn yield 
df_yield_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code with soy yield
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

df_elec = pd.read_excel('corn_stover_electricty_cost.xlsx',header=0, engine='openpyxl') # electricity cost $/ha/yr
EC = df_elec['electricity_cost($/ha)'].values # $/ha yearly

df_elec_Soy = pd.read_excel('soy_LNG_cost.xlsx',header=0, engine='openpyxl') # electricity cost $/ha/yr
EC_S = df_elec_Soy['cost($/kgf)'].values # $/ha yearly

df_elec_Algae = pd.read_excel('algae_electiricity_cost.xlsx',header=0, engine='openpyxl') # electricity cost $/ha/yr
EC_A = df_elec_Algae['cost($/kgf)'].values # $/ha yearly


#Districts
district = list(df_yield_corn['STASD_N'])
years = range(1998,2014)
solutions = range(len(df_ha))

## Acrages 
C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae


## GHG Emission from Power Sector 
CO_emission = df_yield_corn["CO2 lbs/MJ"].values  # same for each crop type (CO2 emission from power sector )
CO_em_power = CO_emission * 0.453592 *1000 # g/ MJ


## Energy 
Unit_el_price = df_yield_corn["Electricity Price $/MJ"].values  # same for each crop type (CO2 emission from power sector )



# ## GHG
# #Cultivation GHG emission 
# GHG_cult_corn = list(df_yield_corn['GHG(g CO2e/ha)']) # corn_GHG_per_ha
# GHG_cult_soy = list(df_yield_soy['soy_GHG(g CO2e/ha)'])   # soy_GHG_per_ha
# GHG_cult_soy_kg = list(df_yield_soy['soy_GHG(g CO2e/kg/yr)'])   # soy_GHG_per_kg/yr
# GHG_cult_grass = list(df_geo_grass['GHG(g CO2e/ha)'])  # grass_GHG_per_ha
# GHG_cult_algal = list(df_geo_algea['GHG(g CO2e/ha)'])  # algae_GHG_per_ha

# # #Process GHG emission
# # GHG_proc_corn = list(df_yield_corn['GHG_proc(g CO2e/kg/yr)']) # corn_GHG_per_kg/yr
# # GHG_proc_soy = list(df_yield_soy['soy_GHG_proc(g CO2e/kg/yr)'])   # soy_GHG_per_kg/yr
# # GHG_proc_grass = list(df_geo_grass['GHG_proc_(g CO2e/kg/yr)'])  # grass_cost_per_kg/yr
# # GHG_proc_algal = list(df_geo_algea['GHG_proc_(g CO2e/kg/yr)'])  # algae_cost_per_kg/yr


corn_GHG = np.zeros((len(district),len(df_ha)))
soy_GHG = np.zeros((len(district),len(df_ha)))
grass_GHG = np.zeros((len(district),len(df_ha)))
algae_GHG = np.zeros((len(district),len(df_ha)))

# for sol in solutions:  
#     GHG_emission_CG_cult = C_ha[:,sol]*GHG_cult_corn #  g CO2 emission from corn cultivation 
#     corn_GHG[:,sol]=GHG_emission_CG_cult
#     GHG_emission_S_cult = S_ha[:,sol]*GHG_cult_soy #  g CO2 emission from soy cultivation
#     soy_GHG[:,sol]=GHG_emission_S_cult
#     GHG_emission_G_cult = G_ha[:,sol]*GHG_cult_grass #  g CO2 emission from grass cultivation
#     grass_GHG[:,sol]=GHG_emission_S_cult
#     GHG_emission_A_cult = A_ha[:,sol]*GHG_cult_algal #  g CO2 emission from algae cultivation
#     algae_GHG[:,sol]=GHG_emission_S_cult


## Yield 
# Corn Grain yield
C_yield = df_yield_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_yield_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algea yield
A_yield = df_geo_algea.loc[:,1998:2013].values  #yield in kg/ha


## Land cost and limits 
land_cost = df_yield_corn.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_yield_corn.loc[:,'land_limits_ha'].values
marginal_LC = df_geo_grass.loc[:,'land_costs-$/ha'].values # $ per ha
marginal_land_limits = df_geo_grass.loc[:,'land_limits_ha'].values



#Mean Yield Calculation
total_yield_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
total_yield_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set


for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    C = sum(C_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_c[i] = C # set all total yield value into created list 
    mean_yield = C/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_c[i] = mean_yield  # set all mean yield value into created list 


for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    S = sum(S_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_s[i] = S # set all total yield value into created list 
    mean_yield = S/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_s[i] = mean_yield  # set all mean yield value into created list 
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    G = sum(G_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_g[i] = G # set all total yield value into created list 
    mean_yield = G/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_g[i] = mean_yield  # set all mean yield value into created list 
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    A = sum(A_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_a[i] = A # set all total yield value into created list 
    mean_yield = A/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_a[i] = mean_yield  # set all mean yield value into created list 
    
    
    
# Used Energy Calculation
# CG_kg_tot = np.zeros((len(land_cost),len(years)))
SB_kg_tot = np.zeros((len(land_cost),len(years)))
G_kg_tot = np.zeros((len(land_cost),len(years)))
A_kg_tot = np.zeros((len(land_cost),len(years)))

for sol in solutions:  
    CG_el = C_ha[:,sol]*EC          # total electricity price for a year ($)
    
    G_el = G_ha[:,sol]*7.51512  # 7.51512 is diesel price for grass cultivation as $/ha 

total_biomass_s = np.zeros((len(district))) # creating empty list for 106 total yield data set
dist_biomass_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_biomass_a = np.zeros((len(district))) # creating empty list for 106 total yield data set
dist_biomass_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set 

for sol in solutions: 
    for year in years:
        i = years.index(year)
        Y = C_yield[:,i]   # corn yield kg/ha
        S = S_yield[:,i]   # soy yield kg/ha
        G = G_yield[:,i]   # grass yield kg/ha
        A = A_yield[:,i]   # algae yield kg/
    
    
        SB_prod = S_ha[:,sol]*S
        SB_kg_tot[:,i] = SB_prod         # total soy biomass production (kg)
    
    
        A_prod = A_ha[:,sol]*A
        A_kg_tot[:,i] = A_prod           # total algae biomass production (kg)

for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    S = sum(SB_kg_tot[i,:]) # for each district summation of total yield throughout 63 years founded
    total_biomass_s[i] = S # set all total yield value into created list 
    mean_biomass = S/(len(years)) #calculating mean yield for each district by dividing year length
    dist_biomass_s[i] = mean_biomass  # mean kg

for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    A = sum(A_kg_tot[i,:]) # for each district summation of total yield throughout 63 years founded
    total_biomass_a[i] = A # set all total yield value into created list 
    mean_biomass = A/(len(years)) #calculating mean yield for each district by dividing year length
    dist_biomass_a[i] = mean_biomass  # set all mean yield value into created list 
    
for sol in solutions:  
    SB_el = dist_biomass_s*EC_S          # total electricity price for a year ($)

    A_el = A_prod*EC_A          # total electricity price for a year ($)
        
        
# R2 calculation         

R2_acrage_vs_cost = np.zeros(len(df_ha))
R2_acrage_vs_mgcost = np.zeros(len(df_ha))
R2_acrage_vs_macost = np.zeros(len(df_ha))
R2_acrage_vs_limit = np.zeros(len(df_ha))
R2_acrage_vs_mglimit = np.zeros(len(df_ha))
R2_acrage_vs_malimit = np.zeros(len(df_ha))

R2_acrage_vs_cyield = np.zeros(len(df_ha))
R2_acrage_vs_syield = np.zeros(len(df_ha))
R2_acrage_vs_gyield = np.zeros(len(df_ha))
R2_acrage_vs_ayield = np.zeros(len(df_ha))

R2_acrage_vs_electricity = np.zeros(len(df_ha))
R2_acrage_vs_selectricity = np.zeros(len(df_ha))
R2_acrage_vs_gelectricity = np.zeros(len(df_ha))
R2_acrage_vs_aelectricity = np.zeros(len(df_ha))

sol_reg_sign = np.zeros(len(df_ha))
sol_reg_sign_s = np.zeros(len(df_ha))
sol_reg_sign_g = np.zeros(len(df_ha))
sol_reg_sign_a = np.zeros(len(df_ha))

R2_acrage_vs_cult_GHG = np.zeros(len(df_ha))
R2_acrage_vs_scult_GHG = np.zeros(len(df_ha))
R2_acrage_vs_gcult_GHG = np.zeros(len(df_ha))
R2_acrage_vs_acult_GHG = np.zeros(len(df_ha))


df_reg['land_cost'] = land_cost
df_reg['land_limits'] = land_limits
df_reg['marginal_land_cost'] = marginal_LC
df_reg['marginal_land_limits'] = marginal_land_limits

df_reg['GHG_emission_power_sector'] = CO_em_power
df_reg['Unit Electricity price ($/MJ)'] = Unit_el_price

df_reg['corn_yield'] =dist_mean_c
df_reg['soy_yield'] =dist_mean_s
df_reg['grass_yield'] =dist_mean_g
df_reg['algae_yield'] =dist_mean_a

df_reg['corn_electricity_cost'] = CG_el
df_reg['soy_electricity_cost'] = SB_el
df_reg['grass_electricity_cost'] = G_el
df_reg['algae_electricity_cost'] = A_el


#### GHG
# ## Corn acrage vs GHG
# for sol in solutions:
#     df_reg['corn_acrage'] = C_ha[:,sol]
#     df_reg['corn_cult_GHG'] = corn_GHG[:,sol]
    
#     y = np.array(df_reg['corn_cult_GHG'])
#     X = np.array(df_reg['corn_acrage'])
#     linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2_acrage_vs_cult_GHG.loc[sol,:] = R2
#     # print(linregress(X, y))


## Corn acrage vs GHG form power system
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]
    
    y = np.array(df_reg['GHG_emission_power_sector'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_cult_GHG[sol] = R2
    # print(linregress(X, y))


## Soy acrage vs GHG
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]

    
    y = np.array(df_reg['GHG_emission_power_sector'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_scult_GHG[sol] = R2
    
    
## Grass acrage vs GHG
for sol in solutions:
    df_reg['grass_acrage'] = G_ha[:,sol]

    
    y = np.array(df_reg['GHG_emission_power_sector'])
    X = np.array(df_reg['grass_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_gcult_GHG[sol] = R2
        
## Algae acrage vs GHG
for sol in solutions:
    df_reg['algae_acrage'] = A_ha[:,sol]

    
    y = np.array(df_reg['GHG_emission_power_sector'])
    X = np.array(df_reg['algae_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_acult_GHG[sol] = R2


df_reg_R2['R2_acrage_vs_cult_GHG'] = R2_acrage_vs_cult_GHG
df_reg_R2['R2_acrage_vs_scult_GHG'] = R2_acrage_vs_scult_GHG
df_reg_R2['R2_acrage_vs_gcult_GHG'] = R2_acrage_vs_gcult_GHG
df_reg_R2['R2_acrage_vs_acult_GHG'] = R2_acrage_vs_acult_GHG

# #### ELECTRICITY
# ## Corn acrage vs electricity
# for sol in solutions:
#     df_reg['corn_acrage'] = C_ha[:,sol]
    
#     y = np.array(df_reg['corn_electricity_cost'])
#     X = np.array(df_reg['corn_acrage'])
#     linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2_acrage_vs_electricity[sol] = R2
#     sol_reg = scipy.stats.pearsonr(X,y) 
#     sol_reg_p = sol_reg[0]
#     sol_reg_sign[sol]= sol_reg_p


# ## Soy acrage vs electricity
# for sol in solutions:
#     df_reg['corn_acrage'] = C_ha[:,sol]
    
#     y = np.array(df_reg['soy_electricity_cost'])
#     X = np.array(df_reg['corn_acrage'])
#     linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2_acrage_vs_selectricity[sol] = R2
#     sol_reg_s = scipy.stats.pearsonr(X,y) 
#     sol_reg_sp = sol_reg_s[0]
#     sol_reg_sign_s[sol]= sol_reg_sp
    
    

# ## Grass acrage vs electricity
# for sol in solutions:
#     df_reg['grass_acrage'] = G_ha[:,sol]
    
#     y = np.array(df_reg['grass_electricity_cost'])
#     X = np.array(df_reg['grass_acrage'])
#     linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2_acrage_vs_gelectricity[sol] = R2
#     sol_reg_g = scipy.stats.pearsonr(X,y) 
#     sol_reg_gp = sol_reg_g[0]
#     sol_reg_sign_g[sol]= sol_reg_gp
    
    
# ## Algae acrage vs electricity
# for sol in solutions:
#     df_reg['algae_acrage'] = A_ha[:,sol]
    
#     y = np.array(df_reg['algae_electricity_cost'])
#     X = np.array(df_reg['algae_acrage'])
#     linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
#     R2_acrage_vs_aelectricity[sol] = R2
#     sol_reg_a = scipy.stats.pearsonr(X,y) 
#     sol_reg_ap = sol_reg_a[0]
#     sol_reg_sign_a[sol]= sol_reg_ap


# df_reg_R2['R2_acrage_vs_electricity'] = R2_acrage_vs_electricity
# df_reg_R2['R2_acrage_vs_electricity_sign'] = sol_reg_sign
# df_reg_R2['R2_acrage_vs_selectricity'] = R2_acrage_vs_selectricity
# df_reg_R2['R2_acrage_vs_selectricity_sign'] = sol_reg_sign_s
# df_reg_R2['R2_acrage_vs_gelectricity'] = R2_acrage_vs_gelectricity
# df_reg_R2['R2_acrage_vs_gelectricity_sign'] = sol_reg_sign_g
# df_reg_R2['R2_acrage_vs_aelectricity'] = R2_acrage_vs_aelectricity
# df_reg_R2['R2_acrage_vs_aelectricity_sign'] = sol_reg_sign_a


#### ELECTRICITY
## Corn acrage vs electricity
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]
    
    y = np.array(df_reg['Unit Electricity price ($/MJ)'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_electricity[sol] = R2
    sol_reg = scipy.stats.pearsonr(X,y) 
    sol_reg_p = sol_reg[0]
    sol_reg_sign[sol]= sol_reg_p


## Soy acrage vs electricity
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]
    
    y = np.array(df_reg['Unit Electricity price ($/MJ)'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_selectricity[sol] = R2
    sol_reg_s = scipy.stats.pearsonr(X,y) 
    sol_reg_sp = sol_reg_s[0]
    sol_reg_sign_s[sol]= sol_reg_sp
    

## Grass acrage vs electricity
for sol in solutions:
    df_reg['grass_acrage'] = G_ha[:,sol]
    
    y = np.array(df_reg['Unit Electricity price ($/MJ)'])
    X = np.array(df_reg['grass_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_gelectricity[sol] = R2
    sol_reg_g = scipy.stats.pearsonr(X,y) 
    sol_reg_gp = sol_reg_g[0]
    sol_reg_sign_g[sol]= sol_reg_gp
    
    
## Algae acrage vs electricity
for sol in solutions:
    df_reg['algae_acrage'] = A_ha[:,sol]
    
    y = np.array(df_reg['Unit Electricity price ($/MJ)'])
    X = np.array(df_reg['algae_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_aelectricity[sol] = R2
    sol_reg_a = scipy.stats.pearsonr(X,y) 
    sol_reg_ap = sol_reg_a[0]
    sol_reg_sign_a[sol]= sol_reg_ap


df_reg_R2['R2_acrage_vs_electricity'] = R2_acrage_vs_electricity
df_reg_R2['R2_acrage_vs_electricity_sign'] = sol_reg_sign
df_reg_R2['R2_acrage_vs_selectricity'] = R2_acrage_vs_selectricity
df_reg_R2['R2_acrage_vs_selectricity_sign'] = sol_reg_sign_s
df_reg_R2['R2_acrage_vs_gelectricity'] = R2_acrage_vs_gelectricity
df_reg_R2['R2_acrage_vs_gelectricity_sign'] = sol_reg_sign_g
df_reg_R2['R2_acrage_vs_aelectricity'] = R2_acrage_vs_aelectricity
df_reg_R2['R2_acrage_vs_aelectricity_sign'] = sol_reg_sign_a



#### LAND COST
## Corn acrage vs land cost
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]
    
    y = np.array(df_reg['land_cost'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_cost[sol] = R2


## Grass acrage vs marginal land cost
for sol in solutions:
    df_reg['grass_acrage'] = G_ha[:,sol]
    
    y = np.array(df_reg['marginal_land_cost'])
    X = np.array(df_reg['grass_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_mgcost[sol] = R2
    
    
## Algae acrage vs marginal land cost
for sol in solutions:
    df_reg['algae_acrage'] = A_ha[:,sol]
    
    y = np.array(df_reg['marginal_land_cost'])
    X = np.array(df_reg['algae_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_macost[sol] = R2
    

df_reg_R2['R2_acrage_vs_cost'] = R2_acrage_vs_cost
df_reg_R2['R2_acrage_vs_mgcost'] = R2_acrage_vs_mgcost
df_reg_R2['R2_acrage_vs_macost'] = R2_acrage_vs_macost

###LAND LIMIT
## Corn acrage vs land limits
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]
    
    y = np.array(df_reg['land_limits'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_limit[sol] = R2


## Grass acrage vs marginal land limits
for sol in solutions:
    df_reg['grass_acrage'] = G_ha[:,sol]
    
    y = np.array(df_reg['marginal_land_limits'])
    X = np.array(df_reg['grass_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_mglimit[sol] = R2
    
    
## Algae acrage vs marginal land limits
for sol in solutions:
    df_reg['algae_acrage'] = A_ha[:,sol]
    
    y = np.array(df_reg['marginal_land_limits'])
    X = np.array(df_reg['algae_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_malimit[sol] = R2
    

df_reg_R2['R2_acrage_vs_limit'] = R2_acrage_vs_limit
df_reg_R2['R2_acrage_vs_mglimit'] = R2_acrage_vs_mglimit
df_reg_R2['R2_acrage_vs_malimit'] = R2_acrage_vs_malimit


### YIELD     
## Corn acrage vs Yield
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]
    
    y = np.array(df_reg['corn_yield'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_cyield[sol] = R2

## Corn acrage vs Yield
for sol in solutions:
    df_reg['corn_acrage'] = C_ha[:,sol]
    
    y = np.array(df_reg['soy_yield'])
    X = np.array(df_reg['corn_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_syield[sol] = R2
    
    
## Grass acrage vs marginal land cost
for sol in solutions:
    df_reg['grass_acrage'] = G_ha[:,sol]
    
    y = np.array(df_reg['grass_yield'])
    X = np.array(df_reg['grass_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_gyield[sol] = R2
    
    
## Algae acrage vs marginal land cost
for sol in solutions:
    df_reg['algae_acrage'] = A_ha[:,sol]
    
    y = np.array(df_reg['algae_yield'])
    X = np.array(df_reg['algae_acrage'])
    linear_model = LinearRegression().fit(X.reshape(-1, 1), y.reshape(-1, 1))
    R2 = linear_model.score(X.reshape(-1, 1), y.reshape(-1, 1))
    R2_acrage_vs_ayield[sol] = R2
    
    
df_reg_R2['R2_acrage_vs_cyield'] = R2_acrage_vs_cyield
df_reg_R2['R2_acrage_vs_syield'] = R2_acrage_vs_syield
df_reg_R2['R2_acrage_vs_gyield'] = R2_acrage_vs_gyield
df_reg_R2['R2_acrage_vs_ayield'] = R2_acrage_vs_ayield

df_reg_R2.to_excel('combined_regression_r2.xlsx')  
