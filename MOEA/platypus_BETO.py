"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation as CS_cultivation

#hello world!

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

# Simple refinery case (remove later)
refinery_idx = int(np.round(np.float(np.random.rand(1)*98),decimals=0))
 
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

# simulation model
def simulate(
        vars, # planted corn stover in hectares
        LC = land_costs, # land costs per county
        C_Y = bu_per_acre_C_yield, # corn yield per acre
        LL = land_limits, # land limits
        DM = dist_map, # distance mapping
        R_idx = refinery_idx # location of refinery in simple case
        ):
    
    CS_kg = 0 # corn stover production in kg
    CS_costs = 0 # total costs
    CS_travel = 0 # travel distance
    Constraints = [] # constraints
       
    #Cultivation   
    for i in range(0,len(counties)):
        
        CS = CS_cultivation.sim(vars[i],C_Y[i])
        CS_kg += CS
        
        # NOTE CONVERT TO HA!
        CS_costs += vars[i]*LC[i]
        
    # Flow to refinery
    
    # Simple case - random location of single refinery of infinite size
        CS_travel += DM[i,refinery_idx]*(CS/20000)
    
    # Processing        
    
    # Constraints
        Constraints.append(vars[i] - LL[i])
        Constraints.append(-vars[i])        
    
    Constraints.append(4490000-CS_kg)
    Constraints.append(CS_kg - 4510000)
    Constraints = list(Constraints)
    
    return [CS_costs, CS_travel], Constraints


#####################################################################
##########           MOEA EXECUTION          ########################
#####################################################################

# Define Platypus problem
problem = Problem(len(counties),2,200)
problem.types[:] = Real(0,100)
problem.constraints[:] = "<=0"
problem.function = simulate
algorithm = NSGAII(problem)

# Evaluate function # of times
algorithm.run(300000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

# limit evalutaion to 'feasible' solutions
feasible_solutions = [s for s in algorithm.result if s.feasible]

obj1 = []
obj2 = []

for s in feasible_solutions:
    obj1.append(s.objectives[0])
    obj2.append(s.objectives[1])
    
min_obj1_idx = obj1.index(min(obj1))
min_obj2_idx = obj2.index(min(obj2))

# find solutions' standardized distance to ideal (origin)
distance_to_origin_pct = []

for s in feasible_solutions:
    d = ((s.objectives[0]/max(obj1))**2 + (s.objectives[1]/max(obj2))**2)**0.5
    distance_to_origin_pct.append(d)

    
# select range of standardized solutions to map
sorted_distance = np.sort(distance_to_origin_pct)
idx = []
idx_obj1 = []
for i in range(0,99,9):
    idx.append(distance_to_origin_pct.index(sorted_distance[i]))
    idx_obj1.append(obj1[i])
    
# display the tradeoff frontier    
import matplotlib.pyplot as plt

plt.scatter([s.objectives[0]/1000 for s in feasible_solutions],
            [s.objectives[1] for s in feasible_solutions],c='red',alpha=0.5)

plt.scatter(obj1[min_obj1_idx]/1000,obj2[min_obj1_idx],s=60,c='cyan',edgecolors='gray')
plt.scatter(obj1[min_obj2_idx]/1000,obj2[min_obj2_idx],s=60,c='cyan',edgecolors='gray')

for i in idx:
    
    plt.scatter(obj1[i]/1000,obj2[i],s=60,c='cyan',edgecolors='gray')
    
plt.xlabel("Costs ($1000s)")
plt.ylabel("Distance (km)")
plt.show()


# visualize (map) solutions
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
import plotly.express as px
import plotly.io as pio
pio.renderers.default='jpg'

# plot in descending order from Obj1
df_combined = pd.DataFrame()
df_combined['idx'] = idx
df_combined['obj1'] = idx_obj1
df_sorted = df_combined.sort_values(by='obj1',ascending=False).reset_index(drop=True)


# map minimum obj1 solution
s = np.array(feasible_solutions[min_obj1_idx].variables)
df_results = pd.DataFrame()
df_results['fips'] = fips
df_results['CS_ha'] = s
df_results['fips'] = df_results['fips'].apply(str)
fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
                           color_continuous_scale="Viridis",
                           range_color=(0, 50),
                           scope="usa",
                           labels={'CS_ha':'Corn Stover Hectares'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

# map rest of selected solutions
for i in range(0,len(df_sorted)):
    j = df_sorted.loc[i,'idx']
    s = np.array(feasible_solutions[j].variables)
    df_results = pd.DataFrame()
    df_results['fips'] = fips
    df_results['CS_ha'] = s
    df_results['fips'] = df_results['fips'].apply(str)
    fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
                               color_continuous_scale="Viridis",
                               range_color=(0, 50),
                               scope="usa",
                               labels={'CS_ha':'Corn Stover Hectares'}
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.show()

# map minimum obj2 solution
s = np.array(feasible_solutions[min_obj2_idx].variables)
df_results = pd.DataFrame()
df_results['fips'] = fips
df_results['CS_ha'] = s
df_results['fips'] = df_results['fips'].apply(str)
fig = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_ha',
                           color_continuous_scale="Viridis",
                           range_color=(0, 50),
                           scope="usa",
                           labels={'CS_ha':'Corn Stover Hectares'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_geos(fitbounds="locations", visible=False)
fig.show()

