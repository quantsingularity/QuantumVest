CREATE TABLE market_predictions (
    id SERIAL PRIMARY KEY,
    asset VARCHAR(10) NOT NULL,
    prediction DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    assets JSONB NOT NULL,
    sharpe_ratio DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);