"""
Quantitative analysis models: returns, volatility, Sharpe, drawdown, MPT optimization.
"""

import logging
from typing import Dict, List

import numpy as np
from scipy.optimize import minimize

logger = logging.getLogger(__name__)


class QuantitativeModels:
    """Pure-function quantitative finance helpers."""

    @staticmethod
    def calculate_returns(prices: np.ndarray) -> np.ndarray:
        if len(prices) < 2:
            return np.array([])
        denom = np.where(prices[:-1] != 0, prices[:-1], 1)
        return np.diff(prices) / denom

    @staticmethod
    def calculate_log_returns(prices: np.ndarray) -> np.ndarray:
        if len(prices) < 2:
            return np.array([])
        return np.diff(np.log(np.where(prices > 0, prices, np.nan)))

    @staticmethod
    def calculate_volatility(returns: np.ndarray, annualize: bool = True) -> float:
        vol = float(np.std(returns))
        return vol * np.sqrt(252) if annualize else vol

    @staticmethod
    def calculate_sharpe_ratio(
        returns: np.ndarray, risk_free_rate: float = 0.02, annualize: bool = True
    ) -> float:
        vol = np.std(returns)
        if vol == 0:
            return 0.0
        mean = np.mean(returns)
        if annualize:
            return float((mean * 252 - risk_free_rate) / (vol * np.sqrt(252)))
        return float((mean - risk_free_rate / 252) / vol)

    @staticmethod
    def calculate_max_drawdown(prices: np.ndarray) -> float:
        if len(prices) < 2:
            return 0.0
        peak = np.maximum.accumulate(prices)
        dd = (prices - peak) / np.where(peak != 0, peak, 1)
        return float(np.min(dd))

    @staticmethod
    def calculate_beta(returns: np.ndarray, benchmark: np.ndarray) -> float:
        if len(returns) != len(benchmark) or len(returns) < 2:
            return 0.0
        bench_var = np.var(benchmark)
        if bench_var == 0:
            return 0.0
        return float(np.cov(returns, benchmark)[0, 1] / bench_var)

    @staticmethod
    def efficient_frontier(
        expected_returns: Dict[str, float],
        cov_matrix: np.ndarray,
        n_points: int = 50,
        risk_free_rate: float = 0.02,
    ) -> List[Dict[str, float]]:
        """Generate efficient frontier points via mean-variance optimization."""
        symbols = list(expected_returns.keys())
        n = len(symbols)
        if n < 2:
            return []

        mu = np.array([expected_returns[s] for s in symbols])
        min_ret, max_ret = float(np.min(mu)), float(np.max(mu))
        target_returns = np.linspace(min_ret, max_ret, n_points)
        frontier = []

        for target in target_returns:

            def portfolio_vol(w):
                return float(np.sqrt(w @ cov_matrix @ w))

            constraints = [
                {"type": "eq", "fun": lambda w: np.sum(w) - 1},
                {"type": "eq", "fun": lambda w, t=target: w @ mu - t},
            ]
            bounds = [(0, 1)] * n
            x0 = np.ones(n) / n

            res = minimize(
                portfolio_vol,
                x0,
                method="SLSQP",
                bounds=bounds,
                constraints=constraints,
            )
            if res.success:
                vol = float(res.fun)
                sharpe = (target - risk_free_rate) / vol if vol > 0 else 0.0
                frontier.append(
                    {
                        "expected_return": round(target, 4),
                        "volatility": round(vol, 4),
                        "sharpe_ratio": round(sharpe, 4),
                        "weights": {
                            s: round(float(res.x[i]), 4) for i, s in enumerate(symbols)
                        },
                    }
                )
        return frontier

    @staticmethod
    def minimum_variance_portfolio(
        cov_matrix: np.ndarray,
        symbols: List[str],
    ) -> Dict[str, float]:
        """Global minimum-variance portfolio weights."""
        n = len(symbols)
        if n < 2:
            return {}

        def vol(w):
            return float(np.sqrt(w @ cov_matrix @ w))

        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1}]
        bounds = [(0, 1)] * n
        res = minimize(
            vol, np.ones(n) / n, method="SLSQP", bounds=bounds, constraints=constraints
        )
        if not res.success:
            return {s: 1 / n for s in symbols}
        return {s: round(float(res.x[i]), 4) for i, s in enumerate(symbols)}
