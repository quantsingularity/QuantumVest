"""
Enhanced API Routes for QuantumVest
Comprehensive REST API with authentication, portfolio management, and advanced features
"""

import logging
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

from auth import AuthService, premium_required, rate_limit, token_required
from data_pipeline.crypto_api import CryptoDataFetcher
from data_pipeline.data_storage import DataStorage
from data_pipeline.prediction_service import PredictionService
from data_pipeline.stock_api import StockDataFetcher
from flask import Blueprint, jsonify, request
from models import Alert, Asset, Portfolio, User, Watchlist, WatchlistItem, db
from portfolio_service import PortfolioService

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

# Initialize services
prediction_service = PredictionService()
stock_fetcher = StockDataFetcher()
crypto_fetcher = CryptoDataFetcher()
data_storage = DataStorage()
portfolio_service = PortfolioService()

# ============================================================================
# Authentication Endpoints
# ============================================================================


@api_bp.route("/auth/register", methods=["POST"])
@rate_limit(limit=5, window=300)  # 5 registrations per 5 minutes
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if not all([username, email, password]):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Username, email, and password are required",
                    }
                ),
                400,
            )

        result = AuthService.register_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error in register endpoint: {e}")
        return jsonify({"success": False, "error": "Registration failed"}), 500


@api_bp.route("/auth/login", methods=["POST"])
@rate_limit(limit=10, window=300)  # 10 login attempts per 5 minutes
def login():
    """User login endpoint"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        username_or_email = data.get("username") or data.get("email")
        password = data.get("password")

        if not all([username_or_email, password]):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Username/email and password are required",
                    }
                ),
                400,
            )

        result = AuthService.login_user(username_or_email, password)

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        logger.error(f"Error in login endpoint: {e}")
        return jsonify({"success": False, "error": "Login failed"}), 500


@api_bp.route("/auth/refresh", methods=["POST"])
def refresh_token():
    """Refresh access token endpoint"""
    try:
        data = request.get_json()

        if not data or "refresh_token" not in data:
            return jsonify({"success": False, "error": "Refresh token required"}), 400

        result = AuthService.refresh_access_token(data["refresh_token"])

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        logger.error(f"Error in refresh token endpoint: {e}")
        return jsonify({"success": False, "error": "Token refresh failed"}), 500


@api_bp.route("/auth/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    """Get user profile endpoint"""
    try:
        return jsonify({"success": True, "user": current_user.to_dict()}), 200

    except Exception as e:
        logger.error(f"Error in get profile endpoint: {e}")
        return jsonify({"success": False, "error": "Failed to get profile"}), 500


@api_bp.route("/auth/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    """Update user profile endpoint"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Update allowed fields
        allowed_fields = [
            "first_name",
            "last_name",
            "phone",
            "risk_tolerance",
            "investment_experience",
            "preferred_currency",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(current_user, field, data[field])

        current_user.updated_at = datetime.now(timezone.utc)
        db.session.commit()

        return jsonify({"success": True, "user": current_user.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error in update profile endpoint: {e}")
        return jsonify({"success": False, "error": "Failed to update profile"}), 500


# ============================================================================
# Portfolio Management Endpoints
# ============================================================================


@api_bp.route("/portfolios", methods=["GET"])
@token_required
def get_portfolios(current_user):
    """Get user portfolios endpoint"""
    try:
        result = portfolio_service.get_user_portfolios(str(current_user.id))

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error in get portfolios endpoint: {e}")
        return jsonify({"success": False, "error": "Failed to get portfolios"}), 500


@api_bp.route("/portfolios", methods=["POST"])
@token_required
def create_portfolio(current_user):
    """Create portfolio endpoint"""
    try:
        data = request.get_json()

        if not data or "name" not in data:
            return (
                jsonify({"success": False, "error": "Portfolio name is required"}),
                400,
            )

        result = portfolio_service.create_portfolio(
            user_id=str(current_user.id),
            name=data["name"],
            description=data.get("description"),
            currency=data.get("currency", "USD"),
            is_default=data.get("is_default", False),
        )

        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error in create portfolio endpoint: {e}")
        return jsonify({"success": False, "error": "Failed to create portfolio"}), 500


@api_bp.route("/portfolios/<portfolio_id>", methods=["GET"])
@token_required
def get_portfolio_details(current_user, portfolio_id):
    """Get portfolio details endpoint"""
    try:
        result = portfolio_service.get_portfolio_details(
            portfolio_id=portfolio_id, user_id=str(current_user.id)
        )

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"Error in get portfolio details endpoint: {e}")
        return (
            jsonify({"success": False, "error": "Failed to get portfolio details"}),
            500,
        )


@api_bp.route("/portfolios/<portfolio_id>/transactions", methods=["POST"])
@token_required
def add_transaction(current_user, portfolio_id):
    """Add transaction endpoint"""
    try:
        data = request.get_json()

        required_fields = ["asset_symbol", "transaction_type", "quantity", "price"]
        if not data or not all(field in data for field in required_fields):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Asset symbol, transaction type, quantity, and price are required",
                    }
                ),
                400,
            )

        result = portfolio_service.add_transaction(
            portfolio_id=portfolio_id,
            user_id=str(current_user.id),
            asset_symbol=data["asset_symbol"],
            transaction_type=data["transaction_type"],
            quantity=float(data["quantity"]),
            price=float(data["price"]),
            fees=float(data.get("fees", 0)),
            notes=data.get("notes"),
        )

        if result["success"]:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error in add transaction endpoint: {e}")
        return jsonify({"success": False, "error": "Failed to add transaction"}), 500


