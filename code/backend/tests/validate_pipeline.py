"""
Validation Script
Tests the data pipeline, model training, and API endpoints
"""

import json
import logging
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import requests

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_pipeline.crypto_api import CryptoDataFetcher
from data_pipeline.data_storage import DataStorage
from data_pipeline.lstm_model import LSTMModel
from data_pipeline.prediction_service import PredictionService
# Import modules
from data_pipeline.stock_api import StockDataFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def test_data_fetching():
    """Test data fetching functionality"""
    logger.info("Testing data fetching...")

    # Test stock data fetching
    stock_fetcher = StockDataFetcher()
    stock_symbols = ["AAPL", "MSFT", "GOOGL"]

    for symbol in stock_symbols:
        logger.info(f"Fetching data for stock {symbol}")
        df = stock_fetcher.fetch_data(symbol)
        if df is not None and not df.empty:
            logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            logger.info(f"Columns: {df.columns.tolist()}")
            logger.info(
                f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}"
            )
        else:
            logger.error(f"Failed to fetch data for {symbol}")

    # Test crypto data fetching
    crypto_fetcher = CryptoDataFetcher()
    crypto_symbols = ["bitcoin", "ethereum", "ripple"]

    for symbol in crypto_symbols:
        logger.info(f"Fetching data for crypto {symbol}")
        df = crypto_fetcher.fetch_data(symbol)
        if df is not None and not df.empty:
            logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            logger.info(f"Columns: {df.columns.tolist()}")
            logger.info(
                f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}"
            )
        else:
            logger.error(f"Failed to fetch data for {symbol}")


def test_data_storage():
    """Test data storage functionality"""
    logger.info("Testing data storage...")

    # Initialize components
    stock_fetcher = StockDataFetcher()
    crypto_fetcher = CryptoDataFetcher()
    data_storage = DataStorage()

    # Test stock data storage
    symbol = "AAPL"
    logger.info(f"Testing storage for stock {symbol}")
    df = stock_fetcher.fetch_data(symbol)
    if df is not None and not df.empty:
        path = data_storage.save_stock_data(df, symbol)
        logger.info(f"Saved stock data to {path}")

        # Test loading
        loaded_df = data_storage.load_stock_data(symbol)
        if loaded_df is not None and not loaded_df.empty:
            logger.info(f"Successfully loaded {len(loaded_df)} records for {symbol}")
        else:
            logger.error(f"Failed to load data for {symbol}")

    # Test crypto data storage
    symbol = "bitcoin"
    logger.info(f"Testing storage for crypto {symbol}")
    df = crypto_fetcher.fetch_data(symbol)
    if df is not None and not df.empty:
        path = data_storage.save_crypto_data(df, symbol)
        logger.info(f"Saved crypto data to {path}")

        # Test loading
        loaded_df = data_storage.load_crypto_data(symbol)
        if loaded_df is not None and not loaded_df.empty:
            logger.info(f"Successfully loaded {len(loaded_df)} records for {symbol}")
        else:
            logger.error(f"Failed to load data for {symbol}")


def test_model_training():
    """Test model training functionality"""
    logger.info("Testing model training...")

    # Initialize components
    stock_fetcher = StockDataFetcher()
    lstm_model = LSTMModel()

    # Test stock model training
    symbol = "AAPL"
    logger.info(f"Testing model training for stock {symbol}")
    df = stock_fetcher.fetch_data(symbol)
    if df is not None and not df.empty:
        # Use a small subset for quick testing
        df = df.tail(200)

        # Train model
        result = lstm_model.train(df, "stock", symbol, epochs=2)
        if result["success"]:
            logger.info(f"Successfully trained model for {symbol}")
            logger.info(f"Model saved to {result['model_path']}")
            logger.info(f"Training loss: {result['training_loss']}")
            logger.info(f"Validation loss: {result['validation_loss']}")
        else:
            logger.error(
                f"Failed to train model for {symbol}: {result.get('error', 'Unknown error')}"
            )


def test_prediction_service():
    """Test prediction service functionality"""
    logger.info("Testing prediction service...")

    # Initialize prediction service
    prediction_service = PredictionService()

    # Test stock prediction
    symbol = "AAPL"
    logger.info(f"Testing prediction for stock {symbol}")
    result = prediction_service.get_stock_prediction(symbol, days_ahead=7)
    if result["success"]:
        logger.info(f"Successfully generated predictions for {symbol}")
        logger.info(f"Predictions: {result['predictions']}")
        logger.info(f"Dates: {result['dates']}")
    else:
        logger.error(
            f"Failed to generate predictions for {symbol}: {result.get('error', 'Unknown error')}"
        )

    # Test crypto prediction
    symbol = "bitcoin"
    logger.info(f"Testing prediction for crypto {symbol}")
    result = prediction_service.get_crypto_prediction(symbol, days_ahead=7)
    if result["success"]:
        logger.info(f"Successfully generated predictions for {symbol}")
        logger.info(f"Predictions: {result['predictions']}")
        logger.info(f"Dates: {result['dates']}")
    else:
        logger.error(
            f"Failed to generate predictions for {symbol}: {result.get('error', 'Unknown error')}"
        )


def test_api_endpoints():
    """Test API endpoints"""
    logger.info("Testing API endpoints...")

    # Start Flask app in a separate process
    # Note: In a real test, you would use Flask's test client or run the app in a separate process
    # For this validation script, we'll assume the app is already running

    base_url = "http://localhost:5000/api/v1"

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            logger.info("Health endpoint is working")
            logger.info(f"Response: {response.json()}")
        else:
            logger.error(
                f"Health endpoint failed with status code {response.status_code}"
            )
    except Exception as e:
        logger.error(f"Error testing health endpoint: {e}")

    # Test stock data endpoint
    try:
        symbol = "AAPL"
        response = requests.get(f"{base_url}/data/stocks/{symbol}")
        if response.status_code == 200:
            logger.info(f"Stock data endpoint for {symbol} is working")
            data = response.json()
            logger.info(f"Received {len(data.get('data', []))} records")
        else:
            logger.error(
                f"Stock data endpoint failed with status code {response.status_code}"
            )
    except Exception as e:
        logger.error(f"Error testing stock data endpoint: {e}")

    # Test stock prediction endpoint
    try:
        symbol = "AAPL"
        response = requests.get(f"{base_url}/predictions/stocks/{symbol}")
        if response.status_code == 200:
            logger.info(f"Stock prediction endpoint for {symbol} is working")
            data = response.json()
            logger.info(f"Predictions: {data.get('predictions', [])}")
        else:
            logger.error(
                f"Stock prediction endpoint failed with status code {response.status_code}"
            )
    except Exception as e:
        logger.error(f"Error testing stock prediction endpoint: {e}")


def run_validation():
    """Run all validation tests"""
    logger.info("Starting validation tests...")

    # Create validation report directory
    report_dir = "../../resources/validation_reports"
    os.makedirs(report_dir, exist_ok=True)

    # Run tests
    test_data_fetching()
    test_data_storage()
    test_model_training()
    test_prediction_service()

    # Note: API endpoint tests require the Flask app to be running
    # Uncomment the following line if the app is running
    # test_api_endpoints()

    logger.info("Validation tests completed")


if __name__ == "__main__":
    run_validation()
