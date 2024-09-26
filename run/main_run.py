import os
import math
import datetime as dt
import datetime
from datetime import datetime
from datetime import timedelta
import time
import json
import glob
import sys, getopt
import numpy as np
import pandas as pd
import configparser
sys.path.append('../indicators/')
from fun_custom import *
from funtalib_cyclical import *
from funtalib_momentum import *
from funtalib_overlap import *
from funtalib_volume import *
from funtalib_volatility import *
from funtalib_statistical import *
from indicatorsheader import *
from sklearn import preprocessing
import json
import xgboost as xgb
from sklearn import preprocessing
from sklearn.utils import shuffle
import seaborn as sns
import pickle
import matplotlib.pylab as plt
import matplotlib.pyplot as mat
import csv
sys.path.append('../Variables/')
import global_variable
from global_variable import *
sys.path.append('../strategy/')
import vs_strategy
from vs_strategy import *


def readConfig():
    print("ticker:",ticker)
    initConfig(ticker)

def read_init_data():
	
	init_data_file = global_variable.INIT_FILE
	#print("init_data_file:",init_data_file)
	df = pd.read_csv(init_data_file)
	
	return df


def updateIndicators(df,indicator_df):
    # if global_variable.DEBUG :
    #     print ("Indicators Calcualtion Starting\n")

    for ind,row in indicator_df.iterrows():
       	_indname =indicator_df['indname'][ind]
       	_indclassname =indicator_df['indClass'][ind]
       	df = indicatorListDict[_indclassname](df,row)
    # if global_variable.DEBUG :
    #    	print ("Indicators Calcualtion COMPLETE \n\n")
    return df

def run_model(df,cur_sys_time):
        # if global_variable.DEBUG :
        # 	print ("run_model Starting\n")
        sig_df = df.tail(1)
        #print("run_model")
        #print(sig_df)
        test = sig_df.drop(['Date Time', 'Open','High','Low','Close','Volume'], axis=1)
        X = [name for name in test.columns]
        data_model = xgb.DMatrix(test[X])
        xgb_model = pickle.load(open(global_variable.MODEL_FILE, "rb"))
        pred_prob = xgb_model.predict(data_model).reshape(test[X].shape[0], 3)
        pred_label = np.argmax(pred_prob, axis=1)
        pred_label = pred_label.tolist()

        #if global_variable.DEBUG :
        	#print("System Time:%18s,Tick Time:%18s, Close Price:%6.2f, Buy Prob:%6.2f,Short Prob:%6.2f,Wait Prob:%6.2f" % (cur_sys_time,str(sig_df.iloc[0]['Date Time']),sig_df.iloc[0]['Close'],pred_prob[:,1] ,pred_prob[:,2],pred_prob[:,0] ))
        #print ('Time', str(sig_df.iloc[0]['Date Time']))
        #print ('Wait probability', pred_prob[:,0])
        #print ('Long probability', pred_prob[:,1])
        #print ('Sell probability', pred_prob[:,2])
        # if global_variable.DEBUG :
        # 	print ("run_model Complete\n")
        return pred_prob[:,1] ,pred_prob[:,2]


def update_signal_df(df_signals,df_tmp,longProb,shortProb,df_data_singlerow):
	#print("update_signal_df")
	#NOT A GOOD WAY TO USE DF_TMP.CHANGE LATER
	df_tmp.at[-1, 'buy_prob'] = longProb
	df_tmp.at[-1, 'sell_prob']= shortProb
	df_tmp.at[-1, 'Date Time']= df_data_singlerow["Date Time"].iloc[-1]
	df_tmp.at[-1, 'open']= df_data_singlerow["Open"].iloc[-1]
	df_tmp.at[-1, 'high']= df_data_singlerow["High"].iloc[-1]
	df_tmp.at[-1, 'low']= df_data_singlerow["Low"].iloc[-1]
	df_tmp.at[-1, 'close']= df_data_singlerow["Close"].iloc[-1]

	df_signals = pd.concat([df_signals, df_tmp], ignore_index=True,sort=False)

	#df_signals.to_csv("df_signals_csv.csv", index=False) # Save the csv file
	return df_signals

