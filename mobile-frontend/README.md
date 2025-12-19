# QuantumVest Mobile Frontend

AI-Powered Predictive Investment Analytics Platform - Mobile Application

## Overview

The QuantumVest Mobile application provides users with a comprehensive mobile experience for investment analytics, portfolio management, and market predictions. Built with React Native and Expo, it offers cross-platform support for both iOS and Android devices.

## Features

- **Authentication**: Secure user registration and login with JWT tokens
- **Dashboard**: Real-time market data visualization with Bitcoin and Ethereum price trends
- **Portfolio Optimization**: AI-powered portfolio optimization with risk analysis
- **Market Predictions**: Get price predictions for cryptocurrencies and stocks
- **Watchlist**: Track your favorite assets with live price updates
- **News Feed**: Stay updated with the latest cryptocurrency news
- **Settings**: Customize app preferences and API configurations
- **Offline Support**: Fallback to mock data when APIs are unavailable

## Technology Stack

- **Framework**: React Native 0.76.9 with Expo 52
- **Navigation**: React Navigation 7
- **UI Library**: React Native Paper 5
- **State Management**: React Context API
- **Charts**: React Native Chart Kit
- **Storage**: AsyncStorage
- **Testing**: Jest, React Native Testing Library, Detox (E2E)
- **API**: Axios for HTTP requests

## Prerequisites

Before you begin, ensure you have the following installed:

- Node.js (v14 or higher)
- npm or yarn package manager
- Expo CLI (`npm install -g expo-cli`)
- For iOS: Xcode (Mac only)
- For Android: Android Studio with Android SDK
- For E2E testing: Detox CLI (`npm install -g detox-cli`)

## Installation

1. **Clone the repository** (if not already done):

    ```bash
    cd mobile-frontend
    ```

2. **Install dependencies**:

    ```bash
    npm install
    # or
    yarn install
    ```

3. **Configure environment variables**:

    ```bash
    cp .env.example .env
    # Edit .env and update the values as needed
    ```

4. **Start the backend API** (required for full functionality):
    ```bash
    # In a separate terminal, navigate to the backend directory
    cd ../code/backend
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    python app.py
    ```

## Running the Application

### Development Mode

1. **Start the Expo development server**:

    ```bash
    npm start
    # or
    yarn start
    ```

2. **Run on specific platform**:

    ```bash
    # iOS (Mac only)
    npm run ios
    # or
    yarn ios

    # Android
    npm run android
    # or
    yarn android

    # Web
    npm run web
    # or
    yarn web
    ```

3. **Scan QR code** with Expo Go app on your physical device for quick testing.

### Production Build

#### iOS

```bash
expo build:ios
```

#### Android

```bash
expo build:android
```

## Testing

### Unit and Integration Tests

Run all tests with coverage:

```bash
npm test
# or
yarn test
```

Run tests in watch mode:

```bash
npm run test:watch
# or
yarn test:watch
```

### End-to-End Tests (Detox)

1. **Build the app for testing**:

    ```bash
    # iOS
    npm run test:e2e:build -- --configuration ios.sim.debug

    # Android
    npm run test:e2e:build -- --configuration android.emu.debug
    ```

2. **Run E2E tests**:

    ```bash
    # iOS
    npm run test:e2e -- --configuration ios.sim.debug

    # Android
    npm run test:e2e -- --configuration android.emu.debug
    ```

## Project Structure

```
mobile-frontend/
├── __mocks__/              # Jest mocks
├── assets/                 # Images, fonts, and static resources
├── e2e/                    # End-to-end tests
│   ├── app.test.js        # E2E test scenarios
│   └── jest.config.js     # E2E Jest configuration
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── ErrorBoundary.js
│   │   └── LoadingSpinner.js
│   ├── context/           # React Context providers
│   │   ├── AppContext.js  # Global app state
│   │   └── AuthContext.js # Authentication state
│   ├── navigation/        # Navigation configuration
│   │   ├── AppNavigator.js
│   │   └── RootNavigator.js
│   ├── screens/           # Application screens
│   │   ├── __tests__/     # Screen tests
│   │   ├── DashboardScreen.js
│   │   ├── LoginScreen.js
│   │   ├── RegisterScreen.js
│   │   ├── NewsScreen.js
│   │   ├── PredictionScreen.js
│   │   ├── PortfolioScreen.js
│   │   ├── WatchlistScreen.js
│   │   └── SettingsScreen.js
│   ├── services/          # API and external services
│   │   └── api.js
│   └── utils/             # Utility functions
│       └── errorHandler.js
├── .detoxrc.js            # Detox configuration
├── .env.example           # Environment variables template
├── App.js                 # Root component
├── app.json               # Expo configuration
├── babel.config.js        # Babel configuration
├── index.js               # Entry point
├── jest.config.js         # Jest configuration
├── jest.setup.js          # Jest setup file
├── metro.config.js        # Metro bundler configuration
├── package.json           # Dependencies and scripts
└── README.md             # This file
```

