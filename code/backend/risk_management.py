"""
Risk Management Service for QuantumVest
Advanced risk assessment and management tools for portfolios
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import numpy as np
from models import PortfolioHolding, PriceData
from scipy import stats

logger = logging.getLogger(__name__)


class RiskManagementService:
    """Service for portfolio risk assessment and management"""

    @staticmethod
    def calculate_var(
        portfolio_id: str,
        confidence_level: float = 0.95,
        time_horizon: int = 1,
        method: str = "historical",
    ) -> Dict:
        """Calculate Value at Risk (VaR) for a portfolio"""
        try:
            # Get portfolio holdings
            holdings = PortfolioHolding.query.filter_by(portfolio_id=portfolio_id).all()

            if not holdings:
                return {"success": False, "error": "No holdings found in portfolio"}

            # Get historical returns for each asset
            portfolio_returns = RiskManagementService._get_portfolio_returns(
                portfolio_id, days=252
            )

            if portfolio_returns is None or len(portfolio_returns) < 30:
                return {
                    "success": False,
                    "error": "Insufficient historical data for VaR calculation",
                }

            # Calculate VaR based on method
            if method == "historical":
                var = RiskManagementService._historical_var(
                    portfolio_returns, confidence_level, time_horizon
                )
            elif method == "parametric":
                var = RiskManagementService._parametric_var(
                    portfolio_returns, confidence_level, time_horizon
                )
            elif method == "monte_carlo":
                var = RiskManagementService._monte_carlo_var(
                    portfolio_returns, confidence_level, time_horizon
                )
            else:
                return {"success": False, "error": "Invalid VaR method"}

            # Calculate Expected Shortfall (Conditional VaR)
            expected_shortfall = RiskManagementService._calculate_expected_shortfall(
                portfolio_returns, confidence_level, time_horizon
            )

            return {
                "success": True,
                "var": {
                    "value": float(var),
                    "confidence_level": confidence_level,
                    "time_horizon_days": time_horizon,
                    "method": method,
                    "expected_shortfall": float(expected_shortfall),
                    "interpretation": f"{confidence_level*100}% confidence that losses will not exceed {abs(var):.2%} over {time_horizon} day(s)",
                },
            }

        except Exception as e:
            logger.error(f"Error calculating VaR: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def calculate_portfolio_metrics(
        portfolio_id: str, benchmark_symbol: str = "SPY"
    ) -> Dict:
        """Calculate comprehensive portfolio risk metrics"""
        try:
            # Get portfolio returns
            portfolio_returns = RiskManagementService._get_portfolio_returns(
                portfolio_id, days=252
            )

            if portfolio_returns is None or len(portfolio_returns) < 30:
                return {"success": False, "error": "Insufficient historical data"}

            # Get benchmark returns
            benchmark_returns = RiskManagementService._get_benchmark_returns(
                benchmark_symbol, len(portfolio_returns)
            )

            # Calculate metrics
            metrics = {}

            # Basic statistics
            metrics["mean_return"] = float(
                np.mean(portfolio_returns) * 252
            )  # Annualized
            metrics["volatility"] = float(
                np.std(portfolio_returns) * np.sqrt(252)
            )  # Annualized
            metrics["skewness"] = float(stats.skew(portfolio_returns))
            metrics["kurtosis"] = float(stats.kurtosis(portfolio_returns))

            # Risk-adjusted returns
            risk_free_rate = 0.02  # Assume 2% risk-free rate
            excess_returns = portfolio_returns - (risk_free_rate / 252)

            if metrics["volatility"] > 0:
                metrics["sharpe_ratio"] = float(
                    np.mean(excess_returns) / np.std(portfolio_returns) * np.sqrt(252)
                )
            else:
                metrics["sharpe_ratio"] = 0

            # Downside risk metrics
            downside_returns = portfolio_returns[portfolio_returns < 0]
            if len(downside_returns) > 0:
                metrics["downside_deviation"] = float(
                    np.std(downside_returns) * np.sqrt(252)
                )
                metrics["sortino_ratio"] = float(
                    metrics["mean_return"] / metrics["downside_deviation"]
                )
            else:
                metrics["downside_deviation"] = 0
                metrics["sortino_ratio"] = float("inf")

            # Maximum drawdown
            cumulative_returns = (1 + portfolio_returns).cumprod()
            peak = np.maximum.accumulate(cumulative_returns)
            drawdown = (cumulative_returns - peak) / peak
            metrics["max_drawdown"] = float(np.min(drawdown))

            # Beta and correlation with benchmark
            if benchmark_returns is not None and len(benchmark_returns) == len(
                portfolio_returns
            ):
                covariance = np.cov(portfolio_returns, benchmark_returns)[0, 1]
                benchmark_variance = np.var(benchmark_returns)

                if benchmark_variance > 0:
                    metrics["beta"] = float(covariance / benchmark_variance)
                    metrics["correlation_with_benchmark"] = float(
                        np.corrcoef(portfolio_returns, benchmark_returns)[0, 1]
                    )

                    # Alpha calculation
                    benchmark_mean = np.mean(benchmark_returns) * 252
                    metrics["alpha"] = float(
                        metrics["mean_return"]
                        - (
                            risk_free_rate
                            + metrics["beta"] * (benchmark_mean - risk_free_rate)
                        )
                    )
                else:
                    metrics["beta"] = 0
                    metrics["correlation_with_benchmark"] = 0
                    metrics["alpha"] = 0
            else:
                metrics["beta"] = None
                metrics["correlation_with_benchmark"] = None
                metrics["alpha"] = None

            # Information ratio
            if benchmark_returns is not None:
                active_returns = portfolio_returns - benchmark_returns
                tracking_error = np.std(active_returns) * np.sqrt(252)
                if tracking_error > 0:
                    metrics["information_ratio"] = float(
                        np.mean(active_returns) * 252 / tracking_error
                    )
                else:
                    metrics["information_ratio"] = 0
            else:
                metrics["information_ratio"] = None

            return {"success": True, "metrics": metrics}

        except Exception as e:
            logger.error(f"Error calculating portfolio metrics: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def stress_test_portfolio(portfolio_id: str, scenarios: List[Dict]) -> Dict:
        """Perform stress testing on portfolio"""
        try:
            # Get current portfolio value and holdings
            holdings = PortfolioHolding.query.filter_by(portfolio_id=portfolio_id).all()

            if not holdings:
                return {"success": False, "error": "No holdings found in portfolio"}

            current_value = sum(float(h.market_value or 0) for h in holdings)

            if current_value == 0:
                return {"success": False, "error": "Portfolio has no market value"}

            stress_results = []

            for scenario in scenarios:
                scenario_name = scenario.get("name", "Unnamed Scenario")
                asset_shocks = scenario.get("asset_shocks", {})
                market_shock = scenario.get("market_shock", 0)

                # Calculate portfolio value under stress
                stressed_value = 0

                for holding in holdings:
                    asset_symbol = holding.asset.symbol
                    current_holding_value = float(holding.market_value or 0)

                    # Apply asset-specific shock if available
                    if asset_symbol in asset_shocks:
                        shock = asset_shocks[asset_symbol]
                    else:
                        shock = market_shock

                    stressed_holding_value = current_holding_value * (1 + shock)
                    stressed_value += stressed_holding_value

                # Calculate impact
                absolute_impact = stressed_value - current_value
                percentage_impact = (absolute_impact / current_value) * 100

                stress_results.append(
                    {
                        "scenario_name": scenario_name,
                        "current_value": current_value,
                        "stressed_value": stressed_value,
                        "absolute_impact": absolute_impact,
                        "percentage_impact": percentage_impact,
                    }
                )

            return {"success": True, "stress_test_results": stress_results}

        except Exception as e:
            logger.error(f"Error performing stress test: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def calculate_concentration_risk(portfolio_id: str) -> Dict:
        """Calculate concentration risk metrics"""
        try:
            holdings = PortfolioHolding.query.filter_by(portfolio_id=portfolio_id).all()

            if not holdings:
                return {"success": False, "error": "No holdings found in portfolio"}

            total_value = sum(float(h.market_value or 0) for h in holdings)

            if total_value == 0:
                return {"success": False, "error": "Portfolio has no market value"}

            # Calculate weights
            weights = [float(h.market_value or 0) / total_value for h in holdings]

            # Herfindahl-Hirschman Index (HHI)
            hhi = sum(w**2 for w in weights)

            # Effective number of holdings
            effective_holdings = 1 / hhi if hhi > 0 else 0

            # Concentration ratio (top 5 holdings)
            sorted_weights = sorted(weights, reverse=True)
            top_5_concentration = sum(sorted_weights[:5])

            # Largest holding weight
            max_weight = max(weights) if weights else 0

            # Risk assessment
            if hhi > 0.25:
                concentration_level = "High"
            elif hhi > 0.15:
                concentration_level = "Medium"
            else:
                concentration_level = "Low"

            return {
                "success": True,
                "concentration_metrics": {
                    "herfindahl_index": float(hhi),
                    "effective_number_of_holdings": float(effective_holdings),
                    "top_5_concentration": float(top_5_concentration),
                    "largest_holding_weight": float(max_weight),
                    "concentration_level": concentration_level,
                    "total_holdings": len(holdings),
                },
            }

        except Exception as e:
            logger.error(f"Error calculating concentration risk: {e}")
            return {"success": False, "error": str(e)}

    @staticmethod
    def _get_portfolio_returns(
        portfolio_id: str, days: int = 252
    ) -> Optional[np.ndarray]:
        """Get historical portfolio returns"""
        try:
            # This is a simplified implementation
            # In practice, you would calculate daily portfolio values and returns
            holdings = PortfolioHolding.query.filter_by(portfolio_id=portfolio_id).all()

            if not holdings:
                return None

            # For now, return mock returns based on a weighted average of asset returns
            # In production, this should use actual portfolio value history
            all_returns = []
            total_weight = 0

            for holding in holdings:
                asset_returns = RiskManagementService._get_asset_returns(
                    holding.asset_id, days
                )
                if asset_returns is not None:
                    weight = float(holding.market_value or 0)
                    all_returns.append(asset_returns * weight)
                    total_weight += weight

            if not all_returns or total_weight == 0:
                return None

            # Weighted average of returns
            portfolio_returns = sum(all_returns) / total_weight
            return portfolio_returns

        except Exception as e:
            logger.error(f"Error getting portfolio returns: {e}")
            return None

    @staticmethod
    def _get_asset_returns(asset_id: str, days: int = 252) -> Optional[np.ndarray]:
        """Get historical returns for an asset"""
        try:
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=days)

            price_data = (
                PriceData.query.filter(
                    PriceData.asset_id == asset_id,
                    PriceData.timestamp >= start_date,
                    PriceData.timestamp <= end_date,
                    PriceData.interval == "1d",
                )
                .order_by(PriceData.timestamp)
                .all()
            )

            if len(price_data) < 2:
                return None

            prices = np.array([float(p.close_price) for p in price_data])
            returns = np.diff(prices) / prices[:-1]

            return returns

        except Exception as e:
            logger.error(f"Error getting asset returns: {e}")
            return None

    @staticmethod
    def _get_benchmark_returns(symbol: str, length: int) -> Optional[np.ndarray]:
        """Get benchmark returns"""
        try:
            # This would typically fetch benchmark data from an external API
            # For now, return mock data
            np.random.seed(42)  # For reproducible results
            return np.random.normal(0.0008, 0.012, length)  # Mock S&P 500 returns

        except Exception as e:
            logger.error(f"Error getting benchmark returns: {e}")
            return None

    @staticmethod
    def _historical_var(
        returns: np.ndarray, confidence_level: float, time_horizon: int
    ) -> float:
        """Calculate historical VaR"""
        # Scale returns for time horizon
        scaled_returns = returns * np.sqrt(time_horizon)

        # Calculate percentile
        percentile = (1 - confidence_level) * 100
        var = np.percentile(scaled_returns, percentile)

        return var

    @staticmethod
    def _parametric_var(
        returns: np.ndarray, confidence_level: float, time_horizon: int
    ) -> float:
        """Calculate parametric VaR assuming normal distribution"""
        mean = np.mean(returns)
        std = np.std(returns)

        # Scale for time horizon
        scaled_mean = mean * time_horizon
        scaled_std = std * np.sqrt(time_horizon)

        # Calculate VaR using normal distribution
        z_score = stats.norm.ppf(1 - confidence_level)
        var = scaled_mean + z_score * scaled_std

        return var

    @staticmethod
    def _monte_carlo_var(
        returns: np.ndarray,
        confidence_level: float,
        time_horizon: int,
        simulations: int = 10000,
    ) -> float:
        """Calculate Monte Carlo VaR"""
        mean = np.mean(returns)
        std = np.std(returns)

        # Generate random scenarios
        np.random.seed(42)  # For reproducible results
        simulated_returns = np.random.normal(mean, std, simulations * time_horizon)
        simulated_returns = simulated_returns.reshape(simulations, time_horizon)

        # Calculate cumulative returns for each simulation
        cumulative_returns = np.sum(simulated_returns, axis=1)

        # Calculate VaR
        percentile = (1 - confidence_level) * 100
        var = np.percentile(cumulative_returns, percentile)

        return var

    @staticmethod
    def _calculate_expected_shortfall(
        returns: np.ndarray, confidence_level: float, time_horizon: int
    ) -> float:
        """Calculate Expected Shortfall (Conditional VaR)"""
        # Scale returns for time horizon
        scaled_returns = returns * np.sqrt(time_horizon)

        # Calculate VaR threshold
        percentile = (1 - confidence_level) * 100
        var_threshold = np.percentile(scaled_returns, percentile)

        # Calculate expected shortfall as mean of returns below VaR
        tail_returns = scaled_returns[scaled_returns <= var_threshold]

        if len(tail_returns) > 0:
            expected_shortfall = np.mean(tail_returns)
        else:
            expected_shortfall = var_threshold

        return expected_shortfall
