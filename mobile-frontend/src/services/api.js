import axios from 'axios';

// Define the base URL for the backend API
const API_BASE_URL = 'http://localhost:5000/api';
// Define the base URL for CoinGecko API
const COINGECKO_API_BASE_URL = 'https://api.coingecko.com/api/v3';
// Define the base URL for CryptoNews API
const CRYPTONEWS_API_BASE_URL = 'https://cryptonews-api.com/api/v1';
// Placeholder for CryptoNews API token - Replace with a real token if available
const CRYPTONEWS_API_TOKEN = 'YOUR_CRYPTONEWS_API_TOKEN'; // TODO: Replace with actual token or handle key management

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Backend API Functions ---

// Function to fetch blockchain data for a specific asset (MOCK - kept for reference, replaced by CoinGecko)
export const getBlockchainData_Mock = (asset) => {
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

// --- CoinGecko API Functions ---

// Function to get historical market chart data from CoinGecko
export const getCoinMarketChart = (coinId, days = '7', vsCurrency = 'usd') => {
  return axios.get(`${COINGECKO_API_BASE_URL}/coins/${coinId}/market_chart`, {
    params: {
      vs_currency: vsCurrency,
      days: days,
      interval: 'daily'
    },
    headers: {
      'Accept': 'application/json',
    }
  });
};

// Function to get basic coin data (like current price, symbol - might be useful later)
export const getCoinData = (coinId) => {
  return axios.get(`${COINGECKO_API_BASE_URL}/coins/${coinId}`, {
    params: {
      localization: 'false',
      tickers: 'false',
      market_data: 'true',
      community_data: 'false',
      developer_data: 'false',
      sparkline: 'false'
    },
    headers: {
      'Accept': 'application/json',
    }
  });
};

// --- CryptoNews API Functions ---

// Function to get general crypto news
export const getCryptoNews = (page = 1, items = 20) => {
  // Check if the placeholder token is still being used
  if (CRYPTONEWS_API_TOKEN === 'YOUR_CRYPTONEWS_API_TOKEN') {
    console.warn('CryptoNews API token is not set. Using fallback/demo mode if available, or request might fail.');
    // Optionally, return a mock response or throw an error
    // return Promise.resolve({ data: { data: [] } }); // Example mock
  }
  return axios.get(CRYPTONEWS_API_BASE_URL, {
    params: {
      // tickers: 'BTC,ETH', // Example: Filter by specific tickers if needed
      items: items,
      page: page,
      token: CRYPTONEWS_API_TOKEN,
    },
    headers: {
      'Accept': 'application/json',
    }
  });
};


export default apiClient; // Export the backend client for existing backend calls

