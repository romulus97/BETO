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

version = 'district'


#objective function
fn = 'Objective_Functions_borg_two_crop_trial' + version + '.csv'
df_O = pd.read_csv(fn,header=0,index_col=0)
df_O.columns = ['cost','min_energy_shortfall','energy_changes']

r = []
t = []
l = []
nd = []

# R = 100000000000000000
# T = 100000000000000000
# L = 100000000000000000

for i in range(0,len(df_O)):
    if i < 1:
        r.append(df_O.loc[i,'min_energy_shortfall']/(10**9))
        t.append(df_O.loc[i,'energy_changes']/(10**11))
        l.append(df_O.loc[i,'cost']/(10**13))
        nd.append(i)
    else:
        n = 1
        for j in r:
            idx = r.index(j)
            if r[idx] < df_O.loc[i,'min_energy_shortfall']/(10**9) and t[idx] < df_O.loc[i,'energy_changes']/(10**11) and l[idx] < df_O.loc[i,'cost']/(10**13):
                n = 0
        if n > 0:
            r.append(df_O.loc[i,'min_energy_shortfall']/(10**9))
            t.append(df_O.loc[i,'energy_changes']/(10**11))   
            l.append(df_O.loc[i,'cost']/(10**13)) 
            nd.append(idx)
    for k in r:
        idx = r.index(k)
        if r[0] > r[idx] and t[0] > t[idx] and l[0] > l[idx]:
            r.pop(0)
            t.pop(0)
            l.pop(0)
            
span = max(l) - min(l)

for i in range(0,len(l)):
    l[i] = 2*(l[i] - min(l))/span


# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')

# p = ax.scatter(r,t,l, c=r, s=l, cmap='hot',linewidth=1, edgecolor='black')
# # fig.colorbar(p, ax=ax)
# fig.colorbar(p, ax=ax, location='left', shrink=0.6)
# ax.scatter(r,t,l,)

# plt.figure()
# plt.scatter(r,t)
# ax.set_xlabel('min_energy_shortfall',fontweight='bold', fontsize=10)
# ax.set_ylabel('energy_changes',fontweight='bold',fontsize=10)
# ax.set_zlabel('cost',fontweight='bold',fontsize=10)

# plt.savefig('pareto.tiff',dpi = 330)

fig = px.scatter_3d(df_O, x='cost', y='min_energy_shortfall', z='energy_changes',color='min_energy_shortfall')
fig.update_layout(title='Comparison min_energy_shortfall,energy_changes and cost')
# fig3.update_layout( height = 900, width = 1000,title='Comparison Biofuel cost-shortfall-Land usage(ha) and ethanol changes')
fig.show()
fig.write_html("Comparison min_energy_shortfall,energy_changes and cost.html")









