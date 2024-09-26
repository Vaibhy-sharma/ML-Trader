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
sys.path.append('../indicators/')
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
import requests

ticker="BANKNIFTYFUT"    
def initConfig(ticker):
    print("ticker:",ticker)
    global INDICATOR_FILE
    global MODEL_FILE
    global MODEL_FILE_NAME
    global LOG_FILE_PATH

    global DATA_FILE_PATH
    global DATA_FILE_NAME
    global DATA_FILE
    global BACKTEST_START_DATE
    global BACKTEST_END_DATE
    
    global INIT_DATA_PATH
    global INIT_DATA_FILE
    global REAL_DATA_PATH
    global REAL_DATA_FILE

    global TRADING_START_TIME
    global TRADING_END_TIME
    global LAST_POS_ENTRY_TIME
    global STOPLOSS_IN_PERC
    global INIT_DATA_PATH
    global last_tick_time
    global initDone 
    global PROFIT_TRAGET_PERC
    global TRADE_TIMEOUT_PERIOD_MIN
    global TRAINING_ALGO
    global LOT_SIZE
    global COST_BPS
    global EXECUTION_STRATEGY
    global THRESHOLD1
    global THRESHOLD2
    global THRESHOLD3
    global QTY_THRESHOLD1
    global QTY_THRESHOLD2
    global QTY_THRESHOLD3
    global NET_QTY_LIMIT
    global SINGLE_SIDE_QTY_LIMIT
    global RUN_MODE
    global ORDER_PLACEMENT
    global DEBUG
    
    configFilePath = r'../config_files/'+ticker+'/conf_60.cfg'
    print("config file path:",configFilePath)
    configParser = configparser.RawConfigParser()
    if configParser.read(configFilePath)!= []:
        pass
    else:
        print('Cannot open configuration file')
        sys.exit(2)
         
    LOG_FILE_PATH = configParser.get('TLCONFIG', 'LOG_FILE_PATH')

    DATA_FILE_PATH = configParser.get('BACKTESTCONFIG', 'DATA_FILE_PATH')
    DATA_FILE_NAME = configParser.get('BACKTESTCONFIG', 'DATA_FILE_NAME')
    DATA_FILE = DATA_FILE_PATH + DATA_FILE_NAME

    BACKTEST_START_DATE = configParser.get('BACKTESTCONFIG', 'BACKTEST_START_DATE')
    BACKTEST_END_DATE = configParser.get('BACKTESTCONFIG', 'BACKTEST_END_DATE')



    INDICATOR_FILE_PATH = configParser.get('TLCONFIG', 'INDICATOR_FILE_PATH')
    IND_FILE_NAME = configParser.get('TLCONFIG', 'INDICATOR_FILE_NAME')
    INDICATOR_FILE = INDICATOR_FILE_PATH+IND_FILE_NAME
    
    MODEL_FILE_PATH = configParser.get('TLCONFIG', 'MODEL_FILE_PATH')
    MODEL_FILE_NAME = configParser.get('TLCONFIG', 'MODEL_FILE_NAME')
    MODEL_FILE = MODEL_FILE_PATH+MODEL_FILE_NAME
   
    TRADING_START_TIME = configParser.get('TLCONFIG', 'TRADING_START_TIME')
    TRADING_END_TIME = configParser.get('TLCONFIG', 'TRADING_END_TIME')
    LAST_POS_ENTRY_TIME = configParser.get('TLCONFIG', 'LAST_POS_ENTRY_TIME')
    
    TRAINING_ALGO = configParser.get('TLCONFIG', 'TRAINING_ALGO')

    PROFIT_TRAGET_PERC = configParser.getfloat ('STRATCONFIG', 'PROFIT_TRAGET_PERC')
    STOPLOSS_IN_PERC = configParser.getfloat('STRATCONFIG', 'STOPLOSS_IN_PERC')
    
    TRADE_TIMEOUT_PERIOD_MIN = configParser.getint('STRATCONFIG', 'TRADE_TIMEOUT_PERIOD_MIN')
    LOT_SIZE = configParser.getint('STRATCONFIG', 'LOT_SIZE')
    COST_BPS = configParser.getfloat('STRATCONFIG', 'COST_BPS')
    EXECUTION_STRATEGY = configParser.get('STRATCONFIG', 'EXECUTION_STRATEGY')
    RUN_MODE = configParser.get('STRATCONFIG', 'RUN_MODE')
    ORDER_PLACEMENT = configParser.getboolean('STRATCONFIG', 'ORDER_PLACEMENT')

    THRESHOLD1 = configParser.getfloat('STRATCONFIG', 'THRESHOLD1')
    THRESHOLD2 = configParser.getfloat('STRATCONFIG', 'THRESHOLD2')
    THRESHOLD3 = configParser.getfloat('STRATCONFIG', 'THRESHOLD3')
    QTY_THRESHOLD1 = configParser.getint('STRATCONFIG', 'QTY_THRESHOLD1')
    QTY_THRESHOLD2 = configParser.getint('STRATCONFIG', 'QTY_THRESHOLD2')
    QTY_THRESHOLD3 = configParser.getint('STRATCONFIG', 'QTY_THRESHOLD3')
    NET_QTY_LIMIT = configParser.getint('STRATCONFIG', 'NET_QTY_LIMIT')
    SINGLE_SIDE_QTY_LIMIT = configParser.getint('STRATCONFIG', 'SINGLE_SIDE_QTY_LIMIT')
    
    DEBUG = configParser.getboolean('STRATCONFIG', 'DEBUG')

    INIT_DATA_PATH = configParser.get('REAL_TIME_CONFIG', 'INIT_DATA_PATH')
    INIT_DATA_FILE = configParser.get('REAL_TIME_CONFIG', 'INIT_DATA_FILE')
    INIT_DATA = INIT_DATA_PATH + INIT_DATA_FILE
    REAL_DATA_PATH = configParser.get('REAL_TIME_CONFIG', 'REAL_DATA_PATH')
    REAL_DATA_FILE = configParser.get('REAL_TIME_CONFIG', 'REAL_DATA_FILE')
    REAL_DATA = REAL_DATA_PATH + REAL_DATA_FILE
    
    # put return and ticker in model file name
      
    initDone=False
    
    print ("------------------------------------TLCONFIG--------------------------------------------------")
    print ("LOG_FILE_PATH:",LOG_FILE_PATH)
    print ("Indicator File:",INDICATOR_FILE)
    print ("Start Time:",TRADING_START_TIME)
    print ("End Time:",TRADING_END_TIME)
    print ("TRAINING_ALGO:",TRAINING_ALGO)
    print ("MODEL_FILE:",MODEL_FILE)

    print ("------------------------------------REAL_TIME_CONFIG------------------------------------------------")
    print ("INIT_DATA File:",INIT_DATA)
    print ("REAL_DATA File:",REAL_DATA)

    print ("------------------------------------STRATEGY CONFIG-------------------------------------------")
        
    print ("RUN_MODE :",RUN_MODE)
    print ("ORDER_PLACEMENT :",ORDER_PLACEMENT)
    print ("STOPLOSS_IN_PERC :",STOPLOSS_IN_PERC)
    print ("PROFIT_TRAGET_PERC:",PROFIT_TRAGET_PERC)
    print ("TRADE_TIMEOUT_PERIOD_MIN:",TRADE_TIMEOUT_PERIOD_MIN)
    print ("LOT_SIZE:",LOT_SIZE)
    print ("COST_BPS:",COST_BPS)
    print ("EXECUTION_STRATEGY:",EXECUTION_STRATEGY)
    print ("initDone:",initDone)
    print("THRESHOLD1:%5.2f, THRESHOLD2:%5.2f,THRESHOLD3:%5.2f" % (THRESHOLD1,THRESHOLD2,THRESHOLD3))
    print("QTY_THRESHOLD1:%5d, QTY_THRESHOLD2:%5d,QTY_THRESHOLD3:%5d" % (QTY_THRESHOLD1,QTY_THRESHOLD2,QTY_THRESHOLD3))
    print ("NET_QTY_LIMIT:",NET_QTY_LIMIT)
    print ("SINGLE_SIDE_QTY_LIMIT:",SINGLE_SIDE_QTY_LIMIT)
    print ("------------------------------------CONFIG END------------------------------------------------")
    print ("\n")

initConfig(ticker)