#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 12:21:25 2020

@author: seanmurphy
"""

from rhodium import *

import math
import numpy as np
import pandas as pd
import math
import bisect
import numbers
import operator
import functools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

nruns = 1000

region = '4007'
pathresults = './Results'
pathdata = './Data'

savename = pathresults + '/results_' + region + '.csv'
datainput = pd.read_csv(pathdata + '/isone' + region + '_2019.csv')

# supporting functions

def gauss2d(A, B, gauss, n):    
    sg = 0
    for i in range(n):
        a = gauss[i*4]
        bA = gauss[i*4 + 1]
        bB = gauss[i*4 + 2]
        c = gauss[i*4 + 3]
        dist = (A - bA)**2 + (B - bB)**2
        denom = 2 * c ** 2
        g = a * np.exp(-1 * dist/ denom)
        sg = sg + g
    return sg

class Battery:

    def __init__(self, effin, effout, maxcharge1hr, capacityMWh, soc, cycles, profit):
        
        self.effin = effin
        self.effout = effout
        self.maxcharge1hr = maxcharge1hr
        self.capacityMWh = capacityMWh
        self.soc = soc
        self.cycles = cycles
        self.profit = profit
        
    def charge(self, amt, price):
        
        # constrain amt to [-1, 1]
        
        if amt > 1:
            amt = 1
        elif amt < -1:
            amt = -1    
        
        # set to range of max charges for 
        amt = amt * self.maxcharge1hr
        
        # narrow to capacity
        if amt > (1 - self.soc):
            amt = 1 - self.soc
        elif amt < -self.soc:
            amt = -self.soc
            
        # actually charge
        self.soc = self.soc + amt
        self.cycles = self.cycles + abs(amt)
        
        # calculate profit to operator; negative profit if positive charge
        # including efficiency!
        
        if amt > 0:
            
            profit = price * amt * self.capacityMWh * -1 / self.effin
            
        elif amt < 0:
            
            profit = price * amt * self.capacityMWh * -1 * self.effout
            
        else:
            
            profit = 0
        
        self.profit = self.profit + profit
    
    def printsoc(self):
        print(self.soc)
        
    def getcycles(self):
        return(self.cycles)
    
    def getprofit(self):
        return(self.profit)

def runopt(data):
    
    rbf = genrbf() #rhodium or platypus
    
    (p, cycles) = evaluate(rbf, data)
    
    return ()
    
    
    return(p, cycles)

def charge(state, rbf, storage):
    # takes in current state (price, forecasted price, )
    
    c_unc = evalrbf(rbfvec, rbftype, ncenters, ndim, state)
    
    c = rbfconstr(c_unc, storage)
    
    cyclesi = abs(c)
    
    pi = -price * c
    
    storage = storage + c
    
    return (pi, cyclesi, storage)

# simulate function
    
def simulate(avec,
             cvec,
             bAvec,
             bBvec,
             data = datainput):
    # simulate is a function that takes in variables manipulated by MOEA and the data df and returns
    # revenue ($) and cycles
    l = len(data.index)
    b = Battery(.9, .9, .25, 10, .5, 0, 0)
    n = len(avec)
    gauss = np.zeros(n * 4)
    for i in range(len(avec)):
        gauss[i*4] = avec[i]
        gauss[i*4 + 1] = bAvec[i]
        gauss[i*4 + 2] = bBvec[i]
        gauss[i*4 + 3] = cvec[i]
    # decide on charge values 
    # isnan replace
    avec = np.nan_to_num(data.A)
    bvec = np.nan_to_num(data.B)
    # amtvec evaluate 
    amt = gauss2d(avec, bvec, gauss, n)
    # in for loop, just run through charge
    for i in range(l):
        b.charge(amt[i], data.LmpTotal[i])
    cycles = b.getcycles()
    profit = b.getprofit()
    return cycles, profit


# Rhodium
    
model = Model(simulate)
# model.parameters - the parameters of interest.
model.parameters = [Parameter("avec"),
                   Parameter("cvec"),
                   Parameter("bAvec"),
                   Parameter("bBvec"),
                   Parameter("data")]
# model.responses - the model responses or outputs.
model.responses = [Response("cycles", Response.MINIMIZE),
                  Response("profit", Response.MAXIMIZE)]
# model.constraints - any hard constraints that must be satisfied.
model.constraints = [Constraint("cycles >= 26"),
                    Constraint("cycles <= 730")]
# model.levers - parameters that we have direct control over.
model.levers = [RealLever("avec", -5, 5, length = 3),
               RealLever("cvec", 0.001, 5, length = 3),
               RealLever("bAvec", 0, 1, length = 3),
               RealLever("bBvec", 0, 1, length = 3)]

out = optimize(model, "NSGAII", nruns)

out.save(savename)

df7 = pd.read_csv(savename)
df7 = df7.sort_values(by = ['cycles']).reset_index()

plt.plot(df7.cycles, df7.profit, c='b')

plt.xlabel('cycles')
plt.ylabel('profit')
plt.title('Optimized Profit (max) vs. Cycles (min) in Western/Central MA')

