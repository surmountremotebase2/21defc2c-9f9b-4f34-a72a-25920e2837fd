from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
from indicator_cci import CCI

ticker = "TSLA"

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "TSLA"
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
        cci_fast = CCI(self.ticker, data["ohlcv"], 26)
        cci_medi = CCI(self.ticker, data["ohlcv"], 127)
        cci_slow = CCI(self.ticker, data["ohlcv"], 132)

        # Equivalent to warm-up period, if all values not ready just show allocation (aka do nothing)
        if len(cci_fast) == 0 or len(cci_medi) == 0 or len(cci_slow) == 0 :
            return TargetAllocation({})

        # Example CCI-based strategy: Enter when CCI(10) crosses above CCI(40)
        if cci_fast[-1] > 0 and cci_medi[-1] > 0 and cci_slow[-1] > 0:
            allocation = 1  # Example fixed allocation
        else:
            allocation = 0  # No position

        return TargetAllocation({self.ticker: allocation})