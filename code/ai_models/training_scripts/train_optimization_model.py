import pandas as pd
from pypfopt import EfficientFrontier, risk_models, expected_returns
import joblib

def train_optimization_model():
    # Load historical price data
    df = pd.read_csv('../../resources/datasets/historical_trends.csv', index_col=0, parse_dates=True)
    
    # Calculate expected returns and covariance matrix
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)
    
    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S)
    ef.max_sharpe()
    weights = ef.clean_weights()
    
    joblib.dump(weights, '../../optimization_model.pkl')

if __name__ == '__main__':
    train_optimization_model();