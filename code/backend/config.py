import os

class Config:
    DB_URI = os.getenv('DB_URI', 'postgresql://user:pass@localhost/investment')
    WEB3_PROVIDER = os.getenv('WEB3_PROVIDER', 'http://localhost:8545')
    MODEL_PATH = os.getenv('MODEL_PATH', '../ai_models/prediction_model.pkl')