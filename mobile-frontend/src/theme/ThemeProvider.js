import React, { useMemo } from "react";
import {
  MD3LightTheme,
  MD3DarkTheme,
  Provider as PaperProvider,
} from "react-native-paper";
import { useApp } from "../context/AppContext";

const lightTheme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary: "#6200ee",
    primaryContainer: "#bb86fc",
    secondary: "#03dac6",
    secondaryContainer: "#018786",
    background: "#ffffff",
    surface: "#ffffff",
    error: "#b00020",
    onPrimary: "#ffffff",
    onSecondary: "#000000",
    onBackground: "#000000",
    onSurface: "#000000",
    onError: "#ffffff",
  },
};

const darkTheme = {
  ...MD3DarkTheme,
  colors: {
    ...MD3DarkTheme.colors,
    primary: "#bb86fc",
    primaryContainer: "#3700b3",
    secondary: "#03dac6",
    secondaryContainer: "#03dac6",
    background: "#121212",
    surface: "#121212",
    error: "#cf6679",
    onPrimary: "#000000",
    onSecondary: "#000000",
    onBackground: "#ffffff",
    onSurface: "#ffffff",
    onError: "#000000",
  },
};

export const ThemeProvider = ({ children }) => {
  const { theme: appTheme } = useApp();

  const theme = useMemo(() => {
    return appTheme === "dark" ? darkTheme : lightTheme;
  }, [appTheme]);

  return <PaperProvider theme={theme}>{children}</PaperProvider>;
};

export { lightTheme, darkTheme };
