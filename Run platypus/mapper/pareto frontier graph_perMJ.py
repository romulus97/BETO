# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 00:07:04 2022

@author: Ece Ari Akdemir
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.express as px
import corn_grain_processing as CG_processing
import soybean_processing as SB_processing 
import Pyrol_processing as G_processing 
import Algal_Oil as A_processing


version = 'district'


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



#objective function
fn = 'Objective_Functions_borg_two_crop_trial' + version + '.csv'
df_O = pd.read_csv(fn,header=0,index_col=0)
df_O.columns = ['cost','energy_shortfall','GHG_emission']
df_O['Energy Production (MJ)'] = Energy_total
df_O['cost/MJ'] = df_O['cost']/df_O['Energy Production (MJ)']
df_O['GHG_emission/MJ'] = df_O['GHG_emission']/df_O['Energy Production (MJ)']

### CALCULATING PERCENTAGE FOR TRANSPARENT SOLUTION FOR COST/MJ
m = len(df_O)	
p = 0.1	
n = m*p  	
sorting_cost = df_O.sort_values(by='cost/MJ', ascending=False)	
min_n_cost = sorting_cost.tail(int(n))	
ind_min_cost = list(min_n_cost.index.values)
num_cost = min_n_cost.head(int(1))['cost/MJ'].values	




fig2 = px.scatter_3d(min_n_cost, x='cost/MJ', y='energy_shortfall', z='GHG_emission/MJ', color='Energy Production (MJ)', opacity = 0.99);

# fig2.update_traces(marker=dict(line=dict(width=10))) # color='black'
fig1 = px.scatter_3d(df_O, x='cost/MJ', y='energy_shortfall', z='GHG_emission/MJ',color='Energy Production (MJ)', opacity=0.04, size_max= 80)
fig3 = go.Figure(data=fig1.data + fig2.data)

fig3.update_layout(title='Comparison energy_shortfall,GHG_emission/MJ and cost/MJ')
fig3.update_layout(scene = dict(xaxis_title='Cost ($/MJ)',yaxis_title='Quota Shortfall',zaxis_title='GHG Intensity (tons CO2(MJ)'))
# fig3.colorbar(label='Energy Production (MJ)')

# fig3.update_layout( height = 900, width = 1000,title='Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes')
fig3.show()
fig3.write_html("Comparison energy_shortfall,GHG_emission and cost with per MJ.html")








