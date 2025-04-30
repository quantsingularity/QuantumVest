import React, { useState } from 'react';
import { View, StyleSheet, Alert, FlatList } from 'react-native';
import { Appbar, Card, Text, TextInput, Button, ActivityIndicator, List, Divider, useTheme } from 'react-native-paper';
import { optimizePortfolio } from '../services/api';

const PortfolioScreen = ({ navigation }) => {
  const [assetsInput, setAssetsInput] = useState('BTC,ETH,ADA'); // Example input
  const [riskToleranceInput, setRiskToleranceInput] = useState('0.5'); // Example input
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const theme = useTheme();

  const handleOptimizePortfolio = async () => {
    const assets = assetsInput.split(',').map(a => a.trim().toUpperCase()).filter(a => a);
    const riskTolerance = parseFloat(riskToleranceInput);

    if (assets.length === 0) {
      Alert.alert('Input Error', 'Please enter at least one asset symbol, separated by commas.');
      return;
    }
    if (isNaN(riskTolerance) || riskTolerance < 0 || riskTolerance > 1) {
      Alert.alert('Input Error', 'Risk tolerance must be a number between 0 and 1.');
      return;
    }

    setLoading(true);
    setOptimizationResult(null);
    try {
      const response = await optimizePortfolio(assets, riskTolerance);
      if (response.data.success) {
        // Combine assets with their weights for display
        const weightedAssets = assets.map((asset, index) => ({
          asset,
          weight: response.data.optimal_weights[index] || 0
        }));
        setOptimizationResult({ ...response.data, weightedAssets });
      } else {
        Alert.alert('Optimization Failed', response.data.error || 'Could not optimize portfolio.');
      }
    } catch (error) {
      console.error("Error optimizing portfolio:", error);
      Alert.alert('Error', 'Failed to optimize portfolio. Check API connection.');
    }
    setLoading(false);
  };

  const renderWeightItem = ({ item }) => (
    <List.Item
      title={item.asset}
      description={`${(item.weight * 100).toFixed(2)}%`}
      left={props => <List.Icon {...props} icon="chart-pie" />} // Example icon
    />
  );

  return (
    <View style={[styles.container, { backgroundColor: theme.colors.background }]}>
      <Appbar.Header>
        {navigation.canGoBack() && <Appbar.BackAction onPress={() => navigation.goBack()} />}
        <Appbar.Content title="Portfolio Optimization" />
      </Appbar.Header>

      <View style={styles.contentContainer}>
        <Card style={styles.card} elevation={2}>
          <Card.Content>
            <TextInput
              label="Assets (comma-separated)"
              value={assetsInput}
              onChangeText={setAssetsInput}
              mode="outlined"
              style={styles.input}
              autoCapitalize="characters"
              placeholder="e.g., BTC,ETH,ADA"
            />
            <TextInput
              label="Risk Tolerance (0.0 to 1.0)"
              value={riskToleranceInput}
              onChangeText={setRiskToleranceInput}
              mode="outlined"
              style={styles.input}
              keyboardType="numeric"
              placeholder="e.g., 0.5"
            />
            <Button 
              mode="contained" 
              onPress={handleOptimizePortfolio} 
              disabled={loading} 
              loading={loading}
              style={styles.button}
              icon="calculator-variant" // Example icon
            >
              Optimize Portfolio
            </Button>
          </Card.Content>
        </Card>

        {loading && <ActivityIndicator animating={true} size="large" style={styles.loader} />}

        {optimizationResult && (
          <Card style={[styles.card, styles.resultCard]} elevation={2}>
            <Card.Title title="Optimization Result" titleVariant="headlineSmall" />
            <Card.Content>
              <Text variant="bodyLarge">Expected Return: {optimizationResult.expected_return.toFixed(2)}%</Text>
              <Text variant="bodyLarge">Volatility: {optimizationResult.volatility.toFixed(2)}%</Text>
              <Text variant="bodyLarge">Sharpe Ratio: {optimizationResult.sharpe_ratio.toFixed(2)}</Text>
              <List.Subheader style={styles.weightsTitle}>Optimal Weights</List.Subheader>
              <FlatList
                data={optimizationResult.weightedAssets}
                renderItem={renderWeightItem}
                keyExtractor={(item) => item.asset}
                ItemSeparatorComponent={Divider}
              />
            </Card.Content>
          </Card>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  contentContainer: {
    flex: 1,
    padding: 15,
  },
  card: {
    marginBottom: 20,
  },
  input: {
    marginBottom: 15,
  },
  button: {
    marginTop: 10,
  },
  loader: {
    marginTop: 20,
  },
  resultCard: {
    // Add specific styling for result card if needed
  },
  weightsTitle: {
    fontSize: 18, // Adjust as needed
    fontWeight: 'bold',
    marginTop: 10,
    marginLeft: -8, // Align with List.Item
  },
});

export default PortfolioScreen;

