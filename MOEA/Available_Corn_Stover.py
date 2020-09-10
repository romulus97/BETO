"""
Created on Tue Jul  7 13:12:23 2020

@author: mzeigha
"""


def Stover (kg_stover_per_ha, arable_land):
    
    kg_available_corn_stover_per_ha = kg_stover_per_ha * arable_land *0.5

    return (kg_available_corn_stover_per_ha)