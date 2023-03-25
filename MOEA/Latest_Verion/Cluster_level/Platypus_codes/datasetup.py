
import csv
import pandas as pd
import numpy as np


data_name = 'biofuels_data'

#Land limits
df_limits = pd.read_excel('total_land_limit_LP.xlsx',header=0,engine = 'openpyxl')

# Yields and land limits : contains State - STASD_N - land_limits_ha - yields (1998-2013)
df_geo_corn = pd.read_excel('combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
df_geo_soy = pd.read_excel('combined_pivot_Soy.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG = pd.read_excel('combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML = pd.read_excel('combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG = pd.read_excel('combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl')  
df_geo_algae_ML = pd.read_excel('combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl')

# Greenhouse gas emission : contains State - STASD_N - greenhouse gas emission (gCO2/MJ) (1998-2013)
df_geo_corn_GHG= pd.read_excel('Corn_GHG.xlsx',header=0, engine='openpyxl')
df_geo_soy_GHG = pd.read_excel('Soy_GHG.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG_GHG = pd.read_excel('Switchgrass_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML_GHG = pd.read_excel('Switchgrass_ML_GHG.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG_GHG = pd.read_excel('Algae_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_GHG = pd.read_excel('Algae_ML_GHG.xlsx',header=0, engine='openpyxl')

# Minimum fuel selling price (MFSP) : contains State - STASD_N - MFSP ($/MJ) (1998-2013)
df_geo_corn_MFSP = pd.read_excel('Corn_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_soy_MFSP = pd.read_excel('Soy_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG_MFSP = pd.read_excel('Switchgrass_AG_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML_MFSP = pd.read_excel('Switchgrass_ML_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG_MFSP = pd.read_excel('Algae_AG_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_MFSP = pd.read_excel('Algae_ML_MFSP.xlsx',header=0, engine='openpyxl')


combined_MFSP = pd.concat([df_geo_corn_MFSP,df_geo_soy_MFSP,df_geo_grass_AG_MFSP,df_geo_grass_ML_MFSP,df_geo_algae_AG_MFSP,df_geo_algae_ML_MFSP])
combined_MFSP = combined_MFSP.reset_index(drop=True)

combined_ghg = pd.concat([df_geo_corn_GHG,df_geo_soy_GHG,df_geo_grass_AG_GHG,df_geo_grass_ML_GHG,df_geo_algae_AG_GHG,df_geo_algae_ML_GHG])
combined_ghg = combined_ghg.reset_index(drop=True)

combined_yield = pd.concat([df_geo_corn,df_geo_soy,df_geo_grass_AG,df_geo_grass_ML,df_geo_algae_AG,df_geo_algae_ML])
combined_yield = combined_yield.reset_index(drop=True)

feedstocks = ['corn','soy','grass','grass_ML','algae','algae_ML']
feedstocks_AG = ['corn','soy','grass','algae']

######=================================================########
######               Segment A.4                       ########
######=================================================########

######====== write data.dat file ======########
with open(''+str(data_name)+'.dat', 'w') as f:

####### Sets
    f.write('set Feedstock :=\n')
    # pull relevant generators
    for d in feedstocks:
        f.write(d + ' ')
    f.write(';\n\n')    

    f.write('set Feedstock_AG :=\n')
    # pull relevant generators
    for d in feedstocks_AG:
        f.write(d + ' ')
    f.write(';\n\n')       

    f.write('set district :=\n')
    # pull relevant generators
    for d in list(df_geo_corn['STASD_N']):
        f.write(str(d) + ' ')
    f.write(';\n\n')  
    
    
####### Parameters    

    f.write('param quota:= 3 \n')
    f.write(';\n\n')
    
    f.write('param fuel_conversion:= \n')
    f.write('corn' + ' ' + str(9.42) + '\n')
    f.write('soy' + ' ' + str(8.02) + '\n')
    f.write('grass' + ' ' + str(8.35) + '\n')
    f.write('algae' + ' ' + str(20.82) + '\n')
    f.write('grass_ML' + ' ' + str(8.35) + '\n')
    f.write('algae_ML' + ' ' + str(20.82) + '\n')
    f.write(';\n\n')
    
    f.write('param: mfsp ghg F_yield :=\n')
    
    for i in range(1998,2014):
        
        sample = combined_MFSP.loc[:,i]
        sample2 = combined_ghg.loc[:,i]
        sample3 = combined_yield.loc[:,i]
        
        # pull relevant generators
        for j in range(0,len(sample)):
            
            k = int(np.floor(j/36))
            
            f.write(feedstocks[k] + ' ' + str(combined_MFSP.loc[j,'STASD_N']) + ' ' + str(i) + ' ' + str(sample.loc[j]) + ' ' + str(sample2.loc[j]) + ' ' + str(sample3.loc[j])+'\n') 
            
    f.write(';\n\n')  
        
        
    f.write('param: AG_limit Grass_ML_limit Algae_ML_limit :=\n')
      
    for i in range(0,len(df_limits)):
        
        sample = df_limits.loc[i,'AG']
        sample2 = df_limits.loc[i,'ML_grass']
        sample3 = df_limits.loc[i,'ML_algae']
        
        f.write(str(df_limits.loc[i,'STASD_N']) + ' ' + str(sample) + ' ' + str(sample2) + ' ' + str(sample3)+'\n') 
            
    f.write(';\n\n')  

