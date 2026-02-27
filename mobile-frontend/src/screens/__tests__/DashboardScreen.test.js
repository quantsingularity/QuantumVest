import React from "react";
import { render, waitFor, fireEvent } from "@testing-library/react-native";
import DashboardScreen from "../DashboardScreen";
import { checkApiHealth, getCoinMarketChart } from "../../services/api";

// Mock navigation
const mockNavigation = {
  navigate: jest.fn(),
  canGoBack: jest.fn(() => false),
};

// Mock the API services
jest.mock("../../services/api", () => ({
  checkApiHealth: jest.fn(),
  getCoinMarketChart: jest.fn(),
}));

// Mock react-native-chart-kit
jest.mock("react-native-chart-kit", () => ({
  LineChart: "LineChart",
}));

describe("DashboardScreen", () => {
  beforeEach(() => {
    checkApiHealth.mockReset();
    getCoinMarketChart.mockReset();
    mockNavigation.navigate.mockReset();
  });

  test("renders loading indicator initially", () => {
    checkApiHealth.mockImplementation(() => new Promise(() => {}));
    getCoinMarketChart.mockImplementation(() => new Promise(() => {}));

    const { getByTestId } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );
    const loader = getByTestId("activity-indicator");
    expect(loader).toBeTruthy();
  });

  test("displays API status correctly when healthy", async () => {
    checkApiHealth.mockResolvedValue({ data: { status: "healthy" } });
    getCoinMarketChart.mockResolvedValue({
      data: {
        prices: [
          [Date.now(), 50000],
          [Date.now() + 86400000, 51000],
        ],
      },
    });

    const { getByText } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );
    await waitFor(() => {
      expect(getByText(/Online/i)).toBeTruthy();
    });
  });

  test("displays API status correctly when offline", async () => {
    checkApiHealth.mockResolvedValue({ data: { status: "offline" } });
    getCoinMarketChart.mockResolvedValue({
      data: {
        prices: [
          [Date.now(), 50000],
          [Date.now() + 86400000, 51000],
        ],
      },
    });

    const { getByText } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );
    await waitFor(() => {
      expect(getByText(/Offline/i)).toBeTruthy();
    });
  });

  test("renders charts when data is available", async () => {
    checkApiHealth.mockResolvedValue({ data: { status: "healthy" } });
    getCoinMarketChart.mockResolvedValue({
      data: {
        prices: [
          [Date.now(), 50000],
          [Date.now() + 86400000, 51000],
        ],
      },
    });

    const { getByText } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );
    await waitFor(() => {
      expect(getByText(/Bitcoin \(BTC\)/i)).toBeTruthy();
      expect(getByText(/Ethereum \(ETH\)/i)).toBeTruthy();
    });
  });

  test("handles API error correctly", async () => {
    checkApiHealth.mockRejectedValue(new Error("API Error"));
    getCoinMarketChart.mockRejectedValue(new Error("Chart Error"));

    const { getByText } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );
    await waitFor(() => {
      expect(getByText(/Error/i)).toBeTruthy();
    });
  });

  test("navigates to News screen when News button is pressed", async () => {
    checkApiHealth.mockResolvedValue({ data: { status: "healthy" } });
    getCoinMarketChart.mockResolvedValue({
      data: {
        prices: [
          [Date.now(), 50000],
          [Date.now() + 86400000, 51000],
        ],
      },
    });

    const { getByText } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );

    await waitFor(() => {
      expect(getByText("News")).toBeTruthy();
    });

    fireEvent.press(getByText("News"));
    expect(mockNavigation.navigate).toHaveBeenCalledWith("News");
  });

  test("navigates to Settings when settings icon is pressed", async () => {
    checkApiHealth.mockResolvedValue({ data: { status: "healthy" } });
    getCoinMarketChart.mockResolvedValue({
      data: {
        prices: [
          [Date.now(), 50000],
          [Date.now() + 86400000, 51000],
        ],
      },
    });

    const { getByTestId } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );

    await waitFor(() => {
      const settingsButton = getByTestId("appbar-action-cog");
      expect(settingsButton).toBeTruthy();
    });
  });

  test("displays empty state when no chart data available", async () => {
    checkApiHealth.mockResolvedValue({ data: { status: "healthy" } });
    getCoinMarketChart.mockResolvedValue({
      data: { prices: [] },
    });

    const { getByText } = render(
      <DashboardScreen navigation={mockNavigation} />,
    );

    await waitFor(() => {
      expect(getByText(/Not enough data/i)).toBeTruthy();
    });
  });
});
