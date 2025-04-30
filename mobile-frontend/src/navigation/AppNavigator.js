import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

// Import Screens (will be created later)
import DashboardScreen from '../screens/DashboardScreen';
import PredictionScreen from '../screens/PredictionScreen';
import PortfolioScreen from '../screens/PortfolioScreen';

const Stack = createStackNavigator();

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Dashboard">
        <Stack.Screen 
          name="Dashboard" 
          component={DashboardScreen} 
          options={{ title: 'QuantumVest Dashboard' }} 
        />
        <Stack.Screen 
          name="Prediction" 
          component={PredictionScreen} 
          options={{ title: 'Market Predictions' }} 
        />
        <Stack.Screen 
          name="Portfolio" 
          component={PortfolioScreen} 
          options={{ title: 'Portfolio Optimization' }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;

