

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