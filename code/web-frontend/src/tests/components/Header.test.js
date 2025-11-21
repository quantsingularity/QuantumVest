import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { BrowserRouter } from "react-router-dom";
import Header from "../../components/layout/Header";
import { ThemeProvider } from "../../contexts/ThemeContext";
import { NotificationProvider } from "../../contexts/NotificationContext";

describe("Header Component", () => {
  const mockToggleSidebar = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders header with logo and search bar", () => {
    render(
      <BrowserRouter>
        <ThemeProvider>
          <NotificationProvider>
            <Header toggleSidebar={mockToggleSidebar} />
          </NotificationProvider>
        </ThemeProvider>
      </BrowserRouter>,
    );

    // Check for logo
    expect(screen.getByText("QuantumVest")).toBeInTheDocument();

    // Check for search bar
    const searchInput = screen.getByPlaceholderText("Search...");
    expect(searchInput).toBeInTheDocument();
  });

  test("calls toggleSidebar when menu button is clicked", () => {
    render(
      <BrowserRouter>
        <ThemeProvider>
          <NotificationProvider>
            <Header toggleSidebar={mockToggleSidebar} />
          </NotificationProvider>
        </ThemeProvider>
      </BrowserRouter>,
    );

    const menuButton = document.querySelector(".menu-toggle");
    fireEvent.click(menuButton);

    expect(mockToggleSidebar).toHaveBeenCalledTimes(1);
  });

  test("toggles notification center when notification bell is clicked", () => {
    render(
      <BrowserRouter>
        <ThemeProvider>
          <NotificationProvider>
            <Header toggleSidebar={mockToggleSidebar} />
          </NotificationProvider>
        </ThemeProvider>
      </BrowserRouter>,
    );

    // Initially notification center should not be visible
    expect(screen.queryByText("Notifications")).not.toBeInTheDocument();

    // Click notification bell
    const notificationBell = document.querySelector(".notification-bell");
    fireEvent.click(notificationBell);

    // Notification center should now be visible
    expect(screen.getByText("Notifications")).toBeInTheDocument();

    // Click again to hide
    fireEvent.click(notificationBell);

    // Notification center should be hidden again
    expect(screen.queryByText("Notifications")).not.toBeInTheDocument();
  });

  test("displays login button", () => {
    render(
      <BrowserRouter>
        <ThemeProvider>
          <NotificationProvider>
            <Header toggleSidebar={mockToggleSidebar} />
          </NotificationProvider>
        </ThemeProvider>
      </BrowserRouter>,
    );

    const loginButton = screen.getByText("Login");
    expect(loginButton).toBeInTheDocument();
    expect(loginButton.tagName).toBe("BUTTON");
    expect(loginButton).toHaveClass("btn-primary");
  });

  test("includes theme toggle component", () => {
    render(
      <BrowserRouter>
        <ThemeProvider>
          <NotificationProvider>
            <Header toggleSidebar={mockToggleSidebar} />
          </NotificationProvider>
        </ThemeProvider>
      </BrowserRouter>,
    );

    // Check for theme toggle button
    const themeToggle = document.querySelector(".theme-toggle");
    expect(themeToggle).toBeInTheDocument();
  });

  test("search functionality works correctly", () => {
    const mockOnSearch = jest.fn();
    render(<Header onSearch={mockOnSearch} />);
    const searchInput = screen.getByPlaceholderText("Search...");
    fireEvent.change(searchInput, { target: { value: "test query" } });
    expect(mockOnSearch).toHaveBeenCalledWith("test query");
  });

  test("notification center toggles correctly", () => {
    render(<Header />);
    const notificationBell = screen.getByTestId("notification-bell");
    fireEvent.click(notificationBell);
    expect(screen.getByTestId("notification-center")).toBeInTheDocument();
    fireEvent.click(notificationBell);
    expect(screen.queryByTestId("notification-center")).not.toBeInTheDocument();
  });
});
