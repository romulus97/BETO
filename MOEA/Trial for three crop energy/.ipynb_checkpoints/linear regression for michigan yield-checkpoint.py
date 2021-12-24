# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 11:18:41 2021

@author: Ece Ari Akdemir
"""

# import pandas as pd
# import numpy as np
# from sklearn.linear_model import LinearRegression

# df_grass = pd.read_excel('combined_pivot_grass_excel_electricity_denenenen.xlsx',header=0, engine='openpyxl') #contains every eg_district code  

# df_WI = df_grass.loc[98:107,1996:2004]
# df_MI = df_grass.loc[36:44,1996:2004]

# df_WI1 = df_grass.loc[98:98,1996:2004]
# df_MI1 = df_grass.loc[36:36,1996:2004]

# df_WI2 = df_grass.loc[98:98,2005:2013]

# X = np.array(df_WI1)
# y = np.array(df_MI1)
# X = X.reshape(1, -1)
# y = y.reshape(1, -1)

# model = LinearRegression()
# model.fit(X, y)

# X_predict = np.array(df_WI2)  # put the dates of which you want to predict kwh here
# y_predict = model.predict(X_predict)

import pandas as pd
import numpy as np
from sklearn import linear_model

df_grass = pd.read_excel('combined_pivot_grass_excel_electricity_denenenen.xlsx',header=0, engine='openpyxl') #contains every eg_district code  

df_WI = df_grass.loc[98:107,1996:2004]
df_MI = df_grass.loc[36:44,1996:2004]

df_WI1 = df_grass.loc[98:98,1996:2004]
df_MI1 = df_grass.loc[36:36,1996:2004]

df_WI2 = df_grass.loc[98:98,2005:2005]

X = np.array(df_WI1)
y = np.array(df_MI1)
X = X.reshape(-1, 1)
y = y.reshape(-1, 1)

lm = linear_model.LinearRegression()
model = lm.fit(X, y)

X_predict = np.array(df_WI2)  # put the dates of which you want to predict kwh here
predictions = lm.predict(X_predict)

print(predictions[0:9])








