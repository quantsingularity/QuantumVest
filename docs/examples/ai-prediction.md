# AI Prediction Example

Get AI-powered price predictions for stocks and cryptocurrencies.

## Prerequisites

- QuantumVest backend running
- Valid access token

## Stock Prediction Example

```python
import requests

BASE_URL = 'http://localhost:5000/api/v1'
headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

# Get 1-week stock prediction
response = requests.get(
    f'{BASE_URL}/predictions/stocks/AAPL',
    headers=headers,
    params={'timeframe': '1w', 'include_analysis': True}
)

prediction = response.json()

print(f"Asset: {prediction['asset']['name']}")
print(f"Current Price: ${prediction['prediction']['current_price']:.2f}")
print(f"Predicted Price: ${prediction['prediction']['predicted_price']:.2f}")
print(f"Change: {prediction['prediction']['predicted_change_percent']:.2f}%")
print(f"Direction: {prediction['prediction']['direction']}")
print(f"Confidence: {prediction['prediction']['confidence_score']:.2%}")
print(f"\nConfidence Interval:")
print(f"  Lower: ${prediction['prediction']['confidence_interval']['lower']:.2f}")
print(f"  Upper: ${prediction['prediction']['confidence_interval']['upper']:.2f}")

if 'factors' in prediction:
    print(f"\nKey Drivers:")
    for driver in prediction['factors']['key_drivers']:
        print(f"  - {driver}")
```

## Crypto Prediction Example

```python
# Get Bitcoin prediction
response = requests.get(
    f'{BASE_URL}/predictions/crypto/BTC',
    headers=headers,
    params={'timeframe': '1d'}
)

prediction = response.json()
print(f"Bitcoin Prediction: ${prediction['prediction']['predicted_price']:.2f}")
print(f"Confidence: {prediction['prediction']['confidence_score']:.2%}")
```

## See Also

- [API Reference](../API.md)
- [Portfolio Management Example](portfolio-management.md)
