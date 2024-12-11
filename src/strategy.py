import pandas as pd


def simple_moving_average_strategy(df, short_window=20, long_window=50):
    """
    Простейшая стратегия на основе скользящих средних.
    Генерирует сигналы покупки и продажи.
    """
    df['SMA_short'] = df['close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['close'].rolling(window=long_window).mean()

    df['Signal'] = 0
    df.loc[df['SMA_short'] > df['SMA_long'], 'Signal'] = 1
    df.loc[df['SMA_short'] < df['SMA_long'], 'Signal'] = -1

    return df


def backtest_strategy(df):
    """
    Простая функция для бэктестинга стратегии.
    """
    df = df.copy().dropna()
    df['Returns'] = df['close'].pct_change()
    df['Strategy'] = df['Signal'].shift(1) * df['Returns']

    cumulative_returns = (1 + df['Returns']).cumprod() - 1
    cumulative_strategy = (1 + df['Strategy']).cumprod() - 1

    performance = pd.DataFrame({
        'Cumulative Returns': cumulative_returns,
        'Strategy Returns': cumulative_strategy
    })

    return performance
