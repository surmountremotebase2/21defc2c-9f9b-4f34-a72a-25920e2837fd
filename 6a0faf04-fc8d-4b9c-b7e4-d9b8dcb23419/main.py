from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
import pandas as pd
import pandas_ta as ta

ticker = "SPY"

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

class TradingStrategy(Strategy):
    def __init__(self, ticker):
        self.ticker = "SPY"
        self.data_list = []

    @property
    def interval(self):
        return "1hour"

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        crossover_values = crossovers(self.ticker, data["ohlcv"], 20, 14)

        # Equivalent to warm-up period, if all values not ready just show allocation (aka do nothing)
        if crossover_values is None or len(crossover_values[0]) == 0 or len(crossover_values[1]) == 0:
            return TargetAllocation({})

        # Example CCI-based strategy: Enter when crossover_ema crosses above crossover_sma
        if crossover_values[0][-1] > crossover_values[1][-1]:
            allocation = 1  # Example fixed allocation
        else:
            allocation = 0  # No position

        return TargetAllocation({self.ticker: allocation})