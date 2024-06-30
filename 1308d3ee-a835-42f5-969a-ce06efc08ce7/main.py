from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
from surmount.logging import log
from indicator_vshape import vshape

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["QQQ"]

    @property
    def interval(self):
        return "1hour"

    def run(self, data):
        d = data["ohlcv"]
        qqq_stake = 0
        if len(d)>3 and "13:00" in d[-1]["QQQ"]["date"]:
            v_shape = vshape(data)
            if v_shape:
                qqq_stake = 1

        return TargetAllocation({"QQQ": qqq_stake})