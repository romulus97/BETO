"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""
import pandas as pd
import numpy as np
import corn_stover_processing_V as CS_processing


# import district level data
df_geo = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
# df_eth = pd.read_excel('yearly_ethanol.xlsx',header=0, engine='openpyxl') #contains every eg_district code 

districts = list(df_geo['STASD_N']) # list of ag_district code
land_costs = df_geo.loc[:,'land_costs-$/ha'].values # $ per ha
land_limits = df_geo['land_limits_ha'].values # county ag production area in acres
cost = list(df_geo['CG_cost_per_ha'])
C_yield = df_geo.iloc[:,8:].values  # Corn Grain yield as kg/ha
# L_ethanol = df_eth.iloc[:,8:].values 

#specify grouping
groups = 20

#district-to-hub data
df_D2H = pd.read_excel('AgD2H_48_cb.xlsx',header=0, engine='openpyxl') # contains travel time and travel distance
c = list(df_D2H['STASD_N']) # list of ag_district code in filename excel sheet 

# Hub grouping information, distance look-up tables
dist_D2H = []
district_hubs = []
for d in districts:
    
    # distance from each district to pre-defined hub
    dist_D2H.append(df_D2H.loc[df_D2H['STASD_N']==d,'travel_dist_km'].values[0])
    
    # list of hubs assigned to each district
    district_hubs.append(df_D2H.loc[df_D2H['STASD_N']==d,'destinationID'].values[0]) # the whole corn belt divided 18 hubs abd this defines which ag_dist found under which hub

#hub-to-hub data
df_H2H =pd.read_excel('AgD_48g_H2H_cb.xlsx', header=0, engine='openpyxl')
hubs = list(df_H2H['OriginID'].unique()) # there is 18 hub 

years = range(1958,2021)
listyears =[]

for year in years :
    listyears.append(str(year))

########################################################################
#########        PRE-PROCESSING       ##################################
########################################################################

# put a number > 0 and < number of hubs if desired; if not, problem defaults to full list of hubs
locations = hubs
    
################################
# Convert to function inputs

dist_map = np.zeros((len(hubs),len(locations))) #creating matrix for representing hub to hub distance as km

# convert look-up table to distance matrix
for i in range(0,len(hubs)):
    c1 = hubs[i]
    for j in range(0,len(locations)):
        c2 = locations[j]
        dist_map[i,j] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers'] 

map_D2H = np.zeros((len(districts), len(hubs))) # 107 district and 18 hubs 

# convert look-up table to distance matrix #when 50 is indexed 49 is not valid because of missing hubs
for i in range(0,len(districts)):
    h = hubs.index(int(district_hubs[i])) # int(county_hubs[i]) - 1
    map_D2H[i,h] = 1    # represnet which district located which hub 

#####################################################################
##########           FUNCTION DEFINITION     ########################
#####################################################################
   
###################################
#pre-load test decision variables
V = []
for i in range(0,len(districts)):
    V.append(land_limits[i]) 
  
LC = land_costs # land costs per county
D2H_map = map_D2H # binary matrix mapping counties (rows) to hubs (columns)
locations = locations #possible location of biorefineries,
hubs = hubs

years = range(1958,2021)
corn_grain = []

for year in years :
    
    # Empty parameters 
    CG_flow_matrix = np.zeros((len(hubs),len(locations)))
    CG_D2H_prod = np.zeros((len(LC),len(hubs)))
    CG_refinery_kg = 0
    CG_ethanol = np.zeros((len(locations),1))
    CG_total = np.zeros((len(years), 107))
    
    b = years.index(year)
    Y = C_yield[:,b]
    CG = (land_limits*Y)
    CG_total[b] = CG

    ##############################
    # Cultivation and Harvesting
    
    for i in range(0,len(LC)):

        # Automatic flow to pre-processing hub
        CG_D2H_prod[i,:] = D2H_map[i,:]*CG[i]
        
    
    # Flow to refinery
    for j in range(0,len(hubs)):
    
        for k in range(0,len(locations)):
        
            V.append(sum(CG_D2H_prod[:,j])*(1/len(locations)))
    
            # Mass transfer (kg of CS) from hub 'j' to hub 'k'
            CG_flow_matrix[j,k] = CG_flow_matrix[j,k] + V[i + 1 + j*len(locations) + k]
            
    
    ###############################
    # Refinery
    for k in range(0,len(locations)):
      
        # Find total mass received at hub 'l'
        CG_refinery_kg = sum(CG_flow_matrix[:,k])
        
        # Ethanol produced at refinery at hub 'l'
        CG_ethanol[k] = CS_processing.sim(CG_refinery_kg)  ##Buraya l-ethanol gelecek direk excel e alinca okutacagim 

###############################
# Upper bound hub kgs
UB = 0
for j in range(0,len(hubs)):
    UB = max(sum(CG_D2H_prod))

v = np.array(V)

   #  return sum(CG_ethanol[:])*p,UB,v*p #50% of theoretical capacity          

    
    