## API Integration

The mobile frontend integrates with the following APIs:

### Backend API (Required for full features)

- **Base URL**: `http://localhost:5000/api/v1`
- **Endpoints**:
    - `/auth/login` - User authentication
    - `/auth/register` - User registration
    - `/predictions/crypto/{symbol}` - Crypto predictions
    - `/predictions/stocks/{symbol}` - Stock predictions
    - `/portfolios/{id}/optimize` - Portfolio optimization
    - `/health` - API health check

### External APIs (Optional - fallback to mock data)

- **CoinGecko API**: Real-time cryptocurrency market data (no key required)
- **CryptoNews API**: Cryptocurrency news articles (requires API token)

To use CryptoNews API:

1. Sign up at https://cryptonews-api.com/
2. Get your free API token
3. Configure it in the app Settings screen

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Backend API Configuration
API_BASE_URL=http://localhost:5000/api/v1

# CoinGecko API (No key required)
COINGECKO_API_URL=https://api.coingecko.com/api/v3

# CryptoNews API Token (Optional)
CRYPTONEWS_API_TOKEN=your_cryptonews_api_token_here

# Application Configuration
APP_ENV=development
ENABLE_MOCK_DATA=false
```

## Features in Detail

### Authentication

- User registration with validation
- Secure login with JWT tokens
- Guest access for quick exploration
- Token refresh mechanism
- Persistent authentication state

### Dashboard

- Real-time Bitcoin and Ethereum price charts
- Backend API health monitoring
- Quick navigation to all features
- Responsive chart visualization

### Portfolio Optimization

- Input multiple assets
- Configure risk tolerance
- Get optimal portfolio weights
- View expected returns and volatility
- Calculate Sharpe ratio

### Market Predictions

- Support for both cryptocurrencies and stocks
- Configurable timeframes
- Confidence scoring
- Historical data integration

### Watchlist

- Add/remove assets
- Real-time price updates
- Persistent storage
- Pull-to-refresh functionality

### News Feed

- Latest cryptocurrency news
- Sentiment analysis
- Multiple sources
- Infinite scroll
- Article preview and external links

## Troubleshooting

### Common Issues

1. **Metro bundler not starting**:

    ```bash
    npm start -- --reset-cache
    ```

2. **iOS build fails**:

    ```bash
    cd ios && pod install && cd ..
    ```

3. **Android build fails**:
    - Ensure Android SDK is properly installed
    - Check `ANDROID_HOME` environment variable
    - Clean gradle: `cd android && ./gradlew clean && cd ..`

4. **API connection errors**:
    - Verify backend is running on `http://localhost:5000`
    - For Android emulator, use `http://10.0.2.2:5000` instead
    - For iOS simulator, use `http://localhost:5000` or your machine's IP
    - Update `API_BASE_URL` in `src/services/api.js` if needed

5. **Test failures**:
    ```bash
    npm test -- --clearCache
    ```

## Development Guidelines

### Code Style

- Use ESLint for code linting
- Follow React Native best practices
- Write tests for new features
- Use TypeScript types where applicable
- Follow component naming conventions

### Git Workflow

1. Create feature branch from `main`
2. Make changes and commit with descriptive messages
3. Write/update tests
4. Run tests and ensure they pass
5. Submit pull request for review

### Performance Optimization

- Use `React.memo()` for expensive components
- Implement proper list virtualization with `FlatList`
- Lazy load screens with React Navigation
- Optimize images and assets
- Monitor bundle size

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
