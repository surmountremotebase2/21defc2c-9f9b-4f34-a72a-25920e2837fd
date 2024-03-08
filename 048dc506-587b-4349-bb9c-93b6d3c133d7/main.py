from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    def __init__(self):
        self.tickers = ["AAPL", "MSFT"]
        self.short_ema_length = 12
        self.long_ema_length = 26

    @property
    def interval(self):
        # Specifies the data interval to be used: daily data.
        return "1day"

    @property
    def assets(self):
        # List of assets that the strategy will analyze and trade.
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        
        for ticker in self.tickers:
            # Calculate Short-term and Long-term EMA for each ticker
            short_ema = EMA(ticker, data["ohlcv"], length=self.short_ema_length)
            long_ema = EMA(ticker, data["ohlcv"], length=self.long_ema_length)
            
            if len(short_ema) == 0 or len(long_ema) == 0:
                # If there's not enough data to compute the EMAs, skip this cycle.
                log(f"Not enough data to compute EMAs for {ticker}")
                continue
            
            # Check for the EMA crossover; Buy signal: Short EMA crosses above Long EMA
            if short_ema[-1] > long_ema[-1] and short_ema[-2] < long_ema[-2]:
                log(f"Buy signal for {ticker}")
                allocation_dict[ticker] = 0.5 # allocating 50% of capital to this asset
            # Sell signal: Short EMA crosses below Long EMA
            elif short_ema[-1] < long_ema[-1] and short_ema[-2] > long_ema[-2]:
                log(f"Sell signal for {ticker}")
                allocation_dict[ticker] = 0   # Exiting the position
            else:
                # If there's no crossover, maintain the current allocation
                log(f"No EMA crossover for {ticker}, maintaining current allocation.")
                # Here, you can choose to maintain the current allocation, or adjust accordingly.
                # For simplicity, this example will keep the position as is without buying or selling additional shares.
                # This part can be adjusted based on the strategy's needs.
                allocation_dict[ticker] = allocation_dict.get(ticker, 0)
                
        return TargetAllocation(allocation_dict)