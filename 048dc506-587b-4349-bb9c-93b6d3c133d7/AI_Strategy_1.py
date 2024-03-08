# trading_logic.py
# This file contains custom trading logic functions to be used in a strategy

from surmount.technical_indicators import SMA, EMA

def calculate_crossover_indicator(ticker, data):
    """
    Calculate the crossover indication based on SMA and EMA.

    :param ticker: the asset's ticker.
    :param data: historical data for the asset.
    :return: True if EMA crosses above SMA (bullish signal), otherwise False.
    """
    sma_values = SMA(ticker, data, length=50)
    ema_values = EMA(ticker, data, length=20)
    
    if sma_values is None or ema_values is None or len(sma_values) < 2 or len(ema_values) < 2:
        return False
    
    # Check for a crossover in the latest two points
    if ema_values[-2] < sma_values[-2] and ema_values[-1] > sma_values[-1]:
        return True
    else:
        return False