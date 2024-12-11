import unittest
import pandas as pd
from src.strategy import simple_moving_average_strategy, backtest_strategy


class TestStrategy(unittest.TestCase):
    def setUp(self):
        data = {
            'close': [100, 102, 101, 103, 105, 104, 106, 108, 107, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118,
                      119, 120]
        }
        self.df = pd.DataFrame(data)

    def test_simple_moving_average_strategy(self):
        df = simple_moving_average_strategy(self.df, short_window=3, long_window=5)
        self.assertIn('SMA_short', df.columns)
        self.assertIn('SMA_long', df.columns)
        self.assertIn('Signal', df.columns)
        self.assertTrue((df['Signal'].isin([0, 1, -1])).all())

    def test_backtest_strategy(self):
        df = simple_moving_average_strategy(self.df, short_window=3, long_window=5)
        performance = backtest_strategy(df)
        self.assertIn('Cumulative Returns', performance.columns)
        self.assertIn('Strategy Returns', performance.columns)
        self.assertEqual(len(performance), len(df.dropna()))


if __name__ == '__main__':
    unittest.main()