@api_bp.route("/portfolios/<portfolio_id>/performance", methods=["GET"])
@token_required
def get_portfolio_performance(current_user, portfolio_id):
    """Get portfolio performance endpoint"""
    try:
        days = int(request.args.get("days", 30))

        result = portfolio_service.get_portfolio_performance(
            portfolio_id=portfolio_id, user_id=str(current_user.id), days=days
        )

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        logger.error(f"Error in get portfolio performance endpoint: {e}")
        return (
            jsonify({"success": False, "error": "Failed to get portfolio performance"}),
            500,
        )


@api_bp.route("/portfolios/<portfolio_id>/optimize", methods=["POST"])
@token_required
@premium_required
def optimize_portfolio(current_user, portfolio_id):
    """Optimize portfolio endpoint (Premium feature)"""
    try:
        data = request.get_json() or {}

        result = portfolio_service.optimize_portfolio(
            portfolio_id=portfolio_id,
            user_id=str(current_user.id),
            target_return=data.get("target_return"),
            risk_tolerance=data.get("risk_tolerance", current_user.risk_tolerance),
        )

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error in optimize portfolio endpoint: {e}")
        return jsonify({"success": False, "error": "Failed to optimize portfolio"}), 500


# ============================================================================
# Asset and Market Data Endpoints
# ============================================================================


@api_bp.route("/assets/search", methods=["GET"])
@token_required
def search_assets(current_user):
    """Search assets endpoint"""
    try:
        query = request.args.get("q", "").strip()
        asset_type = request.args.get("type", "").strip()
        limit = min(int(request.args.get("limit", 20)), 100)

        if not query:
            return jsonify({"success": False, "error": "Search query is required"}), 400

        # Build query
        search_query = Asset.query.filter(Asset.is_active == True)

        if asset_type:
            search_query = search_query.filter(Asset.asset_type == asset_type)

        # Search by symbol or name
        search_query = search_query.filter(
            db.or_(Asset.symbol.ilike(f"%{query}%"), Asset.name.ilike(f"%{query}%"))
        )

        assets = search_query.limit(limit).all()

        return (
            jsonify({"success": True, "assets": [asset.to_dict() for asset in assets]}),
            200,
        )

    except Exception as e:
        logger.error(f"Error in search assets endpoint: {e}")
        return jsonify({"success": False, "error": "Failed to search assets"}), 500


@api_bp.route("/data/stocks/<symbol>", methods=["GET"])
@token_required
def get_stock_data(current_user, symbol):
    """Get stock data endpoint"""
    try:
        # Parse query parameters
        interval = request.args.get("interval", "1d")
        use_cache = request.args.get("use_cache", "true").lower() == "true"

        # Fetch data
        if use_cache:
            df = data_storage.load_stock_data(symbol)
            if df is None or df.empty:
                df = stock_fetcher.fetch_data(symbol, interval=interval)
                if not df.empty:
                    data_storage.save_stock_data(df, symbol)
        else:
            df = stock_fetcher.fetch_data(symbol, interval=interval)
            if not df.empty:
                data_storage.save_stock_data(df, symbol)

        if df is None or df.empty:
            return (
                jsonify(
                    {"success": False, "error": f"No data available for stock {symbol}"}
                ),
                404,
            )

        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient="records")

        # Format timestamps for JSON
        for item in data:
            if "timestamp" in item:
                item["timestamp"] = item["timestamp"].strftime("%Y-%m-%d")

        return jsonify(
            {
                "success": True,
                "symbol": symbol,
                "interval": interval,
                "count": len(data),
                "data": data,
            }
        )

    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/data/crypto/<symbol>", methods=["GET"])
