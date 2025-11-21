import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";

// Import Screens
import DashboardScreen from "../screens/DashboardScreen";
import PredictionScreen from "../screens/PredictionScreen";
import PortfolioScreen from "../screens/PortfolioScreen";
import WatchlistScreen from "../screens/WatchlistScreen";
import NewsScreen from "../screens/NewsScreen"; // Import the new News screen

const Stack = createStackNavigator();

const AppNavigator = () => {
  return (
    <NavigationContainer>
      {/* Use screenOptions to hide the header globally as we use Appbar in each screen */}
      <Stack.Navigator
        initialRouteName="Dashboard"
        screenOptions={{ headerShown: false }}
      >
        <Stack.Screen name="Dashboard" component={DashboardScreen} />
        <Stack.Screen name="Prediction" component={PredictionScreen} />
        <Stack.Screen name="Portfolio" component={PortfolioScreen} />
        <Stack.Screen name="Watchlist" component={WatchlistScreen} />
        <Stack.Screen
          name="News" // Add the News screen route
          component={NewsScreen}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;
