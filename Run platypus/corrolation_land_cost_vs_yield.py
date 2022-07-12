# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 11:26:16 2021

@author: Ece Ari Akdemir
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

district = list(df_yield_corn['STASD_N']) # list of ag_district code
name_district = list(df_yield_corn['State'])

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare

C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae


years = range(1998,2014)
# corn_yield = df_yield_corn.iloc[:,13:].values # filtered the yearly corn yields. 
# soy_yield = df_yield_soy.iloc[:,12:].values # filtered the yearly soy yields.

# Corn Grain yield
corn_yield = df_yield_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
soy_yield = df_yield_soy.loc[:,1998:2013].values  #yield in kg/ha

# Grass yield
G_yield = df_geo_grass.loc[:,1998:2013].values  #yield in kg/ha

# Algea yield
A_yield = df_geo_algea.loc[:,1998:2013].values  #yield in kg/ha

land_cost = df_yield_corn.loc[:,'land_costs-$/ha'].values
land_limits = df_yield_corn.iloc[:,4].values

district = list(df_yield_corn['STASD_N']) # filtered agricultural district code 
name_district = list(df_yield_corn['State'])
total_yield_c = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_c = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_s = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_s = np.zeros((len(district))) # creating empty list for 106 mean yield data set 
total_yield_g = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_g = np.zeros((len(district))) # creating empty list for 106 mean yield data set
total_yield_a = np.zeros((len(district))) # creating empty list for 106 total yield data set 
dist_mean_a = np.zeros((len(district))) # creating empty list for 106 mean yield data set
years = range(1960,2021) # representin year range

for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    C = sum(corn_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_c[i] = C # set all total yield value into created list 
    mean_yield = C/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_c[i] = mean_yield  # set all mean yield value into created list 


for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    S = sum(soy_yield[i,:]) # for each district summation of total yield throughout 63 years founded
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
    
    
df_yield_corn['corn yield'] =dist_mean_c
df_yield_corn['soy yield'] =dist_mean_s
df_yield_corn['grass yield'] =dist_mean_g
df_yield_corn['algae yield'] =dist_mean_a

df_yield_corn['land_cost'] = land_cost
df_yield_corn['State'] = name_district

corr = scipy.stats.pearsonr(dist_mean_c, land_cost) 
print(corr)

fig1 = px.scatter(df_yield_corn, x = 'corn yield' , y = 'land_cost' , color = 'State', size = 'STASD_N')
fig1.update_layout(title='Comparison between avg corn yield and land cost for district')
fig1.update_yaxes(title='land cost')
fig1.update_xaxes(title='avg corn yield')
fig1.write_html("Comparison between avg corn yield and land cost for district.html")
fig1.show()

fig2 = px.scatter(df_yield_corn, x = 'soy yield' , y = 'land_cost' , color = 'State', size = 'STASD_N')
fig2.update_layout(title='Comparison between avg soy yield and land cost for district')
fig2.update_yaxes(title='land cost')
fig2.update_xaxes(title='avg soy yield')
fig2.write_html("Comparison between avg soy yield and land cost for district.html")
fig2.show()

fig3 = px.scatter(df_yield_corn, x = 'grass yield' , y = 'land_cost' , color = 'State', size = 'STASD_N')
fig3.update_layout(title='Comparison between avg grass yield and land cost for district')
fig3.update_yaxes(title='land cost')
fig3.update_xaxes(title='avg grass yield')
fig3.write_html("Comparison between avg grass yield and land cost for district.html")
fig3.show()

fig4 = px.scatter(df_yield_corn, x = 'algae yield' , y = 'land_cost' , color = 'State', size = 'STASD_N')
fig4.update_layout(title='Comparison between avg algae yield and land cost for district')
fig4.update_yaxes(title='land cost')
fig4.update_xaxes(title='avg algae yield')
fig4.write_html("Comparison between avg algae yield and land cost for district.html")
fig4.show()


