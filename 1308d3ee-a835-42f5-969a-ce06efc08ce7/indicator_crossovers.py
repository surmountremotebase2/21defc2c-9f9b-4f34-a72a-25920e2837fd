from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
import pandas as pd
import pandas_ta as ta

def crossovers(ticker, data, length1, length2):
    '''Calculate the crossover between two indicators for the given ticker.

    :param ticker: a string ticker
    :param data: data as provided from the OHLCV data function
    :param length1: the window for the sma
    :param length2: the window for the ema

    :return: list with float values
    '''
    high = [i[ticker]["high"] for i in data]
    low = [i[ticker]["low"] for i in data]
    close = [i[ticker]["close"] for i in data]

    # DataFrame to hold high, low, and close values
    df = pd.DataFrame({
        'high': high,
        'low': low,
        'close': close
    })

    indicator1 = ta.sma(df['high'], df['low'], df['close'], length=length1)
    indicator2 = ta.ema(df['high'], df['low'], df['close'], length=length2)
    
    if indicator1 is None or indicator2 is None:
        return None
    return indicator1.tolist(), indicator2.tolist()