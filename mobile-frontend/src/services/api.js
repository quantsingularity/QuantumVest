import axios from 'axios';

// Define the base URL for the backend API
// Assuming the backend runs on localhost:5000 during development
// This might need to be updated based on the actual deployment URL
const API_BASE_URL = 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to fetch blockchain data for a specific asset
export const getBlockchainData = (asset) => {
  return apiClient.get(`/blockchain-data/${asset}`);
};

// Function to get a prediction for an asset
export const getPrediction = (asset, timeframe, current_price) => {
  return apiClient.post('/predict', { asset, timeframe, current_price });
};

// Function to optimize a portfolio
export const optimizePortfolio = (assets, risk_tolerance) => {
  return apiClient.post('/optimize', { assets, risk_tolerance });
};

// Function to check API health
export const checkApiHealth = () => {
  return apiClient.get('/health');
};

export default apiClient;

