# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 12:41:01 2022

@author: eari
"""


import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd
from pysal.lib import weights
import geopandas as gpd
from pysal.explore import esda

import corn_grain_processing as CG_processing
import soybean_processing as SB_processing 
import Pyrol_processing as G_processing 
import Algal_Oil as A_processing


df_O= pd.read_csv('Objective_Functions_borg_two_crop_trialdistrict.csv',header=0,index_col=0)
df_O.columns = ['cost','energy_shortfall','GHG_emission']


district_map = gpd.read_file('shapefiles/AgD Corn belt.shp')
district_map = district_map.to_crs(epsg=2163)
districts = list(district_map['STASD_N'])

## CALCULATING ENERGY
# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code
df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used hectare

## Dividing corn, soy, grass and algae yield data.
C_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for corn 
S_ha = np.transpose(df_ha).iloc[1:108].values # used hectare for soy
G_ha = np.transpose(df_ha).iloc[108:215].values # used hectare for grass
A_ha = np.transpose(df_ha).iloc[215:].values # used hectare for algae

LC = df_geo_corn.loc[:,'land_costs-$/ha'].values # $ per ha

years = range(1998,2014)
solution = range(len(df_ha))

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


CG_kg_tot = np.zeros((1,len(df_ha)))
SB_kg_tot = np.zeros((1,len(df_ha)))
G_kg_tot = np.zeros((1,len(df_ha)))
A_kg_tot = np.zeros((1,len(df_ha)))

CG_kg_tot_den = np.zeros((len(years),len(df_ha)))
SB_kg_tot_den = np.zeros((len(years),len(df_ha)))
G_kg_tot_den = np.zeros((len(years),len(df_ha)))
A_kg_tot_den = np.zeros((len(years),len(df_ha)))

CG_kg_tot_dd = np.zeros((1,len(df_ha)))
SB_kg_tot_dd = np.zeros((1,len(df_ha)))
G_kg_tot_dd = np.zeros((1,len(df_ha)))
A_kg_tot_dd = np.zeros((1,len(df_ha)))


for year in years:
    i = years.index(year)
    Y = C_yield[:,i]   # corn yield kg/ha
    S = S_yield[:,i]   # soy yield kg/ha
    G = G_yield[:,i]   # grass yield kg/ha
    A = A_yield[:,i]   # algae yield kg/ha
       

    for s in solution:
        CG_prod = sum(C_ha[:,s]*Y) 
        CG_kg_tot[:,s] = CG_prod         # total corn biomass production (kg)
        
        SB_prod = sum(S_ha[:,s]*S)
        SB_kg_tot[:,s] = SB_prod         # total soy biomass production (kg)
        
        
        G_prod = sum(G_ha[:,s]*G)
        G_kg_tot[:,s] = G_prod           # total grass biomass production (kg)
            
        A_prod = sum(A_ha[:,s]*A)
        A_kg_tot[:,s] = A_prod           # total algae biomass production (kg)
        
    CG_kg_tot_den[i] = CG_kg_tot
    SB_kg_tot_den[i] = SB_kg_tot
    G_kg_tot_den[i] = G_kg_tot
    A_kg_tot_den[i] = A_kg_tot
    
    for s in solution:
        CG_dd = sum(CG_kg_tot_den[:,s])
        CG_kg_tot_dd[:,s] = CG_dd/len(years)       # average corn biomass production for 15 years (kg)
        
        SB_dd = sum(SB_kg_tot_den[:,s])
        SB_kg_tot_dd[:,s] = SB_dd/len(years)       # average soy biomass production for 15 years (kg)
        
        G_dd = sum(G_kg_tot_den[:,s])
        G_kg_tot_dd[:,s] = G_dd/len(years)        # average grass biomass production for 15 years (kg)
        
        A_dd = sum(A_kg_tot_den[:,s])
        A_kg_tot_dd[:,s] = A_dd/len(years)        # average algae biomass production for 15 years (kg)
    
        
CG_total = np.transpose(CG_kg_tot_dd)
SB_total = np.transpose(SB_kg_tot_dd)
G_total = np.transpose(G_kg_tot_dd)
A_total = np.transpose(A_kg_tot_dd)

Total = CG_total + SB_total + G_total + A_total
CG_ethanol_total = np.zeros((len(solution),1))
SB_oil_total = np.zeros((len(solution),1))
G_energy_total = np.zeros((len(solution),1))
A_energy_total = np.zeros((len(solution),1))
Energy_total = np.zeros((len(solution),1))


for s in solution:         
    
    GC_t = CG_total[s]   # corn yield kg/ha
    S_t = SB_total[s]   # soy yield kg/ha
    G_t = G_total[s]   # grass yield kg/ha
    A_t = A_total[s]   # algae yield kg/ha
    
    CG_ethanol = CG_processing.sim(GC_t) #kg ethanol
    CG_ethanol_total[s] = CG_ethanol
    
    SB_oil = SB_processing.sim(S_t)  #kg soy oil
    SB_oil_total[s] = SB_oil

    G_energy = G_processing.sim(G_t) # kg biocrude 
    G_energy_total[s] = G_energy
    
    A_energy = A_processing.sim(A_t) # kg algae oil
    A_energy_total[s] = A_energy
    
    Energy =(29.7 * CG_ethanol + 39.6 * SB_oil + 21* G_energy + 22 * A_energy)   # Ethanol * 29.7 MJ/kg + Soy Oil * 39.6 MJ/kg + biocrude * 21 MJ/kg + algae oil * 22 MJ/kg
    Energy_total[s] = Energy   # total energy MJ/yr

df_O['MJ'] = Energy_total
df_O['cost/MJ'] = df_O['cost']/df_O['MJ']
df_O['GHG_emission/MJ'] = df_O['GHG_emission']/df_O['MJ']



# ### Calculating Moran
# df_decision_variables= pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0)
# tc = df_decision_variables.iloc[:,1:108]
# tg = df_decision_variables.iloc[:,108:215]
# tg.columns = tc.columns
# ta = df_decision_variables.iloc[:,215:]
# ta.columns = tc.columns

# tt = tc + tg + ta
# t = tt.transpose(copy=False)
# # to = t.iloc[1:]
# ind =  t.columns

# district_map.index = t.index
# map_c = pd.concat([district_map,t],axis=1)
# db = gpd.GeoDataFrame(map_c)
# db.info()

# Z1 = []

# for i in ind:
    
#     # Generate W from the GeoDataFrame
#     w = weights.KNN.from_dataframe(db, k=8)
#     # Row-standardization
#     w.transform = 'R'
    
#     w.transform = 'R'
#     moran = esda.moran.Moran(db[i], w)
#     moran.I
#     Z1.append(moran.I)

# df_O['Morans_I'] = Z1
colors = df_O['MJ']

x = df_O['cost/MJ']
y = df_O['energy_shortfall']
z = df_O['GHG_emission/MJ']


### CALCULATING PERCENTAGE FOR TRANSPARENT SOLUTION FOR COST/MJ
m = len(df_O)	
p = 0.1	
n = m*p  	
sorting_cost = df_O.sort_values(by='cost/MJ', ascending=False)	
min_n_cost = sorting_cost.tail(int(n))	
ind_min_cost = list(min_n_cost.index.values)
num_cost = min_n_cost.head(int(1))['cost/MJ'].values	


x1 = min_n_cost['cost/MJ']
y1 = min_n_cost['energy_shortfall']
z1 = min_n_cost['GHG_emission/MJ']
colors1 = min_n_cost['MJ']

fig, ax = plt.subplots()

fig1 = plt.scatter(x, y, c=colors, cmap='plasma', alpha = 0.05);
fig2 = plt.axvline(x=num_cost, c= 'black',linestyle='--') # label=int(num_cost)
fig3 = plt.scatter(x1, y1, c=colors1, cmap='plasma',alpha = 0.99,linewidths=0.4, edgecolors= 'black');
# plt.pcolor(colors1, cmap='plasma', vmin=-0.025, vmax=0.20)
# plt.title('Cost/MJ vs Energy shortfall')
ax.tick_params(axis='both', which='major', labelsize=14)
plt.xlabel('Cost ($/MJ)',fontsize=14)
plt.ylabel('Quota Shortfall (MJ)',fontsize=14)
plt.grid(False)
plt.legend()
cbar = plt.colorbar()
cbar.set_label("Energy Production (MJ)",fontsize=14)
plt.clim(1550000000000, 1950000000000)


# ### CALCULATING PERCENTAGE FOR TRANSPARENT SOLUTION FOR COST/MJ
# m = len(df_O)	
# p = 0.1	
# n = m*p  	
# sorting_cost = df_O.sort_values(by='cost/MJ', ascending=False)	
# min_n_cost = sorting_cost.tail(int(n))	
# ind_min_cost = list(min_n_cost.index.values)
# num_cost = min_n_cost.head(int(1))['cost/MJ'].values	


# x1 = min_n_cost['cost/MJ']
# y1 = min_n_cost['energy_shortfall']
# z1 = min_n_cost['GHG_emission/MJ']
# colors1 = min_n_cost['MJ']

# fig, ax = plt.subplots()

# fig1 = plt.scatter(x, z, c=colors, cmap='plasma', alpha = 0.05);
# fig2 = plt.axvline(x=num_cost, c= 'black',linestyle='--') # label=int(num_cost)
# fig3 = plt.scatter(x1, z1, c=colors1, cmap='plasma',alpha = 0.99,linewidths=0.4, edgecolors= 'black');
# # plt.pcolor(colors1, cmap='plasma', vmin=-0.025, vmax=0.20)
# # plt.title('Cost/MJ vs Energy shortfall')
# ax.tick_params(axis='both', which='major', labelsize=14)
# plt.xlabel('Cost ($/MJ)',fontsize=14)

# plt.ylabel(r'GHG Intensity (tons $CO_{2}$ / MJ)',fontsize=14)

# plt.grid(False)
# plt.legend()
# cbar = plt.colorbar()
# cbar.set_label("Energy Production (MJ)",fontsize=14)
# plt.clim(1550000000000, 1950000000000)

# ### CALCULATING PERCENTAGE FOR TRANSPARENT SOLUTION FOR GHG
# m = len(df_O)	
# p = 0.1	
# n = m*p  	
# sorting_GHG = df_O.sort_values(by='GHG_emission/MJ', ascending=False)	
# min_n_GHG = sorting_GHG.tail(int(n))	
# ind_min_GHG = list(min_n_GHG.index.values)
# num_GHG = min_n_GHG.head(int(1))['GHG_emission/MJ'].values	


# x2 = min_n_GHG['cost/MJ']
# y2 = min_n_GHG['energy_shortfall']
# z2 = min_n_GHG['GHG_emission/MJ']
# colors2 = min_n_GHG['MJ']

# fig, ax = plt.subplots()

# fig1 = plt.scatter(z, x, c=colors, cmap='plasma', alpha = 0.05);
# fig2 = plt.axvline(x=num_GHG, c= 'black',linestyle='--')    #label=int(num_GHG)
# fig3 = plt.scatter(z2, x2, c=colors2, cmap='plasma',alpha = 0.99,linewidths=0.4, edgecolors= 'black');
# # plt.title('GHG emission/MJ vs Cost/MJ')
# ax.tick_params(axis='both', which='major', labelsize=14)
# plt.xlabel(r'GHG Intensity (tons $CO_{2}$ / MJ)',fontsize=14)
# plt.ylabel('Cost ($/MJ)',fontsize=14)
# plt.grid(False)
# plt.legend()
# cbar = plt.colorbar()
# cbar.set_label("Energy Production (MJ)",fontsize=14)
# plt.clim(1550000000000, 1950000000000)

# ### CALCULATING PERCENTAGE FOR TRANSPARENT SOLUTION FOR GHG
# m = len(df_O)	
# p = 0.1	
# n = m*p  	
# sorting_GHG = df_O.sort_values(by='GHG_emission/MJ', ascending=False)	
# min_n_GHG = sorting_GHG.tail(int(n))	
# ind_min_GHG = list(min_n_GHG.index.values)
# num_GHG = min_n_GHG.head(int(1))['GHG_emission/MJ'].values	


# x2 = min_n_GHG['cost/MJ']
# y2 = min_n_GHG['energy_shortfall']
# z2 = min_n_GHG['GHG_emission/MJ']
# colors2 = min_n_GHG['MJ']

# fig, ax = plt.subplots()

# fig1 = plt.scatter(z, y, c=colors, cmap='plasma', alpha = 0.05);
# fig2 = plt.axvline(x=num_GHG, c= 'black', linestyle='--')    #label=int(num_GHG)
# fig3 = plt.scatter(z2, y2, c=colors2, cmap='plasma',alpha = 0.99,linewidths=0.4, edgecolors= 'black');
# # plt.title('GHG emission/MJ vs Cost/MJ')
# ax.tick_params(axis='both', which='major', labelsize=14)
# plt.xlabel(r'GHG Intensity (tons $CO_{2}$ / MJ)',fontsize=14)
# plt.ylabel('Quota Shortfall (MJ)',fontsize=14)
# plt.grid(False)
# plt.legend()
# cbar = plt.colorbar()
# cbar.set_label("Energy Production (MJ)",fontsize=14)
# plt.clim(1550000000000, 1950000000000)



# ### CALCULATING PERCENTAGE FOR TRANSPARENT SOLUTION FOR ENERGY SHORTFALL
# m = len(df_O)	
# p = 0.1	
# n = m*p  	
# sorting_energy = df_O.sort_values(by='energy_shortfall', ascending=False)	
# min_n_energy = sorting_energy.tail(int(n))	
# ind_min_energy = list(min_n_energy.index.values)
# num_energy = min_n_energy.head(int(1))['energy_shortfall'].values	


# x2 = min_n_energy['cost/MJ']
# y2 = min_n_energy['energy_shortfall']
# z2 = min_n_energy['GHG_emission/MJ']
# colors2 = min_n_energy['MJ']

# fig, ax = plt.subplots()

# fig1 = plt.scatter(y, z, c=colors, cmap='plasma', alpha = 0.05);
# fig2 = plt.axvline(x=num_energy, c= 'black', linestyle='--') #label=int(num_energy)
# fig3 = plt.scatter(y2, z2, c=colors2, cmap='plasma',alpha = 0.99,linewidths=0.4, edgecolors= 'black');
# # plt.title('Energy_shortfall vs GHG_emission/MJ')
# ax.tick_params(axis='both', which='major', labelsize=14)
# plt.xlabel('Quota Shortfall (MJ)',fontsize=14)
# plt.ylabel(r'GHG Intensity (tons $CO_{2}$ / MJ)',fontsize=14)
# plt.grid(False)
# plt.legend()
# cbar = plt.colorbar()
# cbar.set_label("Energy Production (MJ)",fontsize=14)
# plt.clim(1550000000000, 1950000000000)



# ### CALCULATING PERCENTAGE FOR TRANSPARENT SOLUTION FOR ENERGY SHORTFALL
# m = len(df_O)	
# p = 0.1	
# n = m*p  	
# sorting_energy = df_O.sort_values(by='energy_shortfall', ascending=False)	
# min_n_energy = sorting_energy.tail(int(n))	
# ind_min_energy = list(min_n_energy.index.values)
# num_energy = min_n_energy.head(int(1))['energy_shortfall'].values	


# x2 = min_n_energy['cost/MJ']
# y2 = min_n_energy['energy_shortfall']
# z2 = min_n_energy['GHG_emission/MJ']
# colors2 = min_n_energy['MJ']

# fig, ax = plt.subplots()

# fig1 = plt.scatter(y, x, c=colors, cmap='plasma', alpha = 0.05);
# fig2 = plt.axvline(x=num_energy, c= 'black', linestyle='--') #label=int(num_energy)
# fig3 = plt.scatter(y2, x2, c=colors2, cmap='plasma',alpha = 0.99,linewidths=0.4, edgecolors= 'black');
# # plt.title('Energy_shortfall vs GHG_emission/MJ')
# ax.tick_params(axis='both', which='major', labelsize=14)
# plt.xlabel('Quota Shortfall (MJ)',fontsize=14)
# plt.ylabel('Cost ($/MJ)',fontsize=14)
# plt.grid(False)
# plt.legend()
# cbar = plt.colorbar()
# cbar.set_label("Energy Production (MJ)",fontsize=14)
# plt.clim(1550000000000, 1950000000000)

