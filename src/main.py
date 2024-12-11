# src/main.py
from tinkoff_api import init_sandbox_account, get_instruments_list, get_candles_custom, close_account
from data_loader import fetch_and_save_candles, load_candles_from_csv
from strategy import simple_moving_average_strategy, backtest_strategy
from make_graphics import plot_strategy, plot_performance
import pandas as pd
from datetime import datetime, timedelta


def main():
    # Инициализация песочничного аккаунта
    account_id = init_sandbox_account()
    if not account_id:
        return

    # Получение списка инструментов (акций)
    instruments = get_instruments_list()
    if not instruments:
        return

    # Выберите один инструмент для примера
    instrument = instruments[0]  # Берем первый инструмент
    figi = instrument.figi
    name = instrument.name
    print(f"Выбран инструмент: {name} (FIGI: {figi})")

    # Попробуем загрузить данные из CSV, если их нет - загрузим и сохраним
    df = load_candles_from_csv(figi)
    if df is None:
        fetch_and_save_candles(figi, days=100, interval='day')
        df = load_candles_from_csv(figi)
        if df is None:
            return

    # Применение стратегии
    df = simple_moving_average_strategy(df)

    # Визуализация стратегии
    plot_strategy(df, name)

    # Бэктестинг
    performance = backtest_strategy(df)

    # Визуализация производительности
    plot_performance(performance)

    # Закрытие песочничного аккаунта (если необходимо)
    close_account(account_id)


if __name__ == "__main__":
    main()
