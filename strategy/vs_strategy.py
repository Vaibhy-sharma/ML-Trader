import os
import math
import datetime as dt
import datetime
from datetime import timedelta
import time
import json
import glob
import sys, getopt
import numpy as np
import pandas as pd
import configparser
sys.path.append('./indicators/')
from fun_custom import *
from funtalib_cyclical import *
from funtalib_momentum import *
from funtalib_overlap import *
from funtalib_volume import *
from funtalib_volatility import *
from indicatorsheader import *
from sklearn import preprocessing
import json
import xgboost as xgb
from sklearn.utils import shuffle
import seaborn as sns
import pickle
import matplotlib.pylab as plt
import matplotlib.pyplot as mat
import csv
#from backtester import *
#from kiteconnect import KiteConnect
#import requests
sys.path.append('./Variables/')
import global_variable
from global_variable import *
# sys.path.append('../strategy/')
# import strategy
# from strategy import *


def trading_hour_check(current_tick_time):
    isTradingHour=True
    isPos_Entry_time=True

    current_tick_time_tmp=current_tick_time

 
    time_start=datetime.datetime.strptime(global_variable.TRADING_START_TIME, '%H:%M')
    time_end=datetime.datetime.strptime(global_variable.TRADING_END_TIME, '%H:%M')

    pos_entry_end_time=datetime.datetime.strptime(global_variable.LAST_POS_ENTRY_TIME, '%H:%M')

    if(current_tick_time_tmp.hour < time_start.hour):
        isPos_Entry_time=False
    elif(current_tick_time_tmp.hour==time_start.hour and current_tick_time_tmp.minute<time_start.minute) :
        isPos_Entry_time=False

    if(current_tick_time_tmp.hour>=time_end.hour and current_tick_time_tmp.minute>=time_end.minute):
        isTradingHour=False

    if(current_tick_time_tmp.hour>=pos_entry_end_time.hour and current_tick_time_tmp.minute>=pos_entry_end_time.minute):
        isPos_Entry_time=False

    return isTradingHour,isPos_Entry_time


def get_bid_ask(df):
    try:
        pass

    except:
        print("Getting price from real time data failed.Using closing price now")
        bid_price=df.iloc[-1, 4]
        ask_price=df.iloc[-1, 4]
        
    return bid_price,ask_price

