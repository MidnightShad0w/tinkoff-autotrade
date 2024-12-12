import os
from dotenv import load_dotenv
from tinkoff.invest import Client, RequestError
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.services import CandleInterval
from datetime import datetime

load_dotenv()

TOKEN = os.getenv("TINKOFF_API_SANDBOX_TOKEN")
if not TOKEN:
    raise ValueError("Не найдено значение TINKOFF_API_SANDBOX_TOKEN в переменных окружения.")


def init_sandbox_account():
    """
    Создаёт аккаунт и возвращает его ID.
    """
    try:
        with SandboxClient(TOKEN) as client:
            sandbox_account = client.sandbox.open_sandbox_account(name="danek")
            print(f"Аккаунт создан: {sandbox_account}")

            all_accounts = client.users.get_accounts()
            print(f"Все аккаунты: {all_accounts}")

            account_id = all_accounts.accounts[0].id
            print(f"Аккаунт ID: {account_id}")

        return account_id
    except RequestError as e:
        print(f"Ошибка при создании аккаунта: {e}")
        return None


def close_sandbox_account(account_id):
    """
    Закрывает аккаунт по его ID.
    """
    try:
        with SandboxClient(TOKEN) as client:
            response = client.sandbox.close_sandbox_account(account_id=account_id)
            print(f"Аккаунт {account_id} закрыт: {response}")
    except RequestError as e:
        print(f"Ошибка при закрытии аккаунта: {e}")


def get_instruments_list():
    """
    Получает список доступных акций.
    """
    try:
        with SandboxClient(TOKEN) as client:
            response = client.instruments.shares()
            instruments = response.instruments
            print(f"Найдено {len(instruments)} акций.")
            return instruments
    except RequestError as e:
        print(f"Ошибка при получении списка инструментов: {e}")
        return []


def get_candles_custom(figi, from_, to, interval='day'):
    """
    Получает исторические котировки для заданного FIGI.
    Использует перечисление CandleInterval для интервала.
    """
    try:
        interval_map = {
            '1_min': CandleInterval.CANDLE_INTERVAL_1_MIN,
            '5_min': CandleInterval.CANDLE_INTERVAL_5_MIN,
            '15_min': CandleInterval.CANDLE_INTERVAL_15_MIN,
            '30_min': CandleInterval.CANDLE_INTERVAL_30_MIN,
            'hour': CandleInterval.CANDLE_INTERVAL_HOUR,
            'day': CandleInterval.CANDLE_INTERVAL_DAY,
            'week': CandleInterval.CANDLE_INTERVAL_WEEK,
            'month': CandleInterval.CANDLE_INTERVAL_MONTH,
        }

        if interval not in interval_map:
            raise ValueError(f"Неизвестный интервал: {interval}")

        interval_enum = interval_map[interval]
        print(f"Используем интервал: {interval_enum}, тип: {type(interval_enum)}")

        with SandboxClient(TOKEN) as client:
            response = client.market_data.get_candles(
                figi=figi,
                from_=from_,
                to=to,
                interval=interval_enum
            )
            candles = response.candles
            print(f"Получено {len(candles)} свечей для FIGI {figi}.")
            return candles
    except RequestError as e:
        print(f"Ошибка при получении свечей: {e}")
        return []
    except ValueError as ve:
        print(f"Ошибка: {ve}")
        return []
