"""
Database Models for QuantumVest
SQLAlchemy models for comprehensive investment analytics platform
"""
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Index

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # User preferences
    risk_tolerance = db.Column(db.Float, default=0.5)  # 0.0 to 1.0
    investment_experience = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    preferred_currency = db.Column(db.String(3), default='USD')
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    subscription_tier = db.Column(db.String(20), default='free')  # free, premium, professional
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    portfolios = db.relationship('Portfolio', backref='user', lazy=True, cascade='all, delete-orphan')
    watchlists = db.relationship('Watchlist', backref='user', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'risk_tolerance': self.risk_tolerance,
            'investment_experience': self.investment_experience,
            'preferred_currency': self.preferred_currency,
            'subscription_tier': self.subscription_tier,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Asset(db.Model):
    """Asset model for stocks, cryptocurrencies, and other financial instruments"""
    __tablename__ = 'assets'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = db.Column(db.String(20), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    asset_type = db.Column(db.String(20), nullable=False, index=True)  # stock, crypto, etf, bond, commodity
    exchange = db.Column(db.String(50), nullable=True)
    sector = db.Column(db.String(100), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    market_cap = db.Column(db.BigInteger, nullable=True)
    
    # Asset metadata
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    
    # Trading information
    is_active = db.Column(db.Boolean, default=True)
    is_tradeable = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    price_data = db.relationship('PriceData', backref='asset', lazy=True, cascade='all, delete-orphan')
    portfolio_holdings = db.relationship('PortfolioHolding', backref='asset', lazy=True)
    predictions = db.relationship('Prediction', backref='asset', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert asset to dictionary"""
        return {
            'id': str(self.id),
            'symbol': self.symbol,
            'name': self.name,
            'asset_type': self.asset_type,
            'exchange': self.exchange,
            'sector': self.sector,
            'industry': self.industry,
            'market_cap': self.market_cap,
            'is_active': self.is_active,
            'is_tradeable': self.is_tradeable
        }

class Portfolio(db.Model):
    """Portfolio model for tracking user investments"""
    __tablename__ = 'portfolios'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Portfolio settings
    is_default = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=False)
    currency = db.Column(db.String(3), default='USD')
    
    # Performance tracking
    initial_value = db.Column(db.Numeric(15, 2), default=0)
    current_value = db.Column(db.Numeric(15, 2), default=0)
    total_return = db.Column(db.Numeric(15, 2), default=0)
    total_return_percentage = db.Column(db.Float, default=0)
    
    # Risk metrics
    volatility = db.Column(db.Float, nullable=True)
    sharpe_ratio = db.Column(db.Float, nullable=True)
    max_drawdown = db.Column(db.Float, nullable=True)
    beta = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    holdings = db.relationship('PortfolioHolding', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    performance_history = db.relationship('PortfolioPerformance', backref='portfolio', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert portfolio to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'is_default': self.is_default,
            'currency': self.currency,
            'current_value': float(self.current_value) if self.current_value else 0,
            'total_return': float(self.total_return) if self.total_return else 0,
            'total_return_percentage': self.total_return_percentage,
            'volatility': self.volatility,
            'sharpe_ratio': self.sharpe_ratio,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class PortfolioHolding(db.Model):
    """Portfolio holdings model for tracking individual asset positions"""
    __tablename__ = 'portfolio_holdings'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = db.Column(UUID(as_uuid=True), db.ForeignKey('portfolios.id'), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assets.id'), nullable=False)
    
    # Position information
    quantity = db.Column(db.Numeric(20, 8), nullable=False, default=0)
    average_cost = db.Column(db.Numeric(15, 2), nullable=False, default=0)
    current_price = db.Column(db.Numeric(15, 2), nullable=True)
    market_value = db.Column(db.Numeric(15, 2), nullable=True)
    
    # Performance metrics
    unrealized_pnl = db.Column(db.Numeric(15, 2), default=0)
    unrealized_pnl_percentage = db.Column(db.Float, default=0)
    realized_pnl = db.Column(db.Numeric(15, 2), default=0)
    
    # Allocation
    target_allocation = db.Column(db.Float, nullable=True)  # Target percentage (0.0 to 1.0)
    current_allocation = db.Column(db.Float, nullable=True)  # Current percentage (0.0 to 1.0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Indexes
    __table_args__ = (
        Index('idx_portfolio_asset', 'portfolio_id', 'asset_id'),
    )
    
    def to_dict(self):
        """Convert holding to dictionary"""
        return {
            'id': str(self.id),
            'asset': self.asset.to_dict() if self.asset else None,
            'quantity': float(self.quantity) if self.quantity else 0,
            'average_cost': float(self.average_cost) if self.average_cost else 0,
            'current_price': float(self.current_price) if self.current_price else 0,
            'market_value': float(self.market_value) if self.market_value else 0,
            'unrealized_pnl': float(self.unrealized_pnl) if self.unrealized_pnl else 0,
            'unrealized_pnl_percentage': self.unrealized_pnl_percentage,
            'current_allocation': self.current_allocation,
            'target_allocation': self.target_allocation
        }

class Transaction(db.Model):
    """Transaction model for tracking buy/sell orders"""
    __tablename__ = 'transactions'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = db.Column(UUID(as_uuid=True), db.ForeignKey('portfolios.id'), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assets.id'), nullable=False)
    
    # Transaction details
    transaction_type = db.Column(db.String(10), nullable=False)  # buy, sell, dividend, split
    quantity = db.Column(db.Numeric(20, 8), nullable=False)
    price = db.Column(db.Numeric(15, 2), nullable=False)
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    fees = db.Column(db.Numeric(15, 2), default=0)
    
    # Transaction metadata
    exchange = db.Column(db.String(50), nullable=True)
    order_id = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    executed_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    asset = db.relationship('Asset', backref='transactions')
    
    # Indexes
    __table_args__ = (
        Index('idx_portfolio_asset_date', 'portfolio_id', 'asset_id', 'executed_at'),
        Index('idx_transaction_type_date', 'transaction_type', 'executed_at'),
    )
    
    def to_dict(self):
        """Convert transaction to dictionary"""
        return {
            'id': str(self.id),
            'asset': self.asset.to_dict() if self.asset else None,
            'transaction_type': self.transaction_type,
            'quantity': float(self.quantity),
            'price': float(self.price),
            'total_amount': float(self.total_amount),
            'fees': float(self.fees) if self.fees else 0,
            'executed_at': self.executed_at.isoformat() if self.executed_at else None
        }

class PriceData(db.Model):
    """Price data model for storing historical and real-time price information"""
    __tablename__ = 'price_data'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assets.id'), nullable=False)
    
    # OHLCV data
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    open_price = db.Column(db.Numeric(15, 8), nullable=False)
    high_price = db.Column(db.Numeric(15, 8), nullable=False)
    low_price = db.Column(db.Numeric(15, 8), nullable=False)
    close_price = db.Column(db.Numeric(15, 8), nullable=False)
    volume = db.Column(db.BigInteger, nullable=True)
    
    # Additional metrics
    market_cap = db.Column(db.BigInteger, nullable=True)
    circulating_supply = db.Column(db.BigInteger, nullable=True)
    
    # Data source and interval
    source = db.Column(db.String(50), nullable=True)  # yahoo, coinapi, etc.
    interval = db.Column(db.String(10), nullable=False)  # 1m, 5m, 1h, 1d, etc.
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Indexes
    __table_args__ = (
        Index('idx_asset_timestamp_interval', 'asset_id', 'timestamp', 'interval'),
        db.UniqueConstraint('asset_id', 'timestamp', 'interval', name='uq_asset_timestamp_interval'),
    )
    
    def to_dict(self):
        """Convert price data to dictionary"""
        return {
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'open': float(self.open_price),
            'high': float(self.high_price),
            'low': float(self.low_price),
            'close': float(self.close_price),
            'volume': self.volume
        }

class Prediction(db.Model):
    """Prediction model for storing AI-generated price predictions"""
    __tablename__ = 'predictions'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assets.id'), nullable=False)
    
    # Prediction details
    model_name = db.Column(db.String(100), nullable=False)
    model_version = db.Column(db.String(20), nullable=True)
    prediction_type = db.Column(db.String(20), nullable=False)  # price, trend, volatility
    
    # Time horizon
    prediction_date = db.Column(db.DateTime, nullable=False)  # When prediction was made
    target_date = db.Column(db.DateTime, nullable=False)  # Target date for prediction
    days_ahead = db.Column(db.Integer, nullable=False)
    
    # Prediction values
    predicted_value = db.Column(db.Numeric(15, 8), nullable=False)
    confidence_score = db.Column(db.Float, nullable=True)  # 0.0 to 1.0
    prediction_range_low = db.Column(db.Numeric(15, 8), nullable=True)
    prediction_range_high = db.Column(db.Numeric(15, 8), nullable=True)
    
    # Actual outcome (for evaluation)
    actual_value = db.Column(db.Numeric(15, 8), nullable=True)
    accuracy_score = db.Column(db.Float, nullable=True)
    
    # Model features and metadata
    features_used = db.Column(db.JSON, nullable=True)
    model_parameters = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Indexes
    __table_args__ = (
        Index('idx_asset_prediction_date', 'asset_id', 'prediction_date'),
        Index('idx_asset_target_date', 'asset_id', 'target_date'),
    )
    
    def to_dict(self):
        """Convert prediction to dictionary"""
        return {
            'id': str(self.id),
            'asset': self.asset.to_dict() if self.asset else None,
            'model_name': self.model_name,
            'prediction_type': self.prediction_type,
            'prediction_date': self.prediction_date.isoformat() if self.prediction_date else None,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'days_ahead': self.days_ahead,
            'predicted_value': float(self.predicted_value),
            'confidence_score': self.confidence_score,
            'actual_value': float(self.actual_value) if self.actual_value else None,
            'accuracy_score': self.accuracy_score
        }

class Watchlist(db.Model):
    """Watchlist model for tracking user's assets of interest"""
    __tablename__ = 'watchlists'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_default = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    items = db.relationship('WatchlistItem', backref='watchlist', lazy=True, cascade='all, delete-orphan')

class WatchlistItem(db.Model):
    """Watchlist item model for individual assets in watchlists"""
    __tablename__ = 'watchlist_items'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    watchlist_id = db.Column(UUID(as_uuid=True), db.ForeignKey('watchlists.id'), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assets.id'), nullable=False)
    
    # Item settings
    notes = db.Column(db.Text, nullable=True)
    target_price = db.Column(db.Numeric(15, 2), nullable=True)
    
    # Timestamps
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    asset = db.relationship('Asset', backref='watchlist_items')
    
    # Indexes
    __table_args__ = (
        db.UniqueConstraint('watchlist_id', 'asset_id', name='uq_watchlist_asset'),
    )

class Alert(db.Model):
    """Alert model for price and portfolio alerts"""
    __tablename__ = 'alerts'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    asset_id = db.Column(UUID(as_uuid=True), db.ForeignKey('assets.id'), nullable=True)
    
    # Alert configuration
    alert_type = db.Column(db.String(20), nullable=False)  # price, volume, portfolio_value, etc.
    condition = db.Column(db.String(20), nullable=False)  # above, below, change_percent
    threshold_value = db.Column(db.Numeric(15, 8), nullable=False)
    
    # Alert settings
    is_active = db.Column(db.Boolean, default=True)
    is_recurring = db.Column(db.Boolean, default=False)
    notification_method = db.Column(db.String(20), default='email')  # email, sms, push
    
    # Alert status
    last_triggered = db.Column(db.DateTime, nullable=True)
    trigger_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    asset = db.relationship('Asset', backref='alerts')

class PortfolioPerformance(db.Model):
    """Portfolio performance tracking model"""
    __tablename__ = 'portfolio_performance'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = db.Column(UUID(as_uuid=True), db.ForeignKey('portfolios.id'), nullable=False)
    
    # Performance data
    date = db.Column(db.Date, nullable=False, index=True)
    total_value = db.Column(db.Numeric(15, 2), nullable=False)
    daily_return = db.Column(db.Float, nullable=True)
    cumulative_return = db.Column(db.Float, nullable=True)
    
    # Risk metrics
    volatility = db.Column(db.Float, nullable=True)
    sharpe_ratio = db.Column(db.Float, nullable=True)
    max_drawdown = db.Column(db.Float, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Indexes
    __table_args__ = (
        Index('idx_portfolio_date', 'portfolio_id', 'date'),
        db.UniqueConstraint('portfolio_id', 'date', name='uq_portfolio_date'),
    )

