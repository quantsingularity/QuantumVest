"""
Enhanced Flask Application
Main Flask application with integrated data pipeline and prediction API
"""
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import logging

# Import API routes
from api_routes import api_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__, static_folder='../web-frontend/build')
CORS(app)

# Register API blueprint
app.register_blueprint(api_bp)

# Legacy endpoints for backward compatibility
@app.route('/api/health', methods=['GET'])
def health_check():
    """Legacy health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'environment': os.environ.get('FLASK_ENV', 'production')
    })

@app.route('/api/blockchain-data/<asset>', methods=['GET'])
def blockchain_data(asset):
    """Legacy blockchain data endpoint"""
    # Redirect to new API endpoint
    return jsonify({
        'success': True,
        'message': 'Please use the new API endpoint: /api/v1/data/crypto/' + asset,
        'data': []
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Legacy prediction endpoint"""
    try:
        data = request.json
        
        # Extract parameters
        asset = data.get('asset', 'BTC')
        timeframe = data.get('timeframe', '7d')
        
        # Determine asset type and redirect to new API
        if asset in ['BTC', 'ETH', 'XRP', 'LTC', 'BCH', 'ADA', 'DOT', 'LINK', 'XLM', 'DOGE']:
            # Cryptocurrency
            days_ahead = 7
            if timeframe == '1d':
                days_ahead = 1
            elif timeframe == '7d':
                days_ahead = 7
            elif timeframe == '30d':
                days_ahead = 30
                
            # Redirect to new API endpoint
            return jsonify({
                'success': True,
                'message': f'Please use the new API endpoint: /api/v1/predictions/crypto/{asset.lower()}?days_ahead={days_ahead}',
                'prediction': 0,
                'confidence': 0,
                'asset': asset,
                'timeframe': timeframe
            })
        else:
            # Stock
            days_ahead = 7
            if timeframe == '1d':
                days_ahead = 1
            elif timeframe == '7d':
                days_ahead = 7
            elif timeframe == '30d':
                days_ahead = 30
                
            # Redirect to new API endpoint
            return jsonify({
                'success': True,
                'message': f'Please use the new API endpoint: /api/v1/predictions/stocks/{asset}?days_ahead={days_ahead}',
                'prediction': 0,
                'confidence': 0,
                'asset': asset,
                'timeframe': timeframe
            })
    except Exception as e:
        logger.error(f"Error in legacy predict endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_portfolio():
    """Legacy portfolio optimization endpoint"""
    try:
        data = request.json
        assets = data.get('assets', [])
        risk_tolerance = data.get('risk_tolerance', 0.5)
        
        # Mock optimization logic
        weights = []
        total = 0
        
        # Generate mock weights based on risk tolerance
        for i in range(len(assets)):
            if i == len(assets) - 1:
                weights.append(1.0 - total)
            else:
                weight = (1.0 / len(assets)) * (1 + (i * 0.1 * risk_tolerance))
                weights.append(round(weight, 2))
                total += weights[-1]
        
        return jsonify({
            'success': True,
            'optimal_weights': weights,
            'expected_return': 8.5 + (risk_tolerance * 3),
            'volatility': 5.0 + (risk_tolerance * 5),
            'sharpe_ratio': 1.2 + (risk_tolerance * 0.3)
        })
    except Exception as e:
        logger.error(f"Error in legacy optimize endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Serve static files from React build
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
