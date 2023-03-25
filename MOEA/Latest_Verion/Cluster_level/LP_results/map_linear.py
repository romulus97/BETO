# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 11:27:44 2023

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



plt.rcParams['font.sans-serif'] = "Arial"
plt.rcParams.update({'font.size': 15})

df = pd.read_csv('../Platypus_codes/AgD_48g_cords_cb.csv',header=0)

crs = {'init':'epsg:4326'}
geometry = [Point(xy) for xy in zip(df['Longitude'],df['Latitude'])]
geo_df = gpd.GeoDataFrame(df,crs=crs,geometry=geometry)
geo_df = geo_df.to_crs(epsg=2163)

state_map = gpd.read_file('../shapefiles/geo_export_9ef76f60-e019-451c-be6b-5a879a5e7c07.shp')
state_map = state_map.to_crs(epsg=2163)

df_geo_corn = pd.read_excel('../Platypus_codes/combined_pivot_Corn.xlsx', header=0, engine='openpyxl')

district_map = gpd.read_file('../shapefiles/AgD Corn belt.shp')
district_map = district_map.to_crs(epsg=2163)
districts = list(district_map['STASD_N'])

# district_map = state_map.loc[state_map['state_name'].isin(['Illinois','Indiana','Iowa','Kansas', 'Michigan','Minnesota','Missouri','Nebraska','North Dakota', 'Ohio', 'South Dakota', 'Wisconsin'])]


billion = ['3','6','9','12','15','18','20']



