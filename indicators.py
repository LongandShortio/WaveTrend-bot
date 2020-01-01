import logging
import pandas as pd
import numpy as np
log = logging.getLogger(__name__)


def HA( dataframe ):
    """
    Returns Heikin Ashi candles
    """

    df = dataframe.copy()

    df['HA_Close']=(df.open + df.high + df.low + df.close)/4

    df.reset_index(inplace=True)

    ha_open = [ (df.open[0] + df.close[0]) / 2 ]
    [ ha_open.append((ha_open[i] + df.HA_Close.values[i]) / 2) \
    for i in range(0, len(df)-1) ]
    df['HA_Open'] = ha_open

    df.set_index('index', inplace=True)

    df['HA_High']=df[['HA_Open','HA_Close','high']].max(axis=1)
    df['HA_Low']=df[['HA_Open','HA_Close','low']].min(axis=1)

    return df



def wave_trend(df, n1=10, n2=21):
    """
    Computes the wave trend indicators
    """
    df_ha=HA(df)
    ap=(df_ha['HA_High']+df_ha['HA_Low']+df_ha['HA_Close'])/3
    esa=ap.ewm(span=n1, min_periods=n1).mean().dropna() #ema(ap, n1)
    d=abs(ap - esa).ewm(span=n1, min_periods=n1).mean().dropna() #ema(abs(ap - esa), n1)
    ci=(ap.iloc[-len(ap):] - esa) / (0.015 * d)
    tci =ci.ewm(span=n2, min_periods=n2).mean().dropna() #ema(ci, n2)
    wt1 = tci
    wt2 = wt1.rolling(4, min_periods=4).mean().dropna() #sma(wt1,4)
    diff=wt1.iloc[-len(wt2):]-wt2
    diff= pd.DataFrame(diff, index=df.index, columns=['diff'])
    return diff.dropna()