def vs_strategy(longProb,shortProb,df_signals,df_positions,close_price):
       
        current_tick_time = df_signals.iloc[-1, 0]

        #print("current Tick time:",current_tick_time)

        isTradingHour=True
        isPosEntryTime=True

        isTradingHour,isPosEntryTime=trading_hour_check(current_tick_time)

        df_pos_tmp_logonly = pd.DataFrame()
        #print("input df_positions:")
        #print(df_positions)

        #print("input df_pos_tmp_logonly:")
        #print(df_pos_tmp_logonly)

        send_new_buy=False
        send_new_sell=False
        send_buy_sqoff=False  #on sell signal when we have buy positions | Counter Signal
        send_sell_sqoff=False #on buy signal when we have sell positions | Counter Signal
        #pos_timeout=False # Position timeoutreached
        #buy_target_reached=False
        #buy_SL_reached=False
        #sell_target_reached=False
        #sell_SL_reached=False


        order_price=0
        order_qty=0
        action_type=''
        sendorder=False

        buy_ord_qty,sell_ord_qty,buy_threshold_met,sell_threshold_met = get_signal(longProb,shortProb)

        if(global_variable.RUN_MODE=="LIVE_SIGNAL" or global_variable.RUN_MODE=="LIVE_ORDER"):
            bid_price,ask_price = get_bid_ask(df_signals)
            mid_price= (bid_price+ask_price)/2
        else:
            bid_price = close_price
            ask_price = close_price
            mid_price= close_price

                
        buy_quantity=df_positions.loc[df_positions['longshort'] == 'long', 'quantity'].sum() + df_positions.loc[df_positions['longshort'] == 'short', 'exitqty'].sum()
        sell_quantity=df_positions.loc[df_positions['longshort'] == 'short', 'quantity'].sum() + df_positions.loc[df_positions['longshort'] == 'long', 'exitqty'].sum()
    
        print("Tick Time:%18s,buy_threshold_met:%-6s,sell_threshold_met:%-6s,longProb:%-4.2f,shortProb:%-4.2f,buy_quantity:%-4.2f,sell_quantity:%-4.2f,bid_price:%-4.2f,ask_price:%-4.2f,mid_price:%-4.2f" % (current_tick_time,buy_threshold_met,sell_threshold_met,longProb,shortProb,buy_quantity,sell_quantity,bid_price,ask_price,mid_price))
        #print("buy_quantity:%-6.2f,sell_quantity:%-6.2f" % (buy_quantity,sell_quantity))
    
        #CHECK TARGET SL TIMOUT FOR ALL EXISTING POSITION
        if len(df_positions) != 0:
            for index, row in df_positions.iterrows():
                _isactive =df_positions['isactive'][index]
                _longshort =df_positions['longshort'][index]
                
                if (_isactive==1 and _longshort=='long'):
                    _TP =df_positions['target'][index]
                    _SL =df_positions['stoploss'][index]
                    _timeout =df_positions['timeout'][index]
                    sqOffQty = df_positions['quantity'][index]
                 
                    if(mid_price>_TP):
                        sell_quantity = sell_quantity+sqOffQty
                        exit_price=bid_price
                        exittype='target'
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Sell',bid_price,sqOffQty,True,'target',buy_quantity,sell_quantity)
                        return df_signals,df_positions
                    elif(mid_price<_SL):
                        sell_quantity = sell_quantity+sqOffQty
                        exit_price=bid_price
                        exittype='SL'
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Sell',bid_price,sqOffQty,True,'SL',buy_quantity,sell_quantity)
                        return df_signals,df_positions
                    elif(current_tick_time>=_timeout):
                        print("POSITION TIMEOUT")
                        sell_quantity = sell_quantity+sqOffQty
                        exit_price=bid_price
                        exittype='TIMEOUT'
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Sell',bid_price,sqOffQty,True,'TIMEOUT',buy_quantity,sell_quantity)
                        return df_signals,df_positions    
                
                elif (_isactive==1 and _longshort=='short'):
                    _TP =df_positions['target'][index]
                    _SL =df_positions['stoploss'][index]
                    _timeout =df_positions['timeout'][index]
                    sqOffQty = df_positions['quantity'][index]
                    
                    if(mid_price<_TP):
                        exittype='target'
                        buy_quantity = buy_quantity + sqOffQty
                        exit_price=ask_price
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Buy',ask_price,sqOffQty,True,'target',buy_quantity,sell_quantity)
                        return df_signals,df_positions
                    elif(mid_price>_SL):                        
                        exittype='SL'
                        buy_quantity = buy_quantity + sqOffQty
                        exit_price=ask_price
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Buy',ask_price,sqOffQty,True,'SL',buy_quantity,sell_quantity)
                        return df_signals,df_positions
                    elif(current_tick_time>=_timeout):
                        print("POSITION TIMEOUT")
                        exittype='TIMEOUT'
                        buy_quantity = buy_quantity + sqOffQty
                        exit_price=ask_price
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Buy',ask_price,sqOffQty,True,'TIMEOUT',buy_quantity,sell_quantity)
                        return df_signals,df_positions

                if not isTradingHour:
                    if (_isactive==1 and _longshort=='long'):
                        print("EOD SQOFF")
                        sell_quantity = sell_quantity+sqOffQty
                        exit_price=bid_price
                        exittype='EOD SQOFF'
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Sell',bid_price,sqOffQty,True,'TIMEOUT',buy_quantity,sell_quantity)
                        return df_signals,df_positions
                    elif (_isactive==1 and _longshort=='short'):
                        print("EOD SQOFF")
                        buy_quantity = buy_quantity + sqOffQty
                        exit_price=ask_price
                        exittype='EOD SQOFF'
                        df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                        df_signals,df_positions = update_signal(df_signals,df_positions,'Buy',ask_price,sqOffQty,True,'TIMEOUT',buy_quantity,sell_quantity)
                        return df_signals,df_positions
      
           
        if (buy_threshold_met and (buy_quantity + sell_quantity)<global_variable.NET_QTY_LIMIT):
            action_label='Buy'
            order_price=ask_price
            order_qty=buy_ord_qty
            if (sell_quantity >buy_quantity):
                send_sell_sqoff=True
                sendorder=True
            elif ((buy_quantity >=sell_quantity) and (buy_quantity - sell_quantity)<global_variable.SINGLE_SIDE_QTY_LIMIT):
                send_new_buy=True
                sendorder=True
            else :
                sendorder=False
        elif (sell_threshold_met and (buy_quantity + sell_quantity)<global_variable.NET_QTY_LIMIT ):
            action_label='Sell'
            order_price=bid_price
            order_qty=sell_ord_qty
            if (buy_quantity >sell_quantity):
                send_buy_sqoff=True
                sendorder=True
            elif ((sell_quantity >=buy_quantity) and (sell_quantity - buy_quantity)<global_variable.SINGLE_SIDE_QTY_LIMIT):
                send_new_sell=True
                sendorder=True
            else :
                sendorder=False
        else:
            action_label='Wait'

   
        if (isPosEntryTime):
            if send_new_buy:
                action_type='Buy Entry'
                print("action_type")
                buy_quantity =buy_quantity + order_qty
                longshort ='long'
                df_pos_tmp_logonly = entry_update(current_tick_time,order_price,order_qty,longshort,longProb,shortProb)
                df_positions = pd.concat([df_positions, df_pos_tmp_logonly], ignore_index=True,sort=False)
            
            elif send_new_sell:
                action_type='Sell Entry'
                print("action_type")
                sell_quantity = sell_quantity + order_qty
                longshort ='short'
                df_pos_tmp_logonly = entry_update(current_tick_time,order_price,order_qty,longshort,longProb,shortProb)
                df_positions = pd.concat([df_positions, df_pos_tmp_logonly], ignore_index=True,sort=False)
       
            elif send_buy_sqoff:
                action_type='buyExitonCounter'
                print("action_type")
                if len(df_positions) != 0:
                    for index, row in df_positions.iterrows():
                        _isactive =df_positions['isactive'][index]
                        _longshort =df_positions['longshort'][index]
                        if (_isactive==1 and _longshort=='long'):
                            sell_quantity = sell_quantity+sqOffQty
                            exit_price=bid_price
                            exittype='buyExitonCounter'
                            df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                            df_signals,df_positions = update_signal(df_signals,df_positions,'Sell',bid_price,sqOffQty,True,action_type,buy_quantity,sell_quantity)
                            return df_signals,df_positions
                            
            elif send_sell_sqoff:
                action_type='sellExitonCounter'
                print("action_type")
                if len(df_positions) != 0:
                    for index, row in df_positions.iterrows():
                        _isactive =df_positions['isactive'][index]
                        _longshort =df_positions['longshort'][index]
                        if (_isactive==1 and _longshort=='short'):
                            exittype='sellExitonCounter'
                            buy_quantity = buy_quantity + sqOffQty
                            exit_price=ask_price
                            df_positions = exit_update(current_tick_time,_longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb)
                            df_signals,df_positions = update_signal(df_signals,df_positions,'Buy',bid_price,sqOffQty,True,action_type,buy_quantity,sell_quantity)
                            return df_signals,df_positions
       
            

            #print("df_positions")
            #print(df_positions)

        df_signals,df_positions = update_signal(df_signals,df_positions,action_label,order_price,order_qty,sendorder,action_type,buy_quantity,sell_quantity)

        return df_signals,df_positions

