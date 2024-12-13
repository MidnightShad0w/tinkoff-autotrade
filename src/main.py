from tinkoff_api import init_sandbox_account, get_instruments_list, close_sandbox_account
from data_loader import fetch_and_save_candles, load_candles_from_csv
from strategy import simple_moving_average_strategy, backtest_strategy, rsi_strategy
from make_graphics import plot_strategy, plot_performance, plot_rsi_strategy
import pandas as pd
from datetime import datetime, timedelta


def main():
    use_rsi_strategy = False
    short_window = 5
    long_window = 20

    account_id = init_sandbox_account()
    if not account_id:
        return

    instruments = get_instruments_list()
    if not instruments:
        return

    instrument = instruments[222]  # выбор компании
    print(instrument)
    figi = instrument.figi
    name = instrument.name
    print(f"Выбран инструмент: {name} (FIGI: {figi})")

    df = load_candles_from_csv(figi)
    if df is None:
        fetch_and_save_candles(figi, days=200, interval='day')
        df = load_candles_from_csv(figi)
        if df is None:
            return

    # print("Типы данных после загрузки:")
    # print(df.dtypes)

    try:
        if use_rsi_strategy:
            df = rsi_strategy(df, rsi_window=14, rsi_overbought=70, rsi_oversold=30)
            plot_rsi_strategy(df, name, rsi_window=14, rsi_overbought=70, rsi_oversold=30)
        else:
            df = simple_moving_average_strategy(df, short_window=short_window, long_window=long_window)
            plot_strategy(df, name, short_window, long_window)
    except ValueError as e:
        print(f"Ошибка в стратегии: {e}")
        return

    performance = backtest_strategy(df, initial_capital=100000, commission=0.001)
    plot_performance(performance)

    final_strategy_profit = performance['Strategy Profit'].iloc[-1]
    final_market_profit = performance['Market Profit'].iloc[-1]
    print(f"Конечная прибыль стратегии: {final_strategy_profit - 100000:.2f}")
    print(f"Конечная прибыль рынка: {final_market_profit - 100000:.2f}")

    close_sandbox_account(account_id)


if __name__ == "__main__":
    main()
