import pandas as pd
import numpy as np


def simple_moving_average_strategy(df, short_window=10, long_window=40):
    """
    Реализует простую стратегию на основе пересечений скользящих средних.
    """
    if short_window >= long_window:
        raise ValueError("short_window должен быть меньше long_window.")

    df['SMA_short'] = df['close'].rolling(window=short_window, min_periods=short_window).mean()
    df['SMA_long'] = df['close'].rolling(window=long_window, min_periods=long_window).mean()

    df['Signal'] = 0

    df.loc[
        (df['SMA_short'] > df['SMA_long']) &
        (df['SMA_short'].shift(1) <= df['SMA_long'].shift(1)),
        'Signal'
    ] = 1

    df.loc[
        (df['SMA_short'] < df['SMA_long']) &
        (df['SMA_short'].shift(1) >= df['SMA_long'].shift(1)),
        'Signal'
    ] = -1

    return df


def backtest_strategy(df, initial_capital=100000, commission=0.001):
    """
    Простейший бэктест для стратегии скользящих средних с учётом комиссии.
    """
    df['Position'] = df['Signal'].replace(to_replace=0, method='ffill').shift(1)
    df['Position'] = df['Position'].fillna(0)

    df['Market Returns'] = df['close'].pct_change()
    df['Strategy Returns'] = df['Market Returns'] * df['Position']

    df['Trade'] = df['Signal'].diff().abs()
    df['Strategy Returns'] -= df['Trade'] * commission

    df['Cumulative Market Returns'] = (1 + df['Market Returns']).cumprod()
    df['Cumulative Strategy Returns'] = (1 + df['Strategy Returns']).cumprod()

    df['Cumulative Max'] = df['Cumulative Strategy Returns'].cummax()
    df['Drawdown'] = df['Cumulative Max'] - df['Cumulative Strategy Returns']
    df['Drawdown Percentage'] = df['Drawdown'] / df['Cumulative Max']

    df['Strategy Profit'] = initial_capital * df['Cumulative Strategy Returns']
    df['Market Profit'] = initial_capital * df['Cumulative Market Returns']

    return df
