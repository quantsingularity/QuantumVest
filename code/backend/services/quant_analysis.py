import numpy as np
import pandas as pd


class QuantitativeModels:

    @staticmethod
    def monte_carlo_simulation(
        S0: Any, mu: Any, sigma: Any, days: Any = 365, simulations: Any = 1000
    ) -> Any:
        dt = 1 / days
        returns = np.exp(
            (mu - 0.5 * sigma**2) * dt
            + sigma * np.sqrt(dt) * np.random.normal(size=(days, simulations))
        )
        price_path = S0 * returns.cumprod(axis=0)
        return price_path

    @staticmethod
    def calculate_sharpe_ratio(returns: Any, risk_free_rate: Any = 0.02) -> Any:
        if isinstance(returns, pd.Series):
            daily_returns = returns.pct_change().dropna()
        else:
            daily_returns = returns
        if daily_returns.empty:
            return 0.0
        excess_returns = daily_returns - risk_free_rate / 252
        annualized_return = excess_returns.mean() * 252
        annualized_volatility = excess_returns.std() * np.sqrt(252)
        if annualized_volatility == 0:
            return 0.0
        else:
            return annualized_return / annualized_volatility
