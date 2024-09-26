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

def panda_skewness(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        #print("rolling skewness for period:",_time)
        closep = data_input.ix[:, 'Close'].astype(float).tolist()
        data_input[_name] = pd.DataFrame(closep).rolling(_time).skew().values 
        return data_input

def panda_kurtosis(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        #print("rolling skewness for period:",_time)
        closep = data_input.ix[:, 'Close'].astype(float).tolist()
        data_input[_name] = pd.DataFrame(closep).rolling(_time).kurt().values
        return data_input

def slope(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        #print("rolling skewness for period:",_time)
        data_input[_name] = (data_input['Close'].shift(_time) - data_input['Close'])/_time
        return data_input

def slope_trend(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['HT_TRENDLINE'] = talib.HT_TRENDLINE(data_input['Close'].values)
        data_input[_name] = (data_input['HT_TRENDLINE'].shift(_time) - data_input['HT_TRENDLINE'])/_time
        data_input = data_input.drop(['HT_TRENDLINE'],axis=1)
        
        return data_input

def slope_roc(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        #print("rolling skewness for period:",_time)
        data_input['slope_tmp'] = (data_input['Close'].shift(_time) - data_input['Close'])/_time
        data_input[_name] = (data_input['slope_tmp'].shift(_time) - data_input['slope_tmp'])/_time
        data_input = data_input.drop(['slope_tmp'],axis=1)
        return data_input

def slope_roc_trend(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['HT_TRENDLINE'] = talib.HT_TRENDLINE(data_input['Close'].values)
        data_input['slope_tmp'] = (data_input['HT_TRENDLINE'].shift(_time) - data_input['HT_TRENDLINE'])/_time
        data_input[_name] = (data_input['slope_tmp'].shift(_time) - data_input['slope_tmp'])/_time
        data_input = data_input.drop(['HT_TRENDLINE','slope_tmp'],axis=1)
        
        return data_input

def slope_diff(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['HT_TRENDLINE'] = talib.HT_TRENDLINE(data_input['Close'].values)
        data_input['slope_tmp1'] = (data_input['HT_TRENDLINE'].shift(_time) - data_input['HT_TRENDLINE'])/_time
        data_input['slope_tmp2'] = (data_input['Close'].shift(_time) - data_input['Close'])/_time
        data_input['slope_tmp1_roc'] = (data_input['slope_tmp1'].shift(_time) - data_input['slope_tmp1'])/_time
        data_input['slope_tmp2_roc'] = (data_input['slope_tmp2'].shift(_time) - data_input['slope_tmp2'])/_time
        data_input['slope_diff'+str(_time)] = data_input['slope_tmp2'] - data_input['slope_tmp1']
        data_input['slope_diff_roc'+str(_time)] = data_input['slope_tmp2_roc'] - data_input['slope_tmp1_roc']

        data_input = data_input.drop(['HT_TRENDLINE','slope_tmp1','slope_tmp2','slope_tmp1_roc','slope_tmp2_roc'],axis=1)

        return data_input


def std(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        #print("rolling skewness for period:",_time)
        closep = data_input.ix[:, 'Close'].astype(float).tolist()
        data_input[_name] = pd.DataFrame(closep).rolling(_time).std().values
        return data_input

def stdratio(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        highp =  data_input.ix[:, 'High'].astype(float).tolist()
        lowp = data_input.ix[:, 'Low'].astype(float).tolist()
        data_input['std_high'] = pd.DataFrame(highp).rolling(_time).std().values
        data_input['std_low']  = pd.DataFrame(lowp).rolling(_time).std().values
        data_input[_name] = data_input['std_high']/data_input['std_low']
        data_input = data_input.drop(['std_high','std_low'], axis=1)
        return data_input

def stdhighlow(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        highp =  data_input.ix[:, 'High'].astype(float).tolist()
        lowp = data_input.ix[:, 'Low'].astype(float).tolist()
        data_input['std_high'+str(_time)] = pd.DataFrame(highp).rolling(_time).std().values
        data_input['std_low'+str(_time)]  = pd.DataFrame(lowp).rolling(_time).std().values

        return data_input

def UPD(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['Kch_upper'] = talib.EMA(data_input['Close'],timeperiod=_time)+2.1*(talib.ATR(data_input['High'],data_input['Low'], data_input['Close'], timeperiod=_time))
        data_input[_name] = (data_input['Kch_upper'] - data_input['Close'])
        data_input = data_input.drop(['Kch_upper'], axis=1)
        print(" output columns")
        print(data_input.columns.values)
        return data_input

def LPD(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        data_input['Kch_lower'] = talib.EMA(data_input['Close'],timeperiod=_time)-2.1*(talib.ATR(data_input['High'],data_input['Low'], data_input['Close'], timeperiod=_time))
        data_input[_name] = (data_input['Close'] - data_input['Kch_lower'])
        data_input = data_input.drop(['Kch_lower'], axis=1)
        print(" output columns")
        print(data_input.columns.values)
        return data_input

def DIST_FROM_HIGH(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        highp = data_input.ix[:, 'High'].astype(float).tolist()
        data_input["High_rolling"] = pd.DataFrame(highp).rolling(window=_time).max()
        data_input[_name] = (data_input["High_rolling"] - data_input["Close"])
        data_input = data_input.drop(['High_rolling'], axis=1)
        return data_input

def DIST_OF_MA_FROM_HIGH(data_input,row):
        _time=row["timeperiod"]
        _time2=row["custom1"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        highp = data_input.ix[:, 'High'].astype(float).tolist()
        data_input["High_rolling"] = pd.DataFrame(highp).rolling(window=_time).max()
        data_input[_name] = (data_input["High_rolling"] - talib.SMA(data_input['Close'].values,timeperiod=_time2))
        data_input = data_input.drop(['High_rolling'], axis=1)
        return data_input

def DIST_FROM_LOW(data_input,row):
        _time=row["timeperiod"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        lowp = data_input.ix[:, 'Low'].astype(float).tolist()
        data_input["Low_rolling"] = pd.DataFrame(lowp).rolling(window=_time).min()
        data_input[_name] = (data_input['Close'] - data_input["Low_rolling"])
        data_input = data_input.drop(['Low_rolling'], axis=1)
        return data_input

def DIST_OF_MA_FROM_LOW(data_input,row):
        _time=row["timeperiod"]
        _time2=row["custom1"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        lowp = data_input.ix[:, 'Low'].astype(float).tolist()
        data_input["Low_rolling"] = pd.DataFrame(lowp).rolling(window=_time).min()
        data_input[_name] = (talib.SMA(data_input['Close'].values,timeperiod=_time2) - data_input["Low_rolling"])
        data_input = data_input.drop(['Low_rolling'], axis=1)
        return data_input

def LOW_ROLLING(data_input,row):
        _time=row["timeperiod"]
        _time2=row["custom1"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        lowp = data_input.ix[:, 'Low'].astype(float).tolist()
        data_input["Low"+str(_time)] = pd.DataFrame(lowp).rolling(window=_time).min()
        return data_input

def HIGH_ROLLING(data_input,row):
        _time=row["timeperiod"]
        _time2=row["custom1"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        highp = data_input.ix[:, 'High'].astype(float).tolist()
        data_input["High"+str(_time)] = pd.DataFrame(highp).rolling(window=_time).min()
        return data_input

def ICHIMOKU(data_input,row):
        _time=row["timeperiod"]
        _time2=row["custom1"]
        _name=row["indname"]
        print(" Indicator Arguments")
        print(row)
        print("\n")
        lowp = data_input.ix[:, 'Low'].astype(float).tolist()
        highp = data_input.ix[:, 'High'].astype(float).tolist()
        nine_period_high = pd.DataFrame(lowp).rolling(window=_time).min()
        nine_period_low = pd.DataFrame(highp).rolling(window=_time).max()
        ichimoku = (nine_period_high.values + nine_period_low.values)/2
        data_input['ICHIMOKU'+str(_time)] = ichimoku.reshape(-1,1)
        data_input["ICHI"+str(_time)] = data_input['ICHIMOKU'+str(_time)] - data_input['Close']

        return data_input

def MACONG(data_input,row):
    data_input['SMA_10'] = talib.SMA(data_input['Close'].values,timeperiod=10)
    data_input['SMA_20'] = talib.SMA(data_input['Close'].values,timeperiod=20)
    data_input['SMA_50'] = talib.SMA(data_input['Close'].values,timeperiod=50)
    data_input['SMA_80'] = talib.SMA(data_input['Close'].values,timeperiod=80)

    data_input['MACONG'] = ((data_input['SMA_80'].values - data_input['SMA_50'].values) + 
                            (data_input['SMA_50'].values - data_input['SMA_20'].values) +
                            (data_input['SMA_20'].values - data_input['SMA_10'].values) +
                            (data_input['SMA_80'].values - data_input['SMA_10'].values))

    data_input = data_input.drop(['SMA_10','SMA_20','SMA_50','SMA_80'], axis=1)

    return data_input

def MACP(data_input,row):
    data_input['SMA_80'] = talib.SMA(data_input['Close'].values,timeperiod=80)
    
    data_input['MACP'] = (((data_input['SMA_80'].values - data_input['Close'].values)/data_input['Close'].values)*100)
    
    data_input = data_input.drop(['SMA_80'], axis=1)

    return data_input

def MPC(data_input,row):
    lowp = data_input.ix[:, 'Low'].astype(float).tolist()
    highp = data_input.ix[:, 'High'].astype(float).tolist()
    nine_period_high = pd.DataFrame(lowp).rolling(window=5).min()
    nine_period_low = pd.DataFrame(highp).rolling(window=5).max()
    ichimoku = (nine_period_high.values + nine_period_low.values)/2
    data_input['ICHIMOKU5'] = ichimoku.reshape(-1,1)

    data_input['SMA_10'] = talib.SMA(data_input['Close'].values,timeperiod=10)
    data_input['SMA_20'] = talib.SMA(data_input['Close'].values,timeperiod=20)
    data_input['SMA_50'] = talib.SMA(data_input['Close'].values,timeperiod=50)
    data_input['SMA_80'] = talib.SMA(data_input['Close'].values,timeperiod=80)

    data_input['MACONG'] = ((data_input['SMA_80'].values - data_input['SMA_50'].values) + 
                            (data_input['SMA_50'].values - data_input['SMA_20'].values) +
                            (data_input['SMA_20'].values - data_input['SMA_10'].values) +
                            (data_input['SMA_80'].values - data_input['SMA_10'].values))

    data_input['MACP'] = (((data_input['SMA_80'].values - data_input['Close'].values)/data_input['Close'].values)*100)
    
    data_input['MA_PRC_CONG'] = data_input['MACP'].values + data_input['MACONG'] + data_input['ICHIMOKU5'].values
    
    data_input["MPC"] = data_input['MA_PRC_CONG'] - data_input['Close']

    data_input = data_input.drop(['SMA_10','SMA_20','SMA_50','SMA_80','MACONG','MA_PRC_CONG','MPC','ICHIMOKU5'], axis=1)

    return data_input

