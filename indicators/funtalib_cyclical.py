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


def talib_HT_DCPERIOD(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.HT_DCPERIOD(data_input['Close'].values)
        return data_input

def talib_HT_DCPHASE(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.HT_DCPHASE(data_input['Close'].values)
        return data_input

def talib_HT_PHASOR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        HT_PHASOR = talib.HT_PHASOR(data_input['Close'].values)
        data_input['INPHASE'] = HT_PHASOR[0]
        data_input['QUADRATURE'] = HT_PHASOR[1]
        return data_input

def talib_SINE(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        HT_SINE = talib.HT_SINE(data_input['Close'].values)
        data_input['SINE'] = HT_SINE[0]
        return data_input

def talib_LEADSINE(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        HT_SINE = talib.HT_SINE(data_input['Close'].values)
        data_input['LEADSINE'] = HT_SINE[1]
        return data_input

def talib_HT_TRENDMODE(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.HT_TRENDMODE(data_input['Close'].values)
        return data_input
