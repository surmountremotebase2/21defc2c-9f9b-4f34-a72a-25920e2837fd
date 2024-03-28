from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
import pandas_ta as ta
import pandas as pd

def CCI(ticker, data, length):
    '''Calculate the Commodity Channel Index (CCI) for the given ticker.

    :param ticker: a string ticker
    :param data: data as provided from the OHLCV data function
    :param length: the window

    :return: list with float CCI values
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

    cci = ta.cci(df['high'], df['low'], df['close'], length=length)
    if cci is None:
        return None
    return cci.tolist()

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TSLA"]
        self.data_list = []

    @property
    def interval(self):
        return "1hour"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        cci_fast = CCI("TSLA", data["ohlcv"], 10)
        cci_medi = CCI("TSLA", data["ohlcv"], 20)
        cci_slow = CCI("TSLA", data["ohlcv"], 40)

        # Equivalent to warm-up period, if all values not ready just show allocation (aka do nothing)
        if len(cci_fast) == 0 or len(cci_medi) == 0 or len(cci_slow) == 0 :
                return TargetAllocation({})

        # Example CCI-based strategy: Enter when CCI(10) crosses above CCI(40)
        if cci_fast[-1] > 0 and cci_medi[-1] > 0 and cci_slow[-1] > 0:
                allocation = 1  # Example fixed allocation
        else:
                allocation = 0  # No position

        return TargetAllocation({"TSLA": allocation})