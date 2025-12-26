export default ({ config }) => {
    return {
        ...config,
        name: 'QuantumVestMobile',
        slug: 'QuantumVestMobile',
        version: '1.0.0',
        orientation: 'portrait',
        icon: './assets/icon.png',
        userInterfaceStyle: 'light',
        newArchEnabled: true,
        splash: {
            image: './assets/splash-icon.png',
            resizeMode: 'contain',
            backgroundColor: '#ffffff',
        },
        ios: {
            supportsTablet: true,
            bundleIdentifier: 'com.quantumvest.mobile',
        },
        android: {
            adaptiveIcon: {
                foregroundImage: './assets/adaptive-icon.png',
                backgroundColor: '#ffffff',
            },
            package: 'com.quantumvest.mobile',
        },
        web: {
            favicon: './assets/favicon.png',
        },
        extra: {
            apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:5000/api/v1',
            coingeckoApiUrl: process.env.COINGECKO_API_URL || 'https://api.coingecko.com/api/v3',
            cryptonewsApiToken: process.env.CRYPTONEWS_API_TOKEN || '',
            appEnv: process.env.APP_ENV || 'development',
            enableMockData: process.env.ENABLE_MOCK_DATA === 'true',
        },
    };
};
