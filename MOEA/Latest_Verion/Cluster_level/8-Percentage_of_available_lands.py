# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 10:16:50 2023

@author: eari
"""

# library
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd
import plotly.io as pio
pio.renderers.default='browser'
import plotly.express as px

import matplotlib.patches as mpatches

# import excel sheet  
df_geo_corn = pd.read_excel('Platypus_codes/combined_pivot_Corn.xlsx',header=0, engine='openpyxl') #contains data sets for corn (state, land cost, yield etc)
df_geo_soy = pd.read_excel('Platypus_codes/combined_pivot_Soy.xlsx',header=0, engine='openpyxl') #contains data sets for soy (state, land cost, yield etc)
df_geo_grass_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_grass = pd.read_excel('Platypus_codes/combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') #contains data sets for grass (state, land cost, yield etc) 
df_geo_algae_L = pd.read_excel('Platypus_codes/combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc)   
df_geo_algea = pd.read_excel('Platypus_codes/combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl') #contains data sets for algae (state, land cost, yield etc) 

districts = list(df_geo_corn['STASD_N']) # list of ag_district code
states = list(df_geo_corn['State'])

num_c = len(df_geo_corn)


# objective = 'min_GHG_emission'
# objective = 'cost'

df_total = pd.read_excel('Platypus_codes/total_land_limit.xlsx',header=0, engine='openpyxl')
AG_tot = df_total.iloc[0:num_c]
AG_Land_lim = AG_tot['land_limits_ha']
AG_Land_lim.reset_index(drop=True,inplace=True)

MA_tot_grass = df_total.iloc[num_c:2*num_c]
MA_Land_lim_grass = MA_tot_grass['land_limits_ha']
MA_Land_lim_grass.reset_index(drop=True,inplace=True)

MA_tot_algae = df_total.iloc[2*num_c:3*num_c]
MA_Land_lim_algae = MA_tot_algae['land_limits_ha']
MA_Land_lim_algae.reset_index(drop=True,inplace=True)


version = ['_100000_0.1district','_100000_0.001district',
            '_1000000_0.1district','_1000000_0.001district','_10000000_0.1district','_10000000_0.001district']

# version = ['district']

for v in version:
    
    objective = 'max_energy_shortfall'

    ## 3 billion ###
    
    fn_ha3 = 'Decision_Variables_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    df_ha3 = pd.read_csv(fn_ha3,header=0,index_col=0)
    
    fn3 = 'Objective_functions_borg_crops_GHG3' + v + '_PARETO'  +'.csv'
    df_O3 = pd.read_csv(fn3,header=0,index_col=0)
    # df_O3.reset_index(drop=True,inplace=True)
    
    df_O3.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting3 = df_O3.sort_values(by= objective, ascending=True).head(1)
    my_index3 = list(sorting3.index)
    df_ha3_sorted = df_ha3.loc[my_index3] 
    
    Corn_ha3 = df_ha3_sorted.iloc[0,0:num_c]
    Corn_ha3.reset_index(drop=True,inplace=True)
    
    # Soy_ha3 = df_ha3_sorted.iloc[0,0:107]
    # Soy_ha3.reset_index(drop=True,inplace=True)
    
    Grass_MA_ha3 = df_ha3_sorted.iloc[0,num_c:2*num_c]
    Grass_MA_ha3.reset_index(drop=True,inplace=True)
    
    Algae_MA_ha3 = df_ha3_sorted.iloc[0,2*num_c:3*num_c]
    Algae_MA_ha3.reset_index(drop=True,inplace=True)
    
    Grass_AG_ha3 = df_ha3_sorted.iloc[0,3*num_c:4*num_c]
    Grass_AG_ha3.reset_index(drop=True,inplace=True)
    
    Algae_AG_ha3 = df_ha3_sorted.iloc[0,4*num_c:]
    Algae_AG_ha3.reset_index(drop=True,inplace=True)
    
    
    Total_used_AG_land3 = Corn_ha3 + Grass_AG_ha3 + Algae_AG_ha3
    Total_used_MA_land_grass3 = Grass_MA_ha3 
    Total_used_MA_land_algae3 = Algae_MA_ha3
    
    Total_left_AG3 = AG_Land_lim - Total_used_AG_land3
    Total_left_MA_grass3 = MA_Land_lim_grass - Total_used_MA_land_grass3
    Total_left_MA_algae3 = MA_Land_lim_algae - Total_used_MA_land_algae3
    
    Percentage_AG3 = (100*Total_left_AG3)/AG_Land_lim
    Percentage_MA_grass3 = (100*Total_left_MA_grass3)/MA_Land_lim_grass
    Percentage_MA_algae3 = (100*Total_left_MA_algae3)/MA_Land_lim_algae
    
    
    df = pd.DataFrame(states, columns=['State'])
    df['Districts'] = districts
    df['3 billion'] = Percentage_AG3
    
    df_grass = pd.DataFrame(states, columns=['State'])
    df_grass['Districts'] = districts
    df_grass['3 billion'] = Percentage_MA_grass3
    
    df_algae = pd.DataFrame(states, columns=['State'])
    df_algae['Districts'] = districts
    df_algae['3 billion'] = Percentage_MA_algae3
    
    df_total = pd.DataFrame(states, columns=['State'])
    df_total['Districts'] = districts
    df_total['3 billion'] = Percentage_AG3+Percentage_MA_grass3+Percentage_MA_algae3
    
    ## 6 billion ###
    
    fn_ha6 = 'Decision_Variables_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_ha6 = pd.read_csv(fn_ha6,header=0,index_col=0)
    
    fn6 = 'Objective_functions_borg_crops_GHG6' + v + '_PARETO'  +'.csv'
    df_O6 = pd.read_csv(fn6,header=0,index_col=0)
    # df_O6.reset_index(drop=True,inplace=True)
    
    df_O6.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting6 = df_O6.sort_values(by= objective, ascending=True).head(1)
    my_index6 = list(sorting6.index)
    df_ha6_sorted = df_ha6.loc[my_index6] 
    
    Corn_ha6 = df_ha6_sorted.iloc[0,0:num_c]
    Corn_ha6.reset_index(drop=True,inplace=True)
    
    # Soy_ha6 = df_ha6_sorted.iloc[0,0:107]
    # Soy_ha6.reset_index(drop=True,inplace=True)
    
    Grass_MA_ha6 = df_ha6_sorted.iloc[0,num_c:2*num_c]
    Grass_MA_ha6.reset_index(drop=True,inplace=True)
    
    Algae_MA_ha6 = df_ha6_sorted.iloc[0,2*num_c:3*num_c]
    Algae_MA_ha6.reset_index(drop=True,inplace=True)
    
    Grass_AG_ha6 = df_ha6_sorted.iloc[0,3*num_c:4*num_c]
    Grass_AG_ha6.reset_index(drop=True,inplace=True)
    
    Algae_AG_ha6 = df_ha6_sorted.iloc[0,4*num_c:]
    Algae_AG_ha6.reset_index(drop=True,inplace=True)
    
    
    Total_used_AG_land6 = Corn_ha6 + Grass_AG_ha6 + Algae_AG_ha6
    Total_used_MA_land_grass6 = Grass_MA_ha6 
    Total_used_MA_land_algae6 = Algae_MA_ha6
    
    Total_left_AG6 = AG_Land_lim - Total_used_AG_land6
    Total_left_MA_grass6 = MA_Land_lim_grass - Total_used_MA_land_grass6
    Total_left_MA_algae6 = MA_Land_lim_algae - Total_used_MA_land_algae6
    
    Percentage_AG6 = (100*Total_left_AG6)/AG_Land_lim
    Percentage_MA_grass6 = (100*Total_left_MA_grass6)/MA_Land_lim_grass
    Percentage_MA_algae6 = (100*Total_left_MA_algae6)/MA_Land_lim_algae
    
    
    df['6 billion'] = Percentage_AG6
    
    df_grass['6 billion'] = Percentage_MA_grass6
    
    df_algae['6 billion'] = Percentage_MA_algae6
    df_total['6 billion'] = Percentage_AG6+Percentage_MA_grass6+Percentage_MA_algae6
    
    ## 9 billion ###
    
    fn_ha9 = 'Decision_Variables_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_ha9 = pd.read_csv(fn_ha9,header=0,index_col=0)
    
    fn9 = 'Objective_functions_borg_crops_GHG9' + v + '_PARETO'  +'.csv'
    df_O9 = pd.read_csv(fn9,header=0,index_col=0)
    # df_O9.reset_index(drop=True,inplace=True)
    
    df_O9.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting9 = df_O9.sort_values(by= objective, ascending=True).head(1)
    my_index9 = list(sorting9.index)
    df_ha9_sorted = df_ha9.loc[my_index9] 
    
    Corn_ha9 = df_ha9_sorted.iloc[0,0:num_c]
    Corn_ha9.reset_index(drop=True,inplace=True)
    
    # Soy_ha9 = df_ha9_sorted.iloc[0,0:107]
    # Soy_ha9.reset_index(drop=True,inplace=True)
    
    Grass_MA_ha9 = df_ha9_sorted.iloc[0,num_c:2*num_c]
    Grass_MA_ha9.reset_index(drop=True,inplace=True)
    
    Algae_MA_ha9 = df_ha9_sorted.iloc[0,2*num_c:3*num_c]
    Algae_MA_ha9.reset_index(drop=True,inplace=True)
    
    Grass_AG_ha9 = df_ha9_sorted.iloc[0,3*num_c:4*num_c]
    Grass_AG_ha9.reset_index(drop=True,inplace=True)
    
    Algae_AG_ha9 = df_ha9_sorted.iloc[0,4*num_c:]
    Algae_AG_ha9.reset_index(drop=True,inplace=True)
    
    
    Total_used_AG_land9 = Corn_ha9 + Grass_AG_ha9 + Algae_AG_ha9
    Total_used_MA_land_grass9 = Grass_MA_ha9 
    Total_used_MA_land_algae9 = Algae_MA_ha9
    
    Total_left_AG9 = AG_Land_lim - Total_used_AG_land9
    Total_left_MA_grass9 = MA_Land_lim_grass - Total_used_MA_land_grass9
    Total_left_MA_algae9 = MA_Land_lim_algae - Total_used_MA_land_algae9
    
    Percentage_AG9 = (100*Total_left_AG9)/AG_Land_lim
    Percentage_MA_grass9 = (100*Total_left_MA_grass9)/MA_Land_lim_grass
    Percentage_MA_algae9 = (100*Total_left_MA_algae9)/MA_Land_lim_algae
    
    
    df['9 billion'] = Percentage_AG9
    
    df_grass['9 billion'] = Percentage_MA_grass9
    
    df_algae['9 billion'] = Percentage_MA_algae9
    df_total['9 billion'] = Percentage_AG9+Percentage_MA_grass9+Percentage_MA_algae9
    
    ## 12 billion ###
    
    fn_ha12 = 'Decision_Variables_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_ha12 = pd.read_csv(fn_ha12,header=0,index_col=0)
    
    fn12 = 'Objective_functions_borg_crops_GHG12' + v + '_PARETO'  +'.csv'
    df_O12 = pd.read_csv(fn12,header=0,index_col=0)
    # df_O12.reset_index(drop=True,inplace=True)
    
    df_O12.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting12 = df_O12.sort_values(by= objective, ascending=True).head(1)
    my_index12 = list(sorting12.index)
    df_ha12_sorted = df_ha12.loc[my_index12] 
    
    Corn_ha12 = df_ha12_sorted.iloc[0,0:num_c]
    Corn_ha12.reset_index(drop=True,inplace=True)
    
    # Soy_ha12 = df_ha12_sorted.iloc[0,0:107]
    # Soy_ha12.reset_index(drop=True,inplace=True)
    
    Grass_MA_ha12 = df_ha12_sorted.iloc[0,num_c:2*num_c]
    Grass_MA_ha12.reset_index(drop=True,inplace=True)
    
    Algae_MA_ha12 = df_ha12_sorted.iloc[0,2*num_c:3*num_c]
    Algae_MA_ha12.reset_index(drop=True,inplace=True)
    
    Grass_AG_ha12 = df_ha12_sorted.iloc[0,3*num_c:4*num_c]
    Grass_AG_ha12.reset_index(drop=True,inplace=True)
    
    Algae_AG_ha12 = df_ha12_sorted.iloc[0,4*num_c:]
    Algae_AG_ha12.reset_index(drop=True,inplace=True)
    
    
    Total_used_AG_land12 = Corn_ha12 + Grass_AG_ha12 + Algae_AG_ha12
    Total_used_MA_land_grass12 = Grass_MA_ha12 
    Total_used_MA_land_algae12 = Algae_MA_ha12
    
    Total_left_AG12 = AG_Land_lim - Total_used_AG_land12
    Total_left_MA_grass12 = MA_Land_lim_grass - Total_used_MA_land_grass12
    Total_left_MA_algae12 = MA_Land_lim_algae - Total_used_MA_land_algae12
    
    Percentage_AG12 = (100*Total_left_AG12)/AG_Land_lim
    Percentage_MA_grass12 = (100*Total_left_MA_grass12)/MA_Land_lim_grass
    Percentage_MA_algae12 = (100*Total_left_MA_algae12)/MA_Land_lim_algae
    
    
    df['12 billion'] = Percentage_AG12
    
    df_grass['12 billion'] = Percentage_MA_grass12
    
    df_algae['12 billion'] = Percentage_MA_algae12
    df_total['12 billion'] = Percentage_AG12+Percentage_MA_grass12+Percentage_MA_algae12
    
    
    
    ## 15 billion ###
    
    fn_ha15 = 'Decision_Variables_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_ha15 = pd.read_csv(fn_ha15,header=0,index_col=0)
    
    fn15 = 'Objective_functions_borg_crops_GHG15' + v + '_PARETO'  +'.csv'
    df_O15 = pd.read_csv(fn15,header=0,index_col=0)
    # df_O15.reset_index(drop=True,inplace=True)
    
    df_O15.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting15 = df_O15.sort_values(by= objective, ascending=True).head(1)
    my_index15 = list(sorting15.index)
    df_ha15_sorted = df_ha15.loc[my_index15] 
    
    Corn_ha15 = df_ha15_sorted.iloc[0,0:num_c]
    Corn_ha15.reset_index(drop=True,inplace=True)
    
    # Soy_ha15 = df_ha15_sorted.iloc[0,0:107]
    # Soy_ha15.reset_index(drop=True,inplace=True)
    
    Grass_MA_ha15 = df_ha15_sorted.iloc[0,num_c:2*num_c]
    Grass_MA_ha15.reset_index(drop=True,inplace=True)
    
    Algae_MA_ha15 = df_ha15_sorted.iloc[0,2*num_c:3*num_c]
    Algae_MA_ha15.reset_index(drop=True,inplace=True)
    
    Grass_AG_ha15 = df_ha15_sorted.iloc[0,3*num_c:4*num_c]
    Grass_AG_ha15.reset_index(drop=True,inplace=True)
    
    Algae_AG_ha15 = df_ha15_sorted.iloc[0,4*num_c:]
    Algae_AG_ha15.reset_index(drop=True,inplace=True)
    
    
    Total_used_AG_land15 = Corn_ha15 + Grass_AG_ha15 + Algae_AG_ha15
    Total_used_MA_land_grass15 = Grass_MA_ha15 
    Total_used_MA_land_algae15 = Algae_MA_ha15
    
    Total_left_AG15 = AG_Land_lim - Total_used_AG_land15
    Total_left_MA_grass15 = MA_Land_lim_grass - Total_used_MA_land_grass15
    Total_left_MA_algae15 = MA_Land_lim_algae - Total_used_MA_land_algae15
    
    Percentage_AG15 = (100*Total_left_AG15)/AG_Land_lim
    Percentage_MA_grass15 = (100*Total_left_MA_grass15)/MA_Land_lim_grass
    Percentage_MA_algae15 = (100*Total_left_MA_algae15)/MA_Land_lim_algae
    
    
    df_grass['15 billion'] = Percentage_MA_grass15
    
    df_algae['15 billion'] = Percentage_MA_algae15
    
    df['15 billion'] = Percentage_AG15
    df_total['15 billion'] = Percentage_AG15+Percentage_MA_grass15+Percentage_MA_algae15
    
    ## 18 billion ###
    
    fn_ha18 = 'Decision_Variables_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_ha18 = pd.read_csv(fn_ha18,header=0,index_col=0)
    
    fn18 = 'Objective_functions_borg_crops_GHG18' + v + '_PARETO'  +'.csv'
    df_O18 = pd.read_csv(fn18,header=0,index_col=0)
    # df_O18.reset_index(drop=True,inplace=True)
    
    df_O18.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting18 = df_O18.sort_values(by= objective, ascending=True).head(1)
    my_index18 = list(sorting18.index)
    df_ha18_sorted = df_ha18.loc[my_index18] 
    
    Corn_ha18 = df_ha18_sorted.iloc[0,0:num_c]
    Corn_ha18.reset_index(drop=True,inplace=True)
    
    # Soy_ha18 = df_ha18_sorted.iloc[0,0:107]
    # Soy_ha18.reset_index(drop=True,inplace=True)
    
    Grass_MA_ha18 = df_ha18_sorted.iloc[0,num_c:2*num_c]
    Grass_MA_ha18.reset_index(drop=True,inplace=True)
    
    Algae_MA_ha18 = df_ha18_sorted.iloc[0,2*num_c:3*num_c]
    Algae_MA_ha18.reset_index(drop=True,inplace=True)
    
    Grass_AG_ha18 = df_ha18_sorted.iloc[0,3*num_c:4*num_c]
    Grass_AG_ha18.reset_index(drop=True,inplace=True)
    
    Algae_AG_ha18 = df_ha18_sorted.iloc[0,4*num_c:]
    Algae_AG_ha18.reset_index(drop=True,inplace=True)
    
    
    Total_used_AG_land18 = Corn_ha18 + Grass_AG_ha18 + Algae_AG_ha18
    Total_used_MA_land_grass18 = Grass_MA_ha18 
    Total_used_MA_land_algae18 = Algae_MA_ha18
    
    Total_left_AG18 = AG_Land_lim - Total_used_AG_land18
    Total_left_MA_grass18 = MA_Land_lim_grass - Total_used_MA_land_grass18
    Total_left_MA_algae18 = MA_Land_lim_algae - Total_used_MA_land_algae18
    
    Percentage_AG18 = (100*Total_left_AG18)/AG_Land_lim
    Percentage_MA_grass18 = (100*Total_left_MA_grass18)/MA_Land_lim_grass
    Percentage_MA_algae18 = (100*Total_left_MA_algae18)/MA_Land_lim_algae
    
    
    df_grass['18 billion'] = Percentage_MA_grass18
    
    df_algae['18 billion'] = Percentage_MA_algae18
    
    df['18 billion'] = Percentage_AG18
    df_total['18 billion'] = Percentage_AG18+Percentage_MA_grass18+Percentage_MA_algae18
    
    ## 20 billion ###
    
    fn_ha20 = 'Decision_Variables_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_ha20 = pd.read_csv(fn_ha20,header=0,index_col=0)
    
    fn20 = 'Objective_functions_borg_crops_GHG20' + v + '_PARETO'  +'.csv'
    df_O20 = pd.read_csv(fn20,header=0,index_col=0)
    # df_O20.reset_index(drop=True,inplace=True)
    
    df_O20.columns = ['cost','max_energy_shortfall','min_GHG_emission']
    sorting20 = df_O20.sort_values(by= objective, ascending=True).head(1)
    my_index20 = list(sorting20.index)
    df_ha20_sorted = df_ha20.loc[my_index20] 
    
    Corn_ha20 = df_ha20_sorted.iloc[0,0:num_c]
    Corn_ha20.reset_index(drop=True,inplace=True)
    
    # Soy_ha20 = df_ha20_sorted.iloc[0,0:107]
    # Soy_ha20.reset_index(drop=True,inplace=True)
    
    Grass_MA_ha20 = df_ha20_sorted.iloc[0,num_c:2*num_c]
    Grass_MA_ha20.reset_index(drop=True,inplace=True)
    
    Algae_MA_ha20 = df_ha20_sorted.iloc[0,2*num_c:3*num_c]
    Algae_MA_ha20.reset_index(drop=True,inplace=True)
    
    Grass_AG_ha20 = df_ha20_sorted.iloc[0,3*num_c:4*num_c]
    Grass_AG_ha20.reset_index(drop=True,inplace=True)
    
    Algae_AG_ha20 = df_ha20_sorted.iloc[0,4*num_c:]
    Algae_AG_ha20.reset_index(drop=True,inplace=True)
    
    
    Total_used_AG_land = Corn_ha20 + Grass_AG_ha20 + Algae_AG_ha20
    Total_used_MA_land_grass = Grass_MA_ha20 
    Total_used_MA_land_algae = Algae_MA_ha20
    
    Total_left_AG = AG_Land_lim - Total_used_AG_land
    Total_left_MA_grass = MA_Land_lim_grass - Total_used_MA_land_grass
    Total_left_MA_algae = MA_Land_lim_algae - Total_used_MA_land_algae
    
    Percentage_AG = (100*Total_left_AG)/AG_Land_lim
    Percentage_MA_grass = (100*Total_left_MA_grass)/MA_Land_lim_grass
    Percentage_MA_algae = (100*Total_left_MA_algae)/MA_Land_lim_grass
    
    
    df_grass['20 billion'] = Percentage_MA_grass
    
    df_algae['20 billion'] = Percentage_MA_algae
    
    
    df['20 billion'] = Percentage_AG
    df_total['20 billion'] = Percentage_AG+Percentage_MA_grass+Percentage_MA_algae
    
    # fig = px.scatter(df, x="Districts", y="Available Land Percentages_20 billion", color="State")
    # fig.show()
    
    import seaborn as sns
    fig, ax = plt.subplots(3,2, figsize=(20,10))
    fig.suptitle('Available Land Percentage for Total Land (AG+ML)' + v, fontsize=20)
    
    ax[0,0].set_title('3 billion')
    ax[0,1].set_title('6 billion')
    ax[1,0].set_title('9 billion')
    ax[1,1].set_title('15 billion')
    ax[2,0].set_title('18 billion')
    ax[2,1].set_title('20 billion')
    
    ax[0,0].xaxis.set_visible(False)
    ax[0,1].xaxis.set_visible(False)
    ax[1,0].xaxis.set_visible(False)
    ax[1,1].xaxis.set_visible(False)
    # ax[2,0].xaxis.set_tick_params(labelsize=24)
    # ax[2,1].xaxis.set_tick_params(labelsize=24)
    ax[0,0].yaxis.set_visible(False)
    ax[0,1].yaxis.set_visible(False)
    ax[1,0].yaxis.set_visible(False)
    ax[1,1].yaxis.set_visible(False)
    ax[2,0].yaxis.set_visible(False)
    ax[2,1].yaxis.set_visible(False)
    
    ax[0,0].grid(False)
    ax[0,1].grid(False)
    ax[1,0].grid(False)
    ax[1,1].grid(False)
    ax[2,0].grid(False)
    ax[2,1].grid(False)
    
    kwargs  =   {'edgecolor':"k", # for edge color
                  'linewidth':1, # line width of spot
                }
    
    sns.set(font_scale=3)
    
    sns.scatterplot(data=df_total,x="Districts", y="3 billion", hue="State",ax=ax[0,0],s=100,legend=False,**kwargs)
    sns.scatterplot(data=df_total,x="Districts", y="6 billion", hue="State",ax=ax[0,1],s=100,legend=False,**kwargs)
    sns.scatterplot(data=df_total,x="Districts", y="9 billion", hue="State",ax=ax[1,0],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df,x="Districts", y="12 billion", hue="State",ax=ax[3],legend=False)
    sns.scatterplot(data=df_total,x="Districts", y="15 billion", hue="State",ax=ax[1,1],s=100,legend=False,**kwargs)
    sns.scatterplot(data=df_total,x="Districts", y="18 billion", hue="State",ax=ax[2,0],s=100,legend=False,**kwargs)
    sns.scatterplot(data=df_total,x="Districts", y="20 billion", hue="State",ax=ax[2,1],s=100,legend=False,**kwargs)
    
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
    plt.tight_layout()
    
    # plt.show()
    # plt.clf()
    
    plt.savefig('Available_Land_percentage' + v + '.png',dpi=150, bbox_inches='tight')
    
    
    
    
    # import seaborn as sns
    # fig, ax = plt.subplots(3,2, figsize=(20,10))
    # fig.suptitle('Available Land Percentage for Agricultural Land', fontsize=20)
    
    # ax[0,0].set_title('3 billion')
    # ax[0,1].set_title('6 billion')
    # ax[1,0].set_title('9 billion')
    # ax[1,1].set_title('15 billion')
    # ax[2,0].set_title('18 billion')
    # ax[2,1].set_title('20 billion')
    
    # ax[0,0].xaxis.set_visible(False)
    # ax[0,1].xaxis.set_visible(False)
    # ax[1,0].xaxis.set_visible(False)
    # ax[1,1].xaxis.set_visible(False)
    # # ax[2,0].xaxis.set_tick_params(labelsize=24)
    # # ax[2,1].xaxis.set_tick_params(labelsize=24)
    # # ax[0,0].yaxis.set_visible(False)
    # ax[0,1].yaxis.set_visible(False)
    # # ax[1,0].yaxis.set_visible(False)
    # ax[1,1].yaxis.set_visible(False)
    # # ax[2,0].yaxis.set_visible(False)
    # ax[2,1].yaxis.set_visible(False)
    
    # ax[0,0].grid(False)
    # ax[0,1].grid(False)
    # ax[1,0].grid(False)
    # ax[1,1].grid(False)
    # ax[2,0].grid(False)
    # ax[2,1].grid(False)
    
    # kwargs  =   {'edgecolor':"k", # for edge color
    #               'linewidth':2, # line width of spot
    #             }
    
    # sns.set(font_scale=1.5)
    
    # sns.scatterplot(data=df,x="Districts", y="3 billion", hue="State",ax=ax[0,0],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df,x="Districts", y="6 billion", hue="State",ax=ax[0,1],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df,x="Districts", y="9 billion", hue="State",ax=ax[1,0],s=100,legend=False,**kwargs)
    # # sns.scatterplot(data=df,x="Districts", y="12 billion", hue="State",ax=ax[3],legend=False)
    # sns.scatterplot(data=df,x="Districts", y="15 billion", hue="State",ax=ax[1,1],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df,x="Districts", y="18 billion", hue="State",ax=ax[2,0],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df,x="Districts", y="20 billion", hue="State",ax=ax[2,1],s=100,legend=False,**kwargs)
    
    # # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
    # plt.tight_layout()
    
    # plt.show()
    # plt.clf()
    
    
    # import seaborn as sns
    # fig, ax = plt.subplots(3,2, figsize=(20,10))
    # fig.suptitle('Available Land Percentage for Grass Marginal Land', fontsize=20)
    # ax[0,0].xaxis.set_visible(False)
    # ax[0,1].xaxis.set_visible(False)
    # ax[1,0].xaxis.set_visible(False)
    # ax[1,1].xaxis.set_visible(False)
    # # ax[2,0].xaxis.set_tick_params(labelsize=24)
    # # ax[2,1].xaxis.set_tick_params(labelsize=24)
    # ax[0,0].grid(False)
    # ax[0,1].grid(False)
    # ax[1,0].grid(False)
    # ax[1,1].grid(False)
    # ax[2,0].grid(False)
    # ax[2,1].grid(False)
    
    
    
    # sns.set(font_scale=1.5)
    
    # sns.scatterplot(data=df_grass,x="Districts", y="3 billion", hue="State",ax=ax[0,0],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_grass,x="Districts", y="6 billion", hue="State",ax=ax[0,1],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_grass,x="Districts", y="9 billion", hue="State",ax=ax[1,0],s=100,legend=False,**kwargs)
    # # sns.scatterplot(data=df,x="Districts", y="12 billion", hue="State",ax=ax[3],legend=False)
    # sns.scatterplot(data=df_grass,x="Districts", y="15 billion", hue="State",ax=ax[1,1],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_grass,x="Districts", y="18 billion", hue="State",ax=ax[2,0],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_grass,x="Districts", y="20 billion", hue="State",ax=ax[2,1],s=100,legend=False,**kwargs)
    
    # # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
    # plt.tight_layout()
    
    # plt.show()
    # plt.clf()
    
    
    # import seaborn as sns
    # fig, ax = plt.subplots(3,2, figsize=(20,10))
    # fig.suptitle('Available Land Percentage for Algae Marginal Land', fontsize=20)
    # ax[0,0].xaxis.set_visible(False)
    # ax[0,1].xaxis.set_visible(False)
    # ax[1,0].xaxis.set_visible(False)
    # ax[1,1].xaxis.set_visible(False)
    # # ax[2,0].xaxis.set_tick_params(labelsize=24)
    # # ax[2,1].xaxis.set_tick_params(labelsize=24)
    # ax[0,0].grid(False)
    # ax[0,1].grid(False)
    # ax[1,0].grid(False)
    # ax[1,1].grid(False)
    # ax[2,0].grid(False)
    # ax[2,1].grid(False)
    
    
    
    # sns.set(font_scale=1.5)
    
    # sns.scatterplot(data=df_algae,x="Districts", y="3 billion", hue="State",ax=ax[0,0],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_algae,x="Districts", y="6 billion", hue="State",ax=ax[0,1],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_algae,x="Districts", y="9 billion", hue="State",ax=ax[1,0],s=100,legend=False,**kwargs)
    # # sns.scatterplot(data=df,x="Districts", y="12 billion", hue="State",ax=ax[3],legend=False)
    # sns.scatterplot(data=df_algae,x="Districts", y="15 billion", hue="State",ax=ax[1,1],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_algae,x="Districts", y="18 billion", hue="State",ax=ax[2,0],s=100,legend=False,**kwargs)
    # sns.scatterplot(data=df_algae,x="Districts", y="20 billion", hue="State",ax=ax[2,1],s=100,legend=True,**kwargs)
    
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    
    # plt.tight_layout()
    
    # plt.show()
    # plt.clf()