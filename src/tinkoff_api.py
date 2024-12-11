import os
from dotenv import load_dotenv
from tinkoff.invest import Client, RequestError
from tinkoff.invest.sandbox.client import SandboxClient
from tinkoff.invest.services import CandleInterval

load_dotenv()

TOKEN = os.getenv("TINKOFF_API_SANDBOX_TOKEN")
REAL_TOKEN = os.getenv("TINKOFF_API_REAL_TOKEN")
if not TOKEN:
    raise ValueError("Не найдено значение TINKOFF_API_SANDBOX_TOKEN в переменных окружения.")


# client = SandboxClient(TOKEN)
market_client = Client(REAL_TOKEN)

def init_sandbox_account():
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


def close_account(account_id):
    try:
        with SandboxClient(TOKEN) as client:
            response = client.sandbox.close_sandbox_account(account_id=account_id)
            print(f"Аккаунт {account_id} закрыт: {response}")
    except RequestError as e:
        print(f"Ошибка при закрытии аккаунта: {e}")


def get_instruments_list():
    try:
        # Инициализация клиента
        with SandboxClient(TOKEN) as client:
            response = client.instruments.shares()
            instruments = response.instruments
            print(f"Найдено {len(instruments)} акций.")
            return instruments
    except RequestError as e:
        print(f"Ошибка при получении списка инструментов: {e}")
        return []


def get_candles_custom(figi, from_, to, interval='day'):
    try:
        # Переводим строковый интервал в соответствующее перечисление
        if interval == 'day':
            interval_enum = CandleInterval.CANDLE_INTERVAL_DAY
        elif interval == 'week':
            interval_enum = CandleInterval.CANDLE_INTERVAL_WEEK
        elif interval == 'month':
            interval_enum = CandleInterval.CANDLE_INTERVAL_MONTH
        else:
            raise ValueError(f"Неизвестный интервал: {interval}")

        with market_client as client:
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
