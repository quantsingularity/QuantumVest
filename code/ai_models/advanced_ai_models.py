"""
Advanced AI Models for QuantumVest
State-of-the-art machine learning models for financial forecasting, risk assessment, and portfolio optimization
"""

import logging
import pickle
import warnings
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
import tensorflow as tf
import xgboost as xgb
from catboost import CatBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import (GridSearchCV, TimeSeriesSplit,
                                     train_test_split)
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler
from tensorflow import keras
from tensorflow.keras import callbacks, layers, models, optimizers

warnings.filterwarnings("ignore")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedTimeSeriesPredictor:
    """
    Advanced time series prediction model using ensemble methods and deep learning
    """

    def __init__(self, model_type: str = "ensemble"):
        """
        Initialize the predictor

        Args:
            model_type: Type of model ('lstm', 'transformer', 'ensemble', 'xgboost', 'lightgbm')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.feature_scaler = RobustScaler()
        self.is_trained = False
        self.feature_importance = None
        self.training_history = None

    def create_features(
        self, data: pd.DataFrame, target_col: str = "close"
    ) -> pd.DataFrame:
        """
        Create advanced technical and statistical features
        """
        df = data.copy()

        # Price-based features
        df["returns"] = df[target_col].pct_change()
        df["log_returns"] = np.log(df[target_col] / df[target_col].shift(1))
        df["volatility"] = df["returns"].rolling(window=20).std()

        # Moving averages
        for window in [5, 10, 20, 50, 100, 200]:
            df[f"ma_{window}"] = df[target_col].rolling(window=window).mean()
            df[f"ma_ratio_{window}"] = df[target_col] / df[f"ma_{window}"]

        # Exponential moving averages
        for span in [12, 26, 50]:
            df[f"ema_{span}"] = df[target_col].ewm(span=span).mean()

        # MACD
        df["macd"] = df["ema_12"] - df["ema_26"]
        df["macd_signal"] = df["macd"].ewm(span=9).mean()
        df["macd_histogram"] = df["macd"] - df["macd_signal"]

        # RSI
        delta = df[target_col].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["rsi"] = 100 - (100 / (1 + rs))

        # Bollinger Bands
        df["bb_middle"] = df[target_col].rolling(window=20).mean()
        bb_std = df[target_col].rolling(window=20).std()
        df["bb_upper"] = df["bb_middle"] + (bb_std * 2)
        df["bb_lower"] = df["bb_middle"] - (bb_std * 2)
        df["bb_width"] = df["bb_upper"] - df["bb_lower"]
        df["bb_position"] = (df[target_col] - df["bb_lower"]) / df["bb_width"]

        # Volume features (if available)
        if "volume" in df.columns:
            df["volume_ma"] = df["volume"].rolling(window=20).mean()
            df["volume_ratio"] = df["volume"] / df["volume_ma"]
            df["price_volume"] = df[target_col] * df["volume"]
            df["vwap"] = (
                df["price_volume"].rolling(window=20).sum()
                / df["volume"].rolling(window=20).sum()
            )

        # Statistical features
        for window in [5, 10, 20]:
            df[f"std_{window}"] = df[target_col].rolling(window=window).std()
            df[f"skew_{window}"] = df[target_col].rolling(window=window).skew()
            df[f"kurt_{window}"] = df[target_col].rolling(window=window).kurt()

        # Lag features
        for lag in [1, 2, 3, 5, 10]:
            df[f"lag_{lag}"] = df[target_col].shift(lag)
            df[f"returns_lag_{lag}"] = df["returns"].shift(lag)

        # Time-based features
        df["hour"] = df.index.hour if hasattr(df.index, "hour") else 0
        df["day_of_week"] = df.index.dayofweek if hasattr(df.index, "dayofweek") else 0
        df["month"] = df.index.month if hasattr(df.index, "month") else 0
        df["quarter"] = df.index.quarter if hasattr(df.index, "quarter") else 0

        # Cyclical encoding for time features
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
        df["day_sin"] = np.sin(2 * np.pi * df["day_of_week"] / 7)
        df["day_cos"] = np.cos(2 * np.pi * df["day_of_week"] / 7)
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

        return df

    def prepare_sequences(
        self, data: np.ndarray, sequence_length: int = 60, prediction_horizon: int = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepare sequences for LSTM/Transformer models
        """
        X, y = [], []

        for i in range(sequence_length, len(data) - prediction_horizon + 1):
            X.append(data[i - sequence_length : i])
            y.append(data[i : i + prediction_horizon])

        return np.array(X), np.array(y)

    def build_lstm_model(
        self, input_shape: Tuple[int, int], prediction_horizon: int = 1
    ) -> keras.Model:
        """
        Build advanced LSTM model with attention mechanism
        """
        inputs = keras.Input(shape=input_shape)

        # LSTM layers with dropout
        lstm1 = layers.LSTM(
            128, return_sequences=True, dropout=0.2, recurrent_dropout=0.2
        )(inputs)
        lstm2 = layers.LSTM(
            64, return_sequences=True, dropout=0.2, recurrent_dropout=0.2
        )(lstm1)
        lstm3 = layers.LSTM(
            32, return_sequences=False, dropout=0.2, recurrent_dropout=0.2
        )(lstm2)

        # Dense layers
        dense1 = layers.Dense(50, activation="relu")(lstm3)
        dense1 = layers.Dropout(0.3)(dense1)
        dense2 = layers.Dense(25, activation="relu")(dense1)
        dense2 = layers.Dropout(0.2)(dense2)

        # Output layer
        outputs = layers.Dense(prediction_horizon, activation="linear")(dense2)

        model = keras.Model(inputs=inputs, outputs=outputs)

        # Compile with advanced optimizer
        optimizer = optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999)
        model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

        return model

    def build_transformer_model(
        self, input_shape: Tuple[int, int], prediction_horizon: int = 1
    ) -> keras.Model:
        """
        Build Transformer model for time series prediction
        """
        inputs = keras.Input(shape=input_shape)

        # Positional encoding
        positions = tf.range(start=0, limit=input_shape[0], delta=1)
        positions = tf.cast(positions, tf.float32)

        # Multi-head attention
        attention_output = layers.MultiHeadAttention(
            num_heads=8, key_dim=64, dropout=0.1
        )(inputs, inputs)

        # Add & Norm
        attention_output = layers.Dropout(0.1)(attention_output)
        attention_output = layers.LayerNormalization(epsilon=1e-6)(
            inputs + attention_output
        )

        # Feed forward network
        ffn_output = layers.Dense(128, activation="relu")(attention_output)
        ffn_output = layers.Dropout(0.1)(ffn_output)
        ffn_output = layers.Dense(input_shape[1])(ffn_output)

        # Add & Norm
        ffn_output = layers.LayerNormalization(epsilon=1e-6)(
            attention_output + ffn_output
        )

        # Global average pooling
        pooled = layers.GlobalAveragePooling1D()(ffn_output)

        # Final dense layers
        dense1 = layers.Dense(64, activation="relu")(pooled)
        dense1 = layers.Dropout(0.2)(dense1)
        outputs = layers.Dense(prediction_horizon, activation="linear")(dense1)

        model = keras.Model(inputs=inputs, outputs=outputs)

        # Compile
        optimizer = optimizers.Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

        return model

    def train(
        self,
        data: pd.DataFrame,
        target_col: str = "close",
        validation_split: float = 0.2,
        epochs: int = 100,
    ) -> Dict[str, Any]:
        """
        Train the prediction model
        """
        logger.info(f"Training {self.model_type} model...")

        # Create features
        df_features = self.create_features(data, target_col)
        df_features = df_features.dropna()

        if len(df_features) < 100:
            raise ValueError(
                "Insufficient data for training (minimum 100 samples required)"
            )

        # Prepare target variable
        target = df_features[target_col].values

        if self.model_type in ["lstm", "transformer"]:
            # For deep learning models
            sequence_length = 60
            prediction_horizon = 1

            # Scale the data
            scaled_data = self.scaler.fit_transform(target.reshape(-1, 1))

            # Prepare sequences
            X, y = self.prepare_sequences(
                scaled_data.flatten(), sequence_length, prediction_horizon
            )

            # Split data
            split_idx = int(len(X) * (1 - validation_split))
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]

            # Reshape for model input
            X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
            X_val = X_val.reshape((X_val.shape[0], X_val.shape[1], 1))

            # Build model
            if self.model_type == "lstm":
                self.model = self.build_lstm_model(
                    (sequence_length, 1), prediction_horizon
                )
            else:  # transformer
                self.model = self.build_transformer_model(
                    (sequence_length, 1), prediction_horizon
                )

            # Callbacks
            early_stopping = callbacks.EarlyStopping(
                monitor="val_loss", patience=15, restore_best_weights=True
            )
            reduce_lr = callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.5, patience=10, min_lr=1e-7
            )

            # Train model
            history = self.model.fit(
                X_train,
                y_train,
                validation_data=(X_val, y_val),
                epochs=epochs,
                batch_size=32,
                callbacks=[early_stopping, reduce_lr],
                verbose=1,
            )

            self.training_history = history.history

        else:
            # For traditional ML models
            # Select relevant features
            feature_cols = [
                col
                for col in df_features.columns
                if col not in [target_col]
                and not col.startswith("ma_")
                or col.endswith("_ratio")
            ]

            X = df_features[feature_cols].values
            y = target

            # Handle missing values
            X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)

            # Scale features
            X_scaled = self.feature_scaler.fit_transform(X)

            # Split data
            X_train, X_val, y_train, y_val = train_test_split(
                X_scaled, y, test_size=validation_split, random_state=42, shuffle=False
            )

            if self.model_type == "ensemble":
                # Create ensemble of models
                models = {
                    "xgb": xgb.XGBRegressor(
                        n_estimators=200,
                        max_depth=6,
                        learning_rate=0.1,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        random_state=42,
                    ),
                    "lgb": lgb.LGBMRegressor(
                        n_estimators=200,
                        max_depth=6,
                        learning_rate=0.1,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        random_state=42,
                    ),
                    "cat": CatBoostRegressor(
                        iterations=200,
                        depth=6,
                        learning_rate=0.1,
                        random_seed=42,
                        verbose=False,
                    ),
                    "rf": RandomForestRegressor(
                        n_estimators=100, max_depth=10, random_state=42
                    ),
                }

                # Train all models
                trained_models = {}
                for name, model in models.items():
                    model.fit(X_train, y_train)
                    trained_models[name] = model

                self.model = trained_models

                # Calculate feature importance (using XGBoost as reference)
                self.feature_importance = dict(
                    zip(feature_cols, models["xgb"].feature_importances_)
                )

            elif self.model_type == "xgboost":
                self.model = xgb.XGBRegressor(
                    n_estimators=300,
                    max_depth=8,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=42,
                )
                self.model.fit(X_train, y_train)
                self.feature_importance = dict(
                    zip(feature_cols, self.model.feature_importances_)
                )

            elif self.model_type == "lightgbm":
                self.model = lgb.LGBMRegressor(
                    n_estimators=300,
                    max_depth=8,
                    learning_rate=0.05,
                    subsample=0.8,
                    colsample_bytree=0.8,
                    random_state=42,
                )
                self.model.fit(X_train, y_train)
                self.feature_importance = dict(
                    zip(feature_cols, self.model.feature_importances_)
                )

        self.is_trained = True
        logger.info("Model training completed successfully")

        # Calculate training metrics
        train_predictions = self.predict(data.tail(len(df_features)))
        actual_values = df_features[target_col].values[-len(train_predictions) :]

        metrics = {
            "mse": mean_squared_error(actual_values, train_predictions),
            "mae": mean_absolute_error(actual_values, train_predictions),
            "r2": r2_score(actual_values, train_predictions),
            "training_samples": len(df_features),
        }

        return metrics

    def predict(
        self, data: pd.DataFrame, target_col: str = "close", steps_ahead: int = 1
    ) -> np.ndarray:
        """
        Make predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        # Create features
        df_features = self.create_features(data, target_col)
        df_features = df_features.dropna()

        if self.model_type in ["lstm", "transformer"]:
            # For deep learning models
            sequence_length = 60

            if len(df_features) < sequence_length:
                raise ValueError(
                    f"Insufficient data for prediction (minimum {sequence_length} samples required)"
                )

            # Scale the data
            target_values = df_features[target_col].values
            scaled_data = self.scaler.transform(target_values.reshape(-1, 1))

            # Prepare last sequence
            last_sequence = scaled_data[-sequence_length:].reshape(
                1, sequence_length, 1
            )

            # Make prediction
            scaled_prediction = self.model.predict(last_sequence)
            prediction = self.scaler.inverse_transform(scaled_prediction.reshape(-1, 1))

            return prediction.flatten()

        else:
            # For traditional ML models
            feature_cols = [
                col
                for col in df_features.columns
                if col not in [target_col]
                and not col.startswith("ma_")
                or col.endswith("_ratio")
            ]

            X = df_features[feature_cols].values
            X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
            X_scaled = self.feature_scaler.transform(X)

            if self.model_type == "ensemble":
                # Ensemble prediction
                predictions = []
                for model in self.model.values():
                    pred = model.predict(X_scaled)
                    predictions.append(pred)

                # Average predictions
                ensemble_pred = np.mean(predictions, axis=0)
                return ensemble_pred[-steps_ahead:]

            else:
                prediction = self.model.predict(X_scaled)
                return prediction[-steps_ahead:]

    def save_model(self, filepath: str):
        """Save the trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")

        model_data = {
            "model_type": self.model_type,
            "scaler": self.scaler,
            "feature_scaler": self.feature_scaler,
            "feature_importance": self.feature_importance,
            "training_history": self.training_history,
            "is_trained": self.is_trained,
        }

        if self.model_type in ["lstm", "transformer"]:
            # Save Keras model separately
            self.model.save(f"{filepath}_keras_model")
            model_data["keras_model_path"] = f"{filepath}_keras_model"
        else:
            model_data["model"] = self.model

        # Save with joblib
        joblib.dump(model_data, f"{filepath}.pkl")
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """Load a trained model"""
        try:
            # Load model data
            model_data = joblib.load(f"{filepath}.pkl")

            self.model_type = model_data["model_type"]
            self.scaler = model_data["scaler"]
            self.feature_scaler = model_data["feature_scaler"]
            self.feature_importance = model_data["feature_importance"]
            self.training_history = model_data["training_history"]
            self.is_trained = model_data["is_trained"]

            if self.model_type in ["lstm", "transformer"]:
                # Load Keras model
                self.model = keras.models.load_model(model_data["keras_model_path"])
            else:
                self.model = model_data["model"]

            logger.info(f"Model loaded from {filepath}")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise


class PortfolioOptimizer:
    """
    Advanced portfolio optimization using modern portfolio theory and machine learning
    """

    def __init__(self):
        self.expected_returns = None
        self.covariance_matrix = None
        self.risk_free_rate = 0.02  # 2% risk-free rate

    def calculate_expected_returns(
        self, returns_data: pd.DataFrame, method: str = "mean_historical"
    ) -> pd.Series:
        """
        Calculate expected returns using various methods
        """
        if method == "mean_historical":
            return returns_data.mean() * 252  # Annualized

        elif method == "exponential_weighted":
            return returns_data.ewm(span=60).mean().iloc[-1] * 252

        elif method == "capm":
            # Simplified CAPM implementation
            market_returns = returns_data.mean(axis=1)  # Market proxy
            betas = {}
            alphas = {}

            for asset in returns_data.columns:
                asset_returns = returns_data[asset].dropna()
                market_aligned = market_returns.loc[asset_returns.index]

                if len(asset_returns) > 30:
                    covariance = np.cov(asset_returns, market_aligned)[0, 1]
                    market_variance = np.var(market_aligned)
                    beta = covariance / market_variance if market_variance > 0 else 1.0
                    alpha = np.mean(asset_returns) - beta * np.mean(market_aligned)
                else:
                    beta = 1.0
                    alpha = 0.0

                betas[asset] = beta
                alphas[asset] = alpha

            market_return = np.mean(market_returns) * 252
            expected_returns = {}

            for asset in returns_data.columns:
                expected_returns[asset] = self.risk_free_rate + betas[asset] * (
                    market_return - self.risk_free_rate
                )

            return pd.Series(expected_returns)

        else:
            raise ValueError(f"Unknown method: {method}")

    def calculate_covariance_matrix(
        self, returns_data: pd.DataFrame, method: str = "sample"
    ) -> pd.DataFrame:
        """
        Calculate covariance matrix using various methods
        """
        if method == "sample":
            return returns_data.cov() * 252  # Annualized

        elif method == "exponential_weighted":
            return (
                returns_data.ewm(span=60).cov().iloc[-len(returns_data.columns) :] * 252
            )

        elif method == "shrinkage":
            # Ledoit-Wolf shrinkage
            sample_cov = returns_data.cov() * 252

            # Target matrix (diagonal with average variance)
            avg_var = np.trace(sample_cov) / len(sample_cov)
            target = np.eye(len(sample_cov)) * avg_var

            # Shrinkage intensity (simplified)
            shrinkage = 0.2

            return (1 - shrinkage) * sample_cov + shrinkage * target

        else:
            raise ValueError(f"Unknown method: {method}")

    def optimize_portfolio(
        self,
        returns_data: pd.DataFrame,
        objective: str = "max_sharpe",
        constraints: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Optimize portfolio allocation
        """
        # Calculate expected returns and covariance matrix
        self.expected_returns = self.calculate_expected_returns(returns_data)
        self.covariance_matrix = self.calculate_covariance_matrix(returns_data)

        n_assets = len(self.expected_returns)

        # Default constraints
        if constraints is None:
            constraints = {
                "max_weight": 0.4,  # Maximum 40% in any single asset
                "min_weight": 0.0,  # No short selling
                "sum_weights": 1.0,  # Fully invested
            }

        try:
            import cvxpy as cp

            # Decision variables
            weights = cp.Variable(n_assets)

            # Objective functions
            portfolio_return = self.expected_returns.values @ weights
            portfolio_variance = cp.quad_form(weights, self.covariance_matrix.values)
            portfolio_volatility = cp.sqrt(portfolio_variance)

            if objective == "max_sharpe":
                # Maximize Sharpe ratio (approximate)
                objective_func = cp.Maximize(portfolio_return - self.risk_free_rate)
                constraints_list = [
                    portfolio_variance <= 0.04,  # Max 20% volatility
                    cp.sum(weights) == constraints["sum_weights"],
                ]

            elif objective == "min_variance":
                objective_func = cp.Minimize(portfolio_variance)
                constraints_list = [cp.sum(weights) == constraints["sum_weights"]]

            elif objective == "max_return":
                objective_func = cp.Maximize(portfolio_return)
                constraints_list = [
                    portfolio_variance <= 0.09,  # Max 30% volatility
                    cp.sum(weights) == constraints["sum_weights"],
                ]

            else:
                raise ValueError(f"Unknown objective: {objective}")

            # Add weight constraints
            if "max_weight" in constraints:
                constraints_list.append(weights <= constraints["max_weight"])

            if "min_weight" in constraints:
                constraints_list.append(weights >= constraints["min_weight"])

            # Solve optimization problem
            problem = cp.Problem(objective_func, constraints_list)
            problem.solve()

            if problem.status == cp.OPTIMAL:
                optimal_weights = weights.value

                # Calculate portfolio metrics
                portfolio_return_val = float(
                    self.expected_returns.values @ optimal_weights
                )
                portfolio_variance_val = float(
                    optimal_weights.T @ self.covariance_matrix.values @ optimal_weights
                )
                portfolio_volatility_val = np.sqrt(portfolio_variance_val)
                sharpe_ratio = (
                    portfolio_return_val - self.risk_free_rate
                ) / portfolio_volatility_val

                return {
                    "success": True,
                    "weights": dict(zip(self.expected_returns.index, optimal_weights)),
                    "expected_return": portfolio_return_val,
                    "volatility": portfolio_volatility_val,
                    "sharpe_ratio": sharpe_ratio,
                    "objective": objective,
                }

            else:
                return {
                    "success": False,
                    "error": f"Optimization failed with status: {problem.status}",
                }

        except ImportError:
            logger.warning("CVXPY not available, using scipy optimization")
            return self._optimize_with_scipy(objective, constraints)

        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return {"success": False, "error": str(e)}

    def _optimize_with_scipy(
        self, objective: str, constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Fallback optimization using scipy
        """
        from scipy.optimize import minimize

        n_assets = len(self.expected_returns)

        def portfolio_metrics(weights):
            portfolio_return = np.dot(weights, self.expected_returns.values)
            portfolio_variance = np.dot(
                weights.T, np.dot(self.covariance_matrix.values, weights)
            )
            portfolio_volatility = np.sqrt(portfolio_variance)
            sharpe_ratio = (
                portfolio_return - self.risk_free_rate
            ) / portfolio_volatility
            return portfolio_return, portfolio_volatility, sharpe_ratio

        # Objective function
        if objective == "max_sharpe":

            def objective_func(weights):
                _, volatility, sharpe = portfolio_metrics(weights)
                return -sharpe  # Minimize negative Sharpe ratio

        elif objective == "min_variance":

            def objective_func(weights):
                _, volatility, _ = portfolio_metrics(weights)
                return volatility**2

        elif objective == "max_return":

            def objective_func(weights):
                portfolio_return, _, _ = portfolio_metrics(weights)
                return -portfolio_return

        # Constraints
        constraints_list = [{"type": "eq", "fun": lambda x: np.sum(x) - 1}]  # Sum to 1

        # Bounds
        bounds = tuple(
            (constraints.get("min_weight", 0), constraints.get("max_weight", 1))
            for _ in range(n_assets)
        )

        # Initial guess
        x0 = np.array([1.0 / n_assets] * n_assets)

        # Optimize
        result = minimize(
            objective_func,
            x0,
            method="SLSQP",
            bounds=bounds,
            constraints=constraints_list,
        )

        if result.success:
            optimal_weights = result.x
            portfolio_return, portfolio_volatility, sharpe_ratio = portfolio_metrics(
                optimal_weights
            )

            return {
                "success": True,
                "weights": dict(zip(self.expected_returns.index, optimal_weights)),
                "expected_return": portfolio_return,
                "volatility": portfolio_volatility,
                "sharpe_ratio": sharpe_ratio,
                "objective": objective,
            }

        else:
            return {
                "success": False,
                "error": f"Scipy optimization failed: {result.message}",
            }


class RiskAssessmentModel:
    """
    Advanced risk assessment model using machine learning
    """

    def __init__(self):
        self.var_model = None
        self.volatility_model = None
        self.correlation_model = None
        self.is_trained = False

    def calculate_var(
        self, returns: np.ndarray, confidence_level: float = 0.05
    ) -> float:
        """
        Calculate Value at Risk using multiple methods
        """
        # Historical VaR
        historical_var = np.percentile(returns, confidence_level * 100)

        # Parametric VaR (assuming normal distribution)
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        from scipy.stats import norm

        parametric_var = norm.ppf(confidence_level, mean_return, std_return)

        # Monte Carlo VaR
        np.random.seed(42)
        simulated_returns = np.random.normal(mean_return, std_return, 10000)
        monte_carlo_var = np.percentile(simulated_returns, confidence_level * 100)

        # Return average of methods
        return np.mean([historical_var, parametric_var, monte_carlo_var])

    def calculate_expected_shortfall(
        self, returns: np.ndarray, confidence_level: float = 0.05
    ) -> float:
        """
        Calculate Expected Shortfall (Conditional VaR)
        """
        var = self.calculate_var(returns, confidence_level)
        return np.mean(returns[returns <= var])

    def stress_test(
        self,
        portfolio_weights: np.ndarray,
        returns_data: pd.DataFrame,
        scenarios: Dict[str, Dict[str, float]],
    ) -> Dict[str, float]:
        """
        Perform stress testing on portfolio
        """
        results = {}

        for scenario_name, shocks in scenarios.items():
            # Apply shocks to returns
            stressed_returns = returns_data.copy()

            for asset, shock in shocks.items():
                if asset in stressed_returns.columns:
                    stressed_returns[asset] = stressed_returns[asset] + shock

            # Calculate portfolio returns under stress
            portfolio_returns = (stressed_returns * portfolio_weights).sum(axis=1)

            # Calculate metrics
            results[scenario_name] = {
                "portfolio_return": portfolio_returns.mean() * 252,
                "portfolio_volatility": portfolio_returns.std() * np.sqrt(252),
                "var_95": self.calculate_var(portfolio_returns.values, 0.05),
                "expected_shortfall": self.calculate_expected_shortfall(
                    portfolio_returns.values, 0.05
                ),
            }

        return results


# Model factory
class ModelFactory:
    """
    Factory class for creating and managing AI models
    """

    @staticmethod
    def create_predictor(model_type: str = "ensemble") -> AdvancedTimeSeriesPredictor:
        """Create a time series predictor"""
        return AdvancedTimeSeriesPredictor(model_type)

    @staticmethod
    def create_optimizer() -> PortfolioOptimizer:
        """Create a portfolio optimizer"""
        return PortfolioOptimizer()

    @staticmethod
    def create_risk_assessor() -> RiskAssessmentModel:
        """Create a risk assessment model"""
        return RiskAssessmentModel()


# Example usage and testing
if __name__ == "__main__":
    # Example usage
    logger.info("Testing Advanced AI Models...")

    # Create sample data
    dates = pd.date_range(start="2020-01-01", end="2023-12-31", freq="D")
    np.random.seed(42)

    # Generate synthetic price data
    n_assets = 5
    asset_names = [f"ASSET_{i+1}" for i in range(n_assets)]

    price_data = {}
    for asset in asset_names:
        # Random walk with drift
        returns = np.random.normal(0.0005, 0.02, len(dates))
        prices = [100]  # Starting price

        for ret in returns[1:]:
            prices.append(prices[-1] * (1 + ret))

        price_data[asset] = prices

    df = pd.DataFrame(price_data, index=dates)

    # Test time series predictor
    predictor = ModelFactory.create_predictor("ensemble")

    try:
        # Train model
        metrics = predictor.train(df[["ASSET_1"]], target_col="ASSET_1")
        logger.info(f"Training metrics: {metrics}")

        # Make prediction
        prediction = predictor.predict(df[["ASSET_1"]], target_col="ASSET_1")
        logger.info(f"Prediction: {prediction}")

        # Test portfolio optimizer
        returns_data = df.pct_change().dropna()
        optimizer = ModelFactory.create_optimizer()

        optimization_result = optimizer.optimize_portfolio(
            returns_data, objective="max_sharpe"
        )
        logger.info(f"Optimization result: {optimization_result}")

        # Test risk assessment
        risk_assessor = ModelFactory.create_risk_assessor()

        portfolio_weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

        # Define stress scenarios
        stress_scenarios = {
            "market_crash": {asset: -0.2 for asset in asset_names},  # 20% drop
            "volatility_spike": {
                asset: 0.0 for asset in asset_names
            },  # No return change, but increased vol
            "sector_rotation": {
                asset_names[0]: 0.1,
                asset_names[1]: -0.1,
            },  # Sector-specific shocks
        }

        stress_results = risk_assessor.stress_test(
            portfolio_weights, returns_data, stress_scenarios
        )
        logger.info(f"Stress test results: {stress_results}")

        logger.info("All tests completed successfully!")

    except Exception as e:
        logger.error(f"Error during testing: {e}")
        raise
