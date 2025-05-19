# QuantumVest Enhancement Documentation

## Overview
This document provides an overview of the enhancements made to the QuantumVest project, focusing on the integration of a real-time data pipeline with predictive modeling capabilities.

## Enhancements Implemented

### 1. Real-Time Data Pipeline
- Implemented modular data fetchers for both stock and cryptocurrency data
- Added robust error handling and data validation
- Created caching mechanisms to optimize API usage
- Integrated with Yahoo Finance API for stock data and CoinGecko API for cryptocurrency data

### 2. Time-Series Predictive Modeling
- Developed LSTM-based models for price prediction
- Implemented feature engineering for technical indicators
- Created model training, evaluation, and prediction services
- Added support for model versioning and performance tracking

### 3. Flask API Integration
- Enhanced the existing Flask application with new API endpoints
- Created RESTful endpoints for data and predictions
- Maintained backward compatibility with legacy endpoints
- Added comprehensive error handling and validation

### 4. Project Structure
The enhanced project follows a modular architecture:

```
code/
├── backend/
│   ├── data_pipeline/
│   │   ├── __init__.py
│   │   ├── data_fetcher.py
│   │   ├── stock_api.py
│   │   ├── crypto_api.py
│   │   ├── data_storage.py
│   │   ├── feature_engineering.py
│   │   ├── lstm_model.py
│   │   ├── model_evaluator.py
│   │   └── prediction_service.py
│   ├── tests/
│   │   └── validate_pipeline.py
│   ├── api_routes.py
│   ├── app.py
│   └── requirements.txt
└── ...
```

## API Documentation

### New API Endpoints

#### Data Endpoints
- `GET /api/v1/data/stocks/<symbol>` - Get stock data
  - Query parameters:
    - `interval` (optional): Data interval (default: '1d')
    - `use_cache` (optional): Whether to use cached data (default: true)

- `GET /api/v1/data/crypto/<symbol>` - Get cryptocurrency data
  - Query parameters:
    - `interval` (optional): Data interval (default: 'daily')
    - `use_cache` (optional): Whether to use cached data (default: true)

#### Prediction Endpoints
- `GET /api/v1/predictions/stocks/<symbol>` - Get stock price predictions
  - Query parameters:
    - `days_ahead` (optional): Number of days to predict ahead (default: 7)
    - `use_cache` (optional): Whether to use cached data (default: true)

- `GET /api/v1/predictions/crypto/<symbol>` - Get cryptocurrency price predictions
  - Query parameters:
    - `days_ahead` (optional): Number of days to predict ahead (default: 7)
    - `use_cache` (optional): Whether to use cached data (default: true)

#### Model Status Endpoint
- `GET /api/v1/models/status` - Get model training status and performance metrics

### Legacy API Endpoints (Maintained for Backward Compatibility)
- `GET /api/health` - Health check endpoint
- `GET /api/blockchain-data/<asset>` - Legacy blockchain data endpoint
- `POST /api/predict` - Legacy prediction endpoint
- `POST /api/optimize` - Legacy portfolio optimization endpoint

## Usage Examples

### Fetching Stock Data
```python
import requests

# Get stock data for Apple
response = requests.get('http://localhost:5000/api/v1/data/stocks/AAPL')
data = response.json()
print(f"Retrieved {len(data['data'])} records for {data['symbol']}")
```

### Getting Stock Predictions
```python
import requests

# Get 7-day predictions for Apple
response = requests.get('http://localhost:5000/api/v1/predictions/stocks/AAPL?days_ahead=7')
predictions = response.json()
print(f"Predictions for next {len(predictions['predictions'])} days:")
for date, price in zip(predictions['dates'], predictions['predictions']):
    print(f"{date}: ${price:.2f}")
```

### Fetching Cryptocurrency Data
```python
import requests

# Get data for Bitcoin
response = requests.get('http://localhost:5000/api/v1/data/crypto/bitcoin')
data = response.json()
print(f"Retrieved {len(data['data'])} records for {data['symbol']}")
```

## Running the Application

1. Install dependencies:
```bash
pip install -r code/backend/requirements.txt
```

2. Start the Flask application:
```bash
cd code/backend
python app.py
```

3. Access the API at `http://localhost:5000/api/v1/health`

## Future Enhancements
- Add support for more data sources
- Implement ensemble models for improved prediction accuracy
- Add user authentication for API access
- Implement real-time data streaming
- Add support for more technical indicators and prediction features
