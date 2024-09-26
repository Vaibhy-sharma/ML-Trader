import os
import numpy as np
import talib
import pandas as pd
import math
import seaborn as sns
import datetime as dt


def talib_BETA(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.BETA(data_input['High'].values,data_input['Low'].values,timeperiod=_time)

        return data_input


def talib_CORREL(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.CORREL(data_input['High'].values,data_input['Low'].values,timeperiod=_time)

        return data_input


def talib_LINEARREGDIFF(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['LINEARREG'] = talib.LINEARREG(data_input['Close'].values,timeperiod=_time)
        data_input[_name] = data_input['Close'] - data_input['LINEARREG']
        data_input = data_input.drop(['LINEARREG'], axis=1)


        return data_input

def talib_LINEARREGINTDIFF(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['LINEARREG_INTERCEPT'] = talib.LINEARREG_INTERCEPT(data_input['Close'].values,timeperiod=_time)
        data_input[_name] = data_input['Close'] - data_input['LINEARREG_INTERCEPT']
        data_input = data_input.drop(['LINEARREG_INTERCEPT'], axis=1)


        return data_input

def talib_TSFDIFF(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['TSF'] = talib.TSF(data_input['Close'].values,timeperiod=_time)
        data_input[_name] = data_input['Close'] - data_input['TSF']
        data_input = data_input.drop(['TSF'], axis=1)


        return data_input

def talib_LINEARREG_ANGLE(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.LINEARREG_ANGLE(data_input['Close'].values,timeperiod=_time)

        return data_input

def talib_LINEARREG_SLOPE(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.LINEARREG_SLOPE(data_input['Close'].values,timeperiod=_time)

        return data_input 

def talib_VAR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.VAR(data_input['Close'].values,timeperiod=_time)

        return data_input

def talib_STDDEV(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.STDDEV(data_input['Close'].values,timeperiod=_time)

        return data_input




