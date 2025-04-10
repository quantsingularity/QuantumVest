#!/usr/bin/env python3
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='../frontend/build')
CORS(app)

# Mock data for demonstration
mock_data = {
    'BTC': [
        {'timestamp': 1617235200, 'price': 58900, 'volume': 67000000000},
        {'timestamp': 1617321600, 'price': 59200, 'volume': 65000000000},
        {'timestamp': 1617408000, 'price': 57800, 'volume': 62000000000},
        {'timestamp': 1617494400, 'price': 58500, 'volume': 59000000000},
        {'timestamp': 1617580800, 'price': 59100, 'volume': 61000000000}
    ],
    'ETH': [
        {'timestamp': 1617235200, 'price': 1850, 'volume': 25000000000},
        {'timestamp': 1617321600, 'price': 1920, 'volume': 27000000000},
        {'timestamp': 1617408000, 'price': 1890, 'volume': 24000000000},
        {'timestamp': 1617494400, 'price': 1950, 'volume': 26000000000},
        {'timestamp': 1617580800, 'price': 2020, 'volume': 28000000000}
    ]
}

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'environment': os.environ.get('FLASK_ENV', 'production')
    })

# Blockchain data endpoint
@app.route('/api/blockchain-data/<asset>', methods=['GET'])
def blockchain_data(asset):
    if asset in mock_data:
        return jsonify({
            'success': True,
            'data': mock_data[asset]
        })
    else:
        return jsonify({
            'success': False,
            'error': f'Data for {asset} not found'
        }), 404

# Prediction endpoint
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Mock prediction logic
        asset = data.get('asset', 'BTC')
        timeframe = data.get('timeframe', '7d')
        current_price = data.get('current_price', 45000)
        
        # Generate mock prediction
        prediction = current_price * 1.05  # Simple 5% increase prediction
        
        return jsonify({
            'success': True,
            'prediction': prediction,
            'confidence': 0.85,
            'asset': asset,
            'timeframe': timeframe
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Portfolio optimization endpoint
@app.route('/api/optimize', methods=['POST'])
def optimize_portfolio():
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
