import React from "react";
import { StyleSheet } from "react-native";
import AppNavigator from "./src/navigation/AppNavigator";
import { GestureHandlerRootView } from "react-native-gesture-handler"; // Required for React Navigation
import { SafeAreaProvider } from "react-native-safe-area-context"; // Required for React Navigation
import { Provider as PaperProvider } from "react-native-paper"; // Import PaperProvider

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <SafeAreaProvider>
        <PaperProvider>
          {" "}
          {/* Wrap the app with PaperProvider */}
          <AppNavigator />
        </PaperProvider>
      </SafeAreaProvider>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
  },
});