def run_strat_for_each_day(df,df_signals,df_positions,df_tmp):
    index_count=0;
    count=0;
    for index,row in df.iterrows():
        count = count +1
        df_data_singlerow =df[(df['Date Time'] == df.ix[index,'Date Time'])]
        close_price = df.ix[index,'Close']
        if count >50:
            longProb,shortProb = run_model(df_data_singlerow,datetime.datetime.now().time())

            df_signals =update_signal_df(df_signals,df_tmp,longProb,shortProb,df_data_singlerow)
            df_signals,df_positions = vs_strategy(longProb,shortProb,df_signals,df_positions,close_price)
    return df_signals,df_positions


def backtest_from_data_file(indicator_df,df_signals,df_positions,df_tmp,df_signals_summary,df_positions_summary):

    backtest_data_file = global_variable.DATA_FILE
    print("backtest_data_file:",backtest_data_file)

    start = datetime.datetime.strptime(global_variable.BACKTEST_START_DATE, "%Y%m%d")
    end = datetime.datetime.strptime(global_variable.BACKTEST_END_DATE, "%Y%m%d")

    print("Start Date:",start)
    print("end Date:",end)

    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days +1)]

    for date in date_generated:
        print("Backtesting for date:",date)
        next_date=date + timedelta(days=1)
        df = pd.read_csv(backtest_data_file)

        try:
            d = pd.to_datetime(df['Date Time'], format='%Y-%m-%d %H:%M')
            df['Date Time'] =pd.to_datetime(df['Date Time'])
        except:
            d = pd.to_datetime(df['Date Time'], format='%m/%d/%Y %H:%M')
            df['Date Time'] =pd.to_datetime(df['Date Time'])
        df['Date'] = d.dt.date
        df['Date'] = df['Date'].apply(lambda x: x.strftime('%Y%m%d')).astype(int)

        date_int=int(date.strftime('%Y%m%d'))
        next_date_int=int(next_date.strftime('%Y%m%d'))

        df = df[(df['Date'] >= date_int) & (df['Date'] <next_date_int)]
        df = df.drop(columns=['Date'])

        if(len(df)>100):
            print("STARTED STRATEGY FOR DATE:",date)

            data_df_indicators_updated = updateIndicators(df,indicator_df)

            #data_df_indicators_updated.to_csv("testcsv.csv", index=False) # Save the csv file

            df_signals_out,df_positions_out = run_strat_for_each_day(data_df_indicators_updated,df_signals,df_positions,df_tmp)

            
            df_signals_summary = pd.concat([df_signals_summary, df_signals_out], ignore_index=True,sort=False)
            df_positions_summary = pd.concat([df_positions_summary, df_positions_out], ignore_index=True,sort=False)


            signal_file_name = "%s_%s_%s.%s" % ("df_signals_60", datetime.datetime.now().strftime("%Y%m%d"),os.getpid(),"csv")
            pos_file_name = "%s_%s_%s.%s" % ("df_positions_60", datetime.datetime.now().strftime("%Y%m%d"),os.getpid(),"csv")

            signal_file_name = global_variable.LOG_FILE_PATH+signal_file_name
            pos_file_name = global_variable.LOG_FILE_PATH + pos_file_name
   
            df_signals_summary.to_csv(signal_file_name, index=False) # Save the csv file
            df_positions_summary.to_csv(pos_file_name, index=False) # Save the csv file

        print("Backtesting completed for date:",date)    




