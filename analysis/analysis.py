import os
import math
import datetime as dt
import datetime
from datetime import datetime
from datetime import timedelta
import talib
import time
import json
import glob
import sys, getopt
import numpy as np
import pandas as pd
import configparser
from sklearn import preprocessing
import json
from sklearn.utils import shuffle
import seaborn as sns
import pickle
import matplotlib.pylab as plt
import matplotlib.pyplot as mat
import csv
import os.path
import requests
from kiteconnect import KiteConnect
from enum import Enum

    
def fMain():
    resultdirectory = "C:\\Users\\indva\\Downloads\\gpm\\log\\BANKNIFTYFUT\\"

    
    filename="df_positions_60_20190207_10620.csv"# df_positions_45_20190207_16884 df_positions_30_20190207_2372
    filepath= resultdirectory + filename

    print("\nAnalyzing filepath:", filename) # filepath)

    df = pd.read_csv(filepath)

    print("\nModel Name:",df.iloc[-1, 21])
    print("\n")
    print("THRESHOLD1:",df.iloc[-1, 22],"THRESHOLD2:",df.iloc[-1, 23],"THRESHOLD3:",df.iloc[-1, 24])
    print("\n")
    print("PROFIT TRAGET:",df.iloc[-1, 25] ,"STOPLOSS:",df.iloc[-1, 26] ,"SIDE_QTY_LIMIT:",df.iloc[-1, 27])
    
    #print(df)

    d = pd.to_datetime(df['Date Time'], format='%Y-%m-%d %H:%M')
    df['Date'] = d.dt.date
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y%m%d')).astype(int)

    df_day_PL = df.groupby(['Date'])['netPosPL'].agg('sum').reset_index()
    TotalDays = len(df_day_PL)
    positiveDays = len(df_day_PL[df_day_PL['netPosPL'] >= 0])
    negativeDays = len(df_day_PL[df_day_PL['netPosPL'] < 0])
    avgDayPL = df_day_PL['netPosPL'].mean()
    maxDayPL = df_day_PL['netPosPL'].max()
    minDayPL = df_day_PL['netPosPL'].min()


    print("\n")
    print("Total Trading Days:",TotalDays,"positiveDays:",positiveDays,"negativeDays:",negativeDays)   
    print("\n")
    print("Total PL",round(df['netPosPL'].sum(),2),"avgDayPL",avgDayPL,"maxDayPL",maxDayPL,"minDayPL",minDayPL)   
    print("\n")

    netPL = df['netPosPL'].sum()
    #print("netPL",round(netPL,2))
    TotalTrades = len(df)
    PositiveTrades = len(df[df['netPosPL'] >= 0])
    NegativeTrades = len(df[df['netPosPL'] < 0])
    PercentPositive = PositiveTrades/TotalTrades
    PnLperTrade = netPL/TotalTrades
    print("\n")
    
    print("TotalTrades:",TotalTrades,"PositiveTrades:",PositiveTrades,"NegativeTrades:",NegativeTrades,
          "PercentPositive:",round(PercentPositive*100,2),"PnLperTrade",round(PnLperTrade,1), "\n")
    
     

    print("\n")


    df_ExT_PL = df.groupby(['exittype'])['netPosPL'].agg('sum').reset_index()
    df_ExT_PL = df_ExT_PL.rename(columns = {"netPosPL": "TotalPL"})
    #print(df_ET_PL)


    df_ExT_PL_DESC = df.groupby("exittype")['netPosPL'].describe().reset_index().drop(columns=['std','25%','50%','75%'])
    df_ExT_PL_DESC = df_ExT_PL_DESC.rename(columns = {"mean": "mean_PL","min":"min_PL","max": "max_PL"})
    #print(df_ET_PL_DESC)

    df_ExT_posLife = df.groupby("exittype")['posLife'].describe().reset_index().drop(columns=['count','std','25%','50%','75%'])
    df_ExT_posLife = df_ExT_posLife.rename(columns = {"mean": "mean_age","min":"min_age","max": "max_age"})
    
    df_ExT_merge=df_ExT_PL.merge(df_ExT_PL_DESC, left_on='exittype', right_on='exittype', how='outer')
    
    df_ExT_merge=df_ExT_merge.merge(df_ExT_posLife, left_on='exittype', right_on='exittype', how='outer')
      
    print(df_ExT_merge)

    print("\n")

 


if __name__ == '__main__':
        pd.set_option('display.expand_frame_repr', False)
        argv = sys.argv[1:]
        
        fMain()
