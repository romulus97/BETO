# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 00:25:42 2023

@author: eari
"""

version = 'district'

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default='browser'
import contextily
from shapely.geometry import Point, Polygon
import numpy as np
from matplotlib.cm import ScalarMappable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import geopandas as gpd



plt.rcParams.update({'font.size': 15})

df = pd.read_csv('Platypus_codes/AgD_48g_cords_cb.csv',header=0)


crs = {'init':'epsg:4326'}
# crs = {"init": "epsg:2163"}
geometry = [Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
geo_df = geo_df.to_crs(epsg=2163)

state_map = gpd.read_file('shapefiles/geo_export_9ef76f60-e019-451c-be6b-5a879a5e7c07.shp')
state_map = state_map.to_crs(epsg=2163)

district_map = gpd.read_file('shapefiles/AgD Corn belt.shp')
district_map = district_map.to_crs(epsg=2163)
districts = list(district_map['STASD_N'])


# billion = ['3','6']
# version = ['district']

# billion = ['3','9','12','15']
# version = ['_0.001district']

billion = ['3','6','9','12','15','18','20']

version = ['_100000_0.1district','_100000_0.001district',
            '_1000000_0.1district','_1000000_0.001district','_10000000_0.1district','_10000000_0.001district']

df_geo_corn = pd.read_excel('Platypus_codes/combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
del df_geo_corn['Unnamed: 0']


for b in billion:
    
    for v in version:

        fn_ha = 'Decision_Variables_borg_crops_GHG' + b + v + '_PARETO' +'.csv'
        df_decision_variables = pd.read_csv(fn_ha,header=0,index_col=0)
        
    
        fn = 'Objective_functions_borg_crops_GHG' + b + v + '_PARETO' +'.csv'
        df_O = pd.read_csv(fn,header=0,index_col=0)
        
        df_O.columns = ['cost','max_energy_shortfall','min_GHG_emission']
        
        num_c = len(df_geo_corn)

        tc = df_decision_variables.iloc[:,0:num_c]    ## corn/soy
        tgml = df_decision_variables.iloc[:,num_c:2*num_c]  ## grass
        taml = df_decision_variables.iloc[:,2*num_c:3*num_c]  ## algae
        tgag = df_decision_variables.iloc[:,3*num_c:4*num_c]    ## grass on ag. land 
        taag = df_decision_variables.iloc[:,4*num_c:]     ## algae on ag. land
        
        ###################################
        ####   CORN/SOY MINIMUM MFSP  #####
        ###################################
        
        t = tc.transpose(copy=False)
        to = t  
        ind =  to.columns

        
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_cost[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        f, axs = plt.subplots(2,5, figsize=(15, 7),constrained_layout = True)
        f.suptitle( b + v, fontsize=16)
        
        state_map.plot(ax=axs[0,0],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[0,0]
                )
        
        axs[0,0].set_axis_off()
        axs[0,0].set_box_aspect(1)
        axs[0,0].set_xlim(-750000,2000000)
        axs[0,0].set_ylim([-2000000,500000])
        plt.axis('off')
        
        
        ####################################
        #### CORN/SOY MINIMUM SHORTFALL ####
        ####################################
        
        t = tc.transpose(copy=False)
        to = t  
        ind =  to.columns

        
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_shortfall[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        # f, ax = plt.subplots(1, figsize=(15, 7),constrained_layout = True)
        
        state_map.plot(ax=axs[1,0],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[1,0]
                )
        
        axs[1,0].set_axis_off()
        axs[1,0].set_box_aspect(1)
        axs[1,0].set_xlim(-750000,2000000)
        axs[1,0].set_ylim([-2000000,500000])
        plt.axis('off')
        
        ##################################
        #### SWITCHGRASS MINIMUM MFSP ####
        ##################################
        
        t = tgml.transpose(copy=False)
        to = t  
        ind =  to.columns
 
        
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        # i = ind_min_cost[0]
        i = ind_min_shortfall[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        # f, ax = plt.subplots(1, figsize=(15, 7),constrained_layout = True)
        
        state_map.plot(ax=axs[0,1],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[0,1]
                )
        
        axs[0,1].set_axis_off()
        axs[0,1].set_box_aspect(1)
        axs[0,1].set_xlim(-750000,2000000)
        axs[0,1].set_ylim([-2000000,500000])
        plt.axis('off')
        
        
        
        #######################################
        #### SWITCHGRASS MINIMUM SHORTFALL ####
        #######################################
        
        t = tgml.transpose(copy=False)
        to = t  
        ind =  to.columns

        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_shortfall[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        
        state_map.plot(ax=axs[1,1],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[1,1]
                )
        
        axs[1,1].set_axis_off()
        axs[1,1].set_box_aspect(1)
        axs[1,1].set_xlim(-750000,2000000)
        axs[1,1].set_ylim([-2000000,500000])
        plt.axis('off')
        
        #####################################################
        #### SWITCHGRASS AGRICULTURAL LAND MINIMUM MFSP #####
        #####################################################
        t = tgag.transpose(copy=False)
        to = t  
        ind =  to.columns

        
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_cost[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        
        state_map.plot(ax=axs[0,2],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[0,2]
                )
        
        axs[0,2].set_axis_off()
        axs[0,2].set_box_aspect(1)
        axs[0,2].set_xlim(-750000,2000000)
        axs[0,2].set_ylim([-2000000,500000])
        plt.axis('off')
        
        ####################################################
        #### SWITCHGRASS AGRICULTURAL MINIMUM SHORTFALL ####
        ####################################################
        
        t = tgag.transpose(copy=False)
        to = t  
        ind =  to.columns

        
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_shortfall[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        
        state_map.plot(ax=axs[1,2],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[1,2]
                )
        
        axs[1,2].set_axis_off()
        axs[1,2].set_box_aspect(1)
        axs[1,2].set_xlim(-750000,2000000)
        axs[1,2].set_ylim([-2000000,500000])
        plt.axis('off')
        
        
        
        ##################################
        #### ALGAE MINIMUM MFSP ####
        ##################################
        
        t = taml.transpose(copy=False)
        to = t  
        ind =  to.columns
     
        
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_cost[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        # f, ax = plt.subplots(1, figsize=(15, 7),constrained_layout = True)
        
        state_map.plot(ax=axs[0,3],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[0,3]
                )
        
        axs[0,3].set_axis_off()
        axs[0,3].set_box_aspect(1)
        axs[0,3].set_xlim(-750000,2000000)
        axs[0,3].set_ylim([-2000000,500000])
        plt.axis('off')
        
        
        
        #######################################
        #### SWITCHGRASS MINIMUM SHORTFALL ####
        #######################################
        
        t = taml.transpose(copy=False)
        to = t  
        ind =  to.columns
    
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_shortfall[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        
        state_map.plot(ax=axs[1,3],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[1,3]
                )
        
        axs[1,3].set_axis_off()
        axs[1,3].set_box_aspect(1)
        axs[1,3].set_xlim(-750000,2000000)
        axs[1,3].set_ylim([-2000000,500000])
        plt.axis('off')
        
        #####################################################
        #### ALGAE AGRICULTURAL LAND MINIMUM MFSP #####
        #####################################################
        t = taag.transpose(copy=False)
        to = t  
        ind =  to.columns
        
        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_cost[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        
        state_map.plot(ax=axs[0,4],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=False,
                # legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[0,4]
                )
        
        axs[0,4].set_axis_off()
        axs[0,4].set_box_aspect(1)
        axs[0,4].set_xlim(-750000,2000000)
        axs[0,4].set_ylim([-2000000,500000])
        plt.axis('off')
        
        ####################################################
        #### ALGAE AGRICULTURAL MINIMUM SHORTFALL ####
        ####################################################
        
        t = taag.transpose(copy=False)
        to = t  
        ind =  to.columns

        district_map.index = to.index
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        sorting_cost = df_O.sort_values(by='cost', ascending=False)
        min_cost = sorting_cost.tail(1)
        ind_min_cost = min_cost.index.values
        
        sorting_shortfall = df_O.sort_values(by='max_energy_shortfall', ascending=False)
        min_shortfall = sorting_shortfall.tail(1)
        ind_min_shortfall = min_shortfall.index.values
        
        sorting_emission = df_O.sort_values(by='min_GHG_emission', ascending=False)
        min_emission = sorting_emission.tail(1)
        ind_min_emission = min_emission.index.values
        
        i = ind_min_shortfall[0]
        
        map_c = pd.concat([district_map,to],axis=1)
        
        db = gpd.GeoDataFrame(map_c)
        db.info()
        
        
        state_map.plot(ax=axs[1,4],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
        
        
        import matplotlib.colors as colors
        
        # normalize color
        vmin, vmax, vcenter = 0,300000, 50000
        norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
        
        # create a normalized colorbar
        cmap = 'cool'
        cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
        
        db.plot(column= i, 
                cmap= 'cool', 
                # scheme='MaximumBreaks',
                k=20, 
                edgecolor='black', 
                linewidth=0.9, 
                alpha=0.9, 
                legend=True,
                legend_kwds={"shrink": 0.75, "pad": 0.09},
                norm=norm,
                rasterized = True,
                ax=axs[1,4]
                )
        
        axs[1,4].set_axis_off()
        axs[1,4].set_box_aspect(1)
        axs[1,4].set_xlim(-750000,2000000)
        axs[1,4].set_ylim([-2000000,500000])
        plt.axis('off')
        
        plt.savefig('Compressed_map' + b + v + '.png',dpi=150, bbox_inches='tight')













