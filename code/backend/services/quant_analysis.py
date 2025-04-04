import numpy as np
import pandas as pd
from scipy.stats import norm

class QuantitativeModels:
    @staticmethod
    def monte_carlo_simulation(S0, mu, sigma, days=365, simulations=1000):
        dt = 1/days
        returns = np.exp((mu - 0.5 * sigma**2) * dt + 
                       sigma * np.sqrt(dt) * np.random.normal(size=(days, simulations)))
        price_path = S0 * returns.cumprod(axis=0)
        return price_path
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
        excess_returns = returns - risk_free_rate
        return excess_returns.mean() / excess_returns.std()