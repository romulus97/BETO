# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 17:23:18 2022

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

df_yield_corn = pd.read_excel('combined_pivot_corn_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code with corn yield 
df_yield_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code with soy yield
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae = pd.read_excel('combined_pivot_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

district = list(df_yield_corn['STASD_N']) # list of ag_district code
name_district = list(df_yield_corn['State'])

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare
df_obj =  pd.read_csv('Objective_functions_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare
df_elec = pd.read_excel('corn_stover_electricty_cost.xlsx',header=0, engine='openpyxl') # electricity cost $/ha/yr
 

# ## max energy shortfall 
# #a = 54
# ## min_GHG_emission
# #a = 7758
# ## min_cost
# a = 7368

# min cost solution 
sorting_cost = df_obj.sort_values(by='0', ascending=False)

min_10_cost = sorting_cost.tail(10)
ind_min_cost = list(min_10_cost.index.values)

 
C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae


LC = df_yield_corn.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_yield_corn.loc[:,'land_limits_ha'].values
MLC = df_geo_grass.loc[:,'land_costs-$/ha'].values # $ per ha
marginal_land_limits = df_geo_grass.loc[:,'land_limits_ha'].values

EC = df_elec['electricity_cost($/ha)'].values # $/ha yearly

years = range(1998,2014)

# Corn Grain yield
C_yield = df_yield_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_yield_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algae yield
A_yield = df_geo_algae.loc[:,1998:2013].values  #yield in kg/ha

num_c = np.size(LC) #size of land cost 
Energy_total = np.zeros((len(years),1))

CG_prod_10 = np.zeros((len(LC),10))
# CG_ethanol_total = np.zeros((len(LC),len(years)))
# CG_MJ_total = np.zeros((len(LC),len(years)))
# SB_oil_total = np.zeros((len(LC),len(years)))
# SB_MJ_total = np.zeros((len(LC),len(years)))
# G_energy_total = np.zeros((len(LC),len(years)))
# G_MJ_total = np.zeros((len(LC),len(years)))
# A_energy_total = np.zeros((len(LC),len(years)))
# A_MJ_total = np.zeros((len(LC),len(years)))
CG_kg_tot = np.zeros((len(LC),len(years)))
SB_kg_tot = np.zeros((len(LC),len(years)))
G_kg_tot = np.zeros((len(LC),len(years)))
A_kg_tot = np.zeros((len(LC),len(years)))




for ind in ind_min_cost:
    a = ind_min_cost.index(ind)       # for a specific min cost solution (there is 10 min solution compared in this code)


    for year in years:
        i = years.index(year)
        Y = C_yield[:,i]   # corn yield kg/ha
        S = S_yield[:,i]   # soy yield kg/ha
        G = G_yield[:,i]   # grass yield kg/ha
        A = A_yield[:,i]   # algae yield kg/

        CG_prod = C_ha[:,ind]*Y           # total corn biomass production for min cost solution for a year (kg)
        CG_kg_tot[:,i] = CG_prod          # total soy biomass production throughout years (kg)
        CG_el = C_ha[:,ind]*EC          # total electricity price for a year ($)

        
        SB_prod = S_ha[:,ind]*S
        SB_kg_tot[:,i] = SB_prod         # total soy biomass production (kg)
        SB_el = S_ha[:,ind]*EC

    
        G_prod = G_ha[:,ind]*G
        G_kg_tot[:,i] = G_prod           # total grass biomass production (kg)
        G_el = G_ha[:,ind]*EC

    
        A_prod = A_ha[:,ind]*A
        A_kg_tot[:,i] = A_prod           # total algae biomass production (kg)
        A_el = A_ha[:,ind]*EC

   
    total_biomass_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
    dist_biomass_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
    total_biomass_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
    dist_biomass_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
    total_biomass_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
    dist_biomass_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
    total_biomass_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
    dist_biomass_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set
            
            
    for dist in district:
        i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
        C = sum(CG_kg_tot[i,:]) # for each district summation of total yield throughout 63 years founded
        total_biomass_c[i] = C # set all total yield value into created list 
        mean_yield = C/(len(years)) #calculating mean yield for each district by dividing year length
        dist_biomass_c[i] = mean_yield  # set all mean yield value into created list 
          
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
    df_yield_corn['land_limits'] = land_limits
    df_yield_corn['marginal_land_cost'] = MLC
    df_yield_corn['marginal_land_limits'] = marginal_land_limits
    
    df_yield_corn['corn_electricity_cost'] = CG_el
    df_yield_corn['soy_electricity_cost'] = SB_el
    df_yield_corn['grass_electricity_cost'] = G_el
    df_yield_corn['algae_electricity_cost'] = A_el
    
    df_yield_corn['State'] = name_district
    index = [str (b) for b in ind_min_cost]
    
    
    fig1 = px.scatter(df_yield_corn, x = 'land_limits' , y = 'corn_electricity_cost' , color = 'State', size = 'corn kg')
    fig1.update_layout(title= index[a] +' Comparison between avg corn kg and land cost vs electricity cost for district')
    # fig1.update_yaxes(title='land cost')
    # fig1.update_xaxes(title='avg corn kg')
    fig1.write_html(index[a] +' Comparison between avg corn kg and land cost vs electricity cost for district.html')
    fig1.show()

    fig2 = px.scatter(df_yield_corn, x = 'land_limits' , y = 'soy_electricity_cost' , color = 'State', size = 'soy kg')
    fig2.update_layout(title=index[a] +' Comparison between avg soy kg and land cost vs electricity cost for district')
    # fig2.update_yaxes(title='land cost')
    # fig2.update_xaxes(title='avg soy kg')
    fig2.write_html(index[a] +" Comparison between avg soy kg and land cost vs electricity cost for district.html")
    fig2.show()
    
    fig3 = px.scatter(df_yield_corn, x = 'marginal_land_limits' , y = 'grass_electricity_cost' , color = 'State', size = 'grass kg')
    fig3.update_layout(title=index[a] +' Comparison between avg grass kg and land cost vs electricity cost for district')
    # fig3.update_yaxes(title='land cost')
    # fig3.update_xaxes(title='avg grass kg')
    fig3.write_html(index[a] +" Comparison between avg grass kg and land cost vs electricity cost for district.html")
    fig3.show()
    
    fig4 = px.scatter(df_yield_corn, x = 'marginal_land_limits' , y = 'algae_electricity_cost' , color = 'State', size = 'algae kg')
    fig4.update_layout(title=index[a] +' Comparison between avg algae kg and land cost vs electricity cost for district')
    # fig4.update_yaxes(title='land cost')
    # fig4.update_xaxes(title='avg algae kg')
    fig4.write_html(index[a] +" Comparison between avg algae kg and land cost vs electricity cost for district.html")
    fig4.show()




