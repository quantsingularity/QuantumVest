# QuantumVest Platform

## Financial Industry-Grade Investment Analytics Platform

QuantumVest is a comprehensive, enterprise-ready investment analytics platform designed for financial institutions, portfolio managers, and sophisticated investors. This version includes advanced AI capabilities, institutional-grade security, and comprehensive compliance features.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [API Documentation](#api-documentation)

## Overview

QuantumVest Platform provides:

- **Advanced Portfolio Management**: Multi-asset portfolio optimization with real-time risk assessment
- **AI-Powered Analytics**: Machine learning models for price prediction and market analysis
- **Institutional Security**: Bank-grade security with multi-factor authentication and encryption
- **Regulatory Compliance**: Built-in compliance monitoring and reporting
- **Blockchain Integration**: Smart contracts for transparent and secure transactions
- **Real-time Data Processing**: High-frequency data ingestion and processing capabilities
- **Comprehensive API**: RESTful APIs with extensive documentation and SDKs

## Key Features

### Security & Compliance

- **Multi-Factor Authentication (MFA)** with TOTP support
- **Role-Based Access Control (RBAC)** with granular permissions
- **End-to-End Encryption** for sensitive data
- **Audit Logging** for all user actions and system events
- **Compliance Monitoring** with automated violation detection
- **Threat Detection** with real-time security monitoring

### AI & Machine Learning

- **Advanced Time Series Prediction** using LSTM, Transformer, and ensemble models
- **Portfolio Optimization** with modern portfolio theory and machine learning
- **Risk Assessment** with VaR, CVaR, and stress testing
- **Sentiment Analysis** for market news and social media
- **Anomaly Detection** for fraud prevention and risk management
- **Real-time Model Training** with automated retraining pipelines

### Portfolio Management

- **Multi-Asset Support** (stocks, crypto, bonds, ETFs, commodities, forex)
- **Real-time Portfolio Valuation** with live market data
- **Performance Analytics** with comprehensive metrics
- **Risk Management** with advanced risk models
- **Automated Rebalancing** based on target allocations
- **Transaction Management** with detailed audit trails

### Blockchain Integration

- **Smart Contracts** for transparent portfolio management
- **Token-based Governance** with voting mechanisms
- **Staking and Rewards** system for platform tokens
- **Price Oracles** for reliable asset pricing
- **Decentralized Identity** for enhanced security

### Analytics & Reporting

- **Real-time Dashboards** with customizable widgets
- **Advanced Charting** with technical indicators
- **Performance Attribution** analysis
- **Risk Reports** with stress testing scenarios
- **Compliance Reports** for regulatory requirements
- **Custom Report Builder** with export capabilities

## Architecture

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Frontend  │    │  Mobile Apps    │    │  Third-party    │
│   (React.js)    │    │  (React Native) │    │  Integrations   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────┴─────────────┐
                    │      API Gateway          │
                    │   (Load Balancer +        │
                    │    Rate Limiting)         │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │    Backend Services       │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   Authentication    │  │
                    │  │     Service         │  │
                    │  └─────────────────────┘  │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   Portfolio         │  │
                    │  │   Management        │  │
                    │  └─────────────────────┘  │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   AI/ML Engine      │  │
                    │  └─────────────────────┘  │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   Risk Management   │  │
                    │  └─────────────────────┘  │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   Compliance        │  │
                    │  │   Engine            │  │
                    │  └─────────────────────┘  │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │     Data Layer            │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   PostgreSQL        │  │
                    │  │   (Primary DB)      │  │
                    │  └─────────────────────┘  │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   Redis             │  │
                    │  │   (Cache/Sessions)  │  │
                    │  └─────────────────────┘  │
                    │                           │
                    │  ┌─────────────────────┐  │
                    │  │   InfluxDB          │  │
                    │  │   (Time Series)     │  │
                    │  └─────────────────────┘  │
                    └───────────────────────────┘
```

### Technology Stack

**Backend:**

- **Framework**: Flask 2.3+ with SQLAlchemy ORM
- **Database**: PostgreSQL 14+ (primary), Redis 7+ (cache)
- **AI/ML**: TensorFlow 2.13+, scikit-learn, XGBoost, LightGBM
- **Security**: bcrypt, PyJWT, cryptography
- **API**: RESTful APIs with OpenAPI/Swagger documentation

**Blockchain:**

- **Platform**: Ethereum (Solidity 0.8+)
- **Framework**: Truffle / Hardhat
- **Libraries**: OpenZeppelin contracts
- **Integration**: Web3.py for backend integration

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (optional)

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/quantsingularity/quantumvest.git .

# Start all services with Docker Compose
docker-compose up -d

# The application will be available at:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:5000
# - API Documentation: http://localhost:5000/docs
```

### Manual Installation

#### Backend Setup

```bash
# Navigate to backend directory
cd code/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=development
export DATABASE_URL=postgresql://user:password@localhost/quantumvest
export REDIS_URL=redis://localhost:6379
export SECRET_KEY=your-secret-key

# Initialize database
flask db upgrade

# Start the backend server
python app.py
```

#### AI Models Setup

```bash
# Navigate to AI models directory
cd code/ai_models

# Install additional ML dependencies
pip install -r requirements.txt

# Train initial models (optional)
python training_scripts/training.py
```

#### Blockchain Setup

```bash
# Navigate to blockchain directory
cd code/blockchain

# Install dependencies
npm install

# Compile contracts
truffle compile

# Deploy to local network (Ganache)
truffle migrate --network development
```

## API Documentation

### Authentication

All API endpoints require authentication via JWT tokens.

```bash
# Register a new user
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d
```

### Portfolio Management

```bash
# Create a portfolio
curl -X POST http://localhost:5000/api/v1/portfolios \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d

# Get portfolio details
curl -X GET http://localhost:5000/api/v1/portfolios/{portfolio_id} \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Add a transaction
curl -X POST http://localhost:5000/api/v1/portfolios/{portfolio_id}/transactions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d
```

### AI Predictions

```bash
# Get stock prediction
curl -X GET http://localhost:5000/api/v1/predictions/stocks/AAPL?days_ahead=7 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get portfolio optimization
curl -X POST http://localhost:5000/api/v1/portfolios/{portfolio_id}/optimize \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d
```

### Risk Analysis

```bash
# Get portfolio risk analysis
curl -X GET http://localhost:5000/api/v1/portfolios/{portfolio_id}/risk-analysis \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Get compliance check
curl -X GET http://localhost:5000/api/v1/portfolios/{portfolio_id}/compliance \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```
