# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:41:16 2023

@author: eari
"""

# library
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd
from pysal.lib import weights
import geopandas as gpd
from pysal.explore import esda
import matplotlib as mpl


# objective = 'min_GHG_emission'


total_land_limit =pd.read_excel('Platypus_codes/total_land_limit.xlsx',header=0, engine='openpyxl')
land_limit = total_land_limit['land_limits_ha']

df_geo_corn = pd.read_excel('Platypus_codes/combined_pivot_Corn.xlsx', header=0, engine='openpyxl')

num_c = len(df_geo_corn)


CS_ha_total_AG = sum(np.transpose(land_limit).iloc[0:num_c].values) # used hectare for corn 
G_ha_total_ML = sum(np.transpose(land_limit).iloc[num_c:2*num_c].values) # used hectare for grass
A_ha_total_ML = sum(np.transpose(land_limit).iloc[2*num_c:3*num_c].values) # used hectare for algae
G_ha_total_AG = sum(np.transpose(land_limit).iloc[3*num_c:4*num_c].values) # used hectare for grass
A_ha_total_AG = sum(np.transpose(land_limit).iloc[4*num_c:].values) # used hectare for algae
total_AG = CS_ha_total_AG


# billion = ['3','6','9','12']
# version = ['_100000_0.1district']  

billion = ['3','6','9','12','15','18','20']
version = ['_100000_0.001district', '_1000000_0.001district','_10000000_0.001district'] #,'_10000000_0.1district', '_1000000_0.1district',


for v in version:
    
    objective = 'max_energy_shortfall'

    ### 3 billion ###
    
    fn_ha3 = 'Decision_Variables_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    df_ha3 = pd.read_csv(fn_ha3,header=0,index_col=0)
    
    fn3 = 'Objective_functions_borg_crops_GHG3' + v + '_PARETO' +'.csv'
    df_O3 = pd.read_csv(fn3,header=0,index_col=0)
    # df_O3.reset_index(drop=True,inplace=True)
    
    df_O3.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting3 = df_O3.sort_values(by= objective, ascending=True).head(1)
    
    my_index3 = list(sorting3.index)
    df_ha3_sorted = df_ha3.loc[my_index3]
    
    CS_ha_AG3 = sum(np.transpose(df_ha3_sorted).iloc[0:num_c].values) # used hectare for corn 
    G_ha_ML3 = sum(np.transpose(df_ha3_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML3 = sum(np.transpose(df_ha3_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG3 = sum(np.transpose(df_ha3_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG3 = sum(np.transpose(df_ha3_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_3 = CS_ha_AG3 + G_ha_AG3 + A_ha_AG3
    
    # Selected_ha_C_AG3 = [C_ha_AG3[y] for y in my_index3]
    # Selected_ha_S_AG3 = [S_ha_AG3[y] for y in my_index3]
    # Selected_ha_G_ML3 = [G_ha_ML3[y] for y in my_index3]
    # Selected_ha_A_ML3 = [A_ha_ML3[y] for y in my_index3]
    # Selected_ha_G_AG3 = [G_ha_AG3[y] for y in my_index3]
    # Selected_ha_A_AG3 = [A_ha_AG3[y] for y in my_index3]
    
    
    ### 6 billion ###
    
    fn_ha6 = 'Decision_Variables_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_ha6 = pd.read_csv(fn_ha6,header=0,index_col=0)
    
    fn6 = 'Objective_functions_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_O6 = pd.read_csv(fn6,header=0,index_col=0)
    # df_O6.reset_index(drop=True,inplace=True)
    
    df_O6.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting6 = df_O6.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index6 = list(sorting6.index)
    df_ha6_sorted = df_ha6.loc[my_index6]
    
    CS_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML6 = sum(np.transpose(df_ha6_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML6 = sum(np.transpose(df_ha6_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_6 = CS_ha_AG6 + G_ha_AG6 + A_ha_AG6
    
    # Selected_ha_C_AG6 = [C_ha_AG6[y] for y in my_index6]
    # Selected_ha_S_AG6 = [S_ha_AG6[y] for y in my_index6]
    # Selected_ha_G_ML6 = [G_ha_ML6[y] for y in my_index6]
    # Selected_ha_A_ML6 = [A_ha_ML6[y] for y in my_index6]
    # Selected_ha_G_AG6 = [G_ha_AG6[y] for y in my_index6]
    # Selected_ha_A_AG6 = [A_ha_AG6[y] for y in my_index6]
    
    ### 9 billion ###
    
    fn_ha9 = 'Decision_Variables_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_ha9 = pd.read_csv(fn_ha9,header=0,index_col=0)
    
    fn9 = 'Objective_functions_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_O9 = pd.read_csv(fn9,header=0,index_col=0)
    # df_O9.reset_index(drop=True,inplace=True)
    
    df_O9.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting9 = df_O9.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index9 = list(sorting9.index)
    df_ha9_sorted = df_ha9.loc[my_index9]
    
    CS_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML9 = sum(np.transpose(df_ha9_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML9 = sum(np.transpose(df_ha9_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_9 = CS_ha_AG9 + G_ha_AG9 + A_ha_AG9
    
    # Selected_ha_C_AG9 = [C_ha_AG9[y] for y in my_index9]
    # Selected_ha_S_AG9 = [S_ha_AG9[y] for y in my_index9]
    # Selected_ha_G_ML9 = [G_ha_ML9[y] for y in my_index9]
    # Selected_ha_A_ML9 = [A_ha_ML9[y] for y in my_index9]
    # Selected_ha_G_AG9 = [G_ha_AG9[y] for y in my_index9]
    # Selected_ha_A_AG9 = [A_ha_AG9[y] for y in my_index9]
    
    ### 12 billion ###
    
    fn_ha12 = 'Decision_Variables_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_ha12 = pd.read_csv(fn_ha12,header=0,index_col=0)
    
    fn12 = 'Objective_functions_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_O12 = pd.read_csv(fn12,header=0,index_col=0)
    # df_O12.reset_index(drop=True,inplace=True)
    
    df_O12.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting12 = df_O12.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index12 = list(sorting12.index)
    df_ha12_sorted = df_ha12.loc[my_index12]
    
    CS_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML12 = sum(np.transpose(df_ha12_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML12 = sum(np.transpose(df_ha12_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_12 = CS_ha_AG12 + G_ha_AG12 + A_ha_AG12
    
    # Selected_ha_C_AG12 = [C_ha_AG12[y] for y in my_index12]
    # Selected_ha_S_AG12 = [S_ha_AG12[y] for y in my_index12]
    # Selected_ha_G_ML12 = [G_ha_ML12[y] for y in my_index12]
    # Selected_ha_A_ML12 = [A_ha_ML12[y] for y in my_index12]
    # Selected_ha_G_AG12 = [G_ha_AG12[y] for y in my_index12]
    # Selected_ha_A_AG12 = [A_ha_AG12[y] for y in my_index12]
    
    ### 15 billion ###
    
    fn_ha15 = 'Decision_Variables_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_ha15 = pd.read_csv(fn_ha15,header=0,index_col=0)
    
    fn15 = 'Objective_functions_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_O15 = pd.read_csv(fn15,header=0,index_col=0)
    # df_O15.reset_index(drop=True,inplace=True)
    
    df_O15.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting15 = df_O15.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index15 = list(sorting15.index)
    df_ha15_sorted = df_ha15.loc[my_index15]
    
    CS_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML15 = sum(np.transpose(df_ha15_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML15 = sum(np.transpose(df_ha15_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_15 = CS_ha_AG15 + G_ha_AG15 + A_ha_AG15
    
    # Selected_ha_C_AG15 = [C_ha_AG15[y] for y in my_index15]
    # Selected_ha_S_AG15 = [S_ha_AG15[y] for y in my_index15]
    # Selected_ha_G_ML15 = [G_ha_ML15[y] for y in my_index15]
    # Selected_ha_A_ML15 = [A_ha_ML15[y] for y in my_index15]
    # Selected_ha_G_AG15 = [G_ha_AG15[y] for y in my_index15]
    # Selected_ha_A_AG15 = [A_ha_AG15[y] for y in my_index15]
    
    ### 18 billion ###
    
    fn_ha18 = 'Decision_Variables_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_ha18 = pd.read_csv(fn_ha18,header=0,index_col=0)
    
    fn18 = 'Objective_functions_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_O18 = pd.read_csv(fn18,header=0,index_col=0)
    # df_O18.reset_index(drop=True,inplace=True)
    
    df_O18.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting18 = df_O18.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index18 = list(sorting18.index)
    df_ha18_sorted = df_ha18.loc[my_index18]
    
    CS_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML18 = sum(np.transpose(df_ha18_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML18 = sum(np.transpose(df_ha18_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_18 = CS_ha_AG18 + G_ha_AG18 + A_ha_AG18
    
    # Selected_ha_C_AG18 = [C_ha_AG18[y] for y in my_index18]
    # Selected_ha_S_AG18 = [S_ha_AG18[y] for y in my_index18]
    # Selected_ha_G_ML18 = [G_ha_ML18[y] for y in my_index18]
    # Selected_ha_A_ML18 = [A_ha_ML18[y] for y in my_index18]
    # Selected_ha_G_AG18 = [G_ha_AG18[y] for y in my_index18]
    # Selected_ha_A_AG18 = [A_ha_AG18[y] for y in my_index18]
    
    ### 20 billion ###
    
    fn_ha20 = 'Decision_Variables_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_ha20 = pd.read_csv(fn_ha20,header=0,index_col=0)
    
    fn20 = 'Objective_functions_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_O20 = pd.read_csv(fn20,header=0,index_col=0)
    # df_O20.reset_index(drop=True,inplace=True)
    
    df_O20.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting20 = df_O20.sort_values(by= objective, ascending=True).head(1)
    
    my_index20 = list(sorting20.index)
    df_ha20_sorted = df_ha20.loc[my_index20]
    
    CS_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML20 = sum(np.transpose(df_ha20_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML20 = sum(np.transpose(df_ha20_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_20 = CS_ha_AG20 + G_ha_AG20 + A_ha_AG20
    
    # Selected_ha_C_AG20 = [C_ha_AG20[y] for y in my_index20]
    # Selected_ha_S_AG20 = [S_ha_AG20[y] for y in my_index20]
    # Selected_ha_G_ML20 = [G_ha_ML20[y] for y in my_index20]
    # Selected_ha_A_ML20 = [A_ha_ML20[y] for y in my_index20]
    # Selected_ha_G_AG20 = [G_ha_AG20[y] for y in my_index20]
    # Selected_ha_A_AG20 = [A_ha_AG20[y] for y in my_index20]
    
    
    #### Creating Bar Chart ####
    # set width of bar
    barWidth = 0.1
    fig = plt.subplots(figsize =(12,8))
    
    
    # set height of bar
    # Corn_AG = [Selected_ha_C_AG3[0],Selected_ha_C_AG6[0],Selected_ha_C_AG9[0]]
    # Soy_AG = [Selected_ha_S_AG3[0],Selected_ha_S_AG6[0],Selected_ha_S_AG9[0]]
    # Grass_ML = [Selected_ha_G_ML3[0],Selected_ha_G_ML6[0],Selected_ha_G_ML9[0]]
    # Algae_ML = [Selected_ha_A_ML3[0]]
    # Grass_AG = [Selected_ha_G_AG3[0]]
    # Algae_AG = [Selected_ha_A_AG3[0]]
    
    # billion3 = [C_ha_AG3[0],S_ha_AG3[0],G_ha_ML3[0],A_ha_ML3[0],G_ha_AG3[0],A_ha_AG3[0]]
    # billion6 = [C_ha_AG6[0],S_ha_AG6[0],G_ha_ML6[0],A_ha_ML6[0],G_ha_AG6[0],A_ha_AG6[0]]
    # billion9 = [C_ha_AG9[0],S_ha_AG9[0],G_ha_ML9[0],A_ha_ML9[0],G_ha_AG9[0],A_ha_AG9[0]]
    # billion12 = [C_ha_AG12[0],S_ha_AG12[0],G_ha_ML12[0],A_ha_ML12[0],G_ha_AG12[0],A_ha_AG12[0]]
    # billion15 = [C_ha_AG15[0],S_ha_AG15[0],G_ha_ML15[0],A_ha_ML15[0],G_ha_AG15[0],A_ha_AG15[0]]
    # billion18 = [C_ha_AG18[0],S_ha_AG18[0],G_ha_ML18[0],A_ha_ML18[0],G_ha_AG18[0],A_ha_AG18[0]]
    # billion20 = [C_ha_AG20[0],S_ha_AG20[0],G_ha_ML20[0],A_ha_ML20[0],G_ha_AG20[0],A_ha_AG20[0]]
    
    billion3 = [CS_ha_AG3[0],G_ha_ML3[0],A_ha_ML3[0],G_ha_AG3[0],A_ha_AG3[0],total_AG_3[0]]
    billion6 = [CS_ha_AG6[0],G_ha_ML6[0],A_ha_ML6[0],G_ha_AG6[0],A_ha_AG6[0],total_AG_6[0]]
    billion9 = [CS_ha_AG9[0],G_ha_ML9[0],A_ha_ML9[0],G_ha_AG9[0],A_ha_AG9[0],total_AG_9[0]]
    billion12 = [CS_ha_AG12[0],G_ha_ML12[0],A_ha_ML12[0],G_ha_AG12[0],A_ha_AG12[0],total_AG_12[0]]
    billion15 = [CS_ha_AG15[0],G_ha_ML15[0],A_ha_ML15[0],G_ha_AG15[0],A_ha_AG15[0],total_AG_15[0]]
    billion18 = [CS_ha_AG18[0],G_ha_ML18[0],A_ha_ML18[0],G_ha_AG18[0],A_ha_AG18[0],total_AG_18[0]]
    billion20 = [CS_ha_AG20[0],G_ha_ML20[0],A_ha_ML20[0],G_ha_AG20[0],A_ha_AG20[0],total_AG_20[0]] 
    total = [CS_ha_total_AG,G_ha_total_ML,A_ha_total_ML,G_ha_total_AG,A_ha_total_AG,CS_ha_total_AG]
    
    
    
    # Set position of bar on X axis
    br1 = np.arange(len(billion3))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    br5 = [x + barWidth for x in br4]
    br6 = [x + barWidth for x in br5]
    br7 = [x + barWidth for x in br6]
    br8 = [x + barWidth for x in br7]
    
    # Make the plot
    plt.bar(br1, billion3, color ='#448aff', width = barWidth,
            edgecolor ='black', label ='3 billion')
    plt.bar(br2, billion6, color ='#1565c0', width = barWidth,
            edgecolor ='black', label ='6 billion')
    plt.bar(br3, billion9, color ='#009688', width = barWidth,
            edgecolor ='black', label ='9 billion')
    plt.bar(br4, billion12, color ='#8bc34a', width = barWidth,
            edgecolor ='black', label ='12 billion')
    plt.bar(br5, billion15, color ='#ffc107', width = barWidth,
            edgecolor ='black', label ='15 billion')
    plt.bar(br6, billion18, color ='#ff9800', width = barWidth,
            edgecolor ='black', label ='18 billion')
    plt.bar(br7, billion20, color ='#f44336', width = barWidth,
            edgecolor ='black', label ='20 billion')
    plt.bar(br8, total, color ='#ad1457', width = barWidth,
            edgecolor ='black', label ='total land limit')
     
    
    # # Make the plot
    # plt.bar(br1, billion3, color ='#377eb8', width = barWidth,
    #         edgecolor ='grey', label ='3 billion')
    # plt.bar(br2, billion6, color ='#ff7f00', width = barWidth,
    #         edgecolor ='grey', label ='6 billion')
    # plt.bar(br3, billion9, color ='#4daf4a', width = barWidth,
    #         edgecolor ='grey', label ='9 billion')
    # plt.bar(br4, billion12, color ='#f781bf', width = barWidth,
    #         edgecolor ='grey', label ='12 billion')
    # plt.bar(br5, billion15, color ='#dede00', width = barWidth,
    #         edgecolor ='grey', label ='15 billion')
    # plt.bar(br6, billion18, color ='#984ea3', width = barWidth,
    #         edgecolor ='grey', label ='18 billion')
    # plt.bar(br7, billion20, color ='#999999', width = barWidth,
    #         edgecolor ='grey', label ='20 billion')
    # plt.bar(br8, total, color ='#e41a1c', width = barWidth,
    #         edgecolor ='grey', label ='total land limit')
    
    
    
    
    # Adding Xticks
    plt.xlabel('Crop Type', fontweight ='bold', fontsize = 12)
    plt.ylabel('Total Used ha', fontweight ='bold', fontsize = 12)
    plt.xticks([r + 0.3 for r in range(len(billion3))],
            ['Corn/Soy_AG', 'Grass_ML', 'Algae_ML', 'Grass_AG', 'Algae_AG','Total_AG_land'])
    
    plt.title('Minimize Maximum Energy Shortfall',fontsize=12,fontweight="bold")
    # plt.title('Minimum GHG Emission',fontsize=12,fontweight="bold")
    # plt.title('Minimum Cost',fontsize=12,fontweight="bold")
      
    plt.legend()
    plt.grid(False)
    
    plt.savefig('Bar_graph_energy_shortfall' + v + '.png',dpi=150, bbox_inches='tight')
    
    
    
    
    
    objective = 'cost'
    
    ### 3 billion ###
    
    fn_ha3 = 'Decision_Variables_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    df_ha3 = pd.read_csv(fn_ha3,header=0,index_col=0)
    
    fn3 = 'Objective_functions_borg_crops_GHG3' + v + '_PARETO' +'.csv'
    df_O3 = pd.read_csv(fn3,header=0,index_col=0)
    # df_O3.reset_index(drop=True,inplace=True)
    
    df_O3.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting3 = df_O3.sort_values(by= objective, ascending=True).head(1)
    
    my_index3 = list(sorting3.index)
    df_ha3_sorted = df_ha3.loc[my_index3]
    
    CS_ha_AG3 = sum(np.transpose(df_ha3_sorted).iloc[0:num_c].values) # used hectare for corn 
    G_ha_ML3 = sum(np.transpose(df_ha3_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML3 = sum(np.transpose(df_ha3_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG3 = sum(np.transpose(df_ha3_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG3 = sum(np.transpose(df_ha3_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_3 = CS_ha_AG3 + G_ha_AG3 + A_ha_AG3
    
    # Selected_ha_C_AG3 = [C_ha_AG3[y] for y in my_index3]
    # Selected_ha_S_AG3 = [S_ha_AG3[y] for y in my_index3]
    # Selected_ha_G_ML3 = [G_ha_ML3[y] for y in my_index3]
    # Selected_ha_A_ML3 = [A_ha_ML3[y] for y in my_index3]
    # Selected_ha_G_AG3 = [G_ha_AG3[y] for y in my_index3]
    # Selected_ha_A_AG3 = [A_ha_AG3[y] for y in my_index3]
    
    
    ### 6 billion ###
    
    fn_ha6 = 'Decision_Variables_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_ha6 = pd.read_csv(fn_ha6,header=0,index_col=0)
    
    fn6 = 'Objective_functions_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_O6 = pd.read_csv(fn6,header=0,index_col=0)
    # df_O6.reset_index(drop=True,inplace=True)
    
    df_O6.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting6 = df_O6.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index6 = list(sorting6.index)
    df_ha6_sorted = df_ha6.loc[my_index6]
    
    CS_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML6 = sum(np.transpose(df_ha6_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML6 = sum(np.transpose(df_ha6_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG6 = sum(np.transpose(df_ha6_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_6 = CS_ha_AG6 + G_ha_AG6 + A_ha_AG6
    
    # Selected_ha_C_AG6 = [C_ha_AG6[y] for y in my_index6]
    # Selected_ha_S_AG6 = [S_ha_AG6[y] for y in my_index6]
    # Selected_ha_G_ML6 = [G_ha_ML6[y] for y in my_index6]
    # Selected_ha_A_ML6 = [A_ha_ML6[y] for y in my_index6]
    # Selected_ha_G_AG6 = [G_ha_AG6[y] for y in my_index6]
    # Selected_ha_A_AG6 = [A_ha_AG6[y] for y in my_index6]
    
    ### 9 billion ###
    
    fn_ha9 = 'Decision_Variables_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_ha9 = pd.read_csv(fn_ha9,header=0,index_col=0)
    
    fn9 = 'Objective_functions_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_O9 = pd.read_csv(fn9,header=0,index_col=0)
    # df_O9.reset_index(drop=True,inplace=True)
    
    df_O9.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting9 = df_O9.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index9 = list(sorting9.index)
    df_ha9_sorted = df_ha9.loc[my_index9]
    
    CS_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML9 = sum(np.transpose(df_ha9_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML9 = sum(np.transpose(df_ha9_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG9 = sum(np.transpose(df_ha9_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_9 = CS_ha_AG9 + G_ha_AG9 + A_ha_AG9
    
    # Selected_ha_C_AG9 = [C_ha_AG9[y] for y in my_index9]
    # Selected_ha_S_AG9 = [S_ha_AG9[y] for y in my_index9]
    # Selected_ha_G_ML9 = [G_ha_ML9[y] for y in my_index9]
    # Selected_ha_A_ML9 = [A_ha_ML9[y] for y in my_index9]
    # Selected_ha_G_AG9 = [G_ha_AG9[y] for y in my_index9]
    # Selected_ha_A_AG9 = [A_ha_AG9[y] for y in my_index9]
    
    ### 12 billion ###
    
    fn_ha12 = 'Decision_Variables_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_ha12 = pd.read_csv(fn_ha12,header=0,index_col=0)
    
    fn12 = 'Objective_functions_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_O12 = pd.read_csv(fn12,header=0,index_col=0)
    # df_O12.reset_index(drop=True,inplace=True)
    
    df_O12.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting12 = df_O12.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index12 = list(sorting12.index)
    df_ha12_sorted = df_ha12.loc[my_index12]
    
    CS_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML12 = sum(np.transpose(df_ha12_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML12 = sum(np.transpose(df_ha12_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG12 = sum(np.transpose(df_ha12_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_12 = CS_ha_AG12 + G_ha_AG12 + A_ha_AG12
    
    # Selected_ha_C_AG12 = [C_ha_AG12[y] for y in my_index12]
    # Selected_ha_S_AG12 = [S_ha_AG12[y] for y in my_index12]
    # Selected_ha_G_ML12 = [G_ha_ML12[y] for y in my_index12]
    # Selected_ha_A_ML12 = [A_ha_ML12[y] for y in my_index12]
    # Selected_ha_G_AG12 = [G_ha_AG12[y] for y in my_index12]
    # Selected_ha_A_AG12 = [A_ha_AG12[y] for y in my_index12]
    
    ### 15 billion ###
    
    fn_ha15 = 'Decision_Variables_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_ha15 = pd.read_csv(fn_ha15,header=0,index_col=0)
    
    fn15 = 'Objective_functions_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_O15 = pd.read_csv(fn15,header=0,index_col=0)
    # df_O15.reset_index(drop=True,inplace=True)
    
    df_O15.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting15 = df_O15.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index15 = list(sorting15.index)
    df_ha15_sorted = df_ha15.loc[my_index15]
    
    CS_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML15 = sum(np.transpose(df_ha15_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML15 = sum(np.transpose(df_ha15_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG15 = sum(np.transpose(df_ha15_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_15 = CS_ha_AG15 + G_ha_AG15 + A_ha_AG15
    
    # Selected_ha_C_AG15 = [C_ha_AG15[y] for y in my_index15]
    # Selected_ha_S_AG15 = [S_ha_AG15[y] for y in my_index15]
    # Selected_ha_G_ML15 = [G_ha_ML15[y] for y in my_index15]
    # Selected_ha_A_ML15 = [A_ha_ML15[y] for y in my_index15]
    # Selected_ha_G_AG15 = [G_ha_AG15[y] for y in my_index15]
    # Selected_ha_A_AG15 = [A_ha_AG15[y] for y in my_index15]
    
    ### 18 billion ###
    
    fn_ha18 = 'Decision_Variables_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_ha18 = pd.read_csv(fn_ha18,header=0,index_col=0)
    
    fn18 = 'Objective_functions_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_O18 = pd.read_csv(fn18,header=0,index_col=0)
    # df_O18.reset_index(drop=True,inplace=True)
    
    df_O18.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting18 = df_O18.sort_values(by= objective, ascending=True).head(1)
    
    
    my_index18 = list(sorting18.index)
    df_ha18_sorted = df_ha18.loc[my_index18]
    
    CS_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML18 = sum(np.transpose(df_ha18_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML18 = sum(np.transpose(df_ha18_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG18 = sum(np.transpose(df_ha18_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_18 = CS_ha_AG18 + G_ha_AG18 + A_ha_AG18
    
    # Selected_ha_C_AG18 = [C_ha_AG18[y] for y in my_index18]
    # Selected_ha_S_AG18 = [S_ha_AG18[y] for y in my_index18]
    # Selected_ha_G_ML18 = [G_ha_ML18[y] for y in my_index18]
    # Selected_ha_A_ML18 = [A_ha_ML18[y] for y in my_index18]
    # Selected_ha_G_AG18 = [G_ha_AG18[y] for y in my_index18]
    # Selected_ha_A_AG18 = [A_ha_AG18[y] for y in my_index18]
    
    ### 20 billion ###
    
    fn_ha20 = 'Decision_Variables_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_ha20 = pd.read_csv(fn_ha20,header=0,index_col=0)
    
    fn20 = 'Objective_functions_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_O20 = pd.read_csv(fn20,header=0,index_col=0)
    # df_O20.reset_index(drop=True,inplace=True)
    
    df_O20.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting20 = df_O20.sort_values(by= objective, ascending=True).head(1)
    
    my_index20 = list(sorting20.index)
    df_ha20_sorted = df_ha20.loc[my_index20]
    
    CS_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[0:num_c].values) # used hectare for corn 
    # S_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[0:107].values) # used hectare for soy
    G_ha_ML20 = sum(np.transpose(df_ha20_sorted).iloc[num_c:2*num_c].values) # used hectare for grass
    A_ha_ML20 = sum(np.transpose(df_ha20_sorted).iloc[2*num_c:3*num_c].values) # used hectare for algae
    G_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[3*num_c:4*num_c].values) # used hectare for grass
    A_ha_AG20 = sum(np.transpose(df_ha20_sorted).iloc[4*num_c:].values) # used hectare for algae
    total_AG_20 = CS_ha_AG20 + G_ha_AG20 + A_ha_AG20
    
    # Selected_ha_C_AG20 = [C_ha_AG20[y] for y in my_index20]
    # Selected_ha_S_AG20 = [S_ha_AG20[y] for y in my_index20]
    # Selected_ha_G_ML20 = [G_ha_ML20[y] for y in my_index20]
    # Selected_ha_A_ML20 = [A_ha_ML20[y] for y in my_index20]
    # Selected_ha_G_AG20 = [G_ha_AG20[y] for y in my_index20]
    # Selected_ha_A_AG20 = [A_ha_AG20[y] for y in my_index20]
    
    
    #### Creating Bar Chart ####
    # set width of bar
    barWidth = 0.1
    fig = plt.subplots(figsize =(12,8))
    
    
    # set height of bar
    # Corn_AG = [Selected_ha_C_AG3[0],Selected_ha_C_AG6[0],Selected_ha_C_AG9[0]]
    # Soy_AG = [Selected_ha_S_AG3[0],Selected_ha_S_AG6[0],Selected_ha_S_AG9[0]]
    # Grass_ML = [Selected_ha_G_ML3[0],Selected_ha_G_ML6[0],Selected_ha_G_ML9[0]]
    # Algae_ML = [Selected_ha_A_ML3[0]]
    # Grass_AG = [Selected_ha_G_AG3[0]]
    # Algae_AG = [Selected_ha_A_AG3[0]]
    
    # billion3 = [C_ha_AG3[0],S_ha_AG3[0],G_ha_ML3[0],A_ha_ML3[0],G_ha_AG3[0],A_ha_AG3[0]]
    # billion6 = [C_ha_AG6[0],S_ha_AG6[0],G_ha_ML6[0],A_ha_ML6[0],G_ha_AG6[0],A_ha_AG6[0]]
    # billion9 = [C_ha_AG9[0],S_ha_AG9[0],G_ha_ML9[0],A_ha_ML9[0],G_ha_AG9[0],A_ha_AG9[0]]
    # billion12 = [C_ha_AG12[0],S_ha_AG12[0],G_ha_ML12[0],A_ha_ML12[0],G_ha_AG12[0],A_ha_AG12[0]]
    # billion15 = [C_ha_AG15[0],S_ha_AG15[0],G_ha_ML15[0],A_ha_ML15[0],G_ha_AG15[0],A_ha_AG15[0]]
    # billion18 = [C_ha_AG18[0],S_ha_AG18[0],G_ha_ML18[0],A_ha_ML18[0],G_ha_AG18[0],A_ha_AG18[0]]
    # billion20 = [C_ha_AG20[0],S_ha_AG20[0],G_ha_ML20[0],A_ha_ML20[0],G_ha_AG20[0],A_ha_AG20[0]]
    
    billion3 = [CS_ha_AG3[0],G_ha_ML3[0],A_ha_ML3[0],G_ha_AG3[0],A_ha_AG3[0],total_AG_3[0]]
    billion6 = [CS_ha_AG6[0],G_ha_ML6[0],A_ha_ML6[0],G_ha_AG6[0],A_ha_AG6[0],total_AG_6[0]]
    billion9 = [CS_ha_AG9[0],G_ha_ML9[0],A_ha_ML9[0],G_ha_AG9[0],A_ha_AG9[0],total_AG_9[0]]
    billion12 = [CS_ha_AG12[0],G_ha_ML12[0],A_ha_ML12[0],G_ha_AG12[0],A_ha_AG12[0],total_AG_12[0]]
    billion15 = [CS_ha_AG15[0],G_ha_ML15[0],A_ha_ML15[0],G_ha_AG15[0],A_ha_AG15[0],total_AG_15[0]]
    billion18 = [CS_ha_AG18[0],G_ha_ML18[0],A_ha_ML18[0],G_ha_AG18[0],A_ha_AG18[0],total_AG_18[0]]
    billion20 = [CS_ha_AG20[0],G_ha_ML20[0],A_ha_ML20[0],G_ha_AG20[0],A_ha_AG20[0],total_AG_20[0]] 
    total = [CS_ha_total_AG,G_ha_total_ML,A_ha_total_ML,G_ha_total_AG,A_ha_total_AG,CS_ha_total_AG]
    
    
    
    # Set position of bar on X axis
    br1 = np.arange(len(billion3))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    br4 = [x + barWidth for x in br3]
    br5 = [x + barWidth for x in br4]
    br6 = [x + barWidth for x in br5]
    br7 = [x + barWidth for x in br6]
    br8 = [x + barWidth for x in br7]
    
    # Make the plot
    plt.bar(br1, billion3, color ='#448aff', width = barWidth,
            edgecolor ='black', label ='3 billion')
    plt.bar(br2, billion6, color ='#1565c0', width = barWidth,
            edgecolor ='black', label ='6 billion')
    plt.bar(br3, billion9, color ='#009688', width = barWidth,
            edgecolor ='black', label ='9 billion')
    plt.bar(br4, billion12, color ='#8bc34a', width = barWidth,
            edgecolor ='black', label ='12 billion')
    plt.bar(br5, billion15, color ='#ffc107', width = barWidth,
            edgecolor ='black', label ='15 billion')
    plt.bar(br6, billion18, color ='#ff9800', width = barWidth,
            edgecolor ='black', label ='18 billion')
    plt.bar(br7, billion20, color ='#f44336', width = barWidth,
            edgecolor ='black', label ='20 billion')
    plt.bar(br8, total, color ='#ad1457', width = barWidth,
            edgecolor ='black', label ='total land limit')
     
    
    # # Make the plot
    # plt.bar(br1, billion3, color ='#377eb8', width = barWidth,
    #         edgecolor ='grey', label ='3 billion')
    # plt.bar(br2, billion6, color ='#ff7f00', width = barWidth,
    #         edgecolor ='grey', label ='6 billion')
    # plt.bar(br3, billion9, color ='#4daf4a', width = barWidth,
    #         edgecolor ='grey', label ='9 billion')
    # plt.bar(br4, billion12, color ='#f781bf', width = barWidth,
    #         edgecolor ='grey', label ='12 billion')
    # plt.bar(br5, billion15, color ='#dede00', width = barWidth,
    #         edgecolor ='grey', label ='15 billion')
    # plt.bar(br6, billion18, color ='#984ea3', width = barWidth,
    #         edgecolor ='grey', label ='18 billion')
    # plt.bar(br7, billion20, color ='#999999', width = barWidth,
    #         edgecolor ='grey', label ='20 billion')
    # plt.bar(br8, total, color ='#e41a1c', width = barWidth,
    #         edgecolor ='grey', label ='total land limit')
    
    
    
    
    # Adding Xticks
    plt.xlabel('Crop Type', fontweight ='bold', fontsize = 12)
    plt.ylabel('Total Used ha', fontweight ='bold', fontsize = 12)
    plt.xticks([r + 0.3 for r in range(len(billion3))],
            ['Corn/Soy_AG', 'Grass_ML', 'Algae_ML', 'Grass_AG', 'Algae_AG','Total_AG_land'])

    plt.title('Minimum Cost',fontsize=12,fontweight="bold")
      
    plt.legend()
    plt.grid(False)
    
    plt.savefig('Bar_graph_cost' + v + '.png',dpi=150, bbox_inches='tight')
    
    
    
    
    
    
    
    
    
    
    
    
