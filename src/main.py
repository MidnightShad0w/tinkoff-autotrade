from tinkoff_api import init_sandbox_account, get_instruments_list, close_sandbox_account
from data_loader import fetch_and_save_candles, load_candles_from_csv
from strategy import simple_moving_average_strategy, backtest_strategy
from make_graphics import plot_strategy, plot_performance
import pandas as pd
from datetime import datetime, timedelta


def main():
    short_window = 10
    long_window = 40

    account_id = init_sandbox_account()
    if not account_id:
        return

    instruments = get_instruments_list()
    if not instruments:
        return

    instrument = instruments[0]
    figi = instrument.figi
    name = instrument.name
    print(f"Выбран инструмент: {name} (FIGI: {figi})")

    df = load_candles_from_csv(figi)
    if df is None:
        fetch_and_save_candles(figi, days=500, interval='day')
        df = load_candles_from_csv(figi)
        if df is None:
            return

    print("Типы данных после загрузки:")
    print(df.dtypes)

    try:
        df = simple_moving_average_strategy(df, short_window=short_window, long_window=long_window)
    except ValueError as e:
        print(f"Ошибка в стратегии: {e}")
        return

    plot_strategy(df, name, short_window, long_window)

    performance = backtest_strategy(df)

    plot_performance(performance)

    final_strategy_profit = performance['Strategy Profit'].iloc[-1]
    final_market_profit = performance['Market Profit'].iloc[-1]
    print(f"Конечная прибыль стратегии: {final_strategy_profit - 100000:.2f}")
    print(f"Конечная прибыль рынка: {final_market_profit - 100000:.2f}")

    close_sandbox_account(account_id)


if __name__ == "__main__":
    main()
