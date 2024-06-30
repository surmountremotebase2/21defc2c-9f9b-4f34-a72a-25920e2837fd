from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, SMA
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        # Define assets of interest - in this case, SPY
        return ["SPY"]

    @property
    def interval(self):
        # Define the interval for data fetching; daily in this example
        return "1day"

    def run(self, data):
        # Initialize SPY stake to 0, meaning no position by default
        spy_stake = 0

        # Extract the closing prices for SPY from the provided data
        close_prices = [i["SPY"]["close"] for i in data["ohlcv"]]

        # Check to ensure that there are enough data points for both EMA and SMA calculation
        if len(close_prices) >= 20:
            # Calculate EMA and SMA for the SPY
            ema_20 = EMA("SPY", data["ohlcv"], 20)
            sma_14 = SMA("SPY", data["ohlcv"], 14)

            # Check if EMA(20) has crossed above SMA(14) in the most recent data
            if ema_20[-1] > sma_14[-1] and ema_20[-2] < sma_14[-2]:
                # If EMA crosses above SMA, set SPY stake to 1 (100% allocation)
                spy_stake = 1
                log("EMA(20) crossed above SMA(14) for SPY, buying")
            else:
                # Log the condition when there's no crossover
                log("No EMA(20) and SMA(14) crossover detected for SPY")

        # Return allocation as per above logic
        return Targetmodation({"SPY": spy_stake})