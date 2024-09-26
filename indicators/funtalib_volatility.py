import os
import numpy as np
import talib
import pandas as pd
import math
import seaborn as sns
import datetime as dt
sns.despine()
from pyti.williams_percent_r import williams_percent_r
from pyti.relative_strength_index import relative_strength_index



def talib_TRANGE(data_input,row):
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        _name=row["indname"]
        data_input[_name] = talib.TRANGE(data_input['High'].values, data_input['Low'].values, data_input['Close'].values)
        return data_input

def talib_ATR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.ATR(data_input['High'].values, data_input['Low'].values, data_input['Close'].values,_time)
        return data_input

def talib_NATR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.NATR(data_input['High'].values, data_input['Low'].values, data_input['Close'].values,_time)
        return data_input

def VelocityATR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['ATR'] = talib.ATR(data_input['High'].values, data_input['Low'].values, data_input['Close'].values,14)
        data_input[_name] = (data_input['ATR'].shift(_time) - data_input['ATR'])/_time

        data_input = data_input.drop(['ATR'],axis=1)
    
        return data_input