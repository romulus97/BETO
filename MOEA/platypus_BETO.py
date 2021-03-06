"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation as CS_cultivation
import corn_stover_processing as CS_processing

start = time.time()

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import county level data
df_geo = pd.read_excel('geo.xlsx',sheet_name='counties',header=0)
fips = df_geo['fips'].values
counties = df_geo['name']
land_costs = df_geo.loc[:,'land_cost'].values # $ per ha
land_limits = df_geo['land_limit'].values # ha

# Corn Stover
bu_per_acre_C_yield = df_geo['C_yield'].values 

# import distance look-up table
df_dist = pd.read_excel('geo.xlsx',sheet_name='distance_lookup',header=0)
dist_map = np.zeros((len(counties),len(counties)))

# convert look-up table to matrix
for i in range(0,len(counties)):
    c1 = counties[i]
    for j in range(0,len(counties)):
        c2 = counties[j]
        if i != j:
            a = df_dist.loc[df_dist['county1']==c1]
            b = a.loc[df_dist['county2']==c2]
            dist_map[i,j] = (b['distance_m'].values)/1000
        else:
            dist_map[i,j] = 0
            

#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
###################################
# CONVERSIONS
ha_to_acre = 2.47105 # Hectares to Acres
lb_to_kg= 0.453515 # pounds to kilograms
kg_to_L_Ethanol = 1.273723
    
    
# simulation model (function to be evaluated by MOEA)
def simulate(
        vars, # cultivation hectares per county, mass flows to refineries
        LC = land_costs, # land costs per county
        C_Y = bu_per_acre_C_yield, # corn yield per acre
        LL = land_limits, # land limits
        DM = dist_map, # distance mapping
        ):
    
    # Empty variables 
    CS_farm_kg = 0 # corn stover production in kg
    CS_cultivation_capex = 0 
    CS_cultivation_opex = 0
    CS_travel_opex = 0
    CS_flow_matrix = np.zeros((len(counties),len(counties)))
    CS_flow = 0
    CS_refinery_kg = 0
    CS_ethanol = np.zeros((len(counties),1))
    CS_refinery_opex = 0
    CS_refinery_capex = 0
    
    Constraints = [] # constraints
    
    ##############################
    # Cultivation and Harvesting
    for i in range(0,len(counties)):
        
        # Per ha values (need to expand)
        (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(C_Y[i])
        
        # kg CS produced in given county 'i'
        CS_farm_kg += CS_per_ha*vars[i]

        # Capital costs (need to expand)
        CS_cultivation_capex += vars[i]*LC[i]
        
        # Operating costs (need to expand)
        harvesting = 38.31*ha_to_acre # $ per ha
        CS_cultivation_opex += vars[i]*(seeds_per_ha*.00185 + fertilization_per_ha[0]*0.55 + fertilization_per_ha[1]*0.46 + fertilization_per_ha[2]*0.50 + lime_per_ha*0.01 + harvesting) #herbicide in per ha??
        
        ################################
        # Flow to refinery
        for j in range(0,len(counties)):
            
            # County to county mass transfer (kg of CS) (from county 'i' to county 'j')
            CS_flow_matrix[i,j] += vars[(i+1)*len(counties) + j]
        
            # Travel costs in bale-miles
            CS_travel_opex += DM[i,j]*CS_flow_matrix[i,j]*(lb_to_kg)*(1/1500)*0.50 
        
        # Transportation constraints (flow from county 'i' must be <= mass produced)
        CS_flow = sum(CS_flow_matrix[i,:])
        Constraints.append(CS_flow - CS_farm_kg)
        
        # Cultivation constraints (land limits)
        Constraints.append(vars[i] - LL[i])  
        
        
    ################################
    # Refinery
    for j in range(0,len(counties)):
        
        # Find total mass sent to refinery in county 'j'
        CS_refinery_kg = sum(CS_flow_matrix[:,j])
        
        # Ethanol produced at refinery in county 'j'
        CS_ethanol[j] = CS_processing.sim(CS_refinery_kg)
    
    # Refinery opex
    #ADD THIS        
        
        # Refinery capex
        if CS_refinery_kg > 0:
            scale = CS_refinery_kg/(5563*142) # Based on kg per ha and ha scaling in Jack's TEA file
            CS_refinery_capex+= 400000000*(scale)**.6
    
    # Sets ethanol production quota (L)
    Constraints.append(19000-sum(CS_ethanol))
    Constraints.append(sum(CS_ethanol) - 21000)
    Constraints = list(Constraints)
    
    # Returns list of objectives, Constraints
    return [CS_refinery_capex, CS_travel_opex], Constraints


#####################################################################
##########           MOEA EXECUTION          ########################
#####################################################################

# Define Platypus problem

# Generic upper bound on decision variables
UB = 10000000

# Number of variables, constraints, objectives
num_variables = len(counties) * len(counties) + len(counties)
num_constraints = 2*len(counties)+2
num_objs = 2

problem = Problem(num_variables,num_objs,num_constraints)
problem.types[:] = Real(0,UB)
problem.constraints[:] = "<=0"

#What function?
problem.function = simulate

# What algorithm?
algorithm = NSGAII(problem)

# Evaluate function # of times
algorithm.run(10000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

# limit evalutaion to 'feasible' solutions
feasible_solutions = [s for s in algorithm.result if s.feasible]

# obj1 = []
# obj2 = []

# for s in feasible_solutions:
#     obj1.append(s.objectives[0])
#     obj2.append(s.objectives[1])
    
# min_obj1_idx = obj1.index(min(obj1))
# min_obj2_idx = obj2.index(min(obj2))

# # find solutions' standardized distance to ideal (origin)
# distance_to_origin_pct = []

# for s in feasible_solutions:
#     d = ((s.objectives[0]/max(obj1))**2 + (s.objectives[1]/max(obj2))**2)**0.5
#     distance_to_origin_pct.append(d)

    
# # select range of standardized solutions to map
# sorted_distance = np.sort(distance_to_origin_pct)
# idx = []
# idx_obj1 = []
# for i in range(0,99,9):
#     idx.append(distance_to_origin_pct.index(sorted_distance[i]))
#     idx_obj1.append(obj1[i])
    
# # display the tradeoff frontier    
# import matplotlib.pyplot as plt

# plt.scatter([s.objectives[0]/1000 for s in feasible_solutions],
#             [s.objectives[1] for s in feasible_solutions],c='red',alpha=0.5)

# plt.scatter(obj1[min_obj1_idx]/1000,obj2[min_obj1_idx],s=60,c='cyan',edgecolors='gray')
# plt.scatter(obj1[min_obj2_idx]/1000,obj2[min_obj2_idx],s=60,c='cyan',edgecolors='gray')

# for i in idx:
    
#     plt.scatter(obj1[i]/1000,obj2[i],s=60,c='cyan',edgecolors='gray')
    
# plt.xlabel("Costs ($1000s)")
# plt.ylabel("Distance (km)")
# plt.show()


# # visualize (map) solutions
# from urllib.request import urlopen
# import json
# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)
# import plotly.express as px
# import plotly.io as pio
# pio.renderers.default='jpg'

# # plot in descending order from Obj1
# df_combined = pd.DataFrame()
# df_combined['idx'] = idx
# df_combined['obj1'] = idx_obj1
# df_sorted = df_combined.sort_values(by='obj1',ascending=False).reset_index(drop=True)


# # map minimum obj1 solution
# s = np.array(feasible_solutions[min_obj1_idx].variables)
# df_results = pd.DataFrame()
# df_results['fips'] = fips
# df_results['CS_ha'] = s
# df_results['fips'] = df_results['fips'].apply(str)
# fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 50),
#                            scope="usa",
#                            labels={'CS_ha':'Corn Stover Hectares'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()

# # map rest of selected solutions
# for i in range(0,len(df_sorted)):
#     j = df_sorted.loc[i,'idx']
#     s = np.array(feasible_solutions[j].variables)
#     df_results = pd.DataFrame()
#     df_results['fips'] = fips
#     df_results['CS_ha'] = s
#     df_results['fips'] = df_results['fips'].apply(str)
#     fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
#                                color_continuous_scale="Viridis",
#                                range_color=(0, 50),
#                                scope="usa",
#                                labels={'CS_ha':'Corn Stover Hectares'}
#                               )
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.show()

# # map minimum obj2 solution
# s = np.array(feasible_solutions[min_obj2_idx].variables)
# df_results = pd.DataFrame()
# df_results['fips'] = fips
# df_results['CS_ha'] = s
# df_results['fips'] = df_results['fips'].apply(str)
# fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 50),
#                            scope="usa",
#                            labels={'CS_ha':'Corn Stover Hectares'}
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.update_geos(fitbounds="locations", visible=False)
# fig.show()

