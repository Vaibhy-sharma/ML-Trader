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



def talib_AD(data_input,row):
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        _name=row["indname"]
        data_input[_name] = talib.AD(data_input['High'], data_input['Low'], data_input['Close'],data_input['Volume'])
        return data_input

def talib_ADOSC(data_input,row):
        _time=row["timeperiod"]
        _custom1=row["custom1"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] =  talib.ADOSC(data_input['High'], data_input['Low'], data_input['Close'],data_input['Volume'], fastperiod=_time, slowperiod=_custom1)
        return data_input

def talib_OBV(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] =  talib.OBV(data_input['Close'], data_input['Volume'])
        return data_input

def talib_TREND_VOLUME(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] =  data_input['Volume'] - talib.SMA(data_input['Volume'],timeperiod=_time)
        return data_input


def talib_TREND_VOLUME_MA(data_input,row):
        _time=row["timeperiod"]
        _time2=row["custom1"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] =  talib.SMA(data_input['Volume'],timeperiod=_time2) - talib.SMA(data_input['Volume'],timeperiod=_time)
        return data_input
