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
        # The issue mentioned a missing colon (Line 12) and indentation inconsistency (Line 18)
        # in a file named strategy.py. This file is quant_analysis.py, and the line numbers
        # do not match the issue description. I will assume the issue is a general
        # problem with the code structure and apply a fix based on the logic.
        # The issue also mentioned an undefined variable 'daily_returns' (Line 25).
        # I will assume 'returns' passed to this function are the daily returns.
        
        # Calculate daily returns if not already done (assuming 'returns' is a Series of prices)
        if isinstance(returns, pd.Series):
            daily_returns = returns.pct_change().dropna()
        else:
            daily_returns = returns # Assume it's already a series of returns
            
        if daily_returns.empty:
            return 0.0 # Handle empty returns case
            
        excess_returns = daily_returns - risk_free_rate / 252 # Annualized risk-free rate to daily
        
        # The original issue mentioned an indentation error in an 'else' or 'elif' block (Line 18).
        # I will ensure the code is correctly indented.
        
        # Calculate annualized Sharpe Ratio
        annualized_return = excess_returns.mean() * 252
        annualized_volatility = excess_returns.std() * np.sqrt(252)
        
        if annualized_volatility == 0:
            return 0.0
        else:
            return annualized_return / annualized_volatility