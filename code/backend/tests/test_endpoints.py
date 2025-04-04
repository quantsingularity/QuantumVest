import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_prediction_endpoint(client):
    response = client.post('/api/predict', json={
        'open': 150.25,
        'high': 152.30,
        'low': 149.50,
        'volume': 5000000
    })
    assert response.status_code == 200
    assert 'prediction' in response.json