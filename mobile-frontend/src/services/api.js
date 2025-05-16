import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Define the base URL for the backend API
const API_BASE_URL = 'http://localhost:5000/api';
// Define the base URL for CoinGecko API
const COINGECKO_API_BASE_URL = 'https://api.coingecko.com/api/v3';
// Define the base URL for CryptoNews API
const CRYPTONEWS_API_BASE_URL = 'https://cryptonews-api.com/api/v1';
// Storage key for API token
const API_TOKEN_STORAGE_KEY = '@QuantumVest:cryptonews_api_token';

// Create axios instance for backend API
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- Token Management Functions ---

// Function to save API token to secure storage
export const saveCryptoNewsApiToken = async (token) => {
  try {
    await AsyncStorage.setItem(API_TOKEN_STORAGE_KEY, token);
    return true;
  } catch (error) {
    console.error('Error saving API token:', error);
    return false;
  }
};

// Function to retrieve API token from secure storage
export const getCryptoNewsApiToken = async () => {
  try {
    const token = await AsyncStorage.getItem(API_TOKEN_STORAGE_KEY);
    return token;
  } catch (error) {
    console.error('Error retrieving API token:', error);
    return null;
  }
};

// Function to clear API token from secure storage
export const clearCryptoNewsApiToken = async () => {
  try {
    await AsyncStorage.removeItem(API_TOKEN_STORAGE_KEY);
    return true;
  } catch (error) {
    console.error('Error clearing API token:', error);
    return false;
  }
};

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
  try {
    return apiClient.post('/optimize', { assets, risk_tolerance });
  } catch (error) {
    console.error('Portfolio optimization error:', error);
    // If backend is unavailable, return mock optimization data
    return Promise.resolve({
      data: {
        success: true,
        expected_return: 12.5 + (Math.random() * 5),
        volatility: 8.2 + (Math.random() * 3),
        sharpe_ratio: 1.4 + (Math.random() * 0.5),
        optimal_weights: assets.map(() => Math.random())
          .map((weight, _, weights) => weight / weights.reduce((sum, w) => sum + w, 0))
      }
    });
  }
};

// Function to check API health
export const checkApiHealth = () => {
  return apiClient.get('/health').catch(error => {
    console.warn('API health check failed:', error.message);
    return { data: { status: 'offline', message: 'Backend API is currently unavailable' } };
  });
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
  }).catch(error => {
    console.error(`Error fetching market chart for ${coinId}:`, error);
    // Return mock data if API fails
    return Promise.resolve({
      data: generateMockMarketChartData(days, coinId === 'bitcoin' ? 45000 : 3000)
    });
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
  }).catch(error => {
    console.error(`Error fetching coin data for ${coinId}:`, error);
    // Return mock data if API fails
    return Promise.resolve({
      data: generateMockCoinData(coinId)
    });
  });
};

// --- CryptoNews API Functions ---

// Function to get general crypto news
export const getCryptoNews = async (page = 1, items = 20, tickers = '') => {
  try {
    // Try to get token from storage
    const storedToken = await getCryptoNewsApiToken();
    
    // If we have a valid token, use it for the API request
    if (storedToken && storedToken !== 'YOUR_CRYPTONEWS_API_TOKEN') {
      return axios.get(CRYPTONEWS_API_BASE_URL, {
        params: {
          tickers: tickers || 'BTC,ETH,SOL', // Default to major cryptos if not specified
          items: items,
          page: page,
          token: storedToken,
        },
        headers: {
          'Accept': 'application/json',
        }
      });
    } else {
      // If no valid token, return mock news data
      console.warn('CryptoNews API token not found or invalid. Using mock data.');
      return Promise.resolve({
        data: {
          data: generateMockNewsData(items, page, tickers)
        }
      });
    }
  } catch (error) {
    console.error('Error in getCryptoNews:', error);
    // Return mock data in case of any error
    return Promise.resolve({
      data: {
        data: generateMockNewsData(items, page, tickers)
      }
    });
  }
};

// --- Mock Data Generation Functions ---

// Generate mock market chart data
const generateMockMarketChartData = (days, basePrice) => {
  const numDays = parseInt(days) || 7;
  const prices = [];
  const volumes = [];
  const marketCaps = [];
  
  const now = Date.now();
  const dayInMs = 24 * 60 * 60 * 1000;
  
  for (let i = 0; i < numDays; i++) {
    const timestamp = now - ((numDays - i - 1) * dayInMs);
    const randomFactor = 1 + (Math.random() * 0.1 - 0.05); // -5% to +5%
    const price = basePrice * randomFactor;
    const volume = basePrice * 1000000 * (0.5 + Math.random());
    const marketCap = price * (basePrice * 100000);
    
    prices.push([timestamp, price]);
    volumes.push([timestamp, volume]);
    marketCaps.push([timestamp, marketCap]);
  }
  
  return {
    prices,
    total_volumes: volumes,
    market_caps: marketCaps
  };
};

