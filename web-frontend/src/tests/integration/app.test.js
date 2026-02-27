import React from "react";
import { render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import App from "../../App";

// Mock API modules
jest.mock("../../services/api", () => ({
  authAPI: {
    getProfile: jest.fn().mockResolvedValue({ data: { success: false } }),
  },
  marketDataAPI: {
    getBlockchainData: jest
      .fn()
      .mockResolvedValue({ data: { success: false } }),
  },
  portfolioAPI: {
    getPortfolio: jest
      .fn()
      .mockResolvedValue({ data: { success: false, portfolios: [] } }),
  },
  predictionAPI: {
    getPrediction: jest.fn().mockResolvedValue({ data: { success: false } }),
  },
  settingsAPI: {
    getSettings: jest.fn().mockResolvedValue({ data: { success: false } }),
  },
}));

// Mock framer-motion to avoid animation issues in tests
jest.mock("framer-motion", () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
    header: ({ children, ...props }) => <header {...props}>{children}</header>,
    footer: ({ children, ...props }) => <footer {...props}>{children}</footer>,
    aside: ({ children, ...props }) => <aside {...props}>{children}</aside>,
    li: ({ children, ...props }) => <li {...props}>{children}</li>,
  },
  AnimatePresence: ({ children }) => <>{children}</>,
}));

describe("App Integration Tests", () => {
  test("renders app without crashing", () => {
    render(<App />);
    // App should render successfully
  });

  test("renders sidebar with QuantumVest logo", async () => {
    render(<App />);
    await waitFor(() => {
      const elements = screen.getAllByText("QuantumVest");
      expect(elements.length).toBeGreaterThan(0);
    });
  });

  test("renders header component", async () => {
    render(<App />);
    await waitFor(() => {
      // Look for any header-specific element
      const header = document.querySelector(".header");
      expect(header).toBeInTheDocument();
    });
  });

  test("renders footer with copyright", async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/all rights reserved/i)).toBeInTheDocument();
    });
  });

  test("renders homepage by default", async () => {
    render(<App />);
    await waitFor(() => {
      expect(
        screen.getByText(/Next-Gen Investment Analytics/i),
      ).toBeInTheDocument();
    });
  });
});
