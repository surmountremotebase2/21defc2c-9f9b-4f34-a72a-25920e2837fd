from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
import pandas_ta as ta
import pandas as pd
import indicator_cci



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
        cci_fast = CCI("TSLA", data["ohlcv"], 26)
        cci_medi = CCI("TSLA", data["ohlcv"], 127)
        cci_slow = CCI("TSLA", data["ohlcv"], 132)

        # Equivalent to warm-up period, if all values not ready just show allocation (aka do nothing)
        if len(cci_fast) == 0 or len(cci_medi) == 0 or len(cci_slow) == 0 :
                return TargetAllocation({})

        # Example CCI-based strategy: Enter when CCI(10) crosses above CCI(40)
        if cci_fast[-1] > 0 and cci_medi[-1] > 0 and cci_slow[-1] > 0:
                allocation = 1  # Example fixed allocation
        else:
                allocation = 0  # No position

        return TargetAllocation({"TSLA": allocation})