def update_signal(df_signals_local,df_positions_local,action_label,order_price,order_qty,sendorder,action_type,buy_quantity,sell_quantity):
    #print("update_signal")
    #print(df_signals_local)
    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('action_label')] = action_label
    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('order_price')] = order_price
    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('order_qty')] = order_qty
    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('sendorder')] = sendorder
    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('action_type')] = action_type

    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('net_buy_qty')] = buy_quantity
    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('net_sell_qty')] = sell_quantity
    df_signals_local.iloc[-1, df_signals_local.columns.get_loc('net_position')] = (buy_quantity - sell_quantity)

    #print("postUpdate")
    #print(df_signals_local)
    #signal_file_name ="df_signals.csv"
    #pos_file_name="df_positions.csv"

    signal_file_name = "%s_%s_%s.%s" % ("df_signals", datetime.datetime.now().strftime("%Y%m%d"),os.getpid(),"csv")
    pos_file_name = "%s_%s_%s.%s" % ("df_positions", datetime.datetime.now().strftime("%Y%m%d"),os.getpid(),"csv")

    signal_file_name = global_variable.LOG_FILE_PATH+signal_file_name
    pos_file_name = global_variable.LOG_FILE_PATH + pos_file_name

    if (global_variable.RUN_MODE=="LIVE_SIGNAL" or global_variable.RUN_MODE=="LIVE_ORDER"):
        df_signals_local.to_csv(signal_file_name, index=False) # Save the csv file
        df_positions_local.to_csv(pos_file_name, index=False) # Save the csv file

    return df_signals_local,df_positions_local

