import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/Dashboard.css';

export default function Dashboard() {
  const [marketData, setMarketData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    totalAssets: 0,
    totalGain: 0,
    performance: 0
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/blockchain-data/ETH');
        if (response.data.success) {
          setMarketData(response.data.data || []);

          // Calculate some mock statistics
          const mockStats = {
            totalAssets: 25430.78,
            totalGain: 1245.32,
            performance: 4.9
          };
          setStats(mockStats);
        } else {
          setError('Failed to fetch data');
        }
      } catch (err) {
        setError('Error fetching market data: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading-container">Loading dashboard data...</div>;
  }

  if (error) {
    return <div className="error-container">{error}</div>;
  }

  return (
    <div className="dashboard-container">
      <h1 className="section-title">Investment Dashboard</h1>

      <div className="stats-overview">
        <div className="stat-card">
          <h3>Total Assets</h3>
          <p className="stat-value">${stats.totalAssets.toLocaleString()}</p>
        </div>
        <div className="stat-card">
          <h3>Total Gain/Loss</h3>
          <p className={`stat-value ${stats.totalGain >= 0 ? 'positive' : 'negative'}`}>
            {stats.totalGain >= 0 ? '+' : ''}{stats.totalGain.toLocaleString()}
          </p>
        </div>
        <div className="stat-card">
          <h3>Performance</h3>
          <p className={`stat-value ${stats.performance >= 0 ? 'positive' : 'negative'}`}>
            {stats.performance >= 0 ? '+' : ''}{stats.performance}%
          </p>
        </div>
      </div>

      <h2 className="section-title">Recent Market Data</h2>

      <div className="market-data-grid">
        {marketData.slice(-5).map((entry, index) => (
          <div className="market-card" key={index}>
            <div className="market-card-header">
              <h3>ETH</h3>
              <span className="date">{new Date(entry.timestamp*1000).toLocaleDateString()}</span>
            </div>
            <div className="market-card-content">
              <p className="price">Price: <span>${parseFloat(entry.price).toLocaleString()}</span></p>
              <p className="volume">Volume: <span>{parseInt(entry.volume).toLocaleString()}</span></p>
            </div>
          </div>
        ))}
      </div>

      {marketData.length === 0 && (
        <div className="no-data-message">
          <p>No market data available. Connect to blockchain for real-time data.</p>
        </div>
      )}
    </div>
  );
}
