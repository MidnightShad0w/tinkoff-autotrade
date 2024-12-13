import pandas as pd
import numpy as np


def simple_moving_average_strategy(df, short_window=10, long_window=40):
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


def backtest_strategy(df, initial_capital=100000, commission=0.001, price_column='close'):
    df = df.copy()
    df['Market Returns'] = df[price_column].pct_change()

    # Инициализация
    cash = initial_capital
    shares = 0
    df['Shares'] = 0  # Кол-во акций, которыми мы владеем на конец дня
    df['Trade'] = 0  # Изменение количества акций в этот день (покупка +1, продажа -1, 0 если нет сделки)
    df['Cost'] = 0  # Сумма сделки с учётом комиссии

    for i in range(len(df)):
        signal = df['Signal'].iloc[i]
        price = df[price_column].iloc[i]

        if signal == 1:
            # Сигнал покупки одной акции
            trade_amount = price  # Стоимость 1 акции
            trade_commission = trade_amount * commission
            total_cost = trade_amount + trade_commission
            if cash >= total_cost:
                # Покупаем акцию
                shares += 1
                cash -= total_cost
                df.at[df.index[i], 'Trade'] = 1
                df.at[df.index[i], 'Cost'] = -total_cost
        elif signal == -1:
            # Сигнал продажи одной акции
            if shares > 0:
                # Есть акции для продажи
                trade_amount = price
                trade_commission = trade_amount * commission
                total_gain = trade_amount - trade_commission
                shares -= 1
                cash += total_gain
                df.at[df.index[i], 'Trade'] = -1
                df.at[df.index[i], 'Cost'] = total_gain

        # Записываем текущее количество акций
        df.at[df.index[i], 'Shares'] = shares

    # Рассчёт стоимости портфеля на каждый день
    # Стоимость портфеля = cash + shares * current_price
    df['Portfolio Value'] = cash + df['Shares'] * df[price_column]

    # Доходность стратегии = изменение Portfolio Value относительно initial_capital
    df['Strategy Returns'] = df['Portfolio Value'].pct_change().fillna(0)
    df['Cumulative Strategy Returns'] = (1 + df['Strategy Returns']).cumprod()
    df['Strategy Profit'] = df['Portfolio Value']

    # Рыночная доходность, как будто мы просто держали актив с самого начала
    # Исходя из начальной точки: initial_capital / initial_price
    initial_price = df[price_column].iloc[0]
    initial_shares = initial_capital / initial_price
    df['Market Value'] = initial_shares * df[price_column]
    df['Market Returns'] = df['Market Value'].pct_change().fillna(0)
    df['Cumulative Market Returns'] = (1 + df['Market Returns']).cumprod()
    df['Market Profit'] = df['Market Value']

    return df


def rsi_strategy(df, rsi_window=14, rsi_overbought=70, rsi_oversold=30):
    # Вычисляем RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=rsi_window, min_periods=rsi_window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_window, min_periods=rsi_window).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))

    df['Signal'] = 0
    # Покупаем, если RSI < oversold и до этого не было позиции
    df.loc[df['RSI'] < rsi_oversold, 'Signal'] = 1
    # Продаем, если RSI > overbought
    df.loc[df['RSI'] > rsi_overbought, 'Signal'] = -1

    return df
