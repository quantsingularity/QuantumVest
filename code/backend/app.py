from flask import Flask, jsonify, request
from web3 import Web3
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
model = joblib.load('../ai_models/prediction_model.pkl')

# Load contract ABIs
with open('../blockchain/build/contracts/DataTracking.json') as f:
    data_tracking_abi = json.load(f)['abi']

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return jsonify({'prediction': prediction[0]})

@app.route('/api/blockchain-data/<ticker>')
def get_blockchain_data(ticker):
    contract = w3.eth.contract(
        address='0x...', 
        abi=data_tracking_abi
    )
    data = contract.functions.getHistoricalData(ticker).call()
    return jsonify([{'timestamp': d[0], 'price': d[1], 'volume': d[2]} for d in data])