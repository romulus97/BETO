"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""
import pandas as pd
import numpy as np
import corn_grain_processing as CG_processing

def QD (districts,locations):

    #####################################################################
    ##########           IMPORT DATA           ##########################
    #####################################################################
    
    # import county level data
    df_geo = pd.read_excel('combined_pivot_excel_electricity.xlsx',header=0, engine='openpyxl') #contains every eg_district code 
    districts = list(df_geo['STASD_N'])
    
    #specify grouping
    groups = 20
    
    #district-to-hub data
    filename = 'AgD2H_48_cb.csv'
    df_D2H = pd.read_csv(filename,header=0)
    c = list(df_D2H['STASD_N'])
    
    #eliminate districts that don't appear in both lists
    for i in districts:
        idx = districts.index(i)
        if i in c:
            pass
        else:
            df_geo = df_geo.drop(index=idx)
    
    df_geo = df_geo.reset_index(drop=True)
    # fips = df_geo['fips'].values
    districts = list(df_geo['STASD_N'])
    
    land_costs = df_geo.loc[:,'land_costs-$/ha'].values # $ per ha
    land_limits = df_geo['land_limits_ha'].values # county ag production area in acres
    
    # # Corn Stover
    # C_yield = df_geo['yield_bpa'].values  #yield in bushels per acre
    C_yield = df_geo.iloc[:,8:].values
    
    ########################################################################
    #########        PRE-PROCESSING       ##################################
    ########################################################################
    
    ################################
    # Convert to function inputs
    
    # Hub grouping information, distance look-up tables
    dist_D2H = []
    district_hubs = []
    for d in districts:
        
        # distance from each district to pre-defined hub
        dist_D2H.append(df_D2H.loc[df_D2H['STASD_N']==d,'travel_dist_km'].values[0])
        
        # list of hubs assigned to each county
        district_hubs.append(df_D2H.loc[df_D2H['STASD_N']==d,'destinationID'].values[0])
    
    
    #hub-to-hub data
    filename = 'AgD_48g_H2H_cb.csv'
    df_H2H = pd.read_csv(filename,header=0)
    hubs = list(df_H2H['OriginID'].unique())
    locations=hubs
        
    ################################
    # Convert to function inputs
    
    dist_map = np.zeros((len(hubs),len(locations)))
    
    # convert look-up table to distance matrix
    for i in range(0,len(hubs)):
        c1 = hubs[i]
        for j in range(0,len(locations)):
            c2 = locations[j]
            dist_map[i,j] = df_H2H.loc[(df_H2H['OriginID']==c1) & (df_H2H['DestinationID']==c2),'Total_Kilometers']
    
    map_D2H = np.zeros((len(districts), len(hubs)))
    
    # convert look-up table to distance matrix #when 50 is indexed 49 is not valid because of missing hubs
    for i in range(0,len(districts)):
        h = hubs.index(int(district_hubs[i])) # int(county_hubs[i]) - 1
        map_D2H[i,h] = 1    
                
    #####################################################################
    ##########           FUNCTION DEFINITION     ########################
    #####################################################################
       
    ###################################     
    #pre-load test decision variables
    V = []
    for a in range(0,len(districts)):
        V.append(land_limits[a]) 
      
    LC = land_costs # land costs per county
    D2H_map = map_D2H # binary matrix mapping counties (rows) to hubs (columns)
    locations = locations #possible location of biorefineries,
    hubs = hubs
    
    years = range(1958,2021)
    Q_series = []
    
    ##############################
    # Cultivation and Harvesting
    
    for b in years:
        
        
        # Empty parameters 
        CS_flow_matrix = np.zeros((len(hubs),len(locations)))
        CS_D2H_prod = np.zeros((len(LC),len(hubs)))
        CS_refinery_kg = 0
        CS_ethanol = np.zeros((len(locations),1))
            
        y = years.index(b)
        C_Y = C_yield[:,y]
        
        for c in range(0,len(LC)):
    
            # Automatic flow to pre-processing hub
            CS_D2H_prod[c,:] = D2H_map[c,:]*C_Y[c]*V[c]
    
            # # Automatic flow to pre-processing hub
            # d_index = districts.index(i)
            # CS_D2H_prod[d_index,:] = D2H_map[d_index,:]*C_Y[i]*V[i]
        
        ################################
            
        H2H_flow = []
            
        # Flow to refinery
        for d in range(0,len(hubs)):
            
            for e in range(0,len(locations)):
                
                H2H_flow.append(sum(CS_D2H_prod[:,d])*(1/len(locations)))
            
                # Mass transfer (kg of CS) from hub 'j' to hub 'k'
                CS_flow_matrix[d,e] = CS_flow_matrix[d,e] + H2H_flow[d*len(locations) + e]
                    
            
        ###############################
        # Refinery #what it's doing is it's going through at each hub and figuring out how much biomass is delivered to each hub, and then it's sending that each refinery
        for k in range(0,len(locations)):
              
            # Find total mass received at hub 'l'
            CS_refinery_kg = sum(CS_flow_matrix[:,k])
            
            # Ethanol produced at refinery at hub 'l'
            CS_ethanol[k] = CG_processing.sim(CS_refinery_kg)
            
        
        ###############################
    # Upper bound hub kgs
    UB = 0
    for j in range(0,len(hubs)):
        UB = max(sum(CS_D2H_prod))
        
    v = np.array(H2H_flow)
        
    s = sum(CS_ethanol[:])
    # Q.append(s[0])
    Q_series.append(sum(sum(CS_flow_matrix))) #total corn grain kg 
    Q_min = min(Q_series)

    return Q_min,Q_series 
