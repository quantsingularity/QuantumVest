import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import ThemeToggle from "../../components/ui/ThemeToggle";
import { ThemeProvider } from "../../contexts/ThemeContext";

// Mock localStorage
const localStorageMock = (function () {
  let store = {};
  return {
    getItem: jest.fn((key) => store[key] || null),
    setItem: jest.fn((key, value) => {
      store[key] = value.toString();
    }),
    clear: jest.fn(() => {
      store = {};
    }),
    removeItem: jest.fn((key) => {
      delete store[key];
    }),
  };
})();

Object.defineProperty(window, "localStorage", {
  value: localStorageMock,
});

// Mock document.documentElement.setAttribute
document.documentElement.setAttribute = jest.fn();

describe("ThemeToggle Component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders without crashing", () => {
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>,
    );

    const toggleButton = screen.getByRole("button");
    expect(toggleButton).toBeInTheDocument();
  });

  test("toggles theme when clicked", () => {
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>,
    );

    const toggleButton = screen.getByRole("button");

    // Initial state should be light mode
    expect(toggleButton).toHaveClass("light-mode");

    // Click to toggle to dark mode
    fireEvent.click(toggleButton);

    // Should now be in dark mode
    expect(toggleButton).toHaveClass("dark-mode");

    // Verify localStorage was updated
    expect(localStorage.setItem).toHaveBeenCalledWith("theme", "dark");

    // Verify document attribute was set
    expect(document.documentElement.setAttribute).toHaveBeenCalledWith(
      "data-theme",
      "dark",
    );

    // Click again to toggle back to light mode
    fireEvent.click(toggleButton);

    // Should now be back in light mode
    expect(toggleButton).toHaveClass("light-mode");

    // Verify localStorage was updated again
    expect(localStorage.setItem).toHaveBeenCalledWith("theme", "light");

    // Verify document attribute was set again
    expect(document.documentElement.setAttribute).toHaveBeenCalledWith(
      "data-theme",
      "light",
    );
  });
});
