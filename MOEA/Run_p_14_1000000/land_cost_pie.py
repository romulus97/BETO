# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 16:04:25 2022

@author: eari
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
from matplotlib import pyplot as plt

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_corn_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae = pd.read_excel('combined_pivot_algae_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   


land_costs = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_geo_corn['land_limits_ha'].values # county ag production area in acres
marginal_land_costs = df_geo_grass.loc[:,'land_costs-$/ha'].values # $ per ha
marginal_land_limits = df_geo_grass['land_limits_ha'].values # county ag production area in acres

districts = list(df_geo_corn['STASD_N']) # list of ag_district code
# Algae pie plot 
# land_costs = list(np.reshape(A_MJ_total[:,15:16], (107,)))    # 2013 corn biomass production (kg)


landcost = pd.DataFrame(zip(districts,land_costs), columns=['Dist','land_cost'])


big_MJadf = landcost.loc[landcost['land_cost']>=16000].copy()
small_MJadf = landcost.loc[landcost['land_cost']<16000].copy()
small_total_MJa = sum(small_MJadf['land_cost'])

data_MJa = list(big_MJadf['land_cost'])
labels_MJa = list(big_MJadf['Dist'])

data_MJa = data_MJa + [small_total_MJa]
labels_MJa = labels_MJa + ['Others']
# Create a set of colors

colors = ['#2C699A', '#048ba8','#1fa6b8', '#0db39e', '#16db93', '#83e377', '#b9e769', '#efea5a', '#f1c453','#f29e4c', '#fb9017','#ff6600', '#ff0000', '#ef3c2d','#d55d92','#54478C','#7fdeff']
# explode = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.03]
# colors = sns.color_palette("pastel")
fig4 = plt.pie(data_MJa, labels=labels_MJa, colors = colors, autopct = '%0.0f%%', radius = 2, pctdistance = 0.9)

plt.show(fig4)