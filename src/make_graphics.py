import matplotlib.pyplot as plt


def plot_strategy(df, instrument_name, short_window, long_window):
    df = df.copy()
    shares = 0
    filtered_signals = []  # список кортежей (index, signal, price)

    for i in range(len(df)):
        signal = df['Signal'].iloc[i]
        price = df['close'].iloc[i]
        current_index = df.index[i]

        if signal == 1:
            # Попытка купить
            if shares == 0:
                # Покупаем
                shares = 1
                filtered_signals.append((current_index, 1, price))
            else:
                # Уже есть акция, игнорируем этот сигнал
                pass
        elif signal == -1:
            # Попытка продать
            if shares == 1:
                # Есть акция, продаём
                shares = 0
                filtered_signals.append((current_index, -1, price))
            else:
                # Нет акции для продажи, игнорируем
                pass
        # Если 0, ничего не делаем

    buy_signals = [(idx, p) for (idx, s, p) in filtered_signals if s == 1]
    sell_signals = [(idx, p) for (idx, s, p) in filtered_signals if s == -1]

    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['close'], label='Цена', color='blue')
    if 'SMA_short' in df.columns and 'SMA_long' in df.columns:
        plt.plot(df.index, df['SMA_short'], label=f'SMA_short ({short_window})', color='green')
        plt.plot(df.index, df['SMA_long'], label=f'SMA_long ({long_window})', color='red')

    if buy_signals:
        b_idx, b_price = zip(*buy_signals)
        plt.scatter(b_idx, b_price, marker='^', color='green', label='Покупка', s=100)

    if sell_signals:
        s_idx, s_price = zip(*sell_signals)
        plt.scatter(s_idx, s_price, marker='v', color='red', label='Продажа', s=100)

    plt.title(f'Стратегия на основе скользящих средних для {instrument_name}')
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_rsi_strategy(df, instrument_name, rsi_window=14, rsi_overbought=70, rsi_oversold=30):
    df = df.copy()

    shares = 0
    filtered_signals = []

    for i in range(len(df)):
        signal = df['Signal'].iloc[i]
        price = df['close'].iloc[i]
        current_index = df.index[i]

        if signal == 1:  # покупка
            if shares == 0:
                shares = 1
                filtered_signals.append((current_index, 1, price))
        elif signal == -1:  # продажа
            if shares == 1:
                shares = 0
                filtered_signals.append((current_index, -1, price))
        # Если 0, ничего не делаем

    buy_signals = [(idx, p) for (idx, s, p) in filtered_signals if s == 1]
    sell_signals = [(idx, p) for (idx, s, p) in filtered_signals if s == -1]

    fig, (ax_price, ax_rsi) = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

    ax_price.plot(df.index, df['close'], label='Цена', color='blue')

    if buy_signals:
        b_idx, b_price = zip(*buy_signals)
        ax_price.scatter(b_idx, b_price, marker='^', color='green', label='Покупка', s=100)

    if sell_signals:
        s_idx, s_price = zip(*sell_signals)
        ax_price.scatter(s_idx, s_price, marker='v', color='red', label='Продажа', s=100)

    ax_price.set_title(f'RSI Стратегия для {instrument_name}')
    ax_price.set_ylabel('Цена')
    ax_price.legend()
    ax_price.grid(True)

    if 'RSI' in df.columns:
        ax_rsi.plot(df.index, df['RSI'], color='orange', label=f'RSI ({rsi_window})')
        ax_rsi.axhline(y=rsi_overbought, color='red', linestyle='--', label=f'Перекупленность ({rsi_overbought})')
        ax_rsi.axhline(y=rsi_oversold, color='green', linestyle='--', label=f'Перепроданность ({rsi_oversold})')
        ax_rsi.set_ylabel('RSI')
        ax_rsi.set_xlabel('Дата')
        ax_rsi.grid(True)
        ax_rsi.legend()
    else:
        ax_rsi.text(0.5, 0.5, 'RSI не рассчитан', ha='center', va='center', transform=ax_rsi.transAxes)
        ax_rsi.set_ylabel('RSI')
        ax_rsi.set_xlabel('Дата')
        ax_rsi.grid(True)

    plt.tight_layout()
    plt.show()


def plot_performance(df):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Cumulative Market Returns'], label='Рыночные доходности', color='blue')
    plt.plot(df.index, df['Cumulative Strategy Returns'], label='Доходности стратегии', color='orange')
    plt.title('Сравнение кумулятивных доходностей стратегии и рынка')
    plt.xlabel('Дата')
    plt.ylabel('Кумулятивная доходность')
    plt.legend()
    plt.grid(True)
    plt.show()
