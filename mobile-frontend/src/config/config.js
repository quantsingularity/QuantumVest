import Constants from 'expo-constants';

// Get configuration from app.config.js extra field
const extra = Constants.expoConfig?.extra || {};

export const Config = {
    API_BASE_URL: extra.apiBaseUrl || 'http://localhost:5000/api/v1',
    COINGECKO_API_URL: extra.coingeckoApiUrl || 'https://api.coingecko.com/api/v3',
    CRYPTONEWS_API_TOKEN: extra.cryptonewsApiToken || '',
    APP_ENV: extra.appEnv || 'development',
    ENABLE_MOCK_DATA: extra.enableMockData || false,

    // Helper methods
    isProduction: () => extra.appEnv === 'production',
    isDevelopment: () => extra.appEnv === 'development',
};

export default Config;
