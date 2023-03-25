# coding: utf-8
from pyomo.environ import *
from pyomo.environ import value
import numpy as np

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
model.quota = Param(within=PositiveIntegers)

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
    fuel_cost = 0*sum(model.land_usage[f,d]*model.F_yield[f,d,y]*model.fuel_conversion[f]*model.mfsp[f,d,y] for d in model.district for f in model.Feedstock for y in model.year)
    ghg_emissions = 1*sum(model.land_usage[f,d]*model.F_yield[f,d,y]*model.fuel_conversion[f]*model.ghg[f,d,y] for d in model.district for f in model.Feedstock for y in model.year)
   
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