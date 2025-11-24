# API Documentation

## Overview

The QuantumVest API provides programmatic access to the Predictive Investment Analytics Platform. This documentation outlines all available endpoints, authentication methods, request/response formats, and usage examples.

## Base URL

All API requests should be made to the following base URL:

```
https://api.quantumvest.com/v1
```

## Authentication

### API Keys

Authentication is performed using API keys. To obtain an API key:

1. Log in to your QuantumVest account
2. Navigate to Settings > API Access
3. Click "Generate New API Key"
4. Store your API key securely; it will only be shown once

Include your API key in the request header:

```
Authorization: Bearer YOUR_API_KEY
```

### Rate Limits

- Free tier: 100 requests per day
- Standard tier: 1,000 requests per day
- Premium tier: 10,000 requests per day

Rate limit headers are included in all API responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1619712000
```

## Endpoints

### Predictions

#### Get Prediction for Asset

```
GET /predictions/{asset_type}/{asset_id}
```

Retrieve AI-generated predictions for a specific asset.

**Parameters:**

| Parameter  | Type   | Required | Description                                           |
| ---------- | ------ | -------- | ----------------------------------------------------- |
| asset_type | string | Yes      | Type of asset (stocks, crypto)                        |
| asset_id   | string | Yes      | Identifier for the asset (ticker symbol or crypto ID) |
| timeframe  | string | No       | Prediction timeframe (1d, 1w, 1m, 3m). Default: 1w    |

**Response:**

```json
{
    "asset": {
        "id": "AAPL",
        "name": "Apple Inc.",
        "type": "stocks"
    },
    "prediction": {
        "timestamp": "2025-04-25T10:00:00Z",
        "timeframe": "1w",
        "current_price": 185.92,
        "predicted_price": 192.45,
        "confidence_interval": {
            "lower": 188.76,
            "upper": 196.14
        },
        "direction": "up",
        "confidence_score": 0.78
    },
    "historical_accuracy": {
        "1d": 0.82,
        "1w": 0.76,
        "1m": 0.71
    }
}
```

#### List Recent Predictions

```
GET /predictions
```

Retrieve a list of recent predictions.

**Parameters:**

| Parameter  | Type    | Required | Description                                             |
| ---------- | ------- | -------- | ------------------------------------------------------- |
| asset_type | string  | No       | Filter by asset type (stocks, crypto)                   |
| limit      | integer | No       | Number of predictions to return (default: 10, max: 100) |
| page       | integer | No       | Page number for pagination (default: 1)                 |

**Response:**

```json
{
    "predictions": [
        {
            "asset": {
                "id": "AAPL",
                "name": "Apple Inc.",
                "type": "stocks"
            },
            "prediction": {
                "timestamp": "2025-04-25T10:00:00Z",
                "timeframe": "1w",
                "direction": "up",
                "confidence_score": 0.78
            }
        },
        {
            "asset": {
                "id": "BTC",
                "name": "Bitcoin",
                "type": "crypto"
            },
            "prediction": {
                "timestamp": "2025-04-25T10:00:00Z",
                "timeframe": "1w",
                "direction": "down",
                "confidence_score": 0.65
            }
        }
    ],
    "pagination": {
        "total": 42,
        "page": 1,
        "limit": 10,
        "pages": 5
    }
}
```

### Portfolio

#### Get Portfolio

```
GET /portfolio
```

Retrieve the user's current portfolio.

**Response:**

```json
{
    "portfolio": {
        "total_value": 25000.0,
        "assets": [
            {
                "id": "AAPL",
                "name": "Apple Inc.",
                "type": "stocks",
                "quantity": 10,
                "current_price": 185.92,
                "value": 1859.2,
                "allocation_percentage": 7.44
            },
            {
                "id": "BTC",
                "name": "Bitcoin",
                "type": "crypto",
                "quantity": 0.25,
                "current_price": 65000.0,
                "value": 16250.0,
                "allocation_percentage": 65.0
            }
        ],
        "performance": {
            "daily": 2.3,
            "weekly": -1.5,
            "monthly": 5.7,
            "yearly": 12.4
        }
    }
}
```

#### Update Portfolio

```
PUT /portfolio
```

Update the user's portfolio.

**Request:**

```json
{
    "assets": [
        {
            "id": "AAPL",
            "type": "stocks",
            "quantity": 15
        },
        {
            "id": "BTC",
            "type": "crypto",
            "quantity": 0.3
        }
    ]
}
```

**Response:**

```json
{
    "status": "success",
    "message": "Portfolio updated successfully",
    "portfolio": {
        "total_value": 28538.8,
        "assets": [
            {
                "id": "AAPL",
                "name": "Apple Inc.",
                "type": "stocks",
                "quantity": 15,
                "current_price": 185.92,
                "value": 2788.8,
                "allocation_percentage": 9.77
            },
            {
                "id": "BTC",
                "name": "Bitcoin",
                "type": "crypto",
                "quantity": 0.3,
                "current_price": 65000.0,
                "value": 19500.0,
                "allocation_percentage": 68.33
            }
        ]
    }
}
```

### Optimization

#### Generate Optimization Plan

```
POST /optimization
```

Generate a portfolio optimization plan.

**Request:**

```json
{
    "risk_profile": "moderate",
    "investment_horizon": "medium",
    "initial_investment": 25000,
    "constraints": {
        "max_crypto_allocation": 0.3,
        "min_stock_allocation": 0.4
    }
}
```

**Response:**

```json
{
    "optimization_id": "opt-123456",
    "recommended_allocation": {
        "stocks": {
            "AAPL": 0.15,
            "MSFT": 0.1,
            "GOOGL": 0.1,
            "AMZN": 0.05
        },
        "crypto": {
            "BTC": 0.15,
            "ETH": 0.1
        },
        "bonds": {
            "GOVT": 0.2,
            "VCIT": 0.15
        }
    },
    "expected_performance": {
        "annual_return": 0.12,
        "volatility": 0.08,
        "sharpe_ratio": 1.5
    },
    "implementation_steps": [
        {
            "action": "buy",
            "asset_id": "AAPL",
            "asset_type": "stocks",
            "quantity": 20
        },
        {
            "action": "sell",
            "asset_id": "BTC",
            "asset_type": "crypto",
            "quantity": 0.1
        }
    ]
}
```

### Market Data

#### Get Asset Price

```
GET /market/price/{asset_type}/{asset_id}
```

Retrieve current and historical price data for an asset.

**Parameters:**

| Parameter  | Type   | Required | Description                                              |
| ---------- | ------ | -------- | -------------------------------------------------------- |
| asset_type | string | Yes      | Type of asset (stocks, crypto)                           |
| asset_id   | string | Yes      | Identifier for the asset (ticker symbol or crypto ID)    |
| period     | string | No       | Historical data period (1d, 1w, 1m, 3m, 1y). Default: 1m |
| interval   | string | No       | Data interval (1m, 5m, 15m, 30m, 1h, 1d). Default: 1d    |

**Response:**

```json
{
    "asset": {
        "id": "AAPL",
        "name": "Apple Inc.",
        "type": "stocks"
    },
    "current_price": 185.92,
    "price_change": {
        "value": 2.45,
        "percentage": 1.34
    },
    "historical_data": [
        {
            "timestamp": "2025-04-24T16:00:00Z",
            "open": 183.47,
            "high": 186.2,
            "low": 182.95,
            "close": 185.92,
            "volume": 32456789
        },
        {
            "timestamp": "2025-04-23T16:00:00Z",
            "open": 184.1,
            "high": 185.35,
            "low": 182.8,
            "close": 183.47,
            "volume": 28765432
        }
    ],
    "metadata": {
        "period": "1w",
        "interval": "1d",
        "currency": "USD",
        "timezone": "UTC"
    }
}
```

#### Get Market Sentiment

```
GET /market/sentiment/{asset_type}/{asset_id}
```

Retrieve market sentiment analysis for an asset.

**Parameters:**

| Parameter  | Type   | Required | Description                                           |
| ---------- | ------ | -------- | ----------------------------------------------------- |
| asset_type | string | Yes      | Type of asset (stocks, crypto)                        |
| asset_id   | string | Yes      | Identifier for the asset (ticker symbol or crypto ID) |

**Response:**

```json
{
    "asset": {
        "id": "AAPL",
        "name": "Apple Inc.",
        "type": "stocks"
    },
    "sentiment": {
        "overall_score": 0.72,
        "classification": "bullish",
        "components": {
            "news_sentiment": 0.68,
            "social_media_sentiment": 0.75,
            "technical_indicators": 0.65,
            "analyst_ratings": 0.8
        }
    },
    "sources": {
        "news_articles": 42,
        "social_media_posts": 1250,
        "technical_indicators_analyzed": 15,
        "analysts_coverage": 28
    },
    "timestamp": "2025-04-25T10:00:00Z"
}
```

### User

#### Get User Profile

```
GET /user
```

Retrieve the user's profile information.

**Response:**

```json
{
    "user": {
        "id": "usr-123456",
        "email": "user@example.com",
        "name": "John Doe",
        "subscription_tier": "premium",
        "created_at": "2024-01-15T08:30:00Z",
        "preferences": {
            "theme": "dark",
            "notification_preferences": {
                "email": true,
                "push": true
            }
        }
    }
}
```

#### Update User Profile

```
PUT /user
```

Update the user's profile information.

**Request:**

```json
{
    "name": "John Smith",
    "preferences": {
        "theme": "light",
        "notification_preferences": {
            "email": false,
            "push": true
        }
    }
}
```

**Response:**

```json
{
    "status": "success",
    "message": "User profile updated successfully",
    "user": {
        "id": "usr-123456",
        "email": "user@example.com",
        "name": "John Smith",
        "subscription_tier": "premium",
        "created_at": "2024-01-15T08:30:00Z",
        "preferences": {
            "theme": "light",
            "notification_preferences": {
                "email": false,
                "push": true
            }
        }
    }
}
```

## Error Handling

All API errors follow a standard format:

```json
{
    "error": {
        "code": "invalid_request",
        "message": "The request was invalid",
        "details": "The asset_id parameter is required"
    }
}
```

### Common Error Codes

| Code                 | HTTP Status | Description                                          |
| -------------------- | ----------- | ---------------------------------------------------- |
| authentication_error | 401         | Invalid or missing API key                           |
| permission_denied    | 403         | Insufficient permissions for the requested operation |
| not_found            | 404         | The requested resource was not found                 |
| rate_limit_exceeded  | 429         | You have exceeded your rate limit                    |
| invalid_request      | 400         | The request was invalid or improperly formatted      |
| internal_error       | 500         | An internal server error occurred                    |

## Webhooks

QuantumVest supports webhooks for real-time notifications about various events.

### Setting Up Webhooks

1. Navigate to Settings > API Access > Webhooks
2. Click "Add Webhook"
3. Enter the URL where you want to receive webhook events
4. Select the events you want to subscribe to
5. Click "Save"

### Webhook Events

| Event                  | Description                                      |
| ---------------------- | ------------------------------------------------ |
| prediction.created     | A new prediction has been generated              |
| portfolio.updated      | The user's portfolio has been updated            |
| optimization.completed | A portfolio optimization plan has been generated |
| market.alert           | A market alert has been triggered                |

### Webhook Payload

```json
{
    "event": "prediction.created",
    "timestamp": "2025-04-25T10:00:00Z",
    "data": {
        "asset": {
            "id": "AAPL",
            "name": "Apple Inc.",
            "type": "stocks"
        },
        "prediction": {
            "timeframe": "1w",
            "direction": "up",
            "confidence_score": 0.78
        }
    }
}
```

## SDKs and Client Libraries

We provide official client libraries for the following programming languages:

- Python: [GitHub Repository](https://github.com/quantumvest/python-sdk)
- JavaScript: [GitHub Repository](https://github.com/quantumvest/js-sdk)
- Java: [GitHub Repository](https://github.com/quantumvest/java-sdk)
- Ruby: [GitHub Repository](https://github.com/quantumvest/ruby-sdk)

## Changelog

### v1.2.0 (2025-03-15)

- Added market sentiment analysis endpoint
- Improved prediction accuracy
- Added support for additional cryptocurrencies

### v1.1.0 (2025-01-20)

- Added portfolio optimization endpoints
- Enhanced historical data retrieval
- Improved rate limiting with more granular controls

### v1.0.0 (2024-11-10)

- Initial API release
