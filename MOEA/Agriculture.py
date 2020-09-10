# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 12:08:48 2020

@author: mzeigha
"""


def LDS(arable_land):
    
    seeded_land = arable_land
    
    return seeded_land

#########################################

def Irr(bu_per_acre):
    
    
    h2o_per_acre = ((1/17.4)*bu_per_acre)+8.2221
    
    return h2o_per_acre

#########################################
    
def Frt(fert_per_ha, arable_land):
    
    fertilization_per_ha = fert_per_ha * arable_land

    return (fertilization_per_ha)

##########################################
    
def Stover (kg_stover_per_ha, arable_land):
    
    kg_available_corn_stover_per_ha = kg_stover_per_ha * arable_land *0.5

    return (kg_available_corn_stover_per_ha)

##########################################
    
def TRK (kg_stover_per_ha, Truck_Capasity):
    
    num_of_Trucks = kg_stover_per_ha / (Truck_Capasity * 1000)

    return (num_of_Trucks)