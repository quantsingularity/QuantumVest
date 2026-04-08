"""
Configuration for QuantumVest Backend.
"""

import os
from datetime import timedelta
from typing import Any, Dict, Optional


def _engine_options(db_url: str) -> Dict[str, Any]:
    if db_url.startswith("sqlite"):
        return {}
    return {"pool_size": 10, "pool_recycle": 120, "pool_pre_ping": True}


class Config:
    SECRET_KEY: str = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///quantumvest.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {}

    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=7)

    API_RATE_LIMIT: str = os.environ.get("API_RATE_LIMIT", "1000 per hour")
    API_PAGINATION_DEFAULT: int = 20
    API_PAGINATION_MAX: int = 100

    ALPHA_VANTAGE_API_KEY: Optional[str] = os.environ.get("ALPHA_VANTAGE_API_KEY")
    COINAPI_KEY: Optional[str] = os.environ.get("COINAPI_KEY")

    REDIS_URL: str = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TYPE: str = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT: int = 300

    UPLOAD_FOLDER: str = os.environ.get("UPLOAD_FOLDER", "uploads")
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
    BCRYPT_LOG_ROUNDS: int = int(os.environ.get("BCRYPT_LOG_ROUNDS", "12"))

    MAX_LOGIN_ATTEMPTS: int = int(os.environ.get("MAX_LOGIN_ATTEMPTS", "5"))
    ACCOUNT_LOCKOUT_MINUTES: int = int(os.environ.get("ACCOUNT_LOCKOUT_MINUTES", "30"))

    MODEL_PATH: str = os.environ.get("MODEL_PATH", "resources/models")
    DATA_PATH: str = os.environ.get("DATA_PATH", "resources/data")


class DevelopmentConfig(Config):
    DEBUG: bool = True
    TESTING: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DEV_DATABASE_URL", "sqlite:///quantumvest_dev.db"
    )
    BCRYPT_LOG_ROUNDS: int = 4


class TestingConfig(Config):
    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    WTF_CSRF_ENABLED: bool = False
    BCRYPT_LOG_ROUNDS: int = 4
    API_RATE_LIMIT: Optional[str] = None


class ProductionConfig(Config):
    DEBUG: bool = False
    TESTING: bool = False

    @classmethod
    def init_app(cls, app: Any) -> None:
        import logging
        from logging.handlers import SysLogHandler

        handler = SysLogHandler()
        handler.setLevel(logging.WARNING)
        app.logger.addHandler(handler)


_config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config(env: Optional[str] = None) -> type:
    if env is None:
        env = os.environ.get("FLASK_ENV", "development")
    return _config_map.get(env, _config_map["default"])
