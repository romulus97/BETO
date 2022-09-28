# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 09:54:15 2022

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

df_cost =  pd.read_csv('Objective_functions_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare 

# min cost solution 
sorting_cost = df_cost.sort_values(by='0', ascending=False)

min_10_cost = sorting_cost.tail(10)
ind_min_cost = list(min_10_cost.index.values)

min_10_cost.rename(columns = {'0':'biomass_cost', '1':'shortfall', '2':'GHG'}, inplace = True)

fig1 = px.scatter(min_10_cost, x = 'biomass_cost' , y = 'shortfall' , color = 'GHG', size = 'GHG')
fig1.update_layout(title='Comparison between biomass cost, shortfall and GHG for min cost solutions')
fig1.update_yaxes(title='shortfall')
fig1.update_xaxes(title='biomass_cost')
fig1.write_html("Comparison between biomass cost, shortfall and GHG for min cost solutions.html")
fig1.show()


# min shortfall solution 
sorting_shortfall = df_cost.sort_values(by='1', ascending=False)

min_10_shortfall = sorting_shortfall.tail(10)
ind_min_shortfall = list(min_10_shortfall.index.values)

min_10_shortfall.rename(columns = {'0':'biomass_cost', '1':'shortfall', '2':'GHG'}, inplace = True)

fig2 = px.scatter(min_10_shortfall, x = 'shortfall' , y = 'biomass_cost' , color = 'GHG', size = 'GHG')
fig2.update_layout(title='Comparison between biomass cost, shortfall and GHG for min shortfall solutions')
fig2.update_yaxes(title='biomass_cost')
fig2.update_xaxes(title='shortfall')
fig2.write_html("Comparison between biomass cost, shortfall and GHG for min shortfall solutions.html")
fig2.show()


# min GHG solution 
sorting_GHG = df_cost.sort_values(by='2', ascending=False)


min_10_GHG = sorting_GHG.tail(10)
ind_min_GHG = list(min_10_GHG.index.values)

min_10_GHG.rename(columns = {'0':'biomass_cost', '1':'shortfall', '2':'GHG'}, inplace = True)


fig3 = px.scatter(min_10_GHG, x = 'GHG' , y = 'biomass_cost' , color = 'shortfall', size = 'shortfall')
fig3.update_layout(title='Comparison between biomass cost, shortfall and GHG for min GHG solutions')
fig3.update_yaxes(title='biomass_cost')
fig3.update_xaxes(title='GHG')
fig3.write_html("Comparison between biomass cost, shortfall and GHG for min GHG solutions.html")
fig3.show()