# Risk Analysis Example

Comprehensive risk analysis for portfolios.

## Prerequisites

- QuantumVest backend running
- Valid access token
- Existing portfolio with positions

## Risk Metrics Example

```python
import requests

BASE_URL = 'http://localhost:5000/api/v1'
headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}

portfolio_id = 'your-portfolio-id'

# Get risk metrics
response = requests.get(
    f'{BASE_URL}/portfolios/{portfolio_id}/risk',
    headers=headers
)

risk = response.json()

print("=== Risk Metrics ===")
print(f"Value at Risk (95%): ${risk['var_95']:.2f}")
print(f"Expected Shortfall: ${risk['expected_shortfall']:.2f}")
print(f"Volatility: {risk['volatility']:.2%}")
print(f"Beta: {risk['beta']:.2f}")
print(f"Sharpe Ratio: {risk['sharpe_ratio']:.2f}")
```

## Stress Testing Example

```python
# Run stress test
response = requests.post(
    f'{BASE_URL}/portfolios/{portfolio_id}/stress-test',
    headers=headers,
    json={
        'scenarios': ['market_crash', 'interest_rate_shock', 'inflation_surge']
    }
)

stress_results = response.json()

print("\n=== Stress Test Results ===")
for scenario, result in stress_results['scenarios'].items():
    print(f"{scenario}: {result['impact']:.2%} impact")
```

## See Also

- [Portfolio Management Example](portfolio-management.md)
- [API Reference](../API.md)
