# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 03:49:52 2020

@author: mzeigha
"""


def FP ( kg_ethanol_per_ha , kg_ethanol_to_L_ethanol , gal_to_L , kg_stover_per_ha , kg_to_ton , ton_to_bu ):
    
    L_ethanol_per_ha = kg_ethanol_per_ha * kg_ethanol_to_L_ethanol
    gal_ethanol_per_ton_stover = ( L_ethanol_per_ha / gal_to_L ) / (kg_stover_per_ha * kg_to_ton )
    gal_ethanol_per_bu_corn_grain = gal_ethanol_per_ton_stover / ton_to_bu 
    
    return (L_ethanol_per_ha , gal_ethanol_per_ton_stover , gal_ethanol_per_bu_corn_grain)