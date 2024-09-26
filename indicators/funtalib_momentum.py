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


def talib_ADX(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.ADX(data_input['High'], data_input['Low'], data_input['Close'],timeperiod=_time)
        return data_input

def talib_ADXR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.ADXR(data_input['High'], data_input['Low'], data_input['Close'],timeperiod=_time)
        return data_input

def talib_ADXPLUS(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['tmp1'] = talib.ADX(data_input['High'], data_input['Low'], data_input['Close'],timeperiod=_time)
        data_input['tmp2'] = talib.PLUS_DM(data_input['High'], data_input['Low'], timeperiod=_time)
        data_input['tmp3'] = data_input['tmp1'] + data_input['tmp2']
        data_input[_name] = 100 - data_input['tmp3']

        data_input = data_input.drop(['tmp1','tmp2','tmp3'], axis=1)

        return data_input

def talib_ADXMINUS(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['tmp1'] = talib.ADX(data_input['High'], data_input['Low'], data_input['Close'],timeperiod=_time)
        data_input['tmp2'] = talib.MINUS_DM(data_input['High'], data_input['Low'], timeperiod=_time)
        data_input['tmp3'] = data_input['tmp1'] + data_input['tmp2']
        data_input[_name] = 100 - data_input['tmp3']
        
        data_input = data_input.drop(['tmp1','tmp2','tmp3'], axis=1)

        return data_input

def talib_APO(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.APO(data_input['Close'], fastperiod=12, slowperiod=26, matype=0)
        return data_input

def talib_AROONOSC(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.AROONOSC(data_input['High'],data_input['Low'], timeperiod=_time)
        return data_input

def talib_BOP(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.BOP(data_input['Open'],data_input['High'],data_input['Low'],data_input['Close'])
        return data_input

def talib_CCI(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.CCI(data_input['High'],data_input['Low'],data_input['Close'], timeperiod=_time)
        return data_input

def talib_CMO(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.CMO(data_input['Close'], timeperiod=_time)
        return data_input

def talib_DX(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.DX(data_input['High'], data_input['Low'], data_input['Close'], timeperiod=_time)
        return data_input

def talib_MACD(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        _time2=row["custom1"]
        _time3=row["custom2"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        macd = talib.MACD(data_input['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        #macd = talib.MACD(data_input['Close'], fastperiod=_time, slowperiod=_time2, signalperiod=_time3)
        data_input[_name] = macd[0]
        return data_input

def talib_MACDSIGNAL(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        macd = talib.MACD(data_input['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        data_input[_name] = macd[1]
        return data_input

def talib_MACDHIST(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        macd = talib.MACD(data_input['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
        data_input[_name] = macd[2]
        return data_input

def talib_PLUS_DI(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.PLUS_DI(data_input['High'], data_input['Low'], data_input['Close'], timeperiod=_time)
        return data_input

def talib_MINUS_DI(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.MINUS_DI(data_input['High'], data_input['Low'], data_input['Close'], timeperiod=_time)
        return data_input

def talib_PLUS_DM(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.PLUS_DM(data_input['High'], data_input['Low'], timeperiod=_time)
        return data_input

def talib_MINUS_DM(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.MINUS_DM(data_input['High'], data_input['Low'],timeperiod=_time)
        return data_input

def talib_MOM(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.MOM(data_input['Close'],timeperiod=_time)
        return data_input

def talib_PPO(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.PPO(data_input['Close'].values, fastperiod=12, slowperiod=26, matype=0)
        return data_input

def talib_ROC(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.ROC(data_input['Close'],timeperiod=_time)
        return data_input

def talib_ROCR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.ROCR(data_input['Close'],timeperiod=_time)
        return data_input

def talib_RSI(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.RSI(data_input['Close'],timeperiod=_time)
        data_input[_name+'_'+str(40)] = data_input[_name] - 40
        data_input[_name+'_'+str(60)] = 60 - data_input[_name]
        data_input = data_input.drop([_name], axis=1) 
        return data_input

def talib_STOCH(data_input,row):
        fastk_period=row["timeperiod"]
        slowk_period=row["custom1"]
        slowk_matype=0
        slowd_period=row["custom2"]
        slowd_matype=0
        print(" Indicator Arguments")
        print(row)
        print("\n")
        stoch_slow = talib.STOCH(data_input['High'].values, data_input['Low'].values, data_input['Close'].values, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype)
        data_input['STOCH_'+str(fastk_period)+'_k'] = stoch_slow[0]
        data_input['STOCH_'+str(fastk_period)+'_d'] = stoch_slow[1]
        return data_input

def talib_STOCHDIFF(data_input,row):
        fastk_period1=14
        slowk_period1=3
        slowk_matype=0
        slowd_period1=3
        slowd_matype=0
        fastk_period2=70
        slowk_period2=15
        slowd_period2=15
        print(" Indicator Arguments")
        print(row)
        print("\n")
        stoch_slow1 = talib.STOCH(data_input['High'].values, data_input['Low'].values, data_input['Close'].values, fastk_period1, slowk_period1, slowk_matype, slowd_period1, slowd_matype)
        stoch_slow2 = talib.STOCH(data_input['High'].values, data_input['Low'].values, data_input['Close'].values, fastk_period2, slowk_period2, slowk_matype, slowd_period2, slowd_matype)
        data_input['stock_k1'] = stoch_slow1[0]
        data_input['stock_d1'] = stoch_slow1[1]
        data_input['stock_k2'] = stoch_slow2[0]
        data_input['stock_d2'] = stoch_slow2[1]
        data_input['STOCH_360'] = 360 -(data_input['stock_k1']  + data_input['stock_d1'] + data_input['stock_k2'] + data_input['stock_d2'])
        data_input['STOCH_70'] =  (data_input['stock_k1'] + data_input['stock_d1'] + data_input['stock_k2'] + data_input['stock_d2']) - 70 
        
        data_input = data_input.drop(['stock_k1','stock_d1','stock_k2','stock_d2'], axis=1) 
        return data_input


def talib_STOCHRSI(data_input,row):
        fastk_period=row["timeperiod"]
        slowk_period=row["custom1"]
        slowk_matype=0
        slowd_period=row["custom2"]
        slowd_matype=0
        print(" Indicator Arguments")
        print(row)
        print("\n")
        stochrsi = talib.STOCHRSI(data_input['Close'], timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        data_input['RSI_FAST_k'] = stochrsi[0]
        data_input['RSI_FAST_d'] = stochrsi[1]
        return data_input

def talib_TRIX(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.TRIX(data_input['Close'],timeperiod=_time)
        return data_input

def talib_ULTOSC(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        _time2=row["custom1"]
        _time3=row["custom2"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.ULTOSC(data_input['High'], data_input['Low'], data_input['Close'],timeperiod1=_time, timeperiod2=_time2, timeperiod3=_time3)
        return data_input

def talib_WILLR(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input[_name] = talib.WILLR(data_input['High'], data_input['Low'], data_input['Close'],timeperiod=_time)
        return data_input
