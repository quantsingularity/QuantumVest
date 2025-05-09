import React from 'react';
import { render, waitFor, fireEvent } from '@testing-library/react-native';
import DashboardScreen from './DashboardScreen';
import { checkApiHealth, getCoinMarketChart } from '../services/api';

// Mock the API services
jest.mock('../services/api', () => ({
  checkApiHealth: jest.fn(),
  getCoinMarketChart: jest.fn()
}));

describe('DashboardScreen', () => {
  beforeEach(() => {
    // Reset mocks before each test
    checkApiHealth.mockReset();
    getCoinMarketChart.mockReset();
  });

  test('renders loading indicator initially', () => {
    const { getByTestId } = render(<DashboardScreen navigation={{}} />);
    expect(getByTestId('loading-indicator')).toBeTruthy();
  });

  test('displays API status correctly', async () => {
    checkApiHealth.mockResolvedValue({ data: { status: 'healthy' } });
    getCoinMarketChart.mockResolvedValue({ data: { prices: [[Date.now(), 50000]] } });

    const { getByText } = render(<DashboardScreen navigation={{}} />);
    await waitFor(() => {
      expect(getByText('Backend API Status: Online')).toBeTruthy();
    });
  });

  test('renders charts when data is available', async () => {
    checkApiHealth.mockResolvedValue({ data: { status: 'healthy' } });
    getCoinMarketChart.mockResolvedValue({ data: { prices: [[Date.now(), 50000]] } });

    const { getByText } = render(<DashboardScreen navigation={{}} />);
    await waitFor(() => {
      expect(getByText('Bitcoin (BTC) Price Trend (Last 7 Days)')).toBeTruthy();
      expect(getByText('Ethereum (ETH) Price Trend (Last 7 Days)')).toBeTruthy();
    });
  });

  test('handles API error correctly', async () => {
    checkApiHealth.mockRejectedValue(new Error('API Error'));
    getCoinMarketChart.mockRejectedValue(new Error('Chart Error'));

    const { getByText } = render(<DashboardScreen navigation={{}} />);
    await waitFor(() => {
      expect(getByText('Backend API Status: Error')).toBeTruthy();
    });
  });

  test('navigates to News screen when News button is pressed', async () => {
    const mockNavigation = { navigate: jest.fn() };
    const { getByText } = render(<DashboardScreen navigation={mockNavigation} />);
    fireEvent.press(getByText('News'));
    expect(mockNavigation.navigate).toHaveBeenCalledWith('News');
  });
}); 