for b in billion:

    fn_ha = 'land_usage_out_cluster_level_' + b +'.csv'
    df_decision_variables = pd.read_csv(fn_ha,header=0,index_col=0)
    df_var = df_decision_variables['Value'].values

    num_c = len(df_geo_corn)
    
    tcorn = pd.DataFrame(df_var[0:num_c])
    tsoy = pd.DataFrame(df_var[num_c:2*num_c])
    
    
    tc = tcorn + tsoy   ## corn/soy
    tgag = pd.DataFrame(df_var[2*num_c:3*num_c])  ## grass on ag land 
    tgml = pd.DataFrame(df_var[3*num_c:4*num_c])  ## grass on marginal land
    taag = pd.DataFrame(df_var[4*num_c:5*num_c])  ## algae on ag. land
    taml = pd.DataFrame(df_var[5*num_c:])         ## algae on marginal land

    
        
    ###################################
    ####   CORN/SOY MINIMUM MFSP  #####
    ###################################
    
    t = tc
    to = t  
    ind =  to.columns
    
    
    district_map.index = to.index
    map_c = pd.concat([district_map,to],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    
    map_c = pd.concat([district_map,to],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()
    
    f, axs = plt.subplots(2,5, figsize=(15, 7),constrained_layout = True)
    
    state_map.plot(ax=axs[0,0],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
    f.suptitle( b , fontsize=16)
    
    map_c = pd.concat([district_map,to],axis=1)
    
    
    import matplotlib.colors as colors
    
    # normalize color
    vmin, vmax, vcenter = 0,300000, 50000
    norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    
    # create a normalized colorbar
    cmap = 'cool'
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    db.plot(column= 0, 
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
    
    ##################################
    #### SWITCHGRASS MARGINAL LAND MINIMUM MFSP ####
    ##################################
    
    t = tgml
    to = t  
    ind =  to.columns
    
    district_map.index = to.index
    map_c = pd.concat([district_map,to],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    
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
    
    db.plot(column= 0, 
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
    

    #####################################################
    #### SWITCHGRASS AGRICULTURAL LAND MINIMUM MFSP #####
    #####################################################
    t = tgag
    to = t  
    ind =  to.columns
    
    district_map.index = to.index
    map_c = pd.concat([district_map,to],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

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
    
    db.plot(column= 0, 
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
    
    ##################################
    #### ALGAE MARGINAL LAND MINIMUM MFSP ####
    ##################################
    
    t = taml
    to = t  
    ind =  to.columns
    
    district_map.index = to.index
    map_c = pd.concat([district_map,to],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    
    map_c = pd.concat([district_map,to],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()
    
    state_map.plot(ax=axs[0,3],color='gray',alpha=0.6,edgecolor='black',linewidth=0.8)
    
    
    import matplotlib.colors as colors
    
    # normalize color
    vmin, vmax, vcenter = 0,300000, 50000
    norm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    
    # create a normalized colorbar
    cmap = 'cool'
    cbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    
    db.plot(column= 0, 
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
    
    #####################################################
    #### ALGAE AGRICULTURAL LAND MINIMUM MFSP #####
    #####################################################
    t = taag
    to = t  
    ind =  to.columns
    
    district_map.index = to.index
    map_c = pd.concat([district_map,to],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()
    
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
    
    db.plot(column= 0, 
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
    
    
    
    
    
    
    
    
    
    # ####################################
    # #### CORN/SOY MINIMUM GHG       ####
    # ####################################
    
    fn_ha_ghg = 'land_usage_out_cluster_level_GHG_' + b +'.csv'
    df_decision_variables_ghg = pd.read_csv(fn_ha_ghg,header=0,index_col=0)
    df_var_ghg = df_decision_variables_ghg['Value'].values
    
    tcorn_g = pd.DataFrame(df_var_ghg[0:num_c])
    tsoy_g = pd.DataFrame(df_var_ghg[num_c:2*num_c])
    
    
    tc_g = tcorn_g + tsoy_g   ## corn/soy
    tgag_g = pd.DataFrame(df_var_ghg[2*num_c:3*num_c])  ## grass on ag land 
    tgml_g = pd.DataFrame(df_var_ghg[3*num_c:4*num_c])  ## grass on marginal land
    taag_g = pd.DataFrame(df_var_ghg[4*num_c:5*num_c])  ## algae on ag. land
    taml_g = pd.DataFrame(df_var_ghg[5*num_c:])         ## algae on marginal land

    
    t_g = tc_g
    to_g = t_g  
    ind =  to_g.columns
    
    district_map.index = to_g.index
    map_c = pd.concat([district_map,to_g],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()
    
    map_c = pd.concat([district_map,to_g],axis=1)
    
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
    
    db.plot(column= 0, 
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
    
    #######################################
    #### SWITCHGRASS MINIMUM GHG       ####
    #######################################
    
    t_g = tgml_g
    to_g = t_g  
    ind =  to_g.columns
    
    district_map.index = to_g.index
    map_c = pd.concat([district_map,to_g],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    map_c = pd.concat([district_map,to_g],axis=1)
    
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
    
    db.plot(column= 0, 
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
    
    
    ####################################################
    #### SWITCHGRASS AGRICULTURAL MINIMUM GHG       ####
    ####################################################
    
    t_g = tgag_g
    to_g = t_g  
    ind =  to_g.columns
    
    district_map.index = to_g.index
    map_c = pd.concat([district_map,to_g],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()

    
    map_c = pd.concat([district_map,to_g],axis=1)
    
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
    
    db.plot(column= 0, 
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
     
    
    #######################################
    #### ALGAE MARGINAL LAND MINIMUM GHG ####
    #######################################
    
    t_g = taml_g
    to_g = t_g  
    ind =  to_g.columns

    
    district_map.index = to_g.index
    map_c = pd.concat([district_map,to_g],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()
    
    map_c = pd.concat([district_map,to_g],axis=1)
    
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
    
    db.plot(column= 0, 
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
    
    
    ####################################################
    #### ALGAE AGRICULTURAL MINIMUM SHORTFALL ####
    ####################################################
    
    t_g = taag_g
    to_g = t_g  
    ind =  to_g.columns
    
    district_map.index = to_g.index
    map_c = pd.concat([district_map,to_g],axis=1)
    
    db = gpd.GeoDataFrame(map_c)
    db.info()
    
    map_c = pd.concat([district_map,to_g],axis=1)
    
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
    
    db.plot(column= 0, 
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
            ax=axs[1,4]
            )
    
    axs[1,4].set_axis_off()
    axs[1,4].set_box_aspect(1)
    axs[1,4].set_xlim(-750000,2000000)
    axs[1,4].set_ylim([-2000000,500000])
    plt.axis('off')
    
    
    plt.savefig('Compressed_map_cluster_linear' + b+ '.png',dpi=150, bbox_inches='tight')
    
    
    
    
    
    
    
    
    
    
    
    
