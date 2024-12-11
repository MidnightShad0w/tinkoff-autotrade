import matplotlib.pyplot as plt


def plot_strategy(df, instrument_name):
    """
    Визуализирует стратегию на графике цены с сигналами.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['close'], label='Цена', color='blue')
    plt.plot(df.index, df['SMA_short'], label='Короткая SMA', color='green')
    plt.plot(df.index, df['SMA_long'], label='Длинная SMA', color='red')

    buy_signals = df[df['Signal'] == 1]
    sell_signals = df[df['Signal'] == -1]

    plt.scatter(buy_signals.index, buy_signals['close'], marker='^', color='green', label='Покупка', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['close'], marker='v', color='red', label='Продажа', alpha=1)

    plt.title(f'Стратегия на основе скользящих средних для {instrument_name}')
    plt.xlabel('Дата')
    plt.ylabel('Цена')
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_performance(performance_df):
    """
    Визуализирует производительность стратегии против рыночного индекса.
    """
    plt.figure(figsize=(14, 7))
    plt.plot(performance_df.index, performance_df['Cumulative Returns'], label='Рыночные доходности', color='blue')
    plt.plot(performance_df.index, performance_df['Strategy Returns'], label='Доходности стратегии', color='orange')
    plt.title('Сравнение доходностей стратегии и рынка')
    plt.xlabel('Дата')
    plt.ylabel('Кумулятивная доходность')
    plt.legend()
    plt.grid(True)
    plt.show()
