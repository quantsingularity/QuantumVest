import React from "react";
import { createStackNavigator } from "@react-navigation/stack";

// Import Screens
import DashboardScreen from "../screens/DashboardScreen";
import PredictionScreen from "../screens/PredictionScreen";
import PortfolioScreen from "../screens/PortfolioScreen";
import WatchlistScreen from "../screens/WatchlistScreen";
import NewsScreen from "../screens/NewsScreen";
import SettingsScreen from "../screens/SettingsScreen";

const Stack = createStackNavigator();

const AppNavigator = () => {
  return (
    <Stack.Navigator
      initialRouteName="Dashboard"
      screenOptions={{ headerShown: false }}
    >
      <Stack.Screen name="Dashboard" component={DashboardScreen} />
      <Stack.Screen name="Prediction" component={PredictionScreen} />
      <Stack.Screen name="Portfolio" component={PortfolioScreen} />
      <Stack.Screen name="Watchlist" component={WatchlistScreen} />
      <Stack.Screen name="News" component={NewsScreen} />
      <Stack.Screen name="Settings" component={SettingsScreen} />
    </Stack.Navigator>
  );
};

export default AppNavigator;
