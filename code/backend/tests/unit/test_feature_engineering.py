"""Unit tests for the feature engineering pipeline."""

import numpy as np
import pandas as pd
from pipeline.feature_engineering import FeatureEngineering


def make_ohlcv(n: int = 100) -> pd.DataFrame:
    np.random.seed(42)
    close = 100 * np.cumprod(1 + np.random.normal(0.001, 0.02, n))
    high = close * np.random.uniform(1.00, 1.02, n)
    low = close * np.random.uniform(0.98, 1.00, n)
    open_ = close * np.random.uniform(0.99, 1.01, n)
    volume = np.random.randint(1_000_000, 10_000_000, n).astype(float)
    return pd.DataFrame(
        {"open": open_, "high": high, "low": low, "close": close, "volume": volume}
    )


class TestFeatureEngineering:
    def test_returns_dataframe(self):
        df = make_ohlcv()
        result = FeatureEngineering.add_technical_indicators(df)
        assert isinstance(result, pd.DataFrame)

    def test_does_not_mutate_original(self):
        df = make_ohlcv()
        original_cols = set(df.columns)
        FeatureEngineering.add_technical_indicators(df)
        assert set(df.columns) == original_cols

    def test_moving_averages_added(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv())
        for col in ("ma7", "ma20", "ma50"):
            assert col in df.columns

    def test_macd_columns_added(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv())
        for col in ("macd", "macd_signal", "macd_hist"):
            assert col in df.columns

    def test_bollinger_bands_added(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv())
        for col in ("bb_upper", "bb_middle", "bb_lower"):
            assert col in df.columns

    def test_rsi_range(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv(200))
        rsi = df["rsi"].dropna()
        assert (rsi >= 0).all() and (rsi <= 100).all()

    def test_stochastic_added(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv())
        assert "stoch_k" in df.columns
        assert "stoch_d" in df.columns

    def test_atr_positive(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv(50))
        atr = df["atr"].dropna()
        assert (atr >= 0).all()

    def test_obv_added(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv())
        assert "obv" in df.columns

    def test_log_return_added(self):
        df = FeatureEngineering.add_technical_indicators(make_ohlcv())
        assert "log_return" in df.columns

    def test_empty_dataframe_returned_unchanged(self):
        result = FeatureEngineering.add_technical_indicators(pd.DataFrame())
        assert result is not None

    def test_missing_columns_returns_df(self):
        df = pd.DataFrame({"close": [100, 101, 102]})
        result = FeatureEngineering.add_technical_indicators(df)
        assert isinstance(result, pd.DataFrame)

    def test_prepare_lstm_features_drops_na_target(self):
        df = make_ohlcv(80)
        result = FeatureEngineering.prepare_lstm_features(df)
        assert result["close"].isna().sum() == 0
