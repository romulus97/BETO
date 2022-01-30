# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:16:58 2021

@author: Ece Ari Akdemir
"""


import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

###importing datasets
df_yield = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code
df_yield_soy =  pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code
df_ha = pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains decision variable
df_obj = pd.read_csv('Objective_functions_borg_two_crop_trialdistrict.csv',header=0) #contains objective functions

## Biomass cost and shortfall 
biomass_cost_corn = list(df_obj['biomass_cost_corn'])
biomass_cost_soy = list(df_obj['biomass_cost_soy'])
shortfall_corn = list(df_obj['min_energy_shortfall'])

##minimum shortfall and maximum biomass cost index
maxbio_cost_corn = max(biomass_cost_corn)
idx = biomass_cost_corn.index(maxbio_cost_corn)

##maximum shortfall and minimum biomass cost index
minbio_cost_corn = min(biomass_cost_corn)
idxm = biomass_cost_corn.index(minbio_cost_corn)

##minimum shortfall and maximum biomass cost index
maxbio_cost_soy = max(biomass_cost_soy)
idxs = biomass_cost_soy.index(maxbio_cost_soy)

##maximum shortfall and minimum biomass cost index
minbio_cost_soy = min(biomass_cost_soy)
idxms = biomass_cost_soy.index(minbio_cost_soy)



## Solution and district base ha planted 
selection = (df_ha.iloc[:,1:].values)/2

##minimum shortfall and maximum biomass cost planted ha
selectionmaxc = (df_ha.iloc[idx,1:].values)/2  ## maximum planted ha solution district by district 
maxlandarea = sum(selectionmaxc)

##maximum shortfall and minimum biomass cost planted ha
selectionminc = (df_ha.iloc[idxm,1:].values)/2  ## minimum planted ha solution district by district 
minlandarea = sum(selectionminc)

##minimum shortfall and maximum biomass cost planted ha
selectionmaxs = (df_ha.iloc[idxs,1:].values)/2  ## maximum planted ha solution district by district 

##maximum shortfall and minimum biomass cost planted ha
selectionmins = (df_ha.iloc[idxms,1:].values)/2  ## minimum planted ha solution district by district 



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

##district and solution based ha planted area 
nd = np.transpose(selection) # this is done for transpose table to multiply it with as a column

##kg corn for districts 
CT = dist_mean_cy * nd  # multiplication woth district yield with district land usage (kg)
Tmax_C = pd.DataFrame(CT).iloc[:,idx].values
Tmin_C = pd.DataFrame(CT).iloc[:,idxm].values

ST = dist_mean_sy * nd  # multiplication woth district yield with district land usage (kg)
Tmax_S = pd.DataFrame(ST).iloc[:,idx].values
Tmin_S = pd.DataFrame(ST).iloc[:,idxm].values

fig = px.scatter_3d(x = selectionmaxc , y = Tmax_C , z = district)
fig.update_layout(height = 900, width = 1000, title='maximum shortfall and minimum biomass cost for corn solution')
fig.update_layout(scene = dict(xaxis_title='maximum planted ha solution district by district',yaxis_title='corn kg', zaxis_title='District'))
fig.write_html("maximum shortfall and minimum biomass cost for corn solution.html")
fig.show()


fig2 = px.scatter_3d(x = selectionminc , y = Tmin_C , z = district)
fig2.update_layout(height = 900, width = 1000, title='minimum shortfall and maximum biomass cost for corn solution')
fig2.update_layout(scene = dict(xaxis_title='minimum planted ha solution district by district',yaxis_title='corn kg', zaxis_title='District'))
fig2.write_html("minimum shortfall and maximum biomass cost for corn solution.html")
fig2.show()

##for differences graph 
x = abs(selectionmaxc - selectionminc)
y = abs(Tmax_C - Tmin_C)
fig3 = px.scatter_3d(x = x , y = y , z = district)
fig3.update_layout(height = 900, width = 1000, title='Differences for corn between figure 1 and 2')
fig3.update_layout(scene = dict(xaxis_title='difference between planted ha',yaxis_title='difference between corn kg', zaxis_title='District'))
fig3.show()
fig3.write_html("Differences for corn between figure 1 and 2.html")




fig4 = px.scatter_3d(x = selectionmaxs , y = Tmax_S , z = district)
fig4.update_layout(height = 900, width = 1000, title='maximum shortfall and minimum biomass cost for soy solution')
fig4.update_layout(scene = dict(xaxis_title='maximum planted ha solution district by district',yaxis_title='soy kg', zaxis_title='District'))
fig4.write_html("maximum shortfall and minimum biomass cost for soy solution.html")
fig4.show()


fig5 = px.scatter_3d(x = selectionmins , y = Tmin_S , z = district)
fig5.update_layout(height = 900, width = 1000, title='minimum shortfall and maximum biomass cost for soy solution')
fig5.update_layout(scene = dict(xaxis_title='minimum planted ha solution district by district',yaxis_title='soy kg', zaxis_title='District'))
fig5.write_html("minimum shortfall and maximum biomass cost for soy solution.html")
fig5.show()

##for differences graph 
xs = abs(selectionmaxs - selectionmins)
ys = abs(Tmax_S - Tmin_S)
fig6 = px.scatter_3d(x = xs , y = ys , z = district)
fig6.update_layout(height = 900, width = 1000, title='Differences for soy between figure 1 and 2')
fig6.update_layout(scene = dict(xaxis_title='difference between planted ha',yaxis_title='difference between soy kg', zaxis_title='District'))
fig6.show()
fig6.write_html("Differences for soy between figure 1 and 2.html")



