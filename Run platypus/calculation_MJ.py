# -*- coding: utf-8 -*-
"""
Created on Mon May 23 18:26:44 2022

@author: eari
"""

from platypus import GDE3, Problem, Real
import plotly.express as px
from matplotlib import pyplot as plt
from pyborg import BorgMOEA
import seaborn as sns
import random
from random import randint
import pandas as pd
import numpy as np
import time
import corn_grain_processing as CG_processing
import soybean_processing as SB_processing 
import Pyrol_processing as G_processing 
import Algal_Oil as A_processing

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare

C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae

LC = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha

years = range(1998,2014)


# Corn Grain yield
C_yield = df_geo_corn.loc[:,1998:2013].values  #yield in kg/ha

# Soybean yield
S_yield = df_geo_soy.loc[:,1998:2013].values  #yield in kg/ha

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
    CG_prod = C_ha[:,0]*Y 
    CG_kg_tot[:,i] = CG_prod         # total corn biomass production (kg)
    
    SB_prod = S_ha[:,0]*S
    SB_kg_tot[:,i] = SB_prod         # total soy biomass production (kg)
    
    
    G_prod = G_ha[:,0]*G
    G_kg_tot[:,i] = G_prod           # total grass biomass production (kg)
    
    A_prod = A_ha[:,0]*A
    A_kg_tot[:,i] = A_prod           # total algae biomass production (kg)
    
                
    # Ethanol and oil produced at refinery at hub 'l'
    CG_ethanol = CG_processing.sim(CG_prod) #kg ethanol
    CG_ethanol_total[:,i] = CG_ethanol # throught years kg ethanol
    CG_MJ_total[:,i] = 29.7 *CG_ethanol # MJ from ethanol
    # CG_MJ = 29.7 * CG_ethanol # MJ from ethanol
    
        
    SB_oil = SB_processing.sim(SB_prod)  #kg soy oil
    SB_oil_total[:,i] = SB_oil # throught years kg soy oil
    SB_MJ_total[:,i] = 39.6 * SB_oil # MJ from soy oil
    
        
    G_energy = G_processing.sim(G_prod) # kg biocrude 
    G_energy_total[:,i] = G_energy # throught years kg biocrude
    G_MJ_total[:,i] = 21* G_energy # MJ from biocrude
    
        
    A_energy = A_processing.sim(A_prod) # kg algae oil
    A_energy_total[:,i] = A_energy # throught years kg algae oil
    A_MJ_total[:,i] = 22 * A_energy # MJ from algae oil
    
        
    # Energy =(29.7 * CG_ethanol + 39.6 * SB_oil + 21* G_energy + 22 * A_energy)   # Ethanol * 29.7 MJ/kg + Soy Oil * 39.6 MJ/kg + biocrude * 21 MJ/kg + algae oil * 22 MJ/kg
    # Energy_total[i] = Energy   # total energy MJ/yr


# corn_last_bio = list(np.reshape(CG_kg_tot[:,15:16], (107,)))    # 2013 corn biomass production (kg)

# colors = sns.color_palette('bright')
# plt.pie(corn_last_bio, labels=districts,colors = colors, autopct = '%0.0f%%')
# plt.show()

# mydf = pd.DataFrame(zip(districts,corn_last_bio), columns=['Dist','Corn_kg'])
# mydf['Percent'] = mydf['Corn_kg']/sum(mydf['Corn_kg'])*100

# big_mydf = mydf.loc[mydf['Percent']>=2].copy()
# small_mydf = mydf.loc[mydf['Percent']<2].copy()
# small_total = sum(small_mydf['Corn_kg'])

# data = list(big_mydf['Corn_kg'])
# labels = list(big_mydf['Dist'])

# data = data + [small_total]
# labels = labels + ['Others']
# # Create a set of colors
# colors = ['#54478C', '#2C699A', '#048ba8', '#0db39e', '#16db93', '#83e377', '#b9e769', '#efea5a', '#f1c453', '#f29e4c','#ff0000', '#d55d92']

# # colors = sns.color_palette("pastel")
# plt.pie(data, labels=labels,colors = colors, autopct = '%0.0f%%')
# plt.show()


# # corn and soy pie plot
# corn_last_MJ = list(np.reshape(CG_MJ_total[:,15:16], (107,)))    # 2013 corn biomass production (kg)

# MJdf = pd.DataFrame(zip(districts,corn_last_MJ), columns=['Dist','Ethanol_MJ'])
# MJdf['Percent'] = MJdf['Ethanol_MJ']/sum(MJdf['Ethanol_MJ'])*100

# big_MJdf = MJdf.loc[MJdf['Percent']>=2].copy()
# small_MJdf = MJdf.loc[MJdf['Percent']<2].copy()
# small_total_MJ = sum(small_MJdf['Ethanol_MJ'])

# data_MJ = list(big_MJdf['Ethanol_MJ'])
# labels_MJ = list(big_MJdf['Dist'])

