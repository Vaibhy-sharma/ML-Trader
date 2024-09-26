import os
import pandas as pd
import sys
sys.path.append('../indicators/')
from fun_custom import *
from funtalib_cyclical import *
from funtalib_momentum import *
from funtalib_overlap import *
from funtalib_volatility import *
from funtalib_volume import *
from funtalib_statistical import *

indicatorListDict = {
    'talib_STOCH': talib_STOCH,'talib_TRANGE': talib_TRANGE, 'talib_ATR': talib_ATR,'talib_NATR': talib_NATR,
    'panda_skewness': panda_skewness,'panda_kurtosis': panda_kurtosis,'talib_BBANDS': talib_BBANDS,'talib_trendEMA': talib_trendEMA,
    'talib_trendDEMA': talib_trendDEMA,'talib_trendKAMA': talib_trendKAMA,'talib_trendMAMA': talib_trendMAMA,'talib_trendIF': talib_trendIF,
    'talib_trendSMA': talib_trendSMA,'talib_trendMIDPOINT': talib_trendMIDPOINT,'talib_trendMIDPRICE': talib_trendMIDPRICE,'MACONG':MACONG,
    'talib_HT_DCPERIOD': talib_HT_DCPERIOD,'talib_HT_DCPHASE': talib_HT_DCPHASE,'talib_HT_PHASOR': talib_HT_PHASOR,'MPC':MPC,'MACP':MACP,
    'talib_SINE': talib_SINE,'talib_LEADSINE': talib_LEADSINE,'talib_HT_TRENDMODE': talib_HT_TRENDMODE,'talib_ADX': talib_ADX,'talib_ADXR': talib_ADXR,
    'talib_APO': talib_APO,'talib_AROONOSC': talib_AROONOSC,'talib_BOP': talib_BOP,'stdhighlow':stdhighlow,'talib_STOCHDIFF':talib_STOCHDIFF,
    'talib_CCI': talib_CCI,'talib_CMO': talib_CMO,'talib_DX': talib_DX,'talib_MACD': talib_MACD,'talib_MACDSIGNAL': talib_MACDSIGNAL,
    'talib_MACDHIST': talib_MACDHIST,'talib_PLUS_DI': talib_PLUS_DI,'talib_MINUS_DI': talib_MINUS_DI,'talib_ADXPLUS':talib_ADXPLUS,'talib_ADXMINUS':talib_ADXMINUS,
    'talib_PLUS_DM': talib_PLUS_DM,'talib_MINUS_DM': talib_MINUS_DM,'talib_MOM': talib_MOM,'talib_PPO': talib_PPO,'talib_ROC': talib_ROC,
    'talib_ROCR': talib_ROCR,'talib_RSI': talib_RSI,'talib_STOCH': talib_STOCH,'talib_STOCHRSI': talib_STOCHRSI,'ICHIMOKU':ICHIMOKU,
    'talib_TRIX': talib_TRIX, 'talib_WILLR': talib_WILLR,'talib_AD': talib_AD,'talib_ADOSC': talib_ADOSC,'talib_OBV': talib_OBV,
    'talib_TREND_VOLUME_MA':talib_TREND_VOLUME_MA,'talib_TREND_VOLUME': talib_TREND_VOLUME,'slope': slope,'slope_roc': slope_roc,'slope_trend':slope_trend,
    'slope_roc_trend':slope_roc_trend,'std': std,'stdratio': stdratio,'UPD': UPD,'LPD': LPD,'slope_diff':slope_diff,'HIGH_ROLLING':HIGH_ROLLING,'LOW_ROLLING':LOW_ROLLING,
    'DIST_FROM_HIGH': DIST_FROM_HIGH,'DIST_FROM_LOW': DIST_FROM_LOW,'DIST_OF_MA_FROM_HIGH':DIST_OF_MA_FROM_HIGH,'DIST_OF_MA_FROM_LOW':DIST_OF_MA_FROM_LOW,
    'talib_ULTOSC': talib_ULTOSC,'talib_trendIF':talib_trendIF,'talib_BETA':talib_BETA,'talib_CORREL':talib_CORREL,'VelocityATR':VelocityATR,
    'talib_LINEARREGDIFF':talib_LINEARREGDIFF,'talib_LINEARREGINTDIFF':talib_LINEARREGINTDIFF,'talib_TSFDIFF':talib_TSFDIFF,
    'talib_LINEARREG_ANGLE':talib_LINEARREG_ANGLE,'talib_LINEARREG_SLOPE':talib_LINEARREG_SLOPE,'talib_VAR':talib_VAR,'talib_STDDEV':talib_STDDEV
    }
