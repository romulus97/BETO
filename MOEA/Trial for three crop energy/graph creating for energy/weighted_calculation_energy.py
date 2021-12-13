# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:08:13 2021

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
df_ha = pd.read_csv('Decision_Variables_borg_two_cropdistrict.csv',header=0) #contains decision variable
df_obj = pd.read_csv('Objective_functions_borg_two_cropdistrict.csv',header=0) #contains objective functions
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
df_obj['land_usage_corn(ha)'] = ha/2
df_obj['land_usage_soy(ha)'] = ha/2

nd = np.transpose(selection) # this is done for transpose table to multiply it with as a column

CT = dist_mean_cy * nd  # multiplication woth district yield with district land usage (kg)
solution_yield_for_dist_c = np.transpose(CT)  # produced corn kilogram for each district 
total_solution_yield_c = solution_yield_for_dist_c.sum(axis=1) # this is row summation. This give us total planted land as ha for each solution. #

weighted_by_ha_planted_c = total_solution_yield_c / (df_obj['land_usage_corn(ha)'].values)

ST = dist_mean_sy * nd  # multiplication woth district yield with district land usage (kg)
solution_yield_for_dist_s = np.transpose(ST)  # produced corn kilogram for each district 
total_solution_yield_s = solution_yield_for_dist_s.sum(axis=1) # this is row summation. This give us total planted land as ha for each solution. #

weighted_by_ha_planted_s = total_solution_yield_s / (df_obj['land_usage_soy(ha)'].values)

#pd.DataFrame(weighted_by_ha_planted).to_csv("weighted by ha planted.csv")