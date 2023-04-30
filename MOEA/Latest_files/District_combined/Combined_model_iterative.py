# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 19:38:07 2023

@author: kakdemi
"""

import csv
import pandas as pd
import numpy as np
from pyomo.environ import *
from pyomo.environ import value

from pyomo.opt import SolverFactory
from pyomo.core import Var
from pyomo.core import Constraint
from pyomo.core import Param
from operator import itemgetter
import pandas as pd
import numpy as np
from datetime import datetime
import pyomo.environ as pyo
from pyomo.opt import SolverStatus, TerminationCondition

all_fuel_cost_weights = np.arange(0,1.001,0.001)
all_GHG_cost_weights = np.arange(0,1.001,0.001)
all_GHG_cost_weights[::-1].sort()
weight_length = len(all_GHG_cost_weights)
biofuel_list = [3,6,9,12,15,18,20]

for bio_amount in biofuel_list:
    
    quota_change = bio_amount*0.02
    upper_bound = bio_amount + quota_change
    lower_bound = bio_amount - quota_change
    actual_quota_list = np.arange(lower_bound,upper_bound+0.01,0.01)
    
    for my_quota in actual_quota_list:
    
        ### DATA SETUP PART ###
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

            f.write(f'param quota:= {my_quota} \n')
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
                    
                    k = int(np.floor(j/107))
                    
                    f.write(feedstocks[k] + ' ' + str(combined_MFSP.loc[j,'STASD_N']) + ' ' + str(i) + ' ' + str(sample.loc[j]) + ' ' + str(sample2.loc[j]) + ' ' + str(sample3.loc[j])+'\n') 
                    
            f.write(';\n\n')  
                
                
            f.write('param: AG_limit Grass_ML_limit Algae_ML_limit :=\n')
              
            for i in range(0,len(df_limits)):
                
                sample = df_limits.loc[i,'AG']
                sample2 = df_limits.loc[i,'ML_grass']
                sample3 = df_limits.loc[i,'ML_algae']
                
                f.write(str(df_limits.loc[i,'STASD_N']) + ' ' + str(sample) + ' ' + str(sample2) + ' ' + str(sample3)+'\n') 
                    
            f.write(';\n\n')  

        for we_idx in range(0,weight_length):
            
            cost_weight = all_fuel_cost_weights[we_idx]
            GHG_weight = all_GHG_cost_weights[we_idx]
            
            ### biofuel_LP PART ###
            
            def Biofuel_model():
                
                model = AbstractModel()

                ######=================================================########
                ######               Segment B.1                       ########
                ######=================================================########

                ### Fuel production by feedstock
                model.Feedstock = Set() 
                model.Feedstock_AG = Set()
                # model.Fuel_ML = model.Algae_ML | model.Grass_ML

                #District
                model.district = Set()

                #Year
                model.year = RangeSet(1998,2013)
                model.quota = Param(within=NonNegativeReals)

                #Minimum fuel selling price
                model.mfsp = Param(model.Feedstock,model.district,model.year,within=Any)

                #Greenhouse gas emissions
                model.ghg = Param(model.Feedstock,model.district,model.year,within=Any)

                #Ag Land limits
                model.AG_limit = Param(model.district)

                #Marginal Land limits
                model.Algae_ML_limit = Param(model.district)

                #Marginal Land limits
                model.Grass_ML_limit = Param(model.district)

                #Yields
                model.F_yield = Param(model.Feedstock,model.district,model.year)

                #Fuel conversion
                model.fuel_conversion = Param(model.Feedstock)


                ######=======================Decision variables======================########

                model.land_usage = Var(model.Feedstock,model.district, within=NonNegativeReals,initialize=0)


                ######================Objective function=============########

                def SysCost(model):
                    fuel_cost = cost_weight*sum(model.land_usage[f,d]*model.F_yield[f,d,y]*model.fuel_conversion[f]*model.mfsp[f,d,y] for d in model.district for f in model.Feedstock for y in model.year)
                    ghg_emissions = GHG_weight*sum(model.land_usage[f,d]*model.F_yield[f,d,y]*model.fuel_conversion[f]*model.ghg[f,d,y] for d in model.district for f in model.Feedstock for y in model.year)
                   
                    return fuel_cost + ghg_emissions

                model.SystemCost = Objective(rule=SysCost, sense=minimize)


                #####========== Logical Constraint =========#############

                #Land Limits
                def Land_limits(model,d):
                    
                    return model.land_usage['algae_ML',d] <= model.Algae_ML_limit[d]

                model.LandLimit1 = Constraint(model.district,rule=Land_limits)



                #Land Limits
                def Land_limits2(model,d):
                    
                    return model.land_usage['grass_ML',d] + model.land_usage['algae_ML',d] <= model.Grass_ML_limit[d]

                model.LandLimit2 = Constraint(model.district,rule=Land_limits2)



                #Land Limits
                def Land_limits3(model,f,d):
                    
                    return sum(model.land_usage[f,d] for f in model.Feedstock_AG) <= model.AG_limit[d]

                model.LandLimit3 = Constraint(model.Feedstock_AG,model.district,rule=Land_limits3)


                #Rotation
                def Rotation(model,d):
                    
                    return model.land_usage['corn',d] == model.land_usage['soy',d] 

                model.Rotation1 = Constraint(model.district,rule=Rotation)


                #Quota
                def Quota(model):
                    
                    fuel = sum(model.land_usage[f,d]*model.F_yield[f,d,y]*model.fuel_conversion[f] for d in model.district for f in model.Feedstock for y in model.year)

                    return fuel >= model.quota*1000000000*30.81 * (1/0.2641) *16

                model.Quota1 = Constraint(rule=Quota)
                
                return model
            
            
            ### wrapper PART ### 
            m1 = Biofuel_model()
            
            instance = m1.create_instance('biofuels_data.dat')
            instance.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)

            Solvername = 'cplex'

            opt = SolverFactory(Solvername)
                
            result = opt.solve(instance,tee=True,symbolic_solver_labels=True, load_solutions=False) ##,tee=True to check number of variables\n",
            
            #Checking the solver status and if solution is feasible or not
            if (result.solver.status == SolverStatus.ok) and (result.solver.termination_condition == TerminationCondition.optimal):
                print('Solution is feasible') 
                solver_idx = 'feasible'
            elif (result.solver.termination_condition == TerminationCondition.infeasible):
                print('Solution is INFEASIBLE!') 
                solver_idx = 'INFEASIBLE'
            else:
                print(f'Something else is not right, solver status is {result.solver.status}')
                solver_idx = 'other_problem'
                
            instance.solutions.load_from(result)  
            
            obj_val = instance.SystemCost()
            print(obj_val)

            land_usage = []
                
            for v in instance.component_objects(Var, active=True):
                varobject = getattr(instance, str(v))
                a=str(v)
                          
                if a=='land_usage':
                    for index in varobject:
                        land_usage.append((index[0],index[1],varobject[index].value))
                                
                 
            land_usage=pd.DataFrame(land_usage,columns=('Feedstock','District','Value'))
            land_usage.to_csv(f'Results/Land_usage/land_usage_out_district_level_{my_quota}_cost_{round(cost_weight,3)}_GHG_{round(GHG_weight,3)}_{solver_idx}.csv',index=None)
                
            
            
            
    
    
    
        


