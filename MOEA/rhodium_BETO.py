"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from rhodium import * #import rhodium must be first line

import pandas as pd
import numpy as np
import time
import corn_stover_cultivation as CS_cultivation


start = time.time()

# import county level data
df_geo = pd.read_excel('geo.xlsx',sheet_name='counties',header=0)
counties = df_geo['name']
land_costs = df_geo.loc[:,'land_cost'].values
land_limits = df_geo['land_limit'].values

# Corn Stover
bu_per_acre_C_yield = df_geo['C_yield'].values

# import distance look-up table
df_dist = pd.read_excel('geo.xlsx',sheet_name='distance_lookup',header=0)
dist_map = np.zeros((len(counties),len(counties)))
# convert to matrix
for i in range(0,len(counties)):
    c1 = counties[i]
    for j in range(0,len(counties)):
        c2 = counties[j]
        if i != j:
            a = df_dist.loc[df_dist['county1']==c1]
            b = a.loc[df_dist['county2']==c2]
            dist_map[i,j] = b['distance_m'].values
        else:
            dist_map[i,j] = 0


# simulation model
def simulate(
        CS_acres, # planted corn stover acres
        LC = land_costs, # land costs per county
        C_Y = bu_per_acre_C_yield, # corn yield per ha
        LL = land_limits, # land limits
        DM = dist_map # distance mapping
        ):
    
    CS_kg = 0
    CS_costs = 0
    CS_travel = 0
    
    #Cultivation   
    for i in range(0,len(counties)):
        
        CS = CS_cultivation.sim(CS_acres[i],C_Y[i])
        CS_kg += CS
        CS_costs += CS_acres[i]*LC[i]
        
    # Flow to refinery
    
    # Simple case - specify location of single refinery of infinite size
        refinery_idx = 25
        CS_travel += DM[i,refinery_idx]*(20000/CS)
    
    # Processing        
        
    return CS_costs, CS_travel, CS_kg


# initialize model
model = Model(simulate) # simulate: function name

# # parameters: all inputs, even constant ones, in double quotes

model.parameters = [Parameter("CS_acres"),
                    Parameter("LC"),
                    Parameter("C_Y"),
                    Parameter("LL"),
                    Parameter("DM")]

# # responses: outputs of interest
# # using INFO records output but doesn't do anything with it

model.responses = [Response("CS_costs", Response.MINIMIZE),
                  Response("CS_travel", Response.MINIMIZE)]

# # constraints on outputs
model.constraints = [Constraint("CS_acres <= LL"),
                     Constraint("CS_kg >= 150")]

# decision variables
model.levers = [RealLever("CS_acres", 0, 1000, length = len(counties))] 

# # run model
nruns = 500
out = optimize(model, "NSGAII", nruns)

# # # rhodium output data structures are a bit funky
# #     # all saved as csv
# #     # outputs are saved as numbers
# #     # input vectors are saved as strings, like:
# #         # "[1, 2, 3]"
# #     # if you want to plot the vector policies, you'll need custom plotters that convert string to vector
    
savepath = 'results.csv'
out.save(savepath)


# # df7 = pd.read_csv(savepath)
# # df7 = df7.sort_values(by = ['DeveloperProfits']).reset_index()

# # plt.plot(df7.DeveloperProfits, df7.ratio, c='b')
# # plt.plot(a,b,marker='o',markersize = 3, color='r')

# # plt.xlabel('Developer Profits ($)')
# # plt.ylabel('Ratio')

stop = time.time()
elapsed = (stop - start)/60
mins = str(elapsed) + ' minutes'
print(mins)


