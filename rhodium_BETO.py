"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""

from rhodium import * #import rhodium must be first line

from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import matplotlib.pyplot as plt
import time
import corn_stover_cultivation as CS_cultivation


start = time.time()

# import county level data
df_geo = pd.read_excel('geo.xlsx',sheet_name='counties',header=0)
counties = df_geo['name']
land_costs = df_geo['land_costs']
land_limits = df_geo['land_limits']

# Corn Stover
bu_per_acre_C_yield = df_geo['C_yield']

# import distance look-up table
df_dist = pd.read_excel('geo.xlsx',sheet_name='distance_lookup',header=0)
dist_map = np.zeros((len(counties),len(counties)))
# convert to matrix
for i in range(0,len(counties)):
    for j in range(0,len(counties)):
        if i != j:
            dist_map[i,j] = df_dist.iloc[i,j]
        else:
            dist_map[i,j] = 0


# simulation model
def simulate(CS_acres, land_costs, bu_per_acre_C_yield, land_limits,df_dist):
    
    CS_kg = 0
    CS_costs = 0
    CS_travel_km = 0
    
    #Cultivation   
    for i in range(0,len(counties)):
        
        county = counties[i]
        CS = CS_cultivation.sim(CS_acres[i],bu_per_acre_C_yield[i])
        CS_kg += CS[0]
        CS_costs += CS_acres[i]*land_costs[i]
        
    # Flow to refinery
    
    # Simple case - specify location of single refinery of infinite size
        refinery_idx = 25
        CS_travel += dist_map[i,refinery_idx]*(20000/CS[0])
    
    # Processing        
        
    return CS_costs, CS_travel


# initialize model
model = Model(simulate) # simulate: function name

# # parameters: all inputs, even constant ones, in double quotes

# model.parameters = [Parameter("hedgetargets"),
#                     Parameter("strikeprice"),
#                     Parameter("HP"),
#                     Parameter("NP"),
#                     Parameter("WP"),
#                     Parameter("calendar")]

# # responses: outputs of interest
# # using INFO records output but doesn't do anything with it

# model.responses = [Response("DeveloperProfits", Response.MAXIMIZE),
#                   Response("ratio", Response.MAXIMIZE)]

# # constraints on outputs
#     # not in the function yet, but i would recommend using this for:
#         # generation meets hedge >= 90% of the time
#     # given output of hedge goal satisfaction is "HedgeMet", format:

# # model.constraints = [Constraint("np.hedgetargets[0] + hedgetargets[1] + hedgetargets[0] + hedgetargets[1] + hedgetargets[0] + hedgetargets[1] + hedgetargets[0] + hedgetargets[1]" 
# model.constraints = [Constraint("7*(hedgetargets[0] + hedgetargets[2] + hedgetargets[4] + hedgetargets[6] + hedgetargets[8] + hedgetargets[10] + hedgetargets[12] + hedgetargets[14] + hedgetargets[16] + hedgetargets[18] + hedgetargets[20] + hedgetargets[22]) + 17*(hedgetargets[1] + hedgetargets[3] + hedgetargets[5] + hedgetargets[7] + hedgetargets[9] + hedgetargets[11] + hedgetargets[13] + hedgetargets[15] + hedgetargets[17] + hedgetargets[19] + hedgetargets[21] + hedgetargets[23])>= 10000")] #25470
#                      # Constraint("7*hedgetargets[2] + 17*hedgetargets[3] >= 2049"),
#                      # Constraint("7*hedgetargets[4] + 17*hedgetargets[5] >= 2240"),
#                      # Constraint("7*hedgetargets[6] + 17*hedgetargets[7] >= 2709"),
#                      # Constraint("7*hedgetargets[8] + 17*hedgetargets[9] >= 1977"),
#                      # Constraint("7*hedgetargets[10] + 17*hedgetargets[11] >= 2185"),
#                      # Constraint("7*hedgetargets[12] + 17*hedgetargets[13] >= 1835"),
#                      # Constraint("7*hedgetargets[14] + 17*hedgetargets[15] >= 1522"),
#                      # Constraint("7*hedgetargets[16] + 17*hedgetargets[17] >= 1976"),
#                      # Constraint("7*hedgetargets[18] + 17*hedgetargets[19] >= 2238"),
#                      # Constraint("7*hedgetargets[20] + 17*hedgetargets[21] >= 2653"),
#                      # Constraint("7*hedgetargets[22] + 17*hedgetargets[23] >= 2054")] 

# # levers   
# model.levers = [RealLever("hedgetargets", 0, 250, length = 24)] # considering hedge target as 24 hour vectors each month
#                 # RealLever("strikeprice", 14, 26, length = 1)]

# # run model

# # nruns = 15000
# # out = optimize(model, "NSGAII", nruns)

# # # rhodium output data structures are a bit funky
# #     # all saved as csv
# #     # outputs are saved as numbers
# #     # input vectors are saved as strings, like:
# #         # "[1, 2, 3]"
# #     # if you want to plot the vector policies, you'll need custom plotters that convert string to vector
    
# # savepath = 'results.csv'
# # out.save(savepath)

# strikeprice = 15.14
# df_H = pd.read_excel('P50.xlsx',sheet_name = 'hedge_targets',header=None)
# hedgetargets = df_H.values
# a,b = simulate(hedgetargets,strikeprice,HP=HubPricesConst,NP=NodePricesConst,WP=WindPowerConst,calendar=calendarConst)
#  # plt.plot(out.DeveloperProfits, out.ratio)

# # df7 = pd.read_csv(savepath)
# # df7 = df7.sort_values(by = ['DeveloperProfits']).reset_index()

# # plt.plot(df7.DeveloperProfits, df7.ratio, c='b')
# # plt.plot(a,b,marker='o',markersize = 3, color='r')

# # plt.xlabel('Developer Profits ($)')
# # plt.ylabel('Ratio')

# # stop = time.time()
# # elapsed = (stop - start)/60
# # mins = str(elapsed) + ' minutes'
# # print(mins)


