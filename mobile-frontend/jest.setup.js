import "@testing-library/jest-native/extend-expect";

// Mock AsyncStorage
jest.mock("@react-native-async-storage/async-storage", () =>
  require("@react-native-async-storage/async-storage/jest/async-storage-mock"),
);

// Mock react-native-vector-icons
jest.mock("react-native-vector-icons/MaterialCommunityIcons", () => "Icon");

// Mock Linking
jest.mock("react-native/Libraries/Linking/Linking", () => ({
  openURL: jest.fn(() => Promise.resolve()),
  canOpenURL: jest.fn(() => Promise.resolve(true)),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
}));

// Mock Dimensions
jest.mock("react-native/Libraries/Utilities/Dimensions", () => ({
  get: jest.fn(() => ({ width: 375, height: 667 })),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
}));

// Mock PixelRatio
jest.mock("react-native/Libraries/Utilities/PixelRatio", () => ({
  get: jest.fn(() => 2),
  getFontScale: jest.fn(() => 1),
  getPixelSizeForLayoutSize: jest.fn((size) => size * 2),
  roundToNearestPixel: jest.fn((size) => Math.round(size)),
}));

// Mock react-native-reanimated
jest.mock("react-native-reanimated", () => {
  const Reanimated = require("react-native-reanimated/mock");
  Reanimated.default.call = () => {};
  return Reanimated;
});

// Mock expo-constants
jest.mock("expo-constants", () => ({
  expoConfig: {
    extra: {
      apiBaseUrl: "http://localhost:5000/api/v1",
      coingeckoApiUrl: "https://api.coingecko.com/api/v3",
      cryptonewsApiToken: "",
      appEnv: "development",
      enableMockData: false,
    },
  },
}));

// Global test timeout
jest.setTimeout(10000);

// Suppress console errors in tests
global.console = {
  ...console,
  error: jest.fn(),
  warn: jest.fn(),
};
