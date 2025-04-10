import React, { useState } from 'react';
import axios from 'axios';
import '../../styles/PortfolioOptimization.css';

export default function PortfolioOptimization() {
  const [risk, setRisk] = useState(5);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [assets, setAssets] = useState([
    { symbol: 'BTC', name: 'Bitcoin', allocation: 25, color: '#f7931a' },
    { symbol: 'ETH', name: 'Ethereum', allocation: 20, color: '#627eea' },
    { symbol: 'AAPL', name: 'Apple', allocation: 15, color: '#999999' },
    { symbol: 'MSFT', name: 'Microsoft', allocation: 15, color: '#00a1f1' },
    { symbol: 'GOOGL', name: 'Google', allocation: 10, color: '#4285f4' },
    { symbol: 'AMZN', name: 'Amazon', allocation: 10, color: '#ff9900' },
    { symbol: 'CASH', name: 'Cash', allocation: 5, color: '#85bb65' }
  ]);

  const handleRiskChange = (e) => {
    setRisk(parseInt(e.target.value, 10));
  };

  const handleAssetAllocationChange = (index, newValue) => {
    const updatedAssets = [...assets];
    updatedAssets[index].allocation = parseInt(newValue, 10);
    
    // Recalculate to ensure total is 100%
    const total = updatedAssets.reduce((sum, asset) => sum + asset.allocation, 0);
    if (total !== 100) {
      const diff = 100 - total;
      // Distribute the difference among other assets
      const otherAssets = updatedAssets.filter((_, i) => i !== index);
      const perAssetAdjustment = Math.floor(diff / otherAssets.length);
      let remainder = diff - (perAssetAdjustment * otherAssets.length);
      
      otherAssets.forEach((asset, i) => {
        const assetIndex = updatedAssets.findIndex(a => a.symbol === asset.symbol);
        let adjustment = perAssetAdjustment;
        if (i === 0 && remainder !== 0) {
          adjustment += remainder;
        }
        updatedAssets[assetIndex].allocation = Math.max(0, asset.allocation + adjustment);
      });
    }
    
    setAssets(updatedAssets);
  };

  const optimize = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await axios.post('/api/portfolio/optimize', {
        assets: assets.map(a => a.symbol),
        weights: assets.map(a => a.allocation / 100),
        riskLevel: risk
      });
      
      if (response.data.success) {
        // Transform the response into a more usable format
        const optimizedAssets = [...assets];
        const optimalWeights = response.data.optimal_weights;
        
        optimalWeights.forEach((weight, index) => {
          if (index < optimizedAssets.length) {
            optimizedAssets[index].allocation = Math.round(weight * 100);
          }
        });
        
        setResult({
          assets: optimizedAssets,
          expectedReturn: response.data.expected_return,
          volatility: response.data.volatility,
          sharpeRatio: response.data.sharpe_ratio
        });
      } else {
        setError('Optimization failed: ' + response.data.error);
      }
    } catch (err) {
      setError('Error during optimization: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Mock optimization for demonstration
  const mockOptimize = () => {
    setLoading(true);
    setError(null);
    
    // Simulate API call
    setTimeout(() => {
      try {
        // Create optimized allocation based on risk level
        const optimizedAssets = [...assets];
        
        if (risk <= 3) {
          // Low risk - more conservative allocation
          optimizedAssets[0].allocation = 15; // BTC
          optimizedAssets[1].allocation = 10; // ETH
          optimizedAssets[2].allocation = 20; // AAPL
          optimizedAssets[3].allocation = 20; // MSFT
          optimizedAssets[4].allocation = 15; // GOOGL
          optimizedAssets[5].allocation = 10; // AMZN
          optimizedAssets[6].allocation = 10; // CASH
        } else if (risk <= 7) {
          // Medium risk
          optimizedAssets[0].allocation = 25; // BTC
          optimizedAssets[1].allocation = 20; // ETH
          optimizedAssets[2].allocation = 15; // AAPL
          optimizedAssets[3].allocation = 15; // MSFT
          optimizedAssets[4].allocation = 10; // GOOGL
          optimizedAssets[5].allocation = 10; // AMZN
          optimizedAssets[6].allocation = 5;  // CASH
        } else {
          // High risk - more aggressive allocation
          optimizedAssets[0].allocation = 35; // BTC
          optimizedAssets[1].allocation = 30; // ETH
          optimizedAssets[2].allocation = 10; // AAPL
          optimizedAssets[3].allocation = 10; // MSFT
          optimizedAssets[4].allocation = 5;  // GOOGL
          optimizedAssets[5].allocation = 8;  // AMZN
          optimizedAssets[6].allocation = 2;  // CASH
        }
        
        setResult({
          assets: optimizedAssets,
          expectedReturn: (7 + risk * 0.8).toFixed(2),
          volatility: (5 + risk * 0.7).toFixed(2),
          sharpeRatio: (1.2 + risk * 0.1).toFixed(2)
        });
      } catch (err) {
        setError('Error during optimization simulation');
      } finally {
        setLoading(false);
      }
    }, 1500);
  };

  return (
    <div className="portfolio-container">
      <h1 className="section-title">Portfolio Optimization</h1>
      
      <div className="portfolio-content">
        <div className="current-allocation">
          <h2>Current Allocation</h2>
          
          <div className="asset-list">
            {assets.map((asset, index) => (
              <div className="asset-item" key={index}>
                <div className="asset-header">
                  <div className="asset-symbol" style={{ backgroundColor: asset.color }}>{asset.symbol}</div>
                  <div className="asset-name">{asset.name}</div>
                  <div className="asset-allocation">{asset.allocation}%</div>
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={asset.allocation}
                  onChange={(e) => handleAssetAllocationChange(index, e.target.value)}
                  className="allocation-slider"
                />
              </div>
            ))}
          </div>
          
          <div className="allocation-chart">
            <div className="chart-rings">
              {assets.map((asset, index) => {
                // Calculate the segment size and position
                const total = assets.reduce((sum, a, i) => i <= index ? sum + a.allocation : sum, 0);
                const start = total - asset.allocation;
                return (
                  <div 
                    key={index}
                    className="chart-segment"
                    style={{
                      backgroundColor: asset.color,
                      clipPath: `conic-gradient(from 0deg, transparent ${start}%, ${asset.color} ${start}%, ${asset.color} ${total}%, transparent ${total}%)`
                    }}
                  />
                );
              })}
              <div className="chart-center"></div>
            </div>
          </div>
        </div>
        
        <div className="optimization-controls">
          <h2>Risk Tolerance</h2>
          <div className="risk-slider-container">
            <span className="risk-label">Conservative</span>
            <input
              type="range"
              min="1"
              max="10"
              value={risk}
              onChange={handleRiskChange}
              className="risk-slider"
            />
            <span className="risk-label">Aggressive</span>
            <div className="risk-value">Level: {risk}</div>
          </div>
          
          <button 
            className="optimize-button" 
            onClick={mockOptimize}
            disabled={loading}
          >
            {loading ? 'Optimizing...' : 'Optimize Portfolio'}
          </button>
          
          {error && <div className="error-message">{error}</div>}
        </div>
        
        {result && (
          <div className="optimization-result">
            <h2>Optimized Portfolio</h2>
            
            <div className="result-metrics">
              <div className="metric-card">
                <h3>Expected Return</h3>
                <p className="metric-value">{result.expectedReturn}%</p>
              </div>
              <div className="metric-card">
                <h3>Volatility</h3>
                <p className="metric-value">{result.volatility}%</p>
              </div>
              <div className="metric-card">
                <h3>Sharpe Ratio</h3>
                <p className="metric-value">{result.sharpeRatio}</p>
              </div>
            </div>
            
            <div className="optimized-allocation">
              <h3>Recommended Allocation</h3>
              <div className="allocation-chart optimized-chart">
                <div className="chart-rings">
                  {result.assets.map((asset, index) => {
                    // Calculate the segment size and position
                    const total = result.assets.reduce((sum, a, i) => i <= index ? sum + a.allocation : sum, 0);
                    const start = total - asset.allocation;
                    return (
                      <div 
                        key={index}
                        className="chart-segment"
                        style={{
                          backgroundColor: asset.color,
                          clipPath: `conic-gradient(from 0deg, transparent ${start}%, ${asset.color} ${start}%, ${asset.color} ${total}%, transparent ${total}%)`
                        }}
                      />
                    );
                  })}
                  <div className="chart-center"></div>
                </div>
              </div>
              
              <div className="asset-list optimized-list">
                {result.assets.map((asset, index) => (
                  <div className="asset-item optimized-item" key={index}>
                    <div className="asset-header">
                      <div className="asset-symbol" style={{ backgroundColor: asset.color }}>{asset.symbol}</div>
                      <div className="asset-name">{asset.name}</div>
                      <div className="asset-allocation">{asset.allocation}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}