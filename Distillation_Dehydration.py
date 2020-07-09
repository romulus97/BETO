# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 03:32:16 2020

@author: mzeigha
"""


def DAD (ethanol_per_kWh , kWh_to_MJ ,kg_ethanol_per_ha ,kg_ethanol_to_L_ethanol 
         , MJ_per_ethanol , kg_Stover_PostDAH_per_ha):
    
    Electricity_per_ha = (1 / ethanol_per_kWh) * kWh_to_MJ * kg_ethanol_per_ha * kg_ethanol_to_L_ethanol
    Heat_per_ha = MJ_per_ethanol * kg_ethanol_per_ha * kg_ethanol_to_L_ethanol
    kg_lignin_per_ha = 0.18 * kg_Stover_PostDAH_per_ha
    
    return ( Electricity_per_ha , Heat_per_ha , kg_lignin_per_ha )