def run_live(indicator_df,df_signals,df_positions,df_tmp):

    print ("Download data on init\n")
    global initDone
    print ("initDone:",global_variable.initDone)

    if not global_variable.initDone:

        df_data_combined = read_init_data()

        global_variable.initDone =True

    print ("Read data on init DONE\n")
    print ("initDone:",global_variable.initDone)

      
    
    
    while True:   
        current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_start_time=(last_tick_time + datetime.timedelta(minutes=1))
        # tick for 9:30 will come at 9:31 as thats when OHLC will get completes so we will pull tick at cur tme>9:31
        new_pull_time=(last_tick_time + datetime.timedelta(minutes=2))

        #if global_variable.DEBUG :
            #print("Current time:",datetime.datetime.now().time())
            #print("Last Tick time:",last_tick_time.time())
            #print("new_pull_time:",new_pull_time.time())
            #print("Current time:%-18s,Last Tick time:%-18s, new_pull_time:%-18s" % (datetime.datetime.now().time(),last_tick_time.time(),new_pull_time.time()))
          
        if (datetime.datetime.now().time()>new_pull_time.time()):
            time_start=new_start_time
            time_end=current_time
            if global_variable.DEBUG :
                print("PULL DATA :time_start:%-18s, time_end:%-18s" % (time_start,time_end))

            df_data_singlerow = get_data(time_start,time_end)
            close_price=0
            #print(df_data_combined)  
            #print(df_data_singlerow)
            if len(df_data_singlerow) != 0:
                df_data_combined = pd.concat([df_data_combined, df_data_singlerow], ignore_index=True,sort=False)
                #df_data_combined.to_csv('data.csv', index=False)
                data_indicators = updateIndicators(df_data_combined,indicator_df)
                #data_indicators.to_csv('data.csv', index=False)
                longProb,shortProb = run_model(data_indicators,datetime.datetime.now().time())
                df_signals =update_signal_df(df_signals,df_tmp,longProb,shortProb,df_data_singlerow)
                if global_variable.RUN_MODE==1:
                    df_signals,df_positions = vs_strategy(longProb,shortProb,df_signals,df_positions,close_price)                  
                elif global_variable.RUN_MODE==2:
                    print("Strat")
                    #df_signals,order_id_buy_pending,order_id_sell_pending = runStrategy(kite,longProb,shortProb,df_signals,order_id_buy_pending,order_id_sell_pending)

        time.sleep(3)



def fMain():
    df_data_combined = pd.DataFrame()
    COLUMN_NAMES=['Date Time','open','high','low','close','buy_prob','sell_prob','action_label','sendorder','action_type','order_price','order_qty','net_position','net_buy_qty','net_sell_qty']
    df_signals = pd.DataFrame(columns=COLUMN_NAMES)
    df_tmp = pd.DataFrame(columns=COLUMN_NAMES)
    
    COLUMN_NAMES_POS=['Date Time','price','quantity','longshort','target','stoploss','timeout','longProb','shortProb','isactive','exittime','exittype','exitprice','exitqty','posLife','posPL','cost','netPosPL','AggregatePL','exitlongProb','exitshortProb']
    df_positions = pd.DataFrame(columns=COLUMN_NAMES_POS)

    df_signals_summary = pd.DataFrame(columns=COLUMN_NAMES)
    df_positions_summary=pd.DataFrame(columns=COLUMN_NAMES_POS)
  
    order_id_buy_pending=0
    order_id_sell_pending=0
    count=0;
    print ("Start Reading Config File\n")
    readConfig()
    print ("End Reading Config File\n\n")
    
    if (global_variable.RUN_MODE=="LIVE_SIGNAL" or global_variable.RUN_MODE=="LIVE_ORDER"):
        print ("Setting kite connections\n")
        kite = setKiteConnections()
        print ("kite connections done\n")

    
    try:
        indicator_df = pd.read_csv(global_variable.INDICATOR_FILE)
    except:
        print ("Error in reading INDICATOR_FILE :", global_variable.INDICATOR_FILE)
        sys.exit(2)


    if (global_variable.RUN_MODE=="BACKTEST"):
        print("Start backtest from file\n")
        backtest_from_data_file(indicator_df,df_signals,df_positions,df_tmp,df_signals_summary,df_positions_summary)
        print(datetime.datetime.now(), "Complete backtest from file\n")
    elif (global_variable.RUN_MODE=="LIVE_SIGNAL" or global_variable.RUN_MODE=="LIVE"):
        print ("Start Live/signal only from kite data\n")
        run_live(kite,indicator_df,df_signals,df_positions,df_tmp)

                 

if __name__ == '__main__':
        pd.set_option('display.expand_frame_repr', False)
        argv = sys.argv[1:]
        if len(argv) !=2:
                print ('Invalid no of Args' ,len(argv))
                sys.exit(2)
        try:
                opts, args = getopt.getopt(argv,"ht:",["ticker="])
        except getopt.GetoptError:
                print ('error in args')
        for opt, arg in opts:
            if opt == '-t':
                ticker = arg
                
                if ticker:
                   # got a non-empty string
                   print("argument:" ,ticker)
                else:
                   # got a empty string
                   print ('No Symbol Passed')
                   sys.exit(2)
        
        fMain()





