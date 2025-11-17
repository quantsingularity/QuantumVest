"""
Enhanced Database Models for QuantumVest
Financial industry-grade models with comprehensive features
"""

import enum
import uuid
from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class UserRole(enum.Enum):
    """User roles for role-based access control"""

    ADMIN = "admin"
    PORTFOLIO_MANAGER = "portfolio_manager"
    ANALYST = "analyst"
    CLIENT = "client"
    VIEWER = "viewer"


class AssetType(enum.Enum):
    """Asset types supported by the platform"""

    STOCK = "stock"
    CRYPTO = "crypto"
    BOND = "bond"
    ETF = "etf"
    COMMODITY = "commodity"
    FOREX = "forex"
    OPTION = "option"
    FUTURE = "future"


class TransactionType(enum.Enum):
    """Transaction types for portfolio management"""

    BUY = "buy"
    SELL = "sell"
    DIVIDEND = "dividend"
    SPLIT = "split"
    MERGER = "merger"
    SPINOFF = "spinoff"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class RiskLevel(enum.Enum):
    """Risk levels for portfolio classification"""

    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    SPECULATIVE = "speculative"


class ComplianceStatus(enum.Enum):
    """Compliance status for regulatory tracking"""

    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNDER_REVIEW = "under_review"
    PENDING = "pending"


class User(db.Model):
    """Enhanced user model with comprehensive financial features"""

    __tablename__ = "users"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))

    # Role and permissions
    role = db.Column(db.Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    # Financial profile
    risk_tolerance = db.Column(db.Float, default=0.5)  # 0.0 to 1.0
    investment_experience = db.Column(db.String(50))  # beginner, intermediate, advanced
    annual_income = db.Column(db.Numeric(15, 2))
    net_worth = db.Column(db.Numeric(15, 2))
    investment_goals = db.Column(db.Text)

    # Compliance and regulatory
    kyc_status = db.Column(db.Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    aml_status = db.Column(db.Enum(ComplianceStatus), default=ComplianceStatus.PENDING)
    accredited_investor = db.Column(db.Boolean, default=False)

    # Security
    two_factor_enabled = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime(timezone=True))
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime(timezone=True))

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    portfolios = db.relationship(
        "Portfolio", backref="owner", lazy="dynamic", cascade="all, delete-orphan"
    )
    transactions = db.relationship("Transaction", backref="user", lazy="dynamic")
    alerts = db.relationship(
        "Alert", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    audit_logs = db.relationship("AuditLog", backref="user", lazy="dynamic")

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "email": self.email,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "risk_tolerance": (
                float(self.risk_tolerance) if self.risk_tolerance else None
            ),
            "investment_experience": self.investment_experience,
            "kyc_status": self.kyc_status.value,
            "aml_status": self.aml_status.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Asset(db.Model):
    """Enhanced asset model with comprehensive market data"""

    __tablename__ = "assets"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    asset_type = db.Column(db.Enum(AssetType), nullable=False, index=True)

    # Market data
    exchange = db.Column(db.String(50))
    sector = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    market_cap = db.Column(db.Numeric(20, 2))

    # Trading information
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_tradeable = db.Column(db.Boolean, default=True, nullable=False)
    min_trade_amount = db.Column(db.Numeric(15, 8), default=0.001)

    # Risk metrics
    beta = db.Column(db.Float)
    volatility = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)

    # Metadata
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    metadata = db.Column(JSONB)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    price_history = db.relationship(
        "PriceHistory", backref="asset", lazy="dynamic", cascade="all, delete-orphan"
    )
    portfolio_holdings = db.relationship(
        "PortfolioHolding", backref="asset", lazy="dynamic"
    )
    transactions = db.relationship("Transaction", backref="asset", lazy="dynamic")

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "symbol": self.symbol,
            "name": self.name,
            "asset_type": self.asset_type.value,
            "exchange": self.exchange,
            "sector": self.sector,
            "industry": self.industry,
            "market_cap": float(self.market_cap) if self.market_cap else None,
            "is_active": self.is_active,
            "is_tradeable": self.is_tradeable,
            "beta": self.beta,
            "volatility": self.volatility,
            "sharpe_ratio": self.sharpe_ratio,
        }


