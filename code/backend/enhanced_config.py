"""
Enhanced Configuration for QuantumVest Backend
Comprehensive configuration management with environment-specific settings
"""
import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://quantumvest:password@localhost/quantumvest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 120,
        'pool_pre_ping': True
    }
    
    # JWT settings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    
    # API settings
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '1000 per hour')
    API_PAGINATION_DEFAULT = 20
    API_PAGINATION_MAX = 100
    
    # External API keys
    ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
    COINAPI_KEY = os.environ.get('COINAPI_KEY')
    YAHOO_FINANCE_API_KEY = os.environ.get('YAHOO_FINANCE_API_KEY')
    
    # Blockchain settings
    WEB3_PROVIDER_URL = os.environ.get('WEB3_PROVIDER_URL', 'https://mainnet.infura.io/v3/your-project-id')
    ETHEREUM_NETWORK = os.environ.get('ETHEREUM_NETWORK', 'mainnet')
    
    # Redis settings (for caching and sessions)
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Celery settings (for background tasks)
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', REDIS_URL)
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', REDIS_URL)
    
    # File storage settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Email settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Security settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    BCRYPT_LOG_ROUNDS = int(os.environ.get('BCRYPT_LOG_ROUNDS', '12'))
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'quantumvest.log')
    
    # Model settings
    MODEL_PATH = os.environ.get('MODEL_PATH', '../ai_models/')
    PREDICTION_CACHE_TTL = int(os.environ.get('PREDICTION_CACHE_TTL', '3600'))  # 1 hour
    
    # Performance settings
    ENABLE_PROFILING = os.environ.get('ENABLE_PROFILING', 'false').lower() == 'true'
    SLOW_QUERY_THRESHOLD = float(os.environ.get('SLOW_QUERY_THRESHOLD', '0.5'))
    
    # Feature flags
    ENABLE_PORTFOLIO_OPTIMIZATION = os.environ.get('ENABLE_PORTFOLIO_OPTIMIZATION', 'true').lower() == 'true'
    ENABLE_REAL_TIME_DATA = os.environ.get('ENABLE_REAL_TIME_DATA', 'true').lower() == 'true'
    ENABLE_BLOCKCHAIN_FEATURES = os.environ.get('ENABLE_BLOCKCHAIN_FEATURES', 'false').lower() == 'true'
    ENABLE_ADVANCED_ANALYTICS = os.environ.get('ENABLE_ADVANCED_ANALYTICS', 'true').lower() == 'true'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
    # Use SQLite for development if PostgreSQL not available
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///quantumvest_dev.db'
    
    # Relaxed security for development
    BCRYPT_LOG_ROUNDS = 4
    
    # Enable all features in development
    ENABLE_PORTFOLIO_OPTIMIZATION = True
    ENABLE_REAL_TIME_DATA = True
    ENABLE_BLOCKCHAIN_FEATURES = True
    ENABLE_ADVANCED_ANALYTICS = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    
    # Use in-memory SQLite for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Fast password hashing for tests
    BCRYPT_LOG_ROUNDS = 4
    
    # Disable rate limiting for tests
    API_RATE_LIMIT = None

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Ensure required environment variables are set
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to syslog in production
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

class DockerConfig(ProductionConfig):
    """Docker-specific configuration"""
    
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        # Log to stdout in Docker
        import logging
        import sys
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'docker': DockerConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