def exit_update(current_tick_time,longshort,exittype,index,sqOffQty,df_positions,exit_price,buy_quantity,sell_quantity,longProb,shortProb):
    df_positions.at[index, 'isactive'] = 0
    df_positions.at[index, 'exittype'] = exittype
    df_positions.at[index, 'exittime'] = current_tick_time

    df_positions.at[index, 'exitprice'] = exit_price
    df_positions.at[index, 'exitqty'] = sqOffQty
    df_positions.at[index, 'exitlongProb'] = longProb
    df_positions.at[index, 'exitshortProb'] = shortProb

    entryprice=df_positions['price'][index]
    posPL=0
    if (longshort=='long'):
        posPL=(exit_price-entryprice)*sqOffQty
    elif(longshort=='short'):
        posPL=(entryprice-exit_price)*sqOffQty

    df_positions.at[index, 'posPL'] = posPL

    pos_to=(exit_price +entryprice)*sqOffQty
    pos_cost=(pos_to*(global_variable.COST_BPS))/(100*100)
    netPosPL= posPL-pos_cost

    df_positions.at[index, 'cost'] = pos_cost
    df_positions.at[index, 'netPosPL'] = netPosPL
    df_positions.at[index, 'AggregatePL'] = df_positions['netPosPL'].sum()

    pos_entry_time=df_positions['Date Time'][index]
    date_time_difference= current_tick_time - pos_entry_time
    df_positions['posLife'][index]=round(date_time_difference.total_seconds()/60)

    return df_positions


