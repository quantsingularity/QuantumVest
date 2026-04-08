"""Unit tests for quantitative models."""

import numpy as np
import pytest
from app.services.quant import QuantitativeModels


class TestReturns:
    def test_basic_returns(self):
        prices = np.array([100.0, 110.0, 105.0])
        rets = QuantitativeModels.calculate_returns(prices)
        assert len(rets) == 2
        assert rets[0] == pytest.approx(0.10, rel=1e-4)
        assert rets[1] == pytest.approx(-1 / 22, rel=1e-4)

    def test_empty_input(self):
        rets = QuantitativeModels.calculate_returns(np.array([100.0]))
        assert len(rets) == 0

    def test_log_returns(self):
        prices = np.array([100.0, np.e * 100])  # 1 unit log return
        log_rets = QuantitativeModels.calculate_log_returns(prices)
        assert log_rets[0] == pytest.approx(1.0, rel=1e-5)


class TestVolatility:
    def test_annualised_vol(self):
        np.random.seed(1)
        rets = np.random.normal(0, 0.01, 252)
        vol = QuantitativeModels.calculate_volatility(rets, annualize=True)
        # Should be ~0.01 * sqrt(252) ≈ 0.159
        assert 0.10 < vol < 0.25

    def test_no_annualise(self):
        np.random.seed(1)
        rets = np.random.normal(0, 0.01, 100)
        vol_daily = QuantitativeModels.calculate_volatility(rets, annualize=False)
        vol_annual = QuantitativeModels.calculate_volatility(rets, annualize=True)
        assert vol_annual == pytest.approx(vol_daily * np.sqrt(252), rel=1e-5)


class TestSharpe:
    def test_positive_sharpe(self):
        np.random.seed(42)
        rets = np.random.normal(0.001, 0.01, 252)
        sr = QuantitativeModels.calculate_sharpe_ratio(rets, risk_free_rate=0.0)
        assert sr > 0

    def test_zero_vol_returns_zero(self):
        rets = np.zeros(100)
        sr = QuantitativeModels.calculate_sharpe_ratio(rets)
        assert sr == 0.0


class TestMaxDrawdown:
    def test_monotonic_increase_zero_drawdown(self):
        prices = np.linspace(100, 200, 50)
        dd = QuantitativeModels.calculate_max_drawdown(prices)
        assert dd == pytest.approx(0.0, abs=1e-10)

    def test_known_drawdown(self):
        prices = np.array([100.0, 150.0, 75.0, 125.0])
        dd = QuantitativeModels.calculate_max_drawdown(prices)
        assert dd == pytest.approx(-0.5, rel=1e-4)


class TestBeta:
    def test_unit_beta(self):
        np.random.seed(7)
        rets = np.random.normal(0, 0.01, 200)
        beta = QuantitativeModels.calculate_beta(rets, rets)
        assert beta == pytest.approx(1.0, rel=1e-2)

    def test_mismatched_length_returns_zero(self):
        beta = QuantitativeModels.calculate_beta(np.ones(10), np.ones(20))
        assert beta == 0.0


class TestEfficientFrontier:
    def test_returns_list(self):
        np.random.seed(0)
        rets_df = {"A": 0.10, "B": 0.15}
        cov = np.array([[0.04, 0.01], [0.01, 0.09]])
        frontier = QuantitativeModels.efficient_frontier(rets_df, cov, n_points=10)
        assert isinstance(frontier, list)
        assert len(frontier) > 0
        for pt in frontier:
            assert "expected_return" in pt
            assert "volatility" in pt
            assert "weights" in pt

    def test_single_asset_returns_empty(self):
        frontier = QuantitativeModels.efficient_frontier(
            {"A": 0.10}, np.array([[0.04]])
        )
        assert frontier == []
