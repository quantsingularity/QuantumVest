"""
API Routes Module
Defines Flask API routes for data and predictions
"""
import os
import logging
from flask import Blueprint, jsonify, request
from typing import Dict, List, Any, Optional, Union

from .data_pipeline.prediction_service import PredictionService
from .data_pipeline.stock_api import StockDataFetcher
from .data_pipeline.crypto_api import CryptoDataFetcher
from .data_pipeline.data_storage import DataStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Initialize services
prediction_service = PredictionService()
stock_fetcher = StockDataFetcher()
crypto_fetcher = CryptoDataFetcher()
data_storage = DataStorage()

# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'services': {
            'prediction': True,
            'data_fetching': True,
            'storage': True
        }
    })

# Stock data endpoints
@api_bp.route('/data/stocks/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """Get stock data endpoint"""
    try:
        # Parse query parameters
        interval = request.args.get('interval', '1d')
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'
        
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
            return jsonify({
                'success': False,
                'error': f'No data available for stock {symbol}'
            }), 404
        
        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        
        # Format timestamps for JSON
        for item in data:
            if 'timestamp' in item:
                item['timestamp'] = item['timestamp'].strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'interval': interval,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Crypto data endpoints
@api_bp.route('/data/crypto/<symbol>', methods=['GET'])
def get_crypto_data(symbol):
    """Get cryptocurrency data endpoint"""
    try:
        # Parse query parameters
        interval = request.args.get('interval', 'daily')
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'
        
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
            return jsonify({
                'success': False,
                'error': f'No data available for cryptocurrency {symbol}'
            }), 404
        
        # Convert DataFrame to list of dictionaries
        data = df.to_dict(orient='records')
        
        # Format timestamps for JSON
        for item in data:
            if 'timestamp' in item:
                item['timestamp'] = item['timestamp'].strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'symbol': symbol,
            'interval': interval,
            'count': len(data),
            'data': data
        })
        
    except Exception as e:
        logger.error(f"Error fetching crypto data for {symbol}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Stock prediction endpoints
@api_bp.route('/predictions/stocks/<symbol>', methods=['GET'])
def get_stock_prediction(symbol):
    """Get stock prediction endpoint"""
    try:
        # Parse query parameters
        days_ahead = int(request.args.get('days_ahead', '7'))
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'
        
        # Get prediction
        result = prediction_service.get_stock_prediction(
            symbol, 
            days_ahead=days_ahead,
            use_cached=use_cache
        )
        
        if not result['success']:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting stock prediction for {symbol}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Crypto prediction endpoints
@api_bp.route('/predictions/crypto/<symbol>', methods=['GET'])
def get_crypto_prediction(symbol):
    """Get cryptocurrency prediction endpoint"""
    try:
        # Parse query parameters
        days_ahead = int(request.args.get('days_ahead', '7'))
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'
        
        # Get prediction
        result = prediction_service.get_crypto_prediction(
            symbol, 
            days_ahead=days_ahead,
            use_cached=use_cache
        )
        
        if not result['success']:
            return jsonify(result), 404
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error getting crypto prediction for {symbol}: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Model status endpoint
@api_bp.route('/models/status', methods=['GET'])
def get_model_status():
    """Get model status endpoint"""
    try:
        # Get available models
        available_models = prediction_service.get_available_models()
        
        return jsonify({
            'success': True,
            'available_models': available_models
        })
        
    except Exception as e:
        logger.error(f"Error getting model status: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
