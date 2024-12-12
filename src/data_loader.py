import os
import pandas as pd
from tinkoff_api import get_candles_custom
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def save_candles_to_csv(figi, df):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_path = os.path.join(DATA_DIR, f"{figi}.csv")
    df.to_csv(file_path)
    print(f"Данные сохранены в {file_path}")


def load_candles_from_csv(figi):
    file_path = os.path.join(DATA_DIR, f"{figi}.csv")
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не найден.")
        return None
    df = pd.read_csv(file_path, parse_dates=['time'], index_col='time')
    print(f"Данные загружены из {file_path}")
    print(df.head())
    print(df.dtypes)
    return df


def get_quotation_value(quotation):
    return quotation.units + quotation.nano * 1e-9


def fetch_and_save_candles(figi, days=100, interval='day'):
    to_date = datetime.utcnow()
    from_date = to_date - timedelta(days=days)
    candles = get_candles_custom(figi, from_=from_date, to=to_date, interval=interval)

    if not candles:
        print("Свечи не найдены.")
        return

    data = {
        'time': [candle.time for candle in candles],
        'open': [get_quotation_value(candle.open) for candle in candles],
        'high': [get_quotation_value(candle.high) for candle in candles],
        'low': [get_quotation_value(candle.low) for candle in candles],
        'close': [get_quotation_value(candle.close) for candle in candles],
        'volume': [candle.volume for candle in candles],
    }

    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    print("Типы данных перед сохранением:")
    print(df.dtypes)

    save_candles_to_csv(figi, df)
