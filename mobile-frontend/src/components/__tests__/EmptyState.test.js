import React from "react";
import { render } from "@testing-library/react-native";
import EmptyState from "../EmptyState";
import { PaperProvider } from "react-native-paper";

const renderWithTheme = (component) => {
  return render(<PaperProvider>{component}</PaperProvider>);
};

describe("EmptyState", () => {
  it("renders with default props", () => {
    const { getByText } = renderWithTheme(<EmptyState />);

    expect(getByText("No Data")).toBeTruthy();
    expect(getByText("There is no data to display")).toBeTruthy();
  });

  it("renders with custom props", () => {
    const { getByText } = renderWithTheme(
      <EmptyState
        title="Custom Title"
        message="Custom message"
        icon="alert-circle"
      />,
    );

    expect(getByText("Custom Title")).toBeTruthy();
    expect(getByText("Custom message")).toBeTruthy();
  });

  it("renders action button when provided", () => {
    const mockAction = jest.fn();
    const { getByText } = renderWithTheme(
      <EmptyState actionLabel="Take Action" onAction={mockAction} />,
    );

    expect(getByText("Take Action")).toBeTruthy();
  });

  it("does not render action button when not provided", () => {
    const { queryByText } = renderWithTheme(<EmptyState />);

    expect(queryByText("Take Action")).toBeNull();
  });
});
