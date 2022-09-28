# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:56:32 2022

@author: eari
"""

# importing the modules
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
  
df_O = pd.read_csv('Objective_Functions_borg_two_crop_trialdistrict.csv',header=0,index_col=0)
df_O.columns = ['cost','max_energy_shortfall','min_GHG_emission']

sorting = df_O.sort_values(by='max_energy_shortfall', ascending=True)
# sorting = df_O.sort_values(by='min_GHG_emission', ascending=True)
# sorting = df_O.sort_values(by='cost', ascending=True)
x = sorting.index

data = pd.read_excel('combined_regression_r2_f.xlsx',header=0, engine='openpyxl')
y= data.reindex(sorting.index)

f, ax = plt.subplots(1, figsize=(20, 10))

print("The data to be plotted:\n")
print(y)
  
# plotting the heatmap
norm = TwoSlopeNorm(vcenter=0)
hm = sn.heatmap(data = y,cmap="RdYlGn", fmt="f",vmin=-0.5, center=0, vmax=0.5)
  
# displaying the plotted heatmap

plt.rcParams['font.sans-serif'] = "Arial"
plt.rcParams.update({'font.size': 15})
plt.savefig('heatmap.png',dpi=300, bbox_inches='tight')  

plt.show()
plt.clf()