# data_MJ = data_MJ + [small_total_MJ]
# labels_MJ = labels_MJ + ['Others']
# # Create a set of colors
# colors = ['#2C699A', '#048ba8', '#0db39e', '#16db93', '#83e377', '#b9e769', '#efea5a', '#f1c453', '#f29e4c','#ff0000', '#d55d92', '#54478C', '#7fdeff']
# #explode = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.03]
# # colors = sns.color_palette("pastel")
# fig1 = plt.pie(data_MJ, labels=labels_MJ, colors = colors, autopct = '%0.0f%%', radius = 2, pctdistance = 0.9)

# plt.show(fig1)




# # Soy pie plot
# soy_last_MJ = list(np.reshape(SB_MJ_total[:,15:16], (107,)))    # 2013 corn biomass production (kg)

# MJsdf = pd.DataFrame(zip(districts,soy_last_MJ), columns=['Dist','Soy_Oil_MJ'])
# MJsdf['Percent'] = MJsdf['Soy_Oil_MJ']/sum(MJsdf['Soy_Oil_MJ'])*100

# big_MJsdf = MJsdf.loc[MJsdf['Percent']>=2].copy()
# small_MJsdf = MJsdf.loc[MJsdf['Percent']<2].copy()
# small_total_MJs = sum(small_MJsdf['Soy_Oil_MJ'])

# data_MJs = list(big_MJsdf['Soy_Oil_MJ'])
# labels_MJs = list(big_MJsdf['Dist'])

# data_MJs = data_MJs + [small_total_MJs]
# labels_MJs = labels_MJs + ['Others']
# # Create a set of colors
# colors = [ '#2C699A', '#048ba8', '#0db39e', '#16db93', '#83e377', '#b9e769', '#efea5a', '#f1c453', '#f29e4c', '#fb9017','#ff0000', '#d55d92','#54478C','#7fdeff']
# # explode = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.03]
# # colors = sns.color_palette("pastel")
# fig2 = plt.pie(data_MJs, labels=labels_MJs, colors = colors, autopct = '%0.0f%%', radius = 2, pctdistance = 0.9)

# plt.show(fig2)



# # Grass pie plot 
# grass_last_MJ = list(np.reshape(G_MJ_total[:,15:16], (107,)))    # 2013 corn biomass production (kg)


# MJgdf = pd.DataFrame(zip(districts,grass_last_MJ), columns=['Dist','Biocrude_MJ'])
# MJgdf['Percent'] = MJgdf['Biocrude_MJ']/sum(MJgdf['Biocrude_MJ'])*100

# big_MJgdf = MJgdf.loc[MJgdf['Percent']>=2].copy()
# small_MJgdf = MJgdf.loc[MJgdf['Percent']<2].copy()
# small_total_MJg = sum(small_MJgdf['Biocrude_MJ'])

# data_MJg = list(big_MJgdf['Biocrude_MJ'])
# labels_MJg = list(big_MJgdf['Dist'])

# data_MJg = data_MJg + [small_total_MJg]
# labels_MJg = labels_MJg + ['Others']
# # Create a set of colors

# colors = ['#2C699A', '#048ba8', '#0db39e', '#16db93', '#83e377', '#b9e769', '#efea5a', '#f1c453', '#f29e4c', '#fb9017','#ff0000', '#ef3c2d','#d55d92','#54478C','#7fdeff']
# # explode = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.03]
# # colors = sns.color_palette("pastel")
# fig3 = plt.pie(data_MJg, labels=labels_MJg, colors = colors, autopct = '%0.0f%%', radius = 2, pctdistance = 0.9)

# plt.show(fig3)



# Algae pie plot 
algae_last_MJ = list(np.reshape(A_MJ_total[:,15:16], (107,)))    # 2013 corn biomass production (kg)


MJadf = pd.DataFrame(zip(districts,algae_last_MJ), columns=['Dist','Algal_Oil_MJ'])
MJadf['Percent'] = MJadf['Algal_Oil_MJ']/sum(MJadf['Algal_Oil_MJ'])*100

big_MJadf = MJadf.loc[MJadf['Percent']>=2].copy()
small_MJadf = MJadf.loc[MJadf['Percent']<2].copy()
small_total_MJa = sum(small_MJadf['Algal_Oil_MJ'])

data_MJa = list(big_MJadf['Algal_Oil_MJ'])
labels_MJa = list(big_MJadf['Dist'])

data_MJa = data_MJa + [small_total_MJa]
labels_MJa = labels_MJa + ['Others']
# Create a set of colors

colors = ['#2C699A', '#048ba8','#1fa6b8', '#0db39e', '#16db93', '#83e377', '#b9e769', '#efea5a', '#f1c453','#f29e4c', '#fb9017','#ff6600', '#ff0000', '#ef3c2d','#d55d92','#54478C','#7fdeff']
# explode = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.03]
# colors = sns.color_palette("pastel")
fig4 = plt.pie(data_MJa, labels=labels_MJa, colors = colors, autopct = '%0.0f%%', radius = 2, pctdistance = 0.9)

plt.show(fig4)