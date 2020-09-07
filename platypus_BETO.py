"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from platypus import NSGAII, Problem, Real 
import pandas as pd
import numpy as np
import time
import corn_stover_cultivation as CS_cultivation


start = time.time()

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# import county level data
df_geo = pd.read_excel('geo.xlsx',sheet_name='counties',header=0)
fips = df_geo['fips'].values
counties = df_geo['name']
land_costs = df_geo.loc[:,'land_cost'].values
land_limits = df_geo['land_limit'].values

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

# simulation model
def simulate(
        vars, # planted corn stover acres
        LC = land_costs, # land costs per county
        C_Y = bu_per_acre_C_yield, # corn yield per ha
        LL = land_limits, # land limits
        DM = dist_map # distance mapping
        ):
    
    CS_kg = 0
    CS_costs = 0
    CS_travel = 0
    Constraints = []
    
    #Cultivation   
    for i in range(0,len(counties)):
        
        CS = CS_cultivation.sim(vars[i],C_Y[i])
        CS_kg += CS
        CS_costs += vars[i]*LC[i]
        
    # Flow to refinery
    
    # Simple case - specify location of single refinery of infinite size
        refinery_idx = 25
        CS_travel += DM[i,refinery_idx]*(20000/CS)
    
    # Processing        
    
    # Constraints
        Constraints.append(vars[i] - LL[i])
        Constraints.append(-vars[i])        
    
    Constraints.append(150-CS_kg)
    Constraints = list(Constraints)
    
    return [CS_costs, CS_travel], Constraints


#####################################################################
##########           MOEA EXECUTION          ########################
#####################################################################

# Define Platypus problem
problem = Problem(len(counties),2,199)
problem.types[:] = Real(0,100)
problem.constraints[:] = "<=0"
problem.function = simulate
algorithm = NSGAII(problem)
# Evaluate function # of times
algorithm.run(100000)

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


#####################################################################
##########           OUTPUTS                 ########################
#####################################################################

# display the tradeoff frontier
feasible_solutions = [s for s in algorithm.result if s.feasible]
    
import matplotlib.pyplot as plt

plt.scatter([s.objectives[0] for s in feasible_solutions],
            [s.objectives[1] for s in feasible_solutions])

plt.xlabel("Costs ($)")
plt.ylabel("Distance (km)")
plt.show()

# visualize (map) solutions
import plotly.express as px

# Min Cost
s1 = np.array(feasible_solutions[0].variables)
df_results = pd.DataFrame()
df_results['fips'] = fips
df_results['CS_acres'] = s1
fig1 = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_acres',
                           color_continuous_scale="Viridis",
                           range_color=(0, 5),
                           scope="usa",
                           labels={'CS_acres':'Corn Stover Acres'}
                          )
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig1.show()

# Min distance
s2 = np.array(feasible_solutions[100].variables)
df_results = pd.DataFrame()
df_results['fips'] = fips
df_results['CS_acres'] = s2
fig2 = px.choropleth(df_results, geojson=counties, locations='fips', color='CS_acres',
                           color_continuous_scale="Viridis",
                           range_color=(0, 5),
                           scope="iowa",
                           labels={'CS_acres':'Corn Stover Acres'}
                          )
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig2.show()

# # Compromise
# fig3 = px.choropleth(df_geo, geojson=counties, locations='fips', color='CS_acres',
#                            color_continuous_scale="Viridis",
#                            range_color=(0, 12),
#                            scope="iowa",
#                            labels={'CS_acres':'Corn Stover Acres'}
#                           )
# fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig3.show()



