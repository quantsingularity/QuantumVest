import joblib
import pandas as pd
from pypfopt import EfficientFrontier, expected_returns, risk_models


def train_optimization_model() -> Any:
    df = pd.read_csv(
        "../../resources/datasets/historical_trends.csv", index_col=0, parse_dates=True
    )
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)
    ef = EfficientFrontier(mu, S)
    ef.max_sharpe()
    weights = ef.clean_weights()
    joblib.dump(weights, "../../optimization_model.pkl")


if __name__ == "__main__":
    train_optimization_model()
