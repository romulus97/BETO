# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 20:03:00 2021

@author: Ece Ari Akdemir
"""

from platypus import GDE3, Problem, Real
from pyborg import BorgMOEA
import random
from random import randint
import pandas as pd
import numpy as np
import time

start = time.time()
version = 'district'

#####################################################################
##########           IMPORT DATA           ##########################
#####################################################################

# Yields and land limits : contains State - STASD_N - land_limits_ha - yields (1998-2013)
df_geo_corn = pd.read_excel('Data/combined_pivot_Corn.xlsx',header=0, engine='openpyxl')
df_geo_soy = pd.read_excel('Data/combined_pivot_Soy.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG = pd.read_excel('Data/combined_pivot_AG_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML = pd.read_excel('Data/combined_pivot_ML_Switchgrass.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG = pd.read_excel('Data/combined_pivot_AG_Algae.xlsx',header=0, engine='openpyxl')   
df_geo_algae_ML = pd.read_excel('Data/combined_pivot_ML_Algae.xlsx',header=0, engine='openpyxl')  

state = df_geo_corn['State'].unique()

years = range(1998,2014)
listyears =[]
corn = np.zeros(len(state))
corn_land_limit = np.zeros(len(state))
corn_t = np.zeros((len(years),len(state)))
soy = np.zeros(len(state))
soy_t = np.zeros((len(years),len(state)))
grass_AG = np.zeros(len(state))
grass_AG_t = np.zeros((len(years),len(state)))
grass_ML = np.zeros(len(state))
grass_ML_t = np.zeros((len(years),len(state)))
algae_AG = np.zeros(len(state))
algae_AG_t = np.zeros((len(years),len(state)))
algae_ML = np.zeros(len(state))
algae_ML_t = np.zeros((len(years),len(state)))

for year in years :
    listyears.append(str(year))
    
    for year in years:
        
        i = years.index(year)
        #corn yield kg/ha
        corn_land_limit_illinois= sum(df_geo_corn.loc[df_geo_corn['State'] == 'ILLINOIS','land_limits_ha'].values)
        corn_land_limit_indiana= sum(df_geo_corn.loc[df_geo_corn['State'] == 'INDIANA','land_limits_ha'].values)
        corn_land_limit_iowa= sum(df_geo_corn.loc[df_geo_corn['State'] == 'IOWA','land_limits_ha'].values)
        corn_land_limit_kansas= sum(df_geo_corn.loc[df_geo_corn['State'] == 'KANSAS','land_limits_ha'].values)
        corn_land_limit_michicgan= sum(df_geo_corn.loc[df_geo_corn['State'] == 'MICHIGAN','land_limits_ha'].values)
        corn_land_limit_minnesota= sum(df_geo_corn.loc[df_geo_corn['State'] == 'MINNESOTA','land_limits_ha'].values)
        corn_land_limit_missouri= sum(df_geo_corn.loc[df_geo_corn['State'] == 'MISSOURI','land_limits_ha'].values)
        corn_land_limit_nebraska= sum(df_geo_corn.loc[df_geo_corn['State'] == 'NEBRASKA','land_limits_ha'].values)
        corn_land_limit_north_dakota= sum(df_geo_corn.loc[df_geo_corn['State'] == 'NORTH DAKOTA','land_limits_ha'].values)
        corn_land_limit_ohio= sum(df_geo_corn.loc[df_geo_corn['State'] == 'OHIO','land_limits_ha'].values)
        corn_land_limit_south_dakota= sum(df_geo_corn.loc[df_geo_corn['State'] == 'SOUTH DAKOTA','land_limits_ha'].values)
        corn_land_limit_wisconsin= sum(df_geo_corn.loc[df_geo_corn['State'] == 'WISCONSIN','land_limits_ha'].values)
        corn_land_limit = [corn_land_limit_illinois,corn_land_limit_indiana,corn_land_limit_iowa,corn_land_limit_kansas,corn_land_limit_michicgan,corn_land_limit_minnesota,
                           corn_land_limit_missouri,corn_land_limit_nebraska,corn_land_limit_north_dakota,corn_land_limit_ohio,corn_land_limit_south_dakota,corn_land_limit_wisconsin]
        
        
        corn_illinois = sum(df_geo_corn.loc[df_geo_corn['State'] == 'ILLINOIS',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'ILLINOIS',year].values)
        corn_indiana = sum(df_geo_corn.loc[df_geo_corn['State'] == 'INDIANA',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'INDIANA',year].values)
        corn_iowa = sum(df_geo_corn.loc[df_geo_corn['State'] == 'IOWA',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'IOWA',year].values)
        corn_kansas = sum(df_geo_corn.loc[df_geo_corn['State'] == 'KANSAS',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'KANSAS',year].values)
        corn_michicgan = sum(df_geo_corn.loc[df_geo_corn['State'] == 'MICHIGAN',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'MICHIGAN',year].values)
        corn_minnesota = sum(df_geo_corn.loc[df_geo_corn['State'] == 'MINNESOTA',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'MINNESOTA',year].values)
        corn_missouri = sum(df_geo_corn.loc[df_geo_corn['State'] == 'MISSOURI',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'MISSOURI',year].values)
        corn_nebraska = sum(df_geo_corn.loc[df_geo_corn['State'] == 'NEBRASKA',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'NEBRASKA',year].values)
        corn_north_dakota = sum(df_geo_corn.loc[df_geo_corn['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'NORTH DAKOTA',year].values)
        corn_ohio = sum(df_geo_corn.loc[df_geo_corn['State'] == 'OHIO',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'OHIO',year].values)
        corn_south_dakota = sum(df_geo_corn.loc[df_geo_corn['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'SOUTH DAKOTA',year].values)
        corn_wisconsin = sum(df_geo_corn.loc[df_geo_corn['State'] == 'WISCONSIN',year].values)/len(df_geo_corn.loc[df_geo_corn['State'] == 'WISCONSIN',year].values)
        corn = [corn_illinois,corn_indiana,corn_iowa,corn_kansas,corn_michicgan,corn_minnesota,corn_missouri,corn_nebraska,corn_north_dakota,corn_ohio,corn_south_dakota,corn_wisconsin] 
        corn_t[i] = corn
        df_corn = corn_t.T
        df_corn = pd.DataFrame(df_corn, columns = [*range(1998,2014)]) # list *
        df_corn.insert(0,"state",state)
        df_corn.insert(1,"land_limits_ha",corn_land_limit)
        
        
        
        #soy yield kg/ha
        soy_land_limit_illinois= sum(df_geo_soy.loc[df_geo_soy['State'] == 'ILLINOIS','land_limits_ha'].values)
        soy_land_limit_indiana= sum(df_geo_soy.loc[df_geo_soy['State'] == 'INDIANA','land_limits_ha'].values)
        soy_land_limit_iowa= sum(df_geo_soy.loc[df_geo_soy['State'] == 'IOWA','land_limits_ha'].values)
        soy_land_limit_kansas= sum(df_geo_soy.loc[df_geo_soy['State'] == 'KANSAS','land_limits_ha'].values)
        soy_land_limit_michicgan= sum(df_geo_soy.loc[df_geo_soy['State'] == 'MICHIGAN','land_limits_ha'].values)
        soy_land_limit_minnesota= sum(df_geo_soy.loc[df_geo_soy['State'] == 'MINNESOTA','land_limits_ha'].values)
        soy_land_limit_missouri= sum(df_geo_soy.loc[df_geo_soy['State'] == 'MISSOURI','land_limits_ha'].values)
        soy_land_limit_nebraska= sum(df_geo_soy.loc[df_geo_soy['State'] == 'NEBRASKA','land_limits_ha'].values)
        soy_land_limit_north_dakota= sum(df_geo_soy.loc[df_geo_soy['State'] == 'NORTH DAKOTA','land_limits_ha'].values)
        soy_land_limit_ohio= sum(df_geo_soy.loc[df_geo_soy['State'] == 'OHIO','land_limits_ha'].values)
        soy_land_limit_south_dakota= sum(df_geo_soy.loc[df_geo_soy['State'] == 'SOUTH DAKOTA','land_limits_ha'].values)
        soy_land_limit_wisconsin= sum(df_geo_soy.loc[df_geo_soy['State'] == 'WISCONSIN','land_limits_ha'].values)
        soy_land_limit = [soy_land_limit_illinois,soy_land_limit_indiana,soy_land_limit_iowa,soy_land_limit_kansas,soy_land_limit_michicgan,soy_land_limit_minnesota,
                           soy_land_limit_missouri,soy_land_limit_nebraska,soy_land_limit_north_dakota,soy_land_limit_ohio,soy_land_limit_south_dakota,soy_land_limit_wisconsin]
        
        
        
        soy_illinois = sum(df_geo_soy.loc[df_geo_soy['State'] == 'ILLINOIS',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'ILLINOIS',year].values)
        soy_indiana = sum(df_geo_soy.loc[df_geo_soy['State'] == 'INDIANA',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'INDIANA',year].values)
        soy_iowa = sum(df_geo_soy.loc[df_geo_soy['State'] == 'IOWA',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'IOWA',year].values)
        soy_kansas = sum(df_geo_soy.loc[df_geo_soy['State'] == 'KANSAS',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'KANSAS',year].values)
        soy_michicgan = sum(df_geo_soy.loc[df_geo_soy['State'] == 'MICHIGAN',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'MICHIGAN',year].values)
        soy_minnesota = sum(df_geo_soy.loc[df_geo_soy['State'] == 'MINNESOTA',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'MINNESOTA',year].values)
        soy_missouri = sum(df_geo_soy.loc[df_geo_soy['State'] == 'MISSOURI',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'MISSOURI',year].values)
        soy_nebraska = sum(df_geo_soy.loc[df_geo_soy['State'] == 'NEBRASKA',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'NEBRASKA',year].values)
        soy_north_dakota = sum(df_geo_soy.loc[df_geo_soy['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'NORTH DAKOTA',year].values)
        soy_ohio = sum(df_geo_soy.loc[df_geo_soy['State'] == 'OHIO',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'OHIO',year].values)
        soy_south_dakota = sum(df_geo_soy.loc[df_geo_soy['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'SOUTH DAKOTA',year].values)
        soy_wisconsin = sum(df_geo_soy.loc[df_geo_soy['State'] == 'WISCONSIN',year].values)/len(df_geo_soy.loc[df_geo_soy['State'] == 'WISCONSIN',year].values)
        soy = [soy_illinois,soy_indiana,soy_iowa,soy_kansas,soy_michicgan,soy_minnesota,soy_missouri,soy_nebraska,soy_north_dakota,soy_ohio,soy_south_dakota,soy_wisconsin] 
        soy_t[i] = soy
        df_soy = soy_t.T
        df_soy = pd.DataFrame(df_soy, columns = [*range(1998,2014)]) # list *
        df_soy.insert(0,"state",state)
        df_soy.insert(1,"land_limits_ha",soy_land_limit)
        
        
        #grass AG yield kg/ha
        grass_AG_land_limit_illinois= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'ILLINOIS','land_limits_ha'].values)
        grass_AG_land_limit_indiana= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'INDIANA','land_limits_ha'].values)
        grass_AG_land_limit_iowa= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'IOWA','land_limits_ha'].values)
        grass_AG_land_limit_kansas= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'KANSAS','land_limits_ha'].values)
        grass_AG_land_limit_michicgan= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MICHIGAN','land_limits_ha'].values)
        grass_AG_land_limit_minnesota= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MINNESOTA','land_limits_ha'].values)
        grass_AG_land_limit_missouri= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MISSOURI','land_limits_ha'].values)
        grass_AG_land_limit_nebraska= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'NEBRASKA','land_limits_ha'].values)
        grass_AG_land_limit_north_dakota= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'NORTH DAKOTA','land_limits_ha'].values)
        grass_AG_land_limit_ohio= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'OHIO','land_limits_ha'].values)
        grass_AG_land_limit_south_dakota= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'SOUTH DAKOTA','land_limits_ha'].values)
        grass_AG_land_limit_wisconsin= sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'WISCONSIN','land_limits_ha'].values)
        grass_AG_land_limit = [grass_AG_land_limit_illinois,grass_AG_land_limit_indiana,grass_AG_land_limit_iowa,grass_AG_land_limit_kansas,grass_AG_land_limit_michicgan,grass_AG_land_limit_minnesota,
                           grass_AG_land_limit_missouri,grass_AG_land_limit_nebraska,grass_AG_land_limit_north_dakota,grass_AG_land_limit_ohio,grass_AG_land_limit_south_dakota,grass_AG_land_limit_wisconsin]
        
        
        
        grass_AG_illinois = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'ILLINOIS',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'ILLINOIS',year].values)
        grass_AG_indiana = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'INDIANA',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'INDIANA',year].values)
        grass_AG_iowa = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'IOWA',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'IOWA',year].values)
        grass_AG_kansas = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'KANSAS',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'KANSAS',year].values)
        grass_AG_michicgan = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MICHIGAN',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MICHIGAN',year].values)
        grass_AG_minnesota = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MINNESOTA',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MINNESOTA',year].values)
        grass_AG_missouri = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MISSOURI',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'MISSOURI',year].values)
        grass_AG_nebraska = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'NEBRASKA',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'NEBRASKA',year].values)
        grass_AG_north_dakota = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'NORTH DAKOTA',year].values)
        grass_AG_ohio = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'OHIO',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'OHIO',year].values)
        grass_AG_south_dakota = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'SOUTH DAKOTA',year].values)
        grass_AG_wisconsin = sum(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'WISCONSIN',year].values)/len(df_geo_grass_AG.loc[df_geo_grass_AG['State'] == 'WISCONSIN',year].values)
        grass_AG = [grass_AG_illinois,grass_AG_indiana,grass_AG_iowa,grass_AG_kansas,grass_AG_michicgan,grass_AG_minnesota,grass_AG_missouri,grass_AG_nebraska,grass_AG_north_dakota,grass_AG_ohio,grass_AG_south_dakota,grass_AG_wisconsin] 
        grass_AG_t[i] = grass_AG
        df_grass_AG = grass_AG_t.T
        df_grass_AG = pd.DataFrame(df_grass_AG, columns = [*range(1998,2014)]) # list *
        df_grass_AG.insert(0,"state",state)
        df_grass_AG.insert(1,"land_limits_ha",grass_AG_land_limit)
        
        #grass ML yield kg/ha
        grass_ML_land_limit_illinois= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'ILLINOIS','land_limits_ha'].values)
        grass_ML_land_limit_indiana= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'INDIANA','land_limits_ha'].values)
        grass_ML_land_limit_iowa= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'IOWA','land_limits_ha'].values)
        grass_ML_land_limit_kansas= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'KANSAS','land_limits_ha'].values)
        grass_ML_land_limit_michicgan= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MICHIGAN','land_limits_ha'].values)
        grass_ML_land_limit_minnesota= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MINNESOTA','land_limits_ha'].values)
        grass_ML_land_limit_missouri= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MISSOURI','land_limits_ha'].values)
        grass_ML_land_limit_nebraska= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'NEBRASKA','land_limits_ha'].values)
        grass_ML_land_limit_north_dakota= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'NORTH DAKOTA','land_limits_ha'].values)
        grass_ML_land_limit_ohio= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'OHIO','land_limits_ha'].values)
        grass_ML_land_limit_south_dakota= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'SOUTH DAKOTA','land_limits_ha'].values)
        grass_ML_land_limit_wisconsin= sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'WISCONSIN','land_limits_ha'].values)
        grass_ML_land_limit = [grass_ML_land_limit_illinois,grass_ML_land_limit_indiana,grass_ML_land_limit_iowa,grass_ML_land_limit_kansas,grass_ML_land_limit_michicgan,grass_ML_land_limit_minnesota,
                           grass_ML_land_limit_missouri,grass_ML_land_limit_nebraska,grass_ML_land_limit_north_dakota,grass_ML_land_limit_ohio,grass_ML_land_limit_south_dakota,grass_ML_land_limit_wisconsin]
        
        
        
        grass_ML_illinois = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'ILLINOIS',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'ILLINOIS',year].values)
        grass_ML_indiana = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'INDIANA',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'INDIANA',year].values)
        grass_ML_iowa = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'IOWA',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'IOWA',year].values)
        grass_ML_kansas = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'KANSAS',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'KANSAS',year].values)
        grass_ML_michicgan = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MICHIGAN',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MICHIGAN',year].values)
        grass_ML_minnesota = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MINNESOTA',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MINNESOTA',year].values)
        grass_ML_missouri = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MISSOURI',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'MISSOURI',year].values)
        grass_ML_nebraska = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'NEBRASKA',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'NEBRASKA',year].values)
        grass_ML_north_dakota = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'NORTH DAKOTA',year].values)
        grass_ML_ohio = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'OHIO',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'OHIO',year].values)
        grass_ML_south_dakota = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'SOUTH DAKOTA',year].values)
        grass_ML_wisconsin = sum(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'WISCONSIN',year].values)/len(df_geo_grass_ML.loc[df_geo_grass_ML['State'] == 'WISCONSIN',year].values)
        grass_ML = [grass_ML_illinois,grass_ML_indiana,grass_ML_iowa,grass_ML_kansas,grass_ML_michicgan,grass_ML_minnesota,grass_ML_missouri,grass_ML_nebraska,grass_ML_north_dakota,grass_ML_ohio,grass_ML_south_dakota,grass_ML_wisconsin] 
        grass_ML_t[i] = grass_ML
        df_grass_ML = grass_ML_t.T
        df_grass_ML = pd.DataFrame(df_grass_ML, columns = [*range(1998,2014)]) # list *
        df_grass_ML.insert(0,"state",state)
        df_grass_ML.insert(1,"land_limits_ha",grass_ML_land_limit)
        
        
        #algae AG kg/ha
        algae_AG_land_limit_illinois= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'ILLINOIS','land_limits_ha'].values)
        algae_AG_land_limit_indiana= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'INDIANA','land_limits_ha'].values)
        algae_AG_land_limit_iowa= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'IOWA','land_limits_ha'].values)
        algae_AG_land_limit_kansas= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'KANSAS','land_limits_ha'].values)
        algae_AG_land_limit_michicgan= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MICHIGAN','land_limits_ha'].values)
        algae_AG_land_limit_minnesota= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MINNESOTA','land_limits_ha'].values)
        algae_AG_land_limit_missouri= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MISSOURI','land_limits_ha'].values)
        algae_AG_land_limit_nebraska= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'NEBRASKA','land_limits_ha'].values)
        algae_AG_land_limit_north_dakota= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'NORTH DAKOTA','land_limits_ha'].values)
        algae_AG_land_limit_ohio= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'OHIO','land_limits_ha'].values)
        algae_AG_land_limit_south_dakota= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'SOUTH DAKOTA','land_limits_ha'].values)
        algae_AG_land_limit_wisconsin= sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'WISCONSIN','land_limits_ha'].values)
        algae_AG_land_limit = [algae_AG_land_limit_illinois,algae_AG_land_limit_indiana,algae_AG_land_limit_iowa,algae_AG_land_limit_kansas,algae_AG_land_limit_michicgan,algae_AG_land_limit_minnesota,
                           algae_AG_land_limit_missouri,algae_AG_land_limit_nebraska,algae_AG_land_limit_north_dakota,algae_AG_land_limit_ohio,algae_AG_land_limit_south_dakota,algae_AG_land_limit_wisconsin]
        
        
        
        algae_AG_illinois = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'ILLINOIS',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'ILLINOIS',year].values)
        algae_AG_indiana = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'INDIANA',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'INDIANA',year].values)
        algae_AG_iowa = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'IOWA',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'IOWA',year].values)
        algae_AG_kansas = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'KANSAS',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'KANSAS',year].values)
        algae_AG_michicgan = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MICHIGAN',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MICHIGAN',year].values)
        algae_AG_minnesota = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MINNESOTA',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MINNESOTA',year].values)
        algae_AG_missouri = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MISSOURI',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'MISSOURI',year].values)
        algae_AG_nebraska = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'NEBRASKA',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'NEBRASKA',year].values)
        algae_AG_north_dakota = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'NORTH DAKOTA',year].values)
        algae_AG_ohio = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'OHIO',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'OHIO',year].values)
        algae_AG_south_dakota = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'SOUTH DAKOTA',year].values)
        algae_AG_wisconsin = sum(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'WISCONSIN',year].values)/len(df_geo_algae_AG.loc[df_geo_algae_AG['State'] == 'WISCONSIN',year].values)
        algae_AG = [algae_AG_illinois,algae_AG_indiana,algae_AG_iowa,algae_AG_kansas,algae_AG_michicgan,algae_AG_minnesota,algae_AG_missouri,algae_AG_nebraska,algae_AG_north_dakota,algae_AG_ohio,algae_AG_south_dakota,algae_AG_wisconsin] 
        algae_AG_t[i] = algae_AG
        df_algae_AG = algae_AG_t.T
        df_algae_AG = pd.DataFrame(df_algae_AG, columns = [*range(1998,2014)]) # list *
        df_algae_AG.insert(0,"state",state)
        df_algae_AG.insert(1,"land_limits_ha",algae_AG_land_limit)
        
        
        
        #algae_ML yield kg/ha
        algae_ML_land_limit_illinois= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'ILLINOIS','land_limits_ha'].values)
        algae_ML_land_limit_indiana= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'INDIANA','land_limits_ha'].values)
        algae_ML_land_limit_iowa= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'IOWA','land_limits_ha'].values)
        algae_ML_land_limit_kansas= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'KANSAS','land_limits_ha'].values)
        algae_ML_land_limit_michicgan= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MICHIGAN','land_limits_ha'].values)
        algae_ML_land_limit_minnesota= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MINNESOTA','land_limits_ha'].values)
        algae_ML_land_limit_missouri= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MISSOURI','land_limits_ha'].values)
        algae_ML_land_limit_nebraska= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'NEBRASKA','land_limits_ha'].values)
        algae_ML_land_limit_north_dakota= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'NORTH DAKOTA','land_limits_ha'].values)
        algae_ML_land_limit_ohio= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'OHIO','land_limits_ha'].values)
        algae_ML_land_limit_south_dakota= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'SOUTH DAKOTA','land_limits_ha'].values)
        algae_ML_land_limit_wisconsin= sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'WISCONSIN','land_limits_ha'].values)
        algae_ML_land_limit = [algae_ML_land_limit_illinois,algae_ML_land_limit_indiana,algae_ML_land_limit_iowa,algae_ML_land_limit_kansas,algae_ML_land_limit_michicgan,algae_ML_land_limit_minnesota,
                           algae_ML_land_limit_missouri,algae_ML_land_limit_nebraska,algae_ML_land_limit_north_dakota,algae_ML_land_limit_ohio,algae_ML_land_limit_south_dakota,algae_ML_land_limit_wisconsin]
        
        
        
        algae_ML_illinois = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'ILLINOIS',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'ILLINOIS',year].values)
        algae_ML_indiana = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'INDIANA',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'INDIANA',year].values)
        algae_ML_iowa = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'IOWA',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'IOWA',year].values)
        algae_ML_kansas = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'KANSAS',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'KANSAS',year].values)
        algae_ML_michicgan = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MICHIGAN',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MICHIGAN',year].values)
        algae_ML_minnesota = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MINNESOTA',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MINNESOTA',year].values)
        algae_ML_missouri = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MISSOURI',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'MISSOURI',year].values)
        algae_ML_nebraska = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'NEBRASKA',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'NEBRASKA',year].values)
        algae_ML_north_dakota = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'NORTH DAKOTA',year].values)
        algae_ML_ohio = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'OHIO',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'OHIO',year].values)
        algae_ML_south_dakota = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'SOUTH DAKOTA',year].values)
        algae_ML_wisconsin = sum(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'WISCONSIN',year].values)/len(df_geo_algae_ML.loc[df_geo_algae_ML['State'] == 'WISCONSIN',year].values)
        algae_ML = [algae_ML_illinois,algae_ML_indiana,algae_ML_iowa,algae_ML_kansas,algae_ML_michicgan,algae_ML_minnesota,algae_ML_missouri,algae_ML_nebraska,algae_ML_north_dakota,algae_ML_ohio,algae_ML_south_dakota,algae_ML_wisconsin] 
        algae_ML_t[i] = algae_ML
        df_algae_ML = algae_ML_t.T
        df_algae_ML = pd.DataFrame(df_algae_ML, columns = [*range(1998,2014)]) # list *
        df_algae_ML.insert(0,"state",state)
        df_algae_ML.insert(1,"land_limits_ha",algae_ML_land_limit)



df_corn.to_excel('combined_pivot_Corn.xlsx')
df_soy.to_excel('combined_pivot_Soy.xlsx')
df_grass_AG.to_excel('combined_pivot_AG_Switchgrass.xlsx')
df_grass_ML.to_excel('combined_pivot_ML_Switchgrass.xlsx')
df_algae_AG.to_excel('combined_pivot_AG_Algae.xlsx')
df_algae_ML.to_excel('combined_pivot_ML_Algae.xlsx')

# Greenhouse gas emission : contains State - STASD_N - greenhouse gas emission (gCO2/MJ) (1998-2013)
df_geo_corn_GHG= pd.read_excel('Data/Corn_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_soy_GHG = pd.read_excel('Data/Soy_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_grass_AG_GHG = pd.read_excel('Data/Switchgrass_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_grass_ML_GHG = pd.read_excel('Data/Switchgrass_ML_GHG.xlsx',header=0, engine='openpyxl') 
df_geo_algae_AG_GHG = pd.read_excel('Data/Algae_AG_GHG.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_GHG = pd.read_excel('Data/Algae_ML_GHG.xlsx',header=0, engine='openpyxl')

corn_GHG = np.zeros(len(state))
corn_t_GHG = np.zeros((len(years),len(state)))
soy_GHG = np.zeros(len(state))
soy_t_GHG = np.zeros((len(years),len(state)))
grass_AG_GHG = np.zeros(len(state))
grass_AG_t_GHG = np.zeros((len(years),len(state)))
grass_ML_GHG = np.zeros(len(state))
grass_ML_t_GHG = np.zeros((len(years),len(state)))
algae_AG_GHG = np.zeros(len(state))
algae_AG_t_GHG = np.zeros((len(years),len(state)))
algae_ML_GHG = np.zeros(len(state))
algae_ML_t_GHG = np.zeros((len(years),len(state)))

for year in years :
    listyears.append(str(year))
    
    for year in years:
        
        i = years.index(year)
        #corn yield kg/ha
        
        corn_illinois_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'ILLINOIS',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'ILLINOIS',year].values)
        corn_indiana_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'INDIANA',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'INDIANA',year].values)
        corn_iowa_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'IOWA',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'IOWA',year].values)
        corn_kansas_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'KANSAS',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'KANSAS',year].values)
        corn_michicgan_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'MICHIGAN',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'MICHIGAN',year].values)
        corn_minnesota_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'MINNESOTA',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'MINNESOTA',year].values)
        corn_missouri_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'MISSOURI',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'MISSOURI',year].values)
        corn_nebraska_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'NEBRASKA',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'NEBRASKA',year].values)
        corn_north_dakota_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'NORTH DAKOTA',year].values)
        corn_ohio_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'OHIO',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'OHIO',year].values)
        corn_south_dakota_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'SOUTH DAKOTA',year].values)
        corn_wisconsin_GHG = sum(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'WISCONSIN',year].values)/len(df_geo_corn_GHG.loc[df_geo_corn_GHG['State'] == 'WISCONSIN',year].values)
        corn_GHG = [corn_illinois_GHG,corn_indiana_GHG,corn_iowa_GHG,corn_kansas_GHG,corn_michicgan_GHG,corn_minnesota_GHG,corn_missouri_GHG,corn_nebraska_GHG,corn_north_dakota_GHG,corn_ohio_GHG,corn_south_dakota_GHG,corn_wisconsin_GHG] 
        corn_t_GHG[i] = corn_GHG
        df_corn_GHG = corn_t_GHG.T
        df_corn_GHG = pd.DataFrame(df_corn_GHG, columns = [*range(1998,2014)]) # list *
        df_corn_GHG.insert(0,"state",state)

        
        
        
        #soy yield kg/ha

        soy_illinois_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'ILLINOIS',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'ILLINOIS',year].values)
        soy_indiana_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'INDIANA',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'INDIANA',year].values)
        soy_iowa_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'IOWA',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'IOWA',year].values)
        soy_kansas_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'KANSAS',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'KANSAS',year].values)
        soy_michicgan_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'MICHIGAN',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'MICHIGAN',year].values)
        soy_minnesota_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'MINNESOTA',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'MINNESOTA',year].values)
        soy_missouri_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'MISSOURI',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'MISSOURI',year].values)
        soy_nebraska_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'NEBRASKA',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'NEBRASKA',year].values)
        soy_north_dakota_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'NORTH DAKOTA',year].values)
        soy_ohio_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'OHIO',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'OHIO',year].values)
        soy_south_dakota_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'SOUTH DAKOTA',year].values)
        soy_wisconsin_GHG = sum(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'WISCONSIN',year].values)/len(df_geo_soy_GHG.loc[df_geo_soy_GHG['State'] == 'WISCONSIN',year].values)
        soy_GHG = [soy_illinois_GHG,soy_indiana_GHG,soy_iowa_GHG,soy_kansas_GHG,soy_michicgan_GHG,soy_minnesota_GHG,soy_missouri_GHG,soy_nebraska_GHG,soy_north_dakota_GHG,soy_ohio_GHG,soy_south_dakota_GHG,soy_wisconsin_GHG] 
        soy_t_GHG[i] = soy_GHG
        df_soy_GHG = soy_t_GHG.T
        df_soy_GHG = pd.DataFrame(df_soy_GHG, columns = [*range(1998,2014)]) # list *
        df_soy_GHG.insert(0,"state",state)

        
        
        #grass AG yield kg/ha

        grass_AG_illinois_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'ILLINOIS',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'ILLINOIS',year].values)
        grass_AG_indiana_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'INDIANA',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'INDIANA',year].values)
        grass_AG_iowa_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'IOWA',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'IOWA',year].values)
        grass_AG_kansas_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'KANSAS',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'KANSAS',year].values)
        grass_AG_michicgan_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'MICHIGAN',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'MICHIGAN',year].values)
        grass_AG_minnesota_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'MINNESOTA',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'MINNESOTA',year].values)
        grass_AG_missouri_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'MISSOURI',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'MISSOURI',year].values)
        grass_AG_nebraska_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'NEBRASKA',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'NEBRASKA',year].values)
        grass_AG_north_dakota_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'NORTH DAKOTA',year].values)
        grass_AG_ohio_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'OHIO',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'OHIO',year].values)
        grass_AG_south_dakota_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'SOUTH DAKOTA',year].values)
        grass_AG_wisconsin_GHG = sum(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'WISCONSIN',year].values)/len(df_geo_grass_AG_GHG.loc[df_geo_grass_AG_GHG['State'] == 'WISCONSIN',year].values)
        grass_AG_GHG = [grass_AG_illinois_GHG,grass_AG_indiana_GHG,grass_AG_iowa_GHG,grass_AG_kansas_GHG,grass_AG_michicgan_GHG,grass_AG_minnesota_GHG,grass_AG_missouri_GHG,grass_AG_nebraska_GHG,grass_AG_north_dakota_GHG,grass_AG_ohio_GHG,grass_AG_south_dakota_GHG,grass_AG_wisconsin_GHG] 
        grass_AG_t_GHG[i] = grass_AG_GHG
        df_grass_AG_GHG = grass_AG_t_GHG.T
        df_grass_AG_GHG = pd.DataFrame(df_grass_AG_GHG, columns = [*range(1998,2014)]) # list *
        df_grass_AG_GHG.insert(0,"state",state)

        
        #grass ML yield kg/ha

        grass_ML_illinois_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'ILLINOIS',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'ILLINOIS',year].values)
        grass_ML_indiana_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'INDIANA',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'INDIANA',year].values)
        grass_ML_iowa_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'IOWA',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'IOWA',year].values)
        grass_ML_kansas_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'KANSAS',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'KANSAS',year].values)
        grass_ML_michicgan_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'MICHIGAN',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'MICHIGAN',year].values)
        grass_ML_minnesota_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'MINNESOTA',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'MINNESOTA',year].values)
        grass_ML_missouri_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'MISSOURI',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'MISSOURI',year].values)
        grass_ML_nebraska_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'NEBRASKA',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'NEBRASKA',year].values)
        grass_ML_north_dakota_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'NORTH DAKOTA',year].values)
        grass_ML_ohio_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'OHIO',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'OHIO',year].values)
        grass_ML_south_dakota_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'SOUTH DAKOTA',year].values)
        grass_ML_wisconsin_GHG = sum(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'WISCONSIN',year].values)/len(df_geo_grass_ML_GHG.loc[df_geo_grass_ML_GHG['State'] == 'WISCONSIN',year].values)
        grass_ML_GHG = [grass_ML_illinois_GHG,grass_ML_indiana_GHG,grass_ML_iowa_GHG,grass_ML_kansas_GHG,grass_ML_michicgan_GHG,grass_ML_minnesota_GHG,grass_ML_missouri_GHG,grass_ML_nebraska_GHG,grass_ML_north_dakota_GHG,grass_ML_ohio_GHG,grass_ML_south_dakota_GHG,grass_ML_wisconsin_GHG] 
        grass_ML_t_GHG[i] = grass_ML_GHG
        df_grass_ML_GHG = grass_ML_t_GHG.T
        df_grass_ML_GHG = pd.DataFrame(df_grass_ML_GHG, columns = [*range(1998,2014)]) # list *
        df_grass_ML_GHG.insert(0,"state",state)

        
        
        #algae AG kg/ha

        algae_AG_illinois_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'ILLINOIS',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'ILLINOIS',year].values)
        algae_AG_indiana_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'INDIANA',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'INDIANA',year].values)
        algae_AG_iowa_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'IOWA',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'IOWA',year].values)
        algae_AG_kansas_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'KANSAS',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'KANSAS',year].values)
        algae_AG_michicgan_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'MICHIGAN',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'MICHIGAN',year].values)
        algae_AG_minnesota_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'MINNESOTA',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'MINNESOTA',year].values)
        algae_AG_missouri_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'MISSOURI',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'MISSOURI',year].values)
        algae_AG_nebraska_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'NEBRASKA',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'NEBRASKA',year].values)
        algae_AG_north_dakota_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'NORTH DAKOTA',year].values)
        algae_AG_ohio_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'OHIO',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'OHIO',year].values)
        algae_AG_south_dakota_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'SOUTH DAKOTA',year].values)
        algae_AG_wisconsin_GHG = sum(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'WISCONSIN',year].values)/len(df_geo_algae_AG_GHG.loc[df_geo_algae_AG_GHG['State'] == 'WISCONSIN',year].values)
        algae_AG_GHG = [algae_AG_illinois_GHG,algae_AG_indiana_GHG,algae_AG_iowa_GHG,algae_AG_kansas_GHG,algae_AG_michicgan_GHG,algae_AG_minnesota_GHG,algae_AG_missouri_GHG,algae_AG_nebraska_GHG,algae_AG_north_dakota_GHG,algae_AG_ohio_GHG,algae_AG_south_dakota_GHG,algae_AG_wisconsin_GHG] 
        algae_AG_t_GHG[i] = algae_AG_GHG
        df_algae_AG_GHG = algae_AG_t_GHG.T
        df_algae_AG_GHG = pd.DataFrame(df_algae_AG_GHG, columns = [*range(1998,2014)]) # list *
        df_algae_AG_GHG.insert(0,"state",state)

        
        
        
        #algae_ML yield kg/ha

        algae_ML_illinois_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'ILLINOIS',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'ILLINOIS',year].values)
        algae_ML_indiana_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'INDIANA',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'INDIANA',year].values)
        algae_ML_iowa_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'IOWA',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'IOWA',year].values)
        algae_ML_kansas_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'KANSAS',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'KANSAS',year].values)
        algae_ML_michicgan_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'MICHIGAN',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'MICHIGAN',year].values)
        algae_ML_minnesota_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'MINNESOTA',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'MINNESOTA',year].values)
        algae_ML_missouri_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'MISSOURI',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'MISSOURI',year].values)
        algae_ML_nebraska_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'NEBRASKA',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'NEBRASKA',year].values)
        algae_ML_north_dakota_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'NORTH DAKOTA',year].values)
        algae_ML_ohio_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'OHIO',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'OHIO',year].values)
        algae_ML_south_dakota_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'SOUTH DAKOTA',year].values)
        algae_ML_wisconsin_GHG = sum(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'WISCONSIN',year].values)/len(df_geo_algae_ML_GHG.loc[df_geo_algae_ML_GHG['State'] == 'WISCONSIN',year].values)
        algae_ML_GHG = [algae_ML_illinois_GHG,algae_ML_indiana_GHG,algae_ML_iowa_GHG,algae_ML_kansas_GHG,algae_ML_michicgan_GHG,algae_ML_minnesota_GHG,algae_ML_missouri_GHG,algae_ML_nebraska_GHG,algae_ML_north_dakota_GHG,algae_ML_ohio_GHG,algae_ML_south_dakota_GHG,algae_ML_wisconsin_GHG] 
        algae_ML_t_GHG[i] = algae_ML_GHG
        df_algae_ML_GHG = algae_ML_t_GHG.T
        df_algae_ML_GHG = pd.DataFrame(df_algae_ML_GHG, columns = [*range(1998,2014)]) # list *
        df_algae_ML_GHG.insert(0,"state",state)


df_corn_GHG.to_excel('Corn_GHG.xlsx')
df_soy_GHG.to_excel('Soy_GHG.xlsx')
df_grass_AG_GHG.to_excel('Switchgrass_AG_GHG.xlsx')
df_grass_ML_GHG.to_excel('Switchgrass_ML_GHG.xlsx')
df_algae_AG_GHG.to_excel('Algae_AG_GHG.xlsx')
df_algae_ML_GHG.to_excel('Algae_ML_GHG.xlsx')


# Minimum fuel selling price (MFSP) : contains State - STASD_N - MFSP ($/MJ) (1998-2013)
df_geo_corn_MFSP = pd.read_excel('Data/Corn_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_soy_MFSP = pd.read_excel('Data/Soy_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_grass_AG_MFSP = pd.read_excel('Data/Switchgrass_AG_MFSP.xlsx',header=0, engine='openpyxl') 
df_geo_grass_ML_MFSP = pd.read_excel('Data/Switchgrass_ML_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_AG_MFSP = pd.read_excel('Data/Algae_AG_MFSP.xlsx',header=0, engine='openpyxl')
df_geo_algae_ML_MFSP = pd.read_excel('Data/Algae_ML_MFSP.xlsx',header=0, engine='openpyxl')

corn_MFSP = np.zeros(len(state))
corn_t_MFSP = np.zeros((len(years),len(state)))
soy_MFSP = np.zeros(len(state))
soy_t_MFSP = np.zeros((len(years),len(state)))
grass_AG_MFSP = np.zeros(len(state))
grass_AG_t_MFSP = np.zeros((len(years),len(state)))
grass_ML_MFSP = np.zeros(len(state))
grass_ML_t_MFSP = np.zeros((len(years),len(state)))
algae_AG_MFSP = np.zeros(len(state))
algae_AG_t_MFSP = np.zeros((len(years),len(state)))
algae_ML_MFSP = np.zeros(len(state))
algae_ML_t_MFSP = np.zeros((len(years),len(state)))

for year in years :
    listyears.append(str(year))
    
    for year in years:
        
        i = years.index(year)
        #corn yield kg/ha
        
        corn_illinois_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'ILLINOIS',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'ILLINOIS',year].values)
        corn_indiana_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'INDIANA',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'INDIANA',year].values)
        corn_iowa_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'IOWA',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'IOWA',year].values)
        corn_kansas_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'KANSAS',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'KANSAS',year].values)
        corn_michicgan_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'MICHIGAN',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'MICHIGAN',year].values)
        corn_minnesota_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'MINNESOTA',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'MINNESOTA',year].values)
        corn_missouri_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'MISSOURI',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'MISSOURI',year].values)
        corn_nebraska_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'NEBRASKA',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'NEBRASKA',year].values)
        corn_north_dakota_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'NORTH DAKOTA',year].values)
        corn_ohio_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'OHIO',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'OHIO',year].values)
        corn_south_dakota_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'SOUTH DAKOTA',year].values)
        corn_wisconsin_MFSP = sum(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'WISCONSIN',year].values)/len(df_geo_corn_MFSP.loc[df_geo_corn_MFSP['State'] == 'WISCONSIN',year].values)
        corn_MFSP = [corn_illinois_MFSP,corn_indiana_MFSP,corn_iowa_MFSP,corn_kansas_MFSP,corn_michicgan_MFSP,corn_minnesota_MFSP,corn_missouri_MFSP,corn_nebraska_MFSP,corn_north_dakota_MFSP,corn_ohio_MFSP,corn_south_dakota_MFSP,corn_wisconsin_MFSP] 
        corn_t_MFSP[i] = corn_MFSP
        df_corn_MFSP = corn_t_MFSP.T
        df_corn_MFSP = pd.DataFrame(df_corn_MFSP, columns = [*range(1998,2014)]) # list *
        df_corn_MFSP.insert(0,"state",state)

        
        
        
        #soy yield kg/ha

        soy_illinois_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'ILLINOIS',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'ILLINOIS',year].values)
        soy_indiana_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'INDIANA',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'INDIANA',year].values)
        soy_iowa_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'IOWA',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'IOWA',year].values)
        soy_kansas_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'KANSAS',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'KANSAS',year].values)
        soy_michicgan_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'MICHIGAN',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'MICHIGAN',year].values)
        soy_minnesota_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'MINNESOTA',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'MINNESOTA',year].values)
        soy_missouri_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'MISSOURI',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'MISSOURI',year].values)
        soy_nebraska_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'NEBRASKA',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'NEBRASKA',year].values)
        soy_north_dakota_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'NORTH DAKOTA',year].values)
        soy_ohio_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'OHIO',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'OHIO',year].values)
        soy_south_dakota_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'SOUTH DAKOTA',year].values)
        soy_wisconsin_MFSP = sum(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'WISCONSIN',year].values)/len(df_geo_soy_MFSP.loc[df_geo_soy_MFSP['State'] == 'WISCONSIN',year].values)
        soy_MFSP = [soy_illinois_MFSP,soy_indiana_MFSP,soy_iowa_MFSP,soy_kansas_MFSP,soy_michicgan_MFSP,soy_minnesota_MFSP,soy_missouri_MFSP,soy_nebraska_MFSP,soy_north_dakota_MFSP,soy_ohio_MFSP,soy_south_dakota_MFSP,soy_wisconsin_MFSP] 
        soy_t_MFSP[i] = soy_MFSP
        df_soy_MFSP = soy_t_MFSP.T
        df_soy_MFSP = pd.DataFrame(df_soy_MFSP, columns = [*range(1998,2014)]) # list *
        df_soy_MFSP.insert(0,"state",state)

        
        
        #grass AG yield kg/ha

        grass_AG_illinois_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'ILLINOIS',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'ILLINOIS',year].values)
        grass_AG_indiana_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'INDIANA',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'INDIANA',year].values)
        grass_AG_iowa_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'IOWA',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'IOWA',year].values)
        grass_AG_kansas_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'KANSAS',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'KANSAS',year].values)
        grass_AG_michicgan_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'MICHIGAN',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'MICHIGAN',year].values)
        grass_AG_minnesota_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'MINNESOTA',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'MINNESOTA',year].values)
        grass_AG_missouri_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'MISSOURI',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'MISSOURI',year].values)
        grass_AG_nebraska_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'NEBRASKA',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'NEBRASKA',year].values)
        grass_AG_north_dakota_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'NORTH DAKOTA',year].values)
        grass_AG_ohio_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'OHIO',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'OHIO',year].values)
        grass_AG_south_dakota_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'SOUTH DAKOTA',year].values)
        grass_AG_wisconsin_MFSP = sum(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'WISCONSIN',year].values)/len(df_geo_grass_AG_MFSP.loc[df_geo_grass_AG_MFSP['State'] == 'WISCONSIN',year].values)
        grass_AG_MFSP = [grass_AG_illinois_MFSP,grass_AG_indiana_MFSP,grass_AG_iowa_MFSP,grass_AG_kansas_MFSP,grass_AG_michicgan_MFSP,grass_AG_minnesota_MFSP,grass_AG_missouri_MFSP,grass_AG_nebraska_MFSP,grass_AG_north_dakota_MFSP,grass_AG_ohio_MFSP,grass_AG_south_dakota_MFSP,grass_AG_wisconsin_MFSP] 
        grass_AG_t_MFSP[i] = grass_AG_MFSP
        df_grass_AG_MFSP = grass_AG_t_MFSP.T
        df_grass_AG_MFSP = pd.DataFrame(df_grass_AG_MFSP, columns = [*range(1998,2014)]) # list *
        df_grass_AG_MFSP.insert(0,"state",state)

        
        #grass ML yield kg/ha

        grass_ML_illinois_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'ILLINOIS',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'ILLINOIS',year].values)
        grass_ML_indiana_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'INDIANA',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'INDIANA',year].values)
        grass_ML_iowa_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'IOWA',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'IOWA',year].values)
        grass_ML_kansas_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'KANSAS',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'KANSAS',year].values)
        grass_ML_michicgan_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'MICHIGAN',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'MICHIGAN',year].values)
        grass_ML_minnesota_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'MINNESOTA',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'MINNESOTA',year].values)
        grass_ML_missouri_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'MISSOURI',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'MISSOURI',year].values)
        grass_ML_nebraska_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'NEBRASKA',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'NEBRASKA',year].values)
        grass_ML_north_dakota_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'NORTH DAKOTA',year].values)
        grass_ML_ohio_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'OHIO',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'OHIO',year].values)
        grass_ML_south_dakota_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'SOUTH DAKOTA',year].values)
        grass_ML_wisconsin_MFSP = sum(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'WISCONSIN',year].values)/len(df_geo_grass_ML_MFSP.loc[df_geo_grass_ML_MFSP['State'] == 'WISCONSIN',year].values)
        grass_ML_MFSP = [grass_ML_illinois_MFSP,grass_ML_indiana_MFSP,grass_ML_iowa_MFSP,grass_ML_kansas_MFSP,grass_ML_michicgan_MFSP,grass_ML_minnesota_MFSP,grass_ML_missouri_MFSP,grass_ML_nebraska_MFSP,grass_ML_north_dakota_MFSP,grass_ML_ohio_MFSP,grass_ML_south_dakota_MFSP,grass_ML_wisconsin_MFSP] 
        grass_ML_t_MFSP[i] = grass_ML_MFSP
        df_grass_ML_MFSP = grass_ML_t_MFSP.T
        df_grass_ML_MFSP = pd.DataFrame(df_grass_ML_MFSP, columns = [*range(1998,2014)]) # list *
        df_grass_ML_MFSP.insert(0,"state",state)

        
        
        #algae AG kg/ha

        algae_AG_illinois_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'ILLINOIS',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'ILLINOIS',year].values)
        algae_AG_indiana_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'INDIANA',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'INDIANA',year].values)
        algae_AG_iowa_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'IOWA',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'IOWA',year].values)
        algae_AG_kansas_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'KANSAS',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'KANSAS',year].values)
        algae_AG_michicgan_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'MICHIGAN',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'MICHIGAN',year].values)
        algae_AG_minnesota_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'MINNESOTA',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'MINNESOTA',year].values)
        algae_AG_missouri_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'MISSOURI',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'MISSOURI',year].values)
        algae_AG_nebraska_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'NEBRASKA',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'NEBRASKA',year].values)
        algae_AG_north_dakota_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'NORTH DAKOTA',year].values)
        algae_AG_ohio_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'OHIO',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'OHIO',year].values)
        algae_AG_south_dakota_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'SOUTH DAKOTA',year].values)
        algae_AG_wisconsin_MFSP = sum(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'WISCONSIN',year].values)/len(df_geo_algae_AG_MFSP.loc[df_geo_algae_AG_MFSP['State'] == 'WISCONSIN',year].values)
        algae_AG_MFSP = [algae_AG_illinois_MFSP,algae_AG_indiana_MFSP,algae_AG_iowa_MFSP,algae_AG_kansas_MFSP,algae_AG_michicgan_MFSP,algae_AG_minnesota_MFSP,algae_AG_missouri_MFSP,algae_AG_nebraska_MFSP,algae_AG_north_dakota_MFSP,algae_AG_ohio_MFSP,algae_AG_south_dakota_MFSP,algae_AG_wisconsin_MFSP] 
        algae_AG_t_MFSP[i] = algae_AG_MFSP
        df_algae_AG_MFSP = algae_AG_t_MFSP.T
        df_algae_AG_MFSP = pd.DataFrame(df_algae_AG_MFSP, columns = [*range(1998,2014)]) # list *
        df_algae_AG_MFSP.insert(0,"state",state)

        
        
        
        #algae_ML yield kg/ha

        algae_ML_illinois_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'ILLINOIS',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'ILLINOIS',year].values)
        algae_ML_indiana_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'INDIANA',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'INDIANA',year].values)
        algae_ML_iowa_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'IOWA',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'IOWA',year].values)
        algae_ML_kansas_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'KANSAS',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'KANSAS',year].values)
        algae_ML_michicgan_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'MICHIGAN',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'MICHIGAN',year].values)
        algae_ML_minnesota_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'MINNESOTA',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'MINNESOTA',year].values)
        algae_ML_missouri_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'MISSOURI',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'MISSOURI',year].values)
        algae_ML_nebraska_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'NEBRASKA',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'NEBRASKA',year].values)
        algae_ML_north_dakota_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'NORTH DAKOTA',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'NORTH DAKOTA',year].values)
        algae_ML_ohio_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'OHIO',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'OHIO',year].values)
        algae_ML_south_dakota_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'SOUTH DAKOTA',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'SOUTH DAKOTA',year].values)
        algae_ML_wisconsin_MFSP = sum(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'WISCONSIN',year].values)/len(df_geo_algae_ML_MFSP.loc[df_geo_algae_ML_MFSP['State'] == 'WISCONSIN',year].values)
        algae_ML_MFSP = [algae_ML_illinois_MFSP,algae_ML_indiana_MFSP,algae_ML_iowa_MFSP,algae_ML_kansas_MFSP,algae_ML_michicgan_MFSP,algae_ML_minnesota_MFSP,algae_ML_missouri_MFSP,algae_ML_nebraska_MFSP,algae_ML_north_dakota_MFSP,algae_ML_ohio_MFSP,algae_ML_south_dakota_MFSP,algae_ML_wisconsin_MFSP] 
        algae_ML_t_MFSP[i] = algae_ML_MFSP
        df_algae_ML_MFSP = algae_ML_t_MFSP.T
        df_algae_ML_MFSP = pd.DataFrame(df_algae_ML_MFSP, columns = [*range(1998,2014)]) # list *
        df_algae_ML_MFSP.insert(0,"state",state)


df_corn_MFSP.to_excel('Corn_MFSP.xlsx')
df_soy_MFSP.to_excel('Soy_MFSP.xlsx')
df_grass_AG_MFSP.to_excel('Switchgrass_AG_MFSP.xlsx')
df_grass_ML_MFSP.to_excel('Switchgrass_ML_MFSP.xlsx')
df_algae_AG_MFSP.to_excel('Algae_AG_MFSP.xlsx')
df_algae_ML_MFSP.to_excel('Algae_ML_MFSP.xlsx')


