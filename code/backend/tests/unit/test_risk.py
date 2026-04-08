"""Unit tests for the risk management service."""

import numpy as np
import pytest
from app.services.risk import RiskManagementService


class TestVaR:
    @pytest.fixture(autouse=True)
    def returns(self):
        np.random.seed(42)
        self.ret = np.random.normal(0.001, 0.02, 1000)

    def test_historical_var_is_negative(self):
        var = RiskManagementService.calculate_var(
            self.ret, alpha=0.05, method="historical"
        )
        assert var < 0

    def test_parametric_var_is_negative(self):
        var = RiskManagementService.calculate_var(
            self.ret, alpha=0.05, method="parametric"
        )
        assert var < 0

    def test_monte_carlo_var_is_negative(self):
        var = RiskManagementService.calculate_var(
            self.ret, alpha=0.05, method="monte_carlo"
        )
        assert var < 0

    def test_99_var_worse_than_95(self):
        var95 = RiskManagementService.calculate_var(self.ret, alpha=0.05)
        var99 = RiskManagementService.calculate_var(self.ret, alpha=0.01)
        assert var99 <= var95

    def test_invalid_method_raises(self):
        with pytest.raises(ValueError):
            RiskManagementService.calculate_var(self.ret, method="unknown")

    def test_cvar_worse_than_var(self):
        var = RiskManagementService.calculate_var(self.ret, alpha=0.05)
        cvar = RiskManagementService.calculate_cvar(self.ret, alpha=0.05)
        assert cvar <= var


class TestMetrics:
    @pytest.fixture(autouse=True)
    def data(self):
        np.random.seed(0)
        self.ret = np.random.normal(0.001, 0.015, 500)
        self.bench = np.random.normal(0.0008, 0.012, 500)

    def test_metrics_keys(self):
        m = RiskManagementService.calculate_metrics(self.ret)
        for key in (
            "annualized_return",
            "volatility",
            "sharpe_ratio",
            "max_drawdown",
            "skewness",
            "kurtosis",
            "var_95",
            "cvar_95",
        ):
            assert key in m, f"Missing key: {key}"

    def test_benchmark_adds_alpha_beta(self):
        m = RiskManagementService.calculate_metrics(self.ret, self.bench)
        assert "beta" in m
        assert "alpha" in m
        assert "information_ratio" in m

    def test_volatility_positive(self):
        m = RiskManagementService.calculate_metrics(self.ret)
        assert m["volatility"] > 0

    def test_max_drawdown_nonpositive(self):
        m = RiskManagementService.calculate_metrics(self.ret)
        assert m["max_drawdown"] <= 0


class TestStressTest:
    def test_market_shock(self):
        weights = {"AAPL": 0.5, "MSFT": 0.5}
        scenarios = [{"name": "Crash", "market_shock": -0.20}]
        results = RiskManagementService.stress_test(100_000, weights, scenarios)
        assert len(results) == 1
        r = results[0]
        assert r["scenario_name"] == "Crash"
        assert r["stressed_value"] == pytest.approx(80_000, rel=1e-6)
        assert r["percentage_impact"] == pytest.approx(-20.0, rel=1e-4)

    def test_asset_specific_shock(self):
        weights = {"AAPL": 0.6, "MSFT": 0.4}
        scenarios = [
            {"name": "Tech selloff", "asset_shocks": {"AAPL": -0.30}, "market_shock": 0}
        ]
        results = RiskManagementService.stress_test(100_000, weights, scenarios)
        assert results[0]["stressed_value"] == pytest.approx(82_000, rel=1e-6)


class TestConcentrationRisk:
    def test_uniform_weights(self):
        w = [0.25, 0.25, 0.25, 0.25]
        r = RiskManagementService.concentration_risk(w)
        assert r["herfindahl_index"] == pytest.approx(0.25, rel=1e-4)
        assert r["concentration_level"] == "Medium"

    def test_highly_concentrated(self):
        w = [0.9, 0.05, 0.03, 0.02]
        r = RiskManagementService.concentration_risk(w)
        assert r["concentration_level"] == "High"
        assert r["largest_holding_weight"] == pytest.approx(0.9, rel=1e-4)

    def test_well_diversified(self):
        w = [0.05] * 20
        r = RiskManagementService.concentration_risk(w)
        assert r["concentration_level"] == "Low"

    def test_empty_weights(self):
        r = RiskManagementService.concentration_risk([])
        assert "error" in r
