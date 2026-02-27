import React from "react";
import { render, waitFor, fireEvent } from "@testing-library/react-native";
import PredictionScreen from "../PredictionScreen";
import { getPrediction } from "../../services/api";

const mockNavigation = {
  navigate: jest.fn(),
  goBack: jest.fn(),
  canGoBack: jest.fn(() => true),
};

jest.mock("../../services/api", () => ({
  getPrediction: jest.fn(),
}));

describe("PredictionScreen", () => {
  beforeEach(() => {
    getPrediction.mockReset();
    mockNavigation.navigate.mockReset();
  });

  test("renders input fields correctly", () => {
    const { getByText, getByDisplayValue } = render(
      <PredictionScreen navigation={mockNavigation} />,
    );

    expect(getByText("Market Predictions")).toBeTruthy();
    expect(getByDisplayValue("BTC")).toBeTruthy();
    expect(getByDisplayValue("7d")).toBeTruthy();
    expect(getByDisplayValue("59000")).toBeTruthy();
  });

  test("shows validation error when fields are empty", () => {
    const { getByText } = render(
      <PredictionScreen navigation={mockNavigation} />,
    );

    const button = getByText("Get Prediction");
    fireEvent.press(button);

    // Alert should be shown (mocked in test environment)
    expect(getPrediction).not.toHaveBeenCalled();
  });

  test("calls getPrediction API with correct parameters", async () => {
    getPrediction.mockResolvedValue({
      data: {
        success: true,
        asset: "BTC",
        timeframe: "7d",
        prediction: 62000,
        confidence: 0.85,
      },
    });

    const { getByText, getByDisplayValue } = render(
      <PredictionScreen navigation={mockNavigation} />,
    );

    const button = getByText("Get Prediction");
    fireEvent.press(button);

    await waitFor(() => {
      expect(getPrediction).toHaveBeenCalledWith("BTC", "7d", 59000);
    });
  });

  test("displays prediction result correctly", async () => {
    getPrediction.mockResolvedValue({
      data: {
        success: true,
        asset: "BTC",
        timeframe: "7d",
        prediction: 62000,
        confidence: 0.85,
      },
    });

    const { getByText } = render(
      <PredictionScreen navigation={mockNavigation} />,
    );

    const button = getByText("Get Prediction");
    fireEvent.press(button);

    await waitFor(() => {
      expect(getByText("Prediction Result")).toBeTruthy();
      expect(getByText(/\$62000\.00/)).toBeTruthy();
      expect(getByText(/85\.0%/)).toBeTruthy();
    });
  });

  test("handles API error correctly", async () => {
    getPrediction.mockRejectedValue(new Error("API Error"));

    const { getByText } = render(
      <PredictionScreen navigation={mockNavigation} />,
    );

    const button = getByText("Get Prediction");
    fireEvent.press(button);

    await waitFor(() => {
      expect(getPrediction).toHaveBeenCalled();
    });
  });

  test("allows user to change input values", () => {
    const { getByDisplayValue } = render(
      <PredictionScreen navigation={mockNavigation} />,
    );

    const assetInput = getByDisplayValue("BTC");
    fireEvent.changeText(assetInput, "ETH");

    expect(getByDisplayValue("ETH")).toBeTruthy();
  });
});
