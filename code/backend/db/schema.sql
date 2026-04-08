-- QuantumVest reference schema (auto-managed by Flask-Migrate in practice)

CREATE TABLE IF NOT EXISTS users (
    id          VARCHAR(36) PRIMARY KEY,
    email       VARCHAR(255) UNIQUE NOT NULL,
    username    VARCHAR(80)  UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name  VARCHAR(100),
    last_name   VARCHAR(100),
    role        VARCHAR(30)  NOT NULL DEFAULT 'client',
    is_active   BOOLEAN      NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN      NOT NULL DEFAULT FALSE,
    risk_tolerance FLOAT,
    kyc_status  VARCHAR(30)  DEFAULT 'pending',
    aml_status  VARCHAR(30)  DEFAULT 'pending',
    failed_login_attempts INTEGER DEFAULT 0,
    account_locked_until TIMESTAMP WITH TIME ZONE,
    last_login  TIMESTAMP WITH TIME ZONE,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS assets (
    id          VARCHAR(36) PRIMARY KEY,
    symbol      VARCHAR(20)  UNIQUE NOT NULL,
    name        VARCHAR(255) NOT NULL,
    asset_type  VARCHAR(30)  NOT NULL,
    exchange    VARCHAR(50),
    sector      VARCHAR(100),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    is_tradeable BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolios (
    id              VARCHAR(36) PRIMARY KEY,
    user_id         VARCHAR(36) NOT NULL REFERENCES users(id),
    name            VARCHAR(255) NOT NULL,
    currency        VARCHAR(10)  DEFAULT 'USD',
    is_default      BOOLEAN NOT NULL DEFAULT FALSE,
    risk_level      VARCHAR(30)  DEFAULT 'moderate',
    total_value     NUMERIC(20,2) DEFAULT 0,
    cash_balance    NUMERIC(20,2) DEFAULT 0,
    realized_pnl    NUMERIC(20,2) DEFAULT 0,
    unrealized_pnl  NUMERIC(20,2) DEFAULT 0,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS portfolio_holdings (
    id              VARCHAR(36) PRIMARY KEY,
    portfolio_id    VARCHAR(36) NOT NULL REFERENCES portfolios(id),
    asset_id        VARCHAR(36) NOT NULL REFERENCES assets(id),
    quantity        NUMERIC(20,8) NOT NULL DEFAULT 0,
    average_cost    NUMERIC(15,8) NOT NULL DEFAULT 0,
    current_price   NUMERIC(15,8),
    market_value    NUMERIC(20,2) DEFAULT 0,
    unrealized_pnl  NUMERIC(20,2) DEFAULT 0,
    weight          FLOAT DEFAULT 0,
    UNIQUE(portfolio_id, asset_id),
    CHECK(quantity >= 0),
    CHECK(average_cost >= 0)
);

CREATE TABLE IF NOT EXISTS transactions (
    id               VARCHAR(36) PRIMARY KEY,
    user_id          VARCHAR(36) NOT NULL REFERENCES users(id),
    portfolio_id     VARCHAR(36) NOT NULL REFERENCES portfolios(id),
    asset_id         VARCHAR(36) NOT NULL REFERENCES assets(id),
    transaction_type VARCHAR(30) NOT NULL,
    quantity         NUMERIC(20,8) NOT NULL,
    price            NUMERIC(15,8) NOT NULL,
    total_amount     NUMERIC(20,2) NOT NULL,
    fees             NUMERIC(10,2) DEFAULT 0,
    realized_pnl     NUMERIC(20,2) DEFAULT 0,
    executed_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at       TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CHECK(quantity > 0),
    CHECK(price >= 0),
    CHECK(fees >= 0)
);
