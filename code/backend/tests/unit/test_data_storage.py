"""Unit tests for DataStorage."""

import os

import numpy as np
import pandas as pd
import pytest
from pipeline.data_storage import DataStorage


def sample_df(symbol: str = "TEST") -> pd.DataFrame:
    np.random.seed(0)
    close = 100 * np.cumprod(1 + np.random.normal(0, 0.01, 30))
    return pd.DataFrame(
        {
            "timestamp": pd.date_range("2024-01-01", periods=30),
            "open": close,
            "high": close * 1.01,
            "low": close * 0.99,
            "close": close,
            "volume": np.random.randint(1_000, 10_000, 30).astype(float),
            "symbol": symbol,
        }
    )


@pytest.fixture
def storage(tmp_path):
    return DataStorage(data_dir=str(tmp_path))


class TestDataStorage:
    def test_save_and_load_stock(self, storage):
        df = sample_df("AAPL")
        path = storage.save_stock_data(df, "AAPL")
        assert os.path.exists(path)
        loaded = storage.load_stock_data("AAPL")
        assert loaded is not None
        assert not loaded.empty
        assert len(loaded) == len(df)

    def test_save_and_load_crypto(self, storage):
        df = sample_df("BTC")
        path = storage.save_crypto_data(df, "BTC")
        assert os.path.exists(path)
        loaded = storage.load_crypto_data("BTC")
        assert loaded is not None
        assert len(loaded) == len(df)

    def test_load_nonexistent_returns_none(self, storage):
        assert storage.load_stock_data("NONEXISTENT") is None
        assert storage.load_crypto_data("NONEXISTENT") is None

    def test_save_empty_df_returns_empty_string(self, storage):
        result = storage.save_stock_data(pd.DataFrame(), "EMPTY")
        assert result == ""

    def test_timestamp_parsed_on_load(self, storage):
        df = sample_df("TSLA")
        storage.save_stock_data(df, "TSLA")
        loaded = storage.load_stock_data("TSLA")
        assert pd.api.types.is_datetime64_any_dtype(loaded["timestamp"])

    def test_symbol_case_insensitive_path(self, storage):
        df = sample_df("btc")
        storage.save_crypto_data(df, "BTC")
        loaded_upper = storage.load_crypto_data("BTC")
        loaded_lower = storage.load_crypto_data("btc")
        assert loaded_upper is not None
        assert loaded_lower is not None
