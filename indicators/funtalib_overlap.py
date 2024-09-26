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


def talib_trendIF(data_input,row):
        print(" INPUT columns")
        print(data_input.columns.values)
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['HT_TRENDLINE'] = talib.HT_TRENDLINE(data_input['Close'].values)
        data_input[_name] = data_input['Close'] - data_input['HT_TRENDLINE']
        data_input = data_input.drop(['HT_TRENDLINE'],axis=1)
        print(" RETURN columns")
        print(data_input.columns.values)
        return data_input

def talib_trendSMA(data_input,row):
        _name=row["indname"]
        _time=row["timeperiod"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = ((data_input['Close'] - talib.SMA(data_input['Close'],timeperiod=_time))/data_input['Close'])*100
        return data_input


def talib_trendEMA(data_input,row):
        _name=row["indname"]
        _time=row["timeperiod"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = ((data_input['Close'] - talib.EMA(data_input['Close'],timeperiod=_time))/data_input['Close'])*100
        return data_input

def talib_trendDEMA(data_input,row):
        _name=row["indname"]
        _time=row["timeperiod"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = ((data_input['Close'] - talib.DEMA(data_input['Close'],timeperiod=_time))/data_input['Close'])*100
        return data_input

def talib_trendKAMA(data_input,row):
        _name=row["indname"]
        _time=row["timeperiod"]
        print(" Indicator Arguments")
        print(row)
        print(data_input.columns.values)
        print("\n")
        data_input[_name] = ((data_input['Close'] - talib.KAMA(data_input['Close'],timeperiod=_time))/data_input['Close'])*100
        return data_input

def talib_trendMAMA(data_input,row):
        _name=row["indname"]
        _time=row["timeperiod"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = ((data_input['Close'] - talib.MAMA(data_input['Close'], fastlimit=0, slowlimit=0))/data_input['Close'])*100
        return data_input

def talib_trendMIDPOINT(data_input,row):
        _name=row["indname"]
        _time=row["timeperiod"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = data_input['Close'] - talib.MIDPOINT(data_input['Close'],timeperiod=_time)
        return data_input

def talib_trendMIDPRICE(data_input,row):
        _name=row["indname"]
        _time=row["timeperiod"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = data_input['Close'] - talib.MIDPRICE(data_input['High'],data_input['Low'],timeperiod=_time)
        return data_input

def talib_BBANDS(data_input,row):
        print(" INPUT columns")
        print(data_input.columns.values)
        _time=row["timeperiod"]
        _name=row["indname"]
        _stdev=row["custom1"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        bbands = talib.BBANDS(data_input['Close'], timeperiod=_time, nbdevup=_stdev, nbdevdn=_stdev, matype=0)
        data_input['upperband'] = bbands[0]
        data_input['middleband'] = bbands[1]
        data_input['lowerband'] = bbands[2]
        data_input['updif_'+_name] =  data_input['upperband'] - data_input['Close']
        data_input['middif_'+_name] = data_input['Close'] - data_input['middleband']
        data_input['lowdif_'+_name] = data_input['Close'] - data_input['lowerband']
        data_input = data_input.drop(['upperband'],axis=1)
        data_input = data_input.drop(['middleband'],axis=1)
        data_input = data_input.drop(['lowerband'],axis=1)
        print(" RETURN columns")
        print(data_input.columns.values)
        return data_input


