import pandas as pd

def RSI(df: pd.DataFrame, window_lenght: int = 14):
    """Relative Strength Index

    Args:
        df (pd.DataFrame): Dataframe for one ticker
        window_lenght (int, optional): Window length. Defaults to 14.

    """
    assert "Close" in df.columns
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=window_lenght, min_periods=1).mean()
    avg_loss = loss.rolling(window=window_lenght, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 * rs / (1+rs)

    return rsi

def ADR(df: pd.DataFrame, window_lenght: int = 20):
    """Advance Decline Ratio

    Args:
        df (pd.DataFrame): Dataframe having all tickers
        window_lenght (int, optional): Window length. Defaults to 20.

    """
    assert "Close" in df.columns
    ups = df.groupby("Date")["Change"].apply(lambda x: (x>0).sum())
    downs = df.groupby("Date")["Change"].apply(lambda x: (x<0).sum())

    sum_of_ups = ups.rolling(window=window_lenght, min_periods=1).sum()
    sum_of_downs = downs.rolling(window=window_lenght, min_periods=1).sum()
    adr = (sum_of_ups / sum_of_downs) * 100

    return adr

def MACD(df: pd.DataFrame, window_lenght: tuple = (12, 26)):
    """Moving Average Convergence Divergence

    Args:
        df (pd.DataFrame): Dataframe for one ticker
        window_lenght (tuple, optional): Window length. Defaults to 20.

    """
    ma1 = df["Close"].ewm(span=window_lenght[0]).mean()
    ma2 = df["Close"].ewm(span=window_lenght[1]).mean()
    macd = ma1 - ma2 # MACD
    macds = macd.ewm(span=9).mean() # Signal
    macdo = macd - macds # Oscillator

    return macdo