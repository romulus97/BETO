"""
Created on Fri Jul  3 16:20:20 2020

@author: jkern
"""
import pandas as pd
import numpy as np
import corn_stover_cultivation_V as CS_cultivation
import corn_stover_processing_V as CS_processing

def QD (districts,locations):

        #####################################################################
        ##########           IMPORT DATA           ##########################
        #####################################################################
    
    # import county level data
    df_yield = pd.read_excel('normalized_63_year_corn_yield.xlsx',header=0,engine='openpyxl')
    df_geo = pd.read_csv('US_ag_district_geodata.csv',header=0)
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
    
    land_costs = df_geo.loc[:,'land_costs'].values # $ per acre
    land_limits = df_geo['land_limits_ha'].values # county ag production area in acres
    
    # # Corn Stover
    # C_yield = df_geo['yield_bpa'].values  #yield in bushels per acre
    
    ########################################################################
    #########        PRE-PROCESSING       ##################################
    ########################################################################
    
    ################################
    # Convert to function inputs
    
    # Hub grouping information, distance look-up tables
    dist_D2H = []
    district_hubs = []
    for d in districts:
        
        # distance from each county to pre-defined hub
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
    LC = land_costs # land costs per county
    D2H_map = map_D2H # binary matrix mapping counties (rows) to hubs (columns)
    locations = locations #possible location of biorefineries,
    hubs = hubs
    
    years = range(1958,2021)
    Q_series = []
    
    ##############################
    # Cultivation and Harvesting
    
    for j in years:
        
        
        # Empty parameters 
        CS_flow_matrix = np.zeros((len(hubs),len(locations)))
        CS_D2H_prod = np.zeros((len(LC),len(hubs)))
        CS_refinery_kg = 0
        CS_ethanol = np.zeros((len(locations),1))
            
        C_Y = df_yield.loc[df_yield['Year']==j] # corn yield per acre
        C_Y = C_Y.reset_index(drop=True)
        
        for i in districts:
            
            sample_yield = C_Y.loc[C_Y['STASD_N']==i,'Yield_for_model'].values[0]
            land_use = df_geo.loc[df_geo['STASD_N'] == i,'land_limits_ha'].values[0]
          
            # Per ha values (need to expand)
            (CS_per_ha, seeds_per_ha, fertilization_per_ha, lime_per_ha)  = CS_cultivation.sim(sample_yield)
                  
            # Automatic flow to pre-processing hub
            d_index = districts.index(i)
            CS_D2H_prod[d_index,:] = D2H_map[d_index,:]*CS_per_ha*land_use
        
        ################################
            
        H2H_flow = []
            
        # Flow to refinery
        for n in range(0,len(hubs)):
            
            for k in range(0,len(locations)):
                
                H2H_flow.append(sum(CS_D2H_prod[:,n])*(1/len(locations)))
            
                # Mass transfer (kg of CS) from hub 'j' to hub 'k'
                CS_flow_matrix[n,k] = CS_flow_matrix[n,k] + H2H_flow[n*len(locations) + k]
                    
            
        ###############################
        # Refinery #what it's doing is it's going through at each hub and figuring out how much biomass is delivered to each hub, and then it's sending that each refinery
        for k in range(0,len(locations)):
              
            # Find total mass received at hub 'l'
            CS_refinery_kg = sum(CS_flow_matrix[:,k])
            
            # Ethanol produced at refinery at hub 'l'
            CS_ethanol[k] = CS_processing.sim(CS_refinery_kg)
            
        
        ###############################
        # Upper bound hub kgs
        UB = 0
        for j in range(0,len(hubs)):
            UB = max(sum(CS_D2H_prod))
        
        v = np.array(H2H_flow)
        
        s = sum(CS_ethanol[:])
        # Q.append(s[0])
        Q_series.append(sum(sum(CS_flow_matrix)))
        Q_min = min(Q_series)

    return Q_min,Q_series # 

