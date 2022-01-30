# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 16:16:58 2021

@author: Ece Ari Akdemir
"""

import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px

df_yield = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code
df_yield_soy =  pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code
df_ha = pd.read_csv('Decision_Variables_borg_two_crop_trial_5district.csv',header=0) #contains decision variable
df_obj = pd.read_csv('Objective_functions_borg_two_crop_trial_5district.csv',header=0) #contains objective functions


selection = (df_ha.iloc[:,1:].values)
corn_yield = df_yield.iloc[:,13:].values # filtered the yearly corn yields.
soy_yield = df_yield_soy.iloc[:,12:].values # filtered the yearly corn yields. 
district = list(df_yield['STASD_N']) # filtered agricultural district code 
total_yield_c = np.zeros((len(district), 1)) # creating empty list for 106 total yield data set 
dist_mean_cy = np.zeros((len(district), 1)) # creating empty list for 106 mean yield data set
total_yield_s = np.zeros((len(district), 1)) # creating empty list for 106 total yield data set 
dist_mean_sy = np.zeros((len(district), 1)) # creating empty list for 106 mean yield data set
years = range(1960,2021) # representin year range

for dist in district:
    i = district.index(dist) #for selecting specific district, for loop created and each district index founded 
    CY = sum(corn_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_c[i] = CY # set all total yield value into created list 
    mean_yield_C = CY/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_cy[i] = mean_yield_C  # set all mean yield value into created list 
    
    SY = sum(soy_yield[i,:]) # for each district summation of total yield throughout 63 years founded
    total_yield_s[i] = SY # set all total yield value into created list 
    mean_yield_S = SY/(len(years)) #calculating mean yield for each district by dividing year length
    dist_mean_sy[i] = mean_yield_S  # set all mean yield value into created list

# unit of total_yield kg/ha 
# unit of mean_yield kg/ha*yr 

ha = selection.sum(axis=1) # this is row summation. This give us total planted land as ha for each solution. 
df_obj['land_usage(ha)']=ha
df_obj['land_usage_corn(ha)'] = ha/2
df_obj['land_usage_soy(ha)'] = ha/2


# corn_kg = np.zeros((len(df_obj))) 
# b = len(df_obj)
# h = np.zeros((len(df_obj), len(district)))
# for i in range(0,b):
#     a = np.sum(df_ha.iloc[i,1:].values*dist_mean_y)
#     corn_kg[i] =  a
    
    
# sol_yield = corn_kg/(df_obj['land_usage(ha)'])

# df_obj['corn_kg'] =corn_kg
# df_obj['sol_yield'] =sol_yield

# fig1 = px.scatter_3d(df_obj, x='biomass_cost', y='shortfall', z='land_usage(ha)',color=corn_kg)
# fig1.update_layout(title='Comparison Biofuel cost-shortfall-Land usage(ha) and kg corn production')
# fig1.show()
# fig1.write_html("Comparison Biofuel cost-shortfall-Land usage(ha) and kg corn production.html")

# fig2 = px.scatter_3d(df_obj, x='biomass_cost', y='shortfall', z='land_usage(ha)',color=sol_yield)
# fig2.update_layout(title='Comparison Biofuel cost-shortfall-Land usage(ha) and yield for solution')
# fig2.show()
# fig2.write_html("Comparison Biofuel cost-shortfall-Land usage(ha) and yield for solution.html")

# fig3 = px.scatter_3d(df_obj, x='biomass_cost_corn', y='biomass_cost_soy', z='ethanol changes',color='land_usage(ha)')
# fig3.update_layout(title='Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes')
# # fig3.update_layout( height = 900, width = 1000,title='Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes')
# fig3.show()
# fig3.write_html("Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes.html")

# fig3 = px.scatter_3d(df_obj, x='min_shortfall_corn', y='min_shortfall_soy', z='biomass_cost_corn',color='land_usage(ha)')
# fig3.update_layout(title='Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes')
# # fig3.update_layout( height = 900, width = 1000,title='Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes')
# fig3.show()
# fig3.write_html("Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes.html")

fig = px.scatter_3d(df_obj, x='biomass_cost_corn', y='biomass_cost_soy', z='min_energy_shortfall',color='land_usage(ha)', hover_data=['energy_differences'])
fig.update_layout(height = 900, width = 1000, title='Comparison Biofuel cost-shortfall-Land usage(ha) and energy changes')
fig.show()
fig.write_html("Comparison Biofuel cost-shortfall-Land usage(ha) and energy changes (5).html")




