import React from "react";
import { StyleSheet } from "react-native";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { AuthProvider } from "./src/context/AuthContext";
import { AppProvider } from "./src/context/AppContext";
import { ThemeProvider } from "./src/theme/ThemeProvider";
import ErrorBoundary from "./src/components/ErrorBoundary";
import RootNavigator from "./src/navigation/RootNavigator";

export default function App() {
  return (
    <GestureHandlerRootView style={styles.container}>
      <SafeAreaProvider>
        <ErrorBoundary>
          <AppProvider>
            <ThemeProvider>
              <AuthProvider>
                <RootNavigator />
              </AuthProvider>
            </ThemeProvider>
          </AppProvider>
        </ErrorBoundary>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});