class Portfolio(db.Model):
    """Enhanced portfolio model with comprehensive tracking"""

    __tablename__ = "portfolios"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False, index=True
    )
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    # Portfolio characteristics
    risk_level = db.Column(db.Enum(RiskLevel), default=RiskLevel.MODERATE)
    target_return = db.Column(db.Float)
    benchmark_symbol = db.Column(db.String(20))

    # Financial metrics
    total_value = db.Column(db.Numeric(20, 2), default=0)
    cash_balance = db.Column(db.Numeric(20, 2), default=0)
    invested_amount = db.Column(db.Numeric(20, 2), default=0)
    unrealized_pnl = db.Column(db.Numeric(20, 2), default=0)
    realized_pnl = db.Column(db.Numeric(20, 2), default=0)

    # Performance metrics
    total_return = db.Column(db.Float, default=0)
    annualized_return = db.Column(db.Float)
    volatility = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    max_drawdown = db.Column(db.Float)
    beta = db.Column(db.Float)
    alpha = db.Column(db.Float)

    # Status and settings
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    auto_rebalance = db.Column(db.Boolean, default=False)
    rebalance_threshold = db.Column(db.Float, default=0.05)  # 5%

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    holdings = db.relationship(
        "PortfolioHolding",
        backref="portfolio",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    transactions = db.relationship("Transaction", backref="portfolio", lazy="dynamic")
    performance_history = db.relationship(
        "PortfolioPerformance",
        backref="portfolio",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "name": self.name,
            "description": self.description,
            "risk_level": self.risk_level.value,
            "total_value": float(self.total_value) if self.total_value else 0,
            "cash_balance": float(self.cash_balance) if self.cash_balance else 0,
            "invested_amount": (
                float(self.invested_amount) if self.invested_amount else 0
            ),
            "total_return": self.total_return,
            "annualized_return": self.annualized_return,
            "volatility": self.volatility,
            "sharpe_ratio": self.sharpe_ratio,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class PortfolioHolding(db.Model):
    """Portfolio holdings with detailed tracking"""

    __tablename__ = "portfolio_holdings"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("portfolios.id"), nullable=False, index=True
    )
    asset_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("assets.id"), nullable=False, index=True
    )

    # Holding details
    quantity = db.Column(db.Numeric(20, 8), nullable=False, default=0)
    average_cost = db.Column(db.Numeric(15, 8), nullable=False, default=0)
    current_price = db.Column(db.Numeric(15, 8))

    # Calculated values
    market_value = db.Column(db.Numeric(20, 2), default=0)
    unrealized_pnl = db.Column(db.Numeric(20, 2), default=0)
    unrealized_pnl_percent = db.Column(db.Float, default=0)
    weight = db.Column(db.Float, default=0)  # Portfolio weight percentage

    # Target allocation
    target_weight = db.Column(db.Float)
    weight_deviation = db.Column(db.Float)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    __table_args__ = (
        UniqueConstraint("portfolio_id", "asset_id", name="unique_portfolio_asset"),
        CheckConstraint("quantity >= 0", name="positive_quantity"),
        CheckConstraint("average_cost >= 0", name="positive_average_cost"),
    )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "portfolio_id": str(self.portfolio_id),
            "asset_id": str(self.asset_id),
            "quantity": float(self.quantity) if self.quantity else 0,
            "average_cost": float(self.average_cost) if self.average_cost else 0,
            "current_price": float(self.current_price) if self.current_price else 0,
            "market_value": float(self.market_value) if self.market_value else 0,
            "unrealized_pnl": float(self.unrealized_pnl) if self.unrealized_pnl else 0,
            "unrealized_pnl_percent": self.unrealized_pnl_percent,
            "weight": self.weight,
            "target_weight": self.target_weight,
        }


class Transaction(db.Model):
    """Enhanced transaction model with comprehensive tracking"""

    __tablename__ = "transactions"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False, index=True
    )
    portfolio_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("portfolios.id"), nullable=False, index=True
    )
    asset_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("assets.id"), nullable=False, index=True
    )

    # Transaction details
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False, index=True)
    quantity = db.Column(db.Numeric(20, 8), nullable=False)
    price = db.Column(db.Numeric(15, 8), nullable=False)
    total_amount = db.Column(db.Numeric(20, 2), nullable=False)
    fees = db.Column(db.Numeric(10, 2), default=0)

    # Reference and tracking
    external_id = db.Column(db.String(100))  # External system reference
    order_id = db.Column(db.String(100))
    execution_venue = db.Column(db.String(100))

    # Metadata
    notes = db.Column(db.Text)
    metadata = db.Column(JSONB)

    # Timestamps
    executed_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )

    __table_args__ = (
        Index("idx_transaction_date", "executed_at"),
        Index("idx_transaction_type_date", "transaction_type", "executed_at"),
        CheckConstraint("quantity > 0", name="positive_quantity"),
        CheckConstraint("price >= 0", name="non_negative_price"),
        CheckConstraint("fees >= 0", name="non_negative_fees"),
    )

    def to_dict(self):
        """Convert to dictionary"""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "portfolio_id": str(self.portfolio_id),
            "asset_id": str(self.asset_id),
            "transaction_type": self.transaction_type.value,
            "quantity": float(self.quantity),
            "price": float(self.price),
            "total_amount": float(self.total_amount),
            "fees": float(self.fees) if self.fees else 0,
            "executed_at": self.executed_at.isoformat() if self.executed_at else None,
            "notes": self.notes,
        }