def entry_update(current_tick_time,order_price,order_qty,longshort,longProb,shortProb):
     df_pos_local = pd.DataFrame()
     df_pos_local.at[-1, 'Date Time']=current_tick_time
     df_pos_local.at[-1, 'price'] = order_price
     df_pos_local.at[-1, 'quantity'] = order_qty
     df_pos_local.at[-1, 'longshort'] = longshort
     if longshort=='long':
        df_pos_local.at[-1, 'target'] = order_price + (global_variable.PROFIT_TRAGET_PERC*order_price)/100.0
        df_pos_local.at[-1, 'stoploss'] = order_price - (global_variable.STOPLOSS_IN_PERC*order_price)/100.0
     elif longshort=='short':
        df_pos_local.at[-1, 'target'] = order_price - (global_variable.PROFIT_TRAGET_PERC*order_price)/100.0
        df_pos_local.at[-1, 'stoploss'] = order_price + (global_variable.STOPLOSS_IN_PERC*order_price)/100.0
     df_pos_local.at[-1, 'timeout'] = current_tick_time + datetime.timedelta(minutes=global_variable.TRADE_TIMEOUT_PERIOD_MIN)
     df_pos_local.at[-1, 'isactive'] = 1
     df_pos_local.at[-1, 'exittype'] = ''
     df_pos_local.at[-1, 'exitprice'] = 0
     df_pos_local.at[-1, 'exitqty'] = 0
     df_pos_local.at[-1, 'longProb'] = longProb
     df_pos_local.at[-1, 'shortProb'] = shortProb
     df_pos_local.at[-1, 'posPL'] = 0
     df_pos_local.at[-1, 'AggregatePL'] = 0
     df_pos_local.at[-1, 'modelfile'] = global_variable.MODEL_FILE_NAME
     df_pos_local.at[-1, 'THRESHOLD1'] = global_variable.THRESHOLD1
     df_pos_local.at[-1, 'THRESHOLD2'] = global_variable.THRESHOLD2
     df_pos_local.at[-1, 'THRESHOLD3'] = global_variable.THRESHOLD3
     df_pos_local.at[-1, 'PROFIT_TRAGET'] = global_variable.PROFIT_TRAGET_PERC
     df_pos_local.at[-1, 'STOPLOSS'] = global_variable.STOPLOSS_IN_PERC
     df_pos_local.at[-1, 'SIDE_QTY_LIMIT'] = global_variable.SINGLE_SIDE_QTY_LIMIT
     return df_pos_local

def get_signal(longProb,shortProb):
       
        buy_threshold_met=False
        sell_threshold_met=False
        
        buy_ord_qty=0;
        sell_ord_qty=0;


        if longProb >= global_variable.THRESHOLD3:
            buy_ord_qty=global_variable.QTY_THRESHOLD3
            buy_threshold_met=True
            if global_variable.DEBUG :
                print ("LONG THRESHOLD3 CROSSED:",longProb)
        elif longProb >= global_variable.THRESHOLD2:
            buy_threshold_met=True
            buy_ord_qty=global_variable.QTY_THRESHOLD2
            if global_variable.DEBUG :
                print ("LONG THRESHOLD2 CROSSED:",longProb)     
        elif longProb >= global_variable.THRESHOLD1:
            buy_threshold_met=True
            buy_ord_qty=global_variable.QTY_THRESHOLD1
            if global_variable.DEBUG :
                print ("LONG THRESHOLD1 CROSSED:",longProb)
        elif shortProb >= global_variable.THRESHOLD3:
            sell_threshold_met=True
            sell_ord_qty=global_variable.QTY_THRESHOLD3
            if global_variable.DEBUG :
                print ("SHORT THRESHOLD3 CROSSED:",shortProb)
        elif shortProb >= global_variable.THRESHOLD2:
            sell_threshold_met=True
            sell_ord_qty=global_variable.QTY_THRESHOLD2
            if global_variable.DEBUG :
                print ("SHORT THRESHOLD2 CROSSED:",shortProb)
        elif shortProb >= global_variable.THRESHOLD1:
            sell_threshold_met=True
            sell_ord_qty=global_variable.QTY_THRESHOLD1
            if global_variable.DEBUG :
                print ("SHORT THRESHOLD1 CROSSED:",shortProb)
        # else:
        #     if global_variable.DEBUG:
        #         print ("WAIT SIGNAL:")
        #         print("longProb:%-6.2f,shortProb:%-6.2f" % (longProb,shortProb))

           

        return  buy_ord_qty,sell_ord_qty,buy_threshold_met,sell_threshold_met       