// Generate mock coin data
const generateMockCoinData = (coinId) => {
  const isEthereum = coinId.toLowerCase().includes('eth');
  const isBitcoin = coinId.toLowerCase().includes('btc') || coinId.toLowerCase().includes('bitcoin');
  const isSolana = coinId.toLowerCase().includes('sol');
  
  let basePrice, symbol, name;
  
  if (isEthereum) {
    basePrice = 3000 + (Math.random() * 300);
    symbol = 'eth';
    name = 'Ethereum';
  } else if (isBitcoin) {
    basePrice = 45000 + (Math.random() * 2000);
    symbol = 'btc';
    name = 'Bitcoin';
  } else if (isSolana) {
    basePrice = 100 + (Math.random() * 20);
    symbol = 'sol';
    name = 'Solana';
  } else {
    basePrice = 50 + (Math.random() * 200);
    symbol = coinId.substring(0, 3).toLowerCase();
    name = coinId.charAt(0).toUpperCase() + coinId.slice(1);
  }
  
  return {
    id: coinId,
    symbol: symbol,
    name: name,
    market_data: {
      current_price: {
        usd: basePrice,
        eur: basePrice * 0.92,
        gbp: basePrice * 0.78
      },
      market_cap: {
        usd: basePrice * 1000000000
      },
      total_volume: {
        usd: basePrice * 50000000
      },
      price_change_percentage_24h: (Math.random() * 10) - 5,
      price_change_percentage_7d: (Math.random() * 20) - 10,
      price_change_percentage_30d: (Math.random() * 40) - 20
    }
  };
};

// Generate mock news data
const generateMockNewsData = (items = 20, page = 1, tickers = '') => {
  const tickerList = tickers ? tickers.split(',') : ['BTC', 'ETH', 'SOL', 'DOGE', 'ADA'];
  const newsItems = [];
  const startIndex = (page - 1) * items;
  
  const headlines = [
    "Bitcoin Surges Past $50,000 as Institutional Interest Grows",
    "Ethereum 2.0 Upgrade: What Investors Need to Know",
    "Solana Ecosystem Expands with New DeFi Projects",
    "Regulatory Clarity: New Crypto Framework Announced",
    "NFT Market Shows Signs of Recovery After Slump",
    "DeFi Total Value Locked Reaches New All-Time High",
    "Major Bank Announces Crypto Custody Services",
    "Mining Difficulty Adjusts After Recent Hash Rate Changes",
    "Crypto Exchange Reports Record Trading Volume",
    "Central Bank Digital Currencies: The Future of Money?",
    "Quantum Computing: A Threat to Blockchain Security?",
    "Layer 2 Solutions Gain Traction Amid High Gas Fees",
    "Crypto Adoption Surges in Emerging Markets",
    "Metaverse Tokens Rally as Tech Giants Enter the Space",
    "Stablecoin Regulation: New Guidelines Proposed",
    "Green Bitcoin: Miners Shift to Renewable Energy",
    "Cross-Chain Bridges: Solving the Interoperability Challenge",
    "Crypto Tax Reporting: What You Need to Know",
    "Privacy Coins Face Regulatory Scrutiny",
    "Web3 Development: Building the Decentralized Internet"
  ];
  
  const sources = [
    "CryptoNews", "BlockchainDaily", "CoinDesk", "Cointelegraph", 
    "The Block", "Decrypt", "Bitcoin Magazine", "CryptoSlate"
  ];
  
  for (let i = 0; i < items; i++) {
    const index = startIndex + i;
    if (index >= 100) break; // Limit to 100 mock articles
    
    const randomHeadlineIndex = index % headlines.length;
    const randomSourceIndex = Math.floor(Math.random() * sources.length);
    
    // Generate random date within last 7 days
    const date = new Date();
    date.setDate(date.getDate() - Math.floor(Math.random() * 7));
    
    // Randomly select 1-3 tickers for this article
    const articleTickers = [];
    const numTickers = Math.floor(Math.random() * 3) + 1;
    for (let j = 0; j < numTickers; j++) {
      const randomTicker = tickerList[Math.floor(Math.random() * tickerList.length)];
      if (!articleTickers.includes(randomTicker)) {
        articleTickers.push(randomTicker);
      }
    }
    
    // Generate random sentiment
    const sentiments = ["Positive", "Neutral", "Negative"];
    const sentiment = sentiments[Math.floor(Math.random() * sentiments.length)];
    
    newsItems.push({
      news_id: `mock-${index}`,
      title: headlines[randomHeadlineIndex],
      text: `This is a mock article about ${articleTickers.join(', ')}. It contains placeholder content for development and testing purposes. In a production environment, this would be replaced with actual news content from the CryptoNews API.`,
      news_url: `https://example.com/news/${index}`,
      image_url: `https://picsum.photos/id/${(index % 50) + 1}/800/400`,
      date: date.toISOString(),
      source_name: sources[randomSourceIndex],
      sentiment: sentiment,
      tickers: articleTickers
    });
  }
  
  return newsItems;
};

export default apiClient; // Export the backend client for existing backend calls

