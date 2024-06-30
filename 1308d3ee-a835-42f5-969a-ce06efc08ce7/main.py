#Type code herefrom surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset, InstitutionalOwnership
from indicator_crossovers import crossovers

ticker = "SPY"

class TradingStrategy(Strategy):
    def __init__(self, ticker):
        self.ticker = ticker
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
        crossovers = crossovers(self.ticker, data["ohlcv"], 20)
        crossover_ema = crossovers(self.ticker, data["ohlcv"], 14)

        # Equivalent to warm-up period, if all values not ready just show allocation (aka do nothing)
        if len(crossover_sma) == 0 or len(crossover_ema) == 0:
            return TargetAllocation({})

        # Example CCI-based strategy: Enter when crossover_ema crosses above crossover_sma
        if crossover_ema[-1] > crossover_sma[-1]:
            allocation = 1  # Example fixed allocation
        else:
            allocation = 0  # No position

        return TargetAllocation({self.ticker: allocation})