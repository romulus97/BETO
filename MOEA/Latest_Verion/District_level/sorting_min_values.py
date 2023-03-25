# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 16:43:43 2023

@author: eari
"""

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
import pandas as pd
from pysal.lib import weights
import geopandas as gpd
from pysal.explore import esda
import matplotlib as mpl

billion = ['3','6','9','12','15','18','20']
# billion = ['6']

version = ['_100000_0.001district', '_1000000_0.001district','_10000000_0.001district'] #,'_10000000_0.1district', '_1000000_0.1district',


# version = ['_100000_0.001district']

for b in billion:
    
    for v in version:
        
        fn = 'Objective_functions_borg_crops_GHG' + b + v + '_PARETO' +'.csv'
           
        df_O = pd.read_csv(fn,header=0,index_col=0)
        df_O.columns = ['cost','energy_shortfall','GHG_emission']
        
        objective = 'cost'
        
        sorting = df_O.sort_values(by= objective, ascending=True).reset_index(drop=True)
        min_cost = sorting.loc[0,'cost']
        print(f'For {b} billion, version {v}, minimum cost is {min_cost}')
        
        # objective = 'GHG_emission'
        
        # sorting = df_O.sort_values(by= objective, ascending=True).reset_index(drop=True)
        # min_cost = sorting.loc[0,'GHG_emission']
        # print(f'For {b} billion, version {v}, minimum GHG is {min_cost}')