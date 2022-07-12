# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 22:59:23 2022

@author: eari
"""

import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats

df_yield_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code with corn yield 
df_yield_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code with soy yield
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare

district = list(df_yield_corn['STASD_N']) # list of ag_district code
name_district = list(df_yield_corn['State'])

C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae

LC = df_yield_corn.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_yield_corn.loc[:,'land_limits_ha'].values
MLC = df_geo_grass.loc[:,'land_costs-$/ha'].values # $ per ha
marginal_land_limits = df_geo_grass.loc[:,'land_limits_ha'].values

years = range(1998,2014)


# Corn Grain yield
C_yield = df_yield_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_yield_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algea yield
A_yield = df_geo_algea.loc[:,1998:2013].values  #yield in kg/ha

num_c = np.size(LC) #size of land cost 
Energy_total = np.zeros((len(years),1))


CG_ethanol_total = np.zeros((len(LC),len(years)))
CG_MJ_total = np.zeros((len(LC),len(years)))
SB_oil_total = np.zeros((len(LC),len(years)))
SB_MJ_total = np.zeros((len(LC),len(years)))
G_energy_total = np.zeros((len(LC),len(years)))
G_MJ_total = np.zeros((len(LC),len(years)))
A_energy_total = np.zeros((len(LC),len(years)))
A_MJ_total = np.zeros((len(LC),len(years)))
CG_kg_tot = np.zeros((len(LC),len(years)))
SB_kg_tot = np.zeros((len(LC),len(years)))
G_kg_tot = np.zeros((len(LC),len(years)))
A_kg_tot = np.zeros((len(LC),len(years)))

## max energy shortfall 
#a = 54
## min_GHG_emission
#a = 7758
## min_cost
a = 7368


for year in years:
    i = years.index(year)
    Y = C_yield[:,i]   # corn yield kg/ha
    S = S_yield[:,i]   # soy yield kg/ha
    G = G_yield[:,i]   # grass yield kg/ha
    A = A_yield[:,i]   # algae yield kg/ha
    
    # Constraints = [] # constraints
    
    # Per ha values (need to expand) # this is where we would put in code from Jack 
    
    ##############################
    # Cultivation and Harvesting


    # Operating costs (need to expand)
    CG_prod = C_ha[:,a]*Y 
    CG_kg_tot[:,i] = CG_prod         # total corn biomass production (kg)
    
    SB_prod = S_ha[:,a]*S
    SB_kg_tot[:,i] = SB_prod         # total soy biomass production (kg)
    
    
    G_prod = G_ha[:,a]*G
    G_kg_tot[:,i] = G_prod           # total grass biomass production (kg)
    
    A_prod = A_ha[:,a]*A
    A_kg_tot[:,i] = A_prod           # total algae biomass production (kg)


total_biomass_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_biomass_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_biomass_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_biomass_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_biomass_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_biomass_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
total_biomass_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_biomass_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set
years = range(1960,2021) # representin year range

for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    C = sum(CG_kg_tot[i,:]) # for each district summation of total yield throughout 63 years founded
    total_biomass_c[i] = C # set all total yield value into created list 
    mean_biomass = C/(len(years)) #calculating mean yield for each district by dividing year length
    dist_biomass_c[i] = mean_biomass  # set all mean yield value into created list 


for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    S = sum(SB_kg_tot[i,:]) # for each district summation of total yield throughout 63 years founded
    total_biomass_s[i] = S # set all total yield value into created list 
    mean_biomass = S/(len(years)) #calculating mean yield for each district by dividing year length
    dist_biomass_s[i] = mean_biomass  # set all mean yield value into created list 
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    G = sum(G_kg_tot[i,:]) # for each district summation of total yield throughout 63 years founded
    total_biomass_g[i] = G # set all total yield value into created list 
    mean_biomass = G/(len(years)) #calculating mean yield for each district by dividing year length
    dist_biomass_g[i] = mean_biomass  # set all mean yield value into created list 
    
for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    A = sum(A_kg_tot[i,:]) # for each district summation of total yield throughout 63 years founded
    total_biomass_a[i] = A # set all total yield value into created list 
    mean_biomass = A/(len(years)) #calculating mean yield for each district by dividing year length
    dist_biomass_a[i] = mean_biomass  # set all mean yield value into created list 
    
    
df_yield_corn['corn kg'] =dist_biomass_c
df_yield_corn['soy kg'] =dist_biomass_s
df_yield_corn['grass kg'] =dist_biomass_g
df_yield_corn['algae kg'] =dist_biomass_a

df_yield_corn['land_cost'] = LC
df_yield_corn['marginal_land_cost'] =MLC
df_yield_corn['land_limit'] = land_limits
df_yield_corn['marginal_land_limit'] =marginal_land_limits
df_yield_corn['State'] = name_district

corr = scipy.stats.pearsonr(dist_biomass_c, LC) 
print(corr)

fig1 = px.scatter(df_yield_corn, x = 'corn kg' , y = 'land_cost' , color = 'State', size = 'STASD_N')
fig1.update_layout(title='Comparison between avg corn kg and land cost for district')
fig1.update_yaxes(title='land cost')
fig1.update_xaxes(title='avg corn kg')
fig1.write_html("Comparison between avg corn kg and land cost for district.html")
fig1.show()

fig2 = px.scatter(df_yield_corn, x = 'soy kg' , y = 'land_cost' , color = 'State', size = 'STASD_N')
fig2.update_layout(title='Comparison between avg soy kg and land cost for district')
fig2.update_yaxes(title='land cost')
fig2.update_xaxes(title='avg soy kg')
fig2.write_html("Comparison between avg soy kg and land cost for district.html")
fig2.show()

fig3 = px.scatter(df_yield_corn, x = 'grass kg' , y = 'marginal_land_cost' , color = 'State', size = 'marginal_land_limit')
fig3.update_layout(title='Comparison between avg grass kg and marginal land cost for district')
fig3.update_yaxes(title='marginal land cost')
fig3.update_xaxes(title='avg grass kg')
fig3.write_html("Comparison between avg grass kg and marginal land cost for district.html")
fig3.show()

fig4 = px.scatter(df_yield_corn, x = 'algae kg' , y = 'marginal_land_cost' , color = 'State', size = 'marginal_land_limit')
fig4.update_layout(title='Comparison between avg algae kg and marginal land cost for district')
fig4.update_yaxes(title='marginal land cost')
fig4.update_xaxes(title='avg algae kg')
fig4.write_html("Comparison between avg algae kg and marginal land cost for district.html")
fig4.show()


