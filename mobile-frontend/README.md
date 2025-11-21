# Mobile Frontend Directory

The `mobile-frontend` directory contains the React Native mobile application for QuantumVest, providing users with a responsive and feature-rich mobile experience. This mobile application allows users to access QuantumVest's investment platform, portfolio management tools, and financial analytics on iOS and Android devices.

## Directory Structure

The mobile-frontend directory is organized as follows:

```
mobile-frontend/
├── .expo/
├── App.js
├── app.json
├── assets/
├── index.js
├── package.json
├── src/
└── yarn.lock
```

## Components

### Core Files

- **App.js**: The main entry point for the React Native application. This file initializes the app, sets up navigation, and configures global state management.

- **index.js**: The JavaScript entry point that registers the application with the React Native runtime.

- **app.json**: Contains configuration for the Expo build system, including app name, version, orientation settings, and other metadata required for building and publishing the mobile application.

- **package.json**: Defines the project dependencies, scripts, and metadata for the Node.js ecosystem. This file is essential for managing the project's npm/yarn packages.

- **yarn.lock**: Ensures consistent installations across different environments by locking dependency versions.

### Directories

- **.expo/**: Contains Expo-specific configuration files and caches. This directory is managed by the Expo CLI and should not be manually edited.

- **assets/**: Stores static resources used by the mobile application, including images, fonts, and other media files. These assets are bundled with the application during the build process.

- **src/**: Contains the source code for the mobile application, organized into several subdirectories:
  - **components/**: Reusable UI components
  - **screens/**: Individual application screens
  - **navigation/**: Navigation configuration and routing
  - **services/**: API integration and business logic
  - **utils/**: Utility functions and helpers
  - **styles/**: Global styling and theme definitions
  - **store/**: State management (Redux/Context API)

## Development Environment

### Prerequisites

To work on the mobile frontend, you'll need:

- Node.js (version 14 or higher)
- Yarn or npm package manager
- Expo CLI (`npm install -g expo-cli`)
- iOS Simulator (for Mac users) or Android Emulator
- Expo Go app on a physical device (optional for testing)

### Getting Started

1. Install dependencies:

   ```
   cd mobile-frontend
   yarn install
   ```

2. Start the development server:

   ```
   yarn start
   ```

3. Run on a specific platform:
   ```
   yarn ios     # For iOS simulator
   yarn android # For Android emulator
   ```

The Expo development server provides a QR code that can be scanned with the Expo Go app on a physical device for testing on real hardware.

## Key Features

The mobile application provides several key features:

- **User Authentication**: Secure login, registration, and account management
- **Portfolio Dashboard**: Real-time overview of investment portfolios
- **Market Data**: Current market trends and financial instrument data
- **Investment Tools**: AI-powered investment recommendations
- **Transaction History**: Record of past investment activities
- **Notifications**: Alerts for market changes and portfolio updates
- **Settings**: User preferences and application configuration

## Integration Points

The mobile frontend integrates with several backend services:

- **REST API**: Communicates with the QuantumVest backend services for data retrieval and updates
- **WebSocket**: Establishes real-time connections for market data updates
- **Authentication Service**: Manages user sessions and security
- **Analytics**: Tracks user behavior and application performance

## Building for Production

To create a production build:

1. Update the version in app.json
2. Configure the appropriate build settings for each platform
3. Run the build command:
   ```
   expo build:ios
   expo build:android
   ```

The build process can be customized through the Expo configuration in app.json or by ejecting to a bare React Native project for more control.

## Testing

The mobile application includes several types of tests:

- **Unit Tests**: Verify individual component functionality
- **Integration Tests**: Ensure components work together correctly
- **End-to-End Tests**: Validate complete user flows

Run tests using:

```
yarn test
```

## Design System

The mobile application follows a consistent design system defined in the styles directory. This includes:

- Typography scales
- Color palettes
- Spacing constants
- Component themes
- Responsive layout utilities

Adhering to this design system ensures a consistent user experience across the application.

## Performance Considerations

Mobile performance is critical for user satisfaction. The application implements several optimizations:

- Efficient list rendering with virtualization
- Lazy loading of screens and components
- Image optimization and caching
- Minimized network requests
- Memory management best practices

## Additional Resources

For more information about the mobile frontend:

- Refer to the UI design documentation in the docs directory
- Check the developer guide for coding standards and best practices
- Review the API documentation for backend integration details
