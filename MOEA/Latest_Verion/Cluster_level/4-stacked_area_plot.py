# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 10:56:27 2022

@author: eari
"""

# library
# import Pyrol_processing as G_processing
# import soybean_processing as SB_processing
import matplotlib.patches as mpatches
# import Algal_Oil as A_processing
# import corn_grain_processing as CG_processing
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import plotly.io as pio
pio.renderers.default = 'browser'


labels = ['1998', '1999', '2000', '2001', '2002', '2003', '2004',
          '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013']

# my_billion_list = ['3','6']
# version = ['district']


# my_billion_list = ['3','9','12','15']
# version = ['_0.001district']


my_billion_list = ['3','6','9','12','15','18','20']
version = ['_100000_0.1district','_100000_0.001district',
            '_1000000_0.1district','_1000000_0.001district','_10000000_0.1district','_10000000_0.001district']


for billion in my_billion_list:
    
    bg = int(billion) ## We will try 0, 3, 6, 9, 12, 15, 18, 20   biofuel gallon 
    bgg =  bg*10**9  # conversion to billion  
    con = 30.81*(1/0.2641)  ## MJ/litre * liter/gallons   ## jet fuels conversion
    quota = bgg*con  ## energy as MJ/yr

    quota_U = quota*1.02
    quota_L = quota*0.98
    
    for v in version:

        plt.rcParams.update({'font.size': 14})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams["font.weight"] = "bold"
        plt.rcParams["axes.labelweight"] = "bold"
    
        # import excel sheet
        df_geo_corn = pd.read_excel('Platypus_codes/combined_pivot_Corn.xlsx', header=0, engine='openpyxl')
        df_geo_soy = pd.read_excel('Platypus_codes/combined_pivot_Soy.xlsx', header=0, engine='openpyxl')
        df_geo_grass_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Switchgrass.xlsx', header=0, engine='openpyxl')
        df_geo_grass = pd.read_excel('Platypus_codes/combined_pivot_ML_Switchgrass.xlsx', header=0, engine='openpyxl')
        df_geo_algae_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Algae.xlsx', header=0, engine='openpyxl')
        df_geo_algae = pd.read_excel('Platypus_codes/combined_pivot_ML_Algae.xlsx', header=0, engine='openpyxl')
    

        fn_ha = 'Decision_Variables_borg_crops_GHG' + billion + v + '_PARETO' +'.csv'
        df_ha = pd.read_csv(fn_ha, header=0, index_col=0)
    
        fn = 'Objective_functions_borg_crops_GHG' + billion + v + '_PARETO' +'.csv'
        df_O = pd.read_csv(fn, header=0, index_col=0)

        num_c = len(df_geo_corn)
        
        ## Dividing corn, soy, grass and algae yield data.
        C_ha = np.transpose(df_ha).iloc[0:num_c].values # used hectare for corn 
        S_ha = np.transpose(df_ha).iloc[0:num_c].values # used hectare for soy
        G_ha = np.transpose(df_ha).iloc[num_c:2*num_c].values # used hectare for grass
        A_ha = np.transpose(df_ha).iloc[2*num_c:3*num_c].values # used hectare for algae
        G_ha_L = np.transpose(df_ha).iloc[3*num_c:4*num_c].values # used hectare for grass
        A_ha_L = np.transpose(df_ha).iloc[4*num_c:].values # used hectare for algae
    
        LL = df_geo_corn['land_limits_ha'].values
    
        years = range(1998, 2014)
        solution = range(len(df_ha))
    
        # Corn Grain yield
        C_yield = df_geo_corn.loc[:, 1998:2013].values  # yield in kg/ha
    
        # Soybean yield
        S_yield = df_geo_soy.loc[:, 1998:2013].values  # yield in kg/ha
    
        # Grass yield
        G_yield_L = df_geo_grass_L.loc[:, 1998:2013].values  # yield in kg/ha
    
        G_yield = df_geo_grass.loc[:, 1998:2013].values  # yield in kg/ha
    
        # Algea yield
        A_yield_L = df_geo_algae_L.loc[:, 1998:2013].values  # yield in kg/ha
    
        A_yield = df_geo_algae.loc[:, 1998:2013].values  # yield in kg/ha
    
        num_c = np.size(LL)  # size of land cost
        Energy_total = np.zeros((len(years), 1))
    
        CG_ethanol_total_MJ = np.zeros((len(df_ha), len(years)))
        SB_oil_total_MJ = np.zeros((len(df_ha), len(years)))
        CS_total_MJ = np.zeros((len(df_ha), len(years)))
        G_energy_total_MJ = np.zeros((len(df_ha), len(years)))
        A_energy_total_MJ = np.zeros((len(df_ha), len(years)))
        G_energy_total_MJ_L = np.zeros((len(df_ha), len(years)))
        A_energy_total_MJ_L = np.zeros((len(df_ha), len(years)))
    
        CS_ethanol_avg = np.zeros((len(df_ha), 1))
        SB_oil_avg = np.zeros((len(df_ha), 1))
        CS_avg = np.zeros((len(df_ha), 1))
        G_energy_avg = np.zeros((len(df_ha), 1))
        A_energy_avg = np.zeros((len(df_ha), 1))
        G_energy_avg_L = np.zeros((len(df_ha), 1))
        A_energy_avg_L = np.zeros((len(df_ha), 1))
    
        # Energy_total = np.zeros((len(solution),1))
    
        for year in years:
            i = years.index(year)
            Y = C_yield[:, i]   # corn yield kg/ha
            S = S_yield[:, i]   # soy yield kg/ha
            G = G_yield[:, i]   # grass yield kg/ha
            A = A_yield[:, i]   # algae yield kg/ha
            G_L = G_yield_L[:, i]   # grass yield kg/ha
            A_L = A_yield_L[:, i]   # algae yield kg/ha
    
            for s in solution:
                CG_prod = sum(C_ha[:, s]*Y/2) #Based on each year and each state total corn biomass production (kg) calculated

                SB_prod = sum(S_ha[:, s]*S/2) #Based on each year and each state total corn biomass production (kg) calculated
    
                G_prod = sum(G_ha[:, s]*G) #Based on each year and each state total corn biomass production (kg) calculated
    
                A_prod = sum(A_ha[:, s]*A) #Based on each year and each state total corn biomass production (kg) calculated
    
                G_prod_L = sum(G_ha_L[:, s]*G_L) #Based on each year and each state total corn biomass production (kg) calculated
    
                A_prod_L = sum(A_ha_L[:, s]*A_L) #Based on each year and each state total corn biomass production (kg) calculated
                
                CG_MJ = CG_prod*9.42 #MJ/kg
                S_MJ = SB_prod*8.02 #MJ/kg
                CS_MJ = CG_MJ + S_MJ
                G_MJ = G_prod*8.35 #MJ/kg
                A_MJ = A_prod*20.82 #MJ/kg
                G_AG_MJ = G_prod_L*8.35 #MJ/kg
                A_AG_MJ = A_prod_L*20.82 #MJ/kg
                
                CG_ethanol_total_MJ[s] = CG_MJ
                SB_oil_total_MJ[s] = S_MJ
                CS_total_MJ[s] = CS_MJ
                G_energy_total_MJ[s] = G_MJ
                A_energy_total_MJ[s] = A_MJ
                G_energy_total_MJ_L[s] = G_AG_MJ
                A_energy_total_MJ_L[s] = A_AG_MJ
                
    
        df_O.columns = ['cost', 'max_energy_shortfall','min_GHG_emission']
        df_O.reset_index(drop=True, inplace=True)
        
        
        fig, ax = plt.subplots(1,2, figsize=(13, 5.3),constrained_layout = True)
        fig.suptitle(billion + v, fontsize=16)
    
    
        sorting = df_O.sort_values(by='max_energy_shortfall', ascending=True)
        # sorting = df_O.sort_values(by='min_GHG_emission', ascending=True)
        
        
        CS_en = CS_total_MJ
        G_en = G_energy_total_MJ
        A_en = A_energy_total_MJ
        G_en_L = G_energy_total_MJ_L
        A_en_L = A_energy_total_MJ_L
    
    
        C_corn = [a[0] for a in CS_en]
        G_grass = [a[0] for a in G_en]
        A_algae = [a[0] for a in A_en]
        G_grass_L = [a[0] for a in G_en_L]
        A_algae_L = [a[0] for a in A_en_L]
    
        my_index = list(sorting.index)
        # plt.stackplot()
        CC_corn = [C_corn[y] for y in my_index]
        GG_grass = [G_grass[y] for y in my_index]
        AA_algae = [A_algae[y] for y in my_index]
        GG_grass_L = [G_grass_L[y] for y in my_index]
        AA_algae_L = [A_algae_L[y] for y in my_index]
    
        a = len(df_ha)
        x = list(range(0, a))
        
        color_map = ["#023e8a", "#ffbe0b", "#d90429", "#8ac926", "#6a4c93"]
        ax[0].stackplot(x, CC_corn, GG_grass, AA_algae, GG_grass_L, AA_algae_L, labels=[
                      'Corn/soy_AG', 'Grass_ML', 'Algae_ML', 'Grass_AG', 'Algae_AG'], colors=color_map)
        ax[0].axhline(y=quota, xmin=0, xmax=3, c="black", linewidth=2, zorder=1, linestyle = '--')
        ax[0].axhline(y=quota_U, xmin=0, xmax=3, c="red", linewidth=2, zorder=1, linestyle = '--')
        ax[0].axhline(y=quota_L, xmin=0, xmax=3, c="red", linewidth=2, zorder=1, linestyle = '--')
            
        # plt.legend( bbox_to_anchor=(2, 2),  loc='upper right')
        axis_fontsize = 14
        axis_fontsize = 14
        ax[0].set_ylabel('Total Fuel Production (MJ)')
        ax[0].set_xticks(np.arange(0, a, step=100), rotation=40)
        ax[0].grid(False)
        
        ax[0].set_title('Sorted Energy Shortfall Solution',fontsize=14, fontweight="bold")
        # ax[0].set_title('Sorted GHG Emission Solution',fontsize=14, fontweight="bold")
        
        
        
        sorting = df_O.sort_values(by='cost', ascending=True)
    
        CS_en = CS_total_MJ
        G_en = G_energy_total_MJ
        A_en = A_energy_total_MJ
        G_en_L = G_energy_total_MJ_L
        A_en_L = A_energy_total_MJ_L
    
    
        C_corn = [a[0] for a in CS_en]
        G_grass = [a[0] for a in G_en]
        A_algae = [a[0] for a in A_en]
        G_grass_L = [a[0] for a in G_en_L]
        A_algae_L = [a[0] for a in A_en_L]
    
        my_index = list(sorting.index)
        # plt.stackplot()
        CC_corn = [C_corn[y] for y in my_index]
        GG_grass = [G_grass[y] for y in my_index]
        AA_algae = [A_algae[y] for y in my_index]
        GG_grass_L = [G_grass_L[y] for y in my_index]
        AA_algae_L = [A_algae_L[y] for y in my_index]
    
        a = len(df_ha)
        x = list(range(0, a))

        color_map = ["#023e8a", "#ffbe0b", "#d90429", "#8ac926", "#6a4c93"]
        ax[1].stackplot(x, CC_corn, GG_grass, AA_algae, GG_grass_L, AA_algae_L, labels=[
                      'Corn/soy_AG', 'Grass_ML', 'Algae_ML', 'Grass_AG', 'Algae_AG'], colors=color_map)
        ax[1].axhline(y=quota, xmin=0, xmax=3, c="black", linewidth=2, zorder=1, linestyle = '--')
        ax[1].axhline(y=quota_U, xmin=0, xmax=3, c="red", linewidth=2, zorder=1, linestyle = '--')
        ax[1].axhline(y=quota_L, xmin=0, xmax=3, c="red", linewidth=2, zorder=1, linestyle = '--')
        # ax[1].legend( bbox_to_anchor=(2, 2),  loc='upper right')
        axis_fontsize = 14
        axis_fontsize = 14
        ax[1].set_ylabel('Total Fuel Production (MJ)')
        ax[1].set_xticks(np.arange(0, a, step=100), rotation=40)
        ax[1].grid(False)
    
        ax[1].set_title('Sorted Cost Solution',fontsize=14,fontweight="bold")
        
        plt.savefig('Stack_graph_cluster' + billion + v + '.png',dpi=150, bbox_inches='tight')
        
        # sorting = df_O.sort_values(by='min_GHG_emission', ascending=True)