@token_required
def get_crypto_data(current_user, symbol):
    """Get cryptocurrency data endpoint"""
    try:
        # Parse query parameters
        interval = request.args.get("interval", "daily")
        use_cache = request.args.get("use_cache", "true").lower() == "true"

        # Fetch data
        if use_cache:
            df = data_storage.load_crypto_data(symbol)
            if df is None or df.empty:
                df = crypto_fetcher.fetch_data(symbol, interval=interval)
                if not df.empty:
                    data_storage.save_crypto_data(df, symbol)
        else:
            df = crypto_fetcher.fetch_data(symbol, interval=interval)
            if not df.empty:
                data_storage.save_crypto_data(df, symbol)

        if df is None or df.empty:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"No data available for cryptocurrency {symbol}",
                    }
                ),
                404,
            )

        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient="records")

        # Format timestamps for JSON
        for item in data:
            if "timestamp" in item:
                item["timestamp"] = item["timestamp"].strftime("%Y-%m-%d")

        return jsonify(
            {
                "success": True,
                "symbol": symbol,
                "interval": interval,
                "count": len(data),
                "data": data,
            }
        )

    except Exception as e:
        logger.error(f"Error fetching crypto data for {symbol}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# Prediction Endpoints
# ============================================================================


@api_bp.route("/predictions/stocks/<symbol>", methods=["GET"])
@token_required
def get_stock_prediction(current_user, symbol):
    """Get stock prediction endpoint"""
    try:
        # Parse query parameters
        days_ahead = int(request.args.get("days_ahead", "7"))
        use_cache = request.args.get("use_cache", "true").lower() == "true"

        # Get prediction
        result = prediction_service.get_stock_prediction(
            symbol, days_ahead=days_ahead, use_cached=use_cache
        )

        if not result["success"]:
            return jsonify(result), 404

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error getting stock prediction for {symbol}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@api_bp.route("/predictions/crypto/<symbol>", methods=["GET"])
@token_required
def get_crypto_prediction(current_user, symbol):
    """Get cryptocurrency prediction endpoint"""
    try:
        # Parse query parameters
        days_ahead = int(request.args.get("days_ahead", "7"))
        use_cache = request.args.get("use_cache", "true").lower() == "true"

        # Get prediction
        result = prediction_service.get_crypto_prediction(
            symbol, days_ahead=days_ahead, use_cached=use_cache
        )

        if not result["success"]:
            return jsonify(result), 404

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error getting crypto prediction for {symbol}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# Watchlist Endpoints
# ============================================================================


@api_bp.route("/watchlists", methods=["GET"])
@token_required
def get_watchlists(current_user):
    """Get user watchlists endpoint"""
    try:
        watchlists = Watchlist.query.filter_by(user_id=current_user.id).all()

        watchlist_data = []
        for watchlist in watchlists:
            watchlist_dict = {
                "id": str(watchlist.id),
                "name": watchlist.name,
                "description": watchlist.description,
                "is_default": watchlist.is_default,
                "created_at": (
                    watchlist.created_at.isoformat() if watchlist.created_at else None
                ),
                "items_count": len(watchlist.items),
            }
            watchlist_data.append(watchlist_dict)

        return jsonify({"success": True, "watchlists": watchlist_data}), 200

    except Exception as e:
        logger.error(f"Error getting watchlists: {e}")
        return jsonify({"success": False, "error": "Failed to get watchlists"}), 500


@api_bp.route("/watchlists", methods=["POST"])
@token_required
def create_watchlist(current_user):
    """Create watchlist endpoint"""
    try:
        data = request.get_json()

        if not data or "name" not in data:
            return (
                jsonify({"success": False, "error": "Watchlist name is required"}),
                400,
            )

        watchlist = Watchlist(
            user_id=current_user.id,
            name=data["name"],
            description=data.get("description"),
            is_default=data.get("is_default", False),
        )

        db.session.add(watchlist)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "watchlist": {
                        "id": str(watchlist.id),
                        "name": watchlist.name,
                        "description": watchlist.description,
                        "is_default": watchlist.is_default,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating watchlist: {e}")
        return jsonify({"success": False, "error": "Failed to create watchlist"}), 500


# ============================================================================
# Health and System Endpoints
# ============================================================================


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "version": "2.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "database": True,
                "prediction": True,
                "data_fetching": True,
                "storage": True,
            },
        }
    )


@api_bp.route("/models/status", methods=["GET"])
@token_required
def get_model_status(current_user):
    """Get model status endpoint"""
    try:
        # Get available models
        available_models = prediction_service.get_available_models()

        return jsonify({"success": True, "available_models": available_models})

    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
