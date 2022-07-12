# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:56:27 2022

@author: eari
"""

# library
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px
import corn_grain_processing as CG_processing
import soybean_processing as SB_processing 
import Pyrol_processing as G_processing 
import Algal_Oil as A_processing
import matplotlib.patches as mpatches


labels = ['1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013']

version = 'district'


# import excel sheet  
df_geo_corn = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('combined_pivot_soy_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass = pd.read_excel('combined_pivot_grass_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algea = pd.read_excel('combined_pivot_algea_excel_electricity.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code

df_ha =  pd.read_csv('Decision_Variables_borg_two_crop_trialdistrict.csv',header=0) #contains data sets for used 
df_O = pd.read_csv('Objective_Functions_borg_two_crop_trialdistrict.csv',header=0,index_col=0)

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



CG_ethanol_total_MJ = np.zeros((len(df_ha),len(years)))
SB_oil_total_MJ = np.zeros((len(df_ha),len(years)))
CS_total_MJ = np.zeros((len(df_ha),len(years)))
G_energy_total_MJ = np.zeros((len(df_ha),len(years)))
A_energy_total_MJ = np.zeros((len(df_ha),len(years)))

CS_ethanol_avg = np.zeros((len(df_ha),1))
SB_oil_avg = np.zeros((len(df_ha),1))
CS_avg = np.zeros((len(df_ha),1))
G_energy_avg = np.zeros((len(df_ha),1))
A_energy_avg = np.zeros((len(df_ha),1))

# Energy_total = np.zeros((len(solution),1))

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
    
        CG_ethanol = CG_processing.sim(CG_kg_tot_den[:,s]) #kg ethanol
        CG_ethanol_total_MJ[s] = CG_ethanol*29.7   #MJ/kg
        CG_ethanol_total_MJ_avg = sum(CG_ethanol_total_MJ[s])/len(CG_ethanol_total_MJ[s])
        CS_ethanol_avg[s] = CG_ethanol_total_MJ_avg
    
        SB_oil = SB_processing.sim(SB_kg_tot_den[:,s])  #kg soy oil
        SB_oil_total_MJ[s] = SB_oil*39.6           #MJ/kg
        SB_oil_total_MJ_avg = sum(SB_oil_total_MJ[s])/len(SB_oil_total_MJ[s])
        SB_oil_avg[s] = SB_oil_total_MJ_avg
        
        CS_total_MJ[s] = CG_ethanol*29.7 + SB_oil*39.6   #MJ
        CS_avg[s] = CG_ethanol_total_MJ_avg + SB_oil_total_MJ_avg
        
        G_energy = G_processing.sim(G_kg_tot_den[:,s]) # kg biocrude 
        G_energy_total_MJ[s] = G_energy*21         #MJ
        G_energy_total_MJ_avg = sum(G_energy_total_MJ[s])/len(G_energy_total_MJ[s])
        G_energy_avg[s] = G_energy_total_MJ_avg        
        
        A_energy = A_processing.sim(A_kg_tot_den[:,s]) # kg algae oil
        A_energy_total_MJ[s] = A_energy*22         #MJ
        A_energy_total_MJ_avg = sum(A_energy_total_MJ[s])/len(A_energy_total_MJ[s])
        A_energy_avg[s] = A_energy_total_MJ_avg     

df_O.columns = ['cost','max_energy_shortfall','min_GHG_emission']

#sorting = df_O.sort_values(by='max_energy_shortfall', ascending=True)
#sorting = df_O.sort_values(by='min_GHG_emission', ascending=True)
sorting = df_O.sort_values(by='cost', ascending=True)


CS = CS_total_MJ
G = G_energy_total_MJ
A = A_energy_total_MJ

CS_avg = CS_avg
G_avg = G_energy_avg
A_avg = A_energy_avg

CC = [a[0] for a in CS_avg]
GG = [a[0] for a in G_avg]
AA = [a[0] for a in A_avg]

my_index = list(sorting.index)
# plt.stackplot()
CCC = [CC[y] for y in my_index]
GGG = [GG[y] for y in my_index]
AAA = [AA[y] for y in my_index]


x=list(range(0,8485))
# MJ_avg_prod = pd.DataFrame(zip(CS_avg,G_avg,A_avg))


# Basic stacked area chart.


fig = plt.figure(figsize =(15, 15))
ax = fig.add_subplot(1,1,1)

ax.stackplot(x,CCC, GGG, AAA, labels = ['corn/soy','grass','algae'])
plt.legend(loc='upper left')
plt.ylabel('MJ')
plt.xticks(np.arange(0, 8484,step=1000), rotation=40)

m = len(df_O)	
p = 0.1	
q = 0.5
z = 0.98
n = m*p 
k = m*q
r = m*z 	

plt.axvline(x=(int(n)),color='black')
plt.axvline(x=(int(k)),color='navy')
plt.axvline(x=(int(r)),color='red')


#plt.title('Sorted Energy Shortfall Solution')
#plt.title('Sorted GHG Emission Solution')
plt.title('Sorted Cost Solution')