class PriceHistory(db.Model):
    """Historical price data for assets"""

    __tablename__ = "price_history"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("assets.id"), nullable=False, index=True
    )

    # Price data
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    open_price = db.Column(db.Numeric(15, 8), nullable=False)
    high_price = db.Column(db.Numeric(15, 8), nullable=False)
    low_price = db.Column(db.Numeric(15, 8), nullable=False)
    close_price = db.Column(db.Numeric(15, 8), nullable=False)
    volume = db.Column(db.Numeric(20, 2))

    # Calculated metrics
    price_change = db.Column(db.Numeric(15, 8))
    price_change_percent = db.Column(db.Float)

    # Data source
    source = db.Column(db.String(50), default="api")

    __table_args__ = (
        UniqueConstraint("asset_id", "timestamp", name="unique_asset_timestamp"),
        Index("idx_price_history_timestamp", "timestamp"),
        CheckConstraint("open_price > 0", name="positive_open_price"),
        CheckConstraint("high_price > 0", name="positive_high_price"),
        CheckConstraint("low_price > 0", name="positive_low_price"),
        CheckConstraint("close_price > 0", name="positive_close_price"),
        CheckConstraint("volume >= 0", name="non_negative_volume"),
    )


class PortfolioPerformance(db.Model):
    """Portfolio performance tracking over time"""

    __tablename__ = "portfolio_performance"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("portfolios.id"), nullable=False, index=True
    )

    # Performance data
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    total_value = db.Column(db.Numeric(20, 2), nullable=False)
    cash_balance = db.Column(db.Numeric(20, 2), default=0)
    invested_amount = db.Column(db.Numeric(20, 2), default=0)

    # Returns
    daily_return = db.Column(db.Float)
    cumulative_return = db.Column(db.Float)
    benchmark_return = db.Column(db.Float)

    # Risk metrics
    volatility = db.Column(db.Float)
    sharpe_ratio = db.Column(db.Float)
    beta = db.Column(db.Float)
    alpha = db.Column(db.Float)

    __table_args__ = (
        UniqueConstraint(
            "portfolio_id", "timestamp", name="unique_portfolio_timestamp"
        ),
        Index("idx_performance_timestamp", "timestamp"),
    )


class Alert(db.Model):
    """User alerts and notifications"""

    __tablename__ = "alerts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False, index=True
    )

    # Alert details
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(
        db.String(50), nullable=False, index=True
    )  # price, portfolio, news, system
    severity = db.Column(
        db.String(20), default="info"
    )  # info, warning, error, critical

    # Status
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    is_dismissed = db.Column(db.Boolean, default=False, nullable=False)

    # Metadata
    metadata = db.Column(JSONB)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    read_at = db.Column(db.DateTime(timezone=True))

    __table_args__ = (
        Index("idx_alert_user_created", "user_id", "created_at"),
        Index("idx_alert_type_created", "alert_type", "created_at"),
    )


class AuditLog(db.Model):
    """Audit log for compliance and security tracking"""

    __tablename__ = "audit_logs"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), index=True)

    # Event details
    event_type = db.Column(db.String(100), nullable=False, index=True)
    event_description = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)

    # Request details
    endpoint = db.Column(db.String(255))
    method = db.Column(db.String(10))
    status_code = db.Column(db.Integer)

    # Metadata
    metadata = db.Column(JSONB)

    # Timestamp
    created_at = db.Column(
        db.DateTime(timezone=True), default=datetime.now(timezone.utc), index=True
    )

    __table_args__ = (
        Index("idx_audit_user_created", "user_id", "created_at"),
        Index("idx_audit_event_created", "event_type", "created_at"),
    )


class RiskMetrics(db.Model):
    """Risk metrics calculation and storage"""

    __tablename__ = "risk_metrics"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("portfolios.id"), nullable=False, index=True
    )

    # Risk calculations
    calculation_date = db.Column(db.DateTime(timezone=True), nullable=False, index=True)
    var_95 = db.Column(db.Float)  # Value at Risk 95%
    var_99 = db.Column(db.Float)  # Value at Risk 99%
    cvar_95 = db.Column(db.Float)  # Conditional VaR 95%
    cvar_99 = db.Column(db.Float)  # Conditional VaR 99%

    # Portfolio risk metrics
    portfolio_volatility = db.Column(db.Float)
    portfolio_beta = db.Column(db.Float)
    correlation_matrix = db.Column(JSONB)

    # Stress test results
    stress_test_results = db.Column(JSONB)

    __table_args__ = (
        UniqueConstraint(
            "portfolio_id", "calculation_date", name="unique_portfolio_risk_date"
        ),
    )


class ComplianceCheck(db.Model):
    """Compliance monitoring and reporting"""

    __tablename__ = "compliance_checks"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False, index=True
    )
    portfolio_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("portfolios.id"), index=True
    )

    # Check details
    check_type = db.Column(db.String(100), nullable=False, index=True)
    check_description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(ComplianceStatus), nullable=False)

    # Results
    findings = db.Column(JSONB)
    recommendations = db.Column(db.Text)

    # Timestamps
    checked_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc)
    )
    resolved_at = db.Column(db.DateTime(timezone=True))

    __table_args__ = (
        Index("idx_compliance_user_checked", "user_id", "checked_at"),
        Index("idx_compliance_type_status", "check_type", "status"),
    )
