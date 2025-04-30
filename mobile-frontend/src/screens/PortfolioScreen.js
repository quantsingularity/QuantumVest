import React, { useState } from 'react';
import { View, Text, StyleSheet, Button, TextInput, ActivityIndicator, Alert, FlatList } from 'react-native';
import { optimizePortfolio } from '../services/api';

const PortfolioScreen = () => {
  const [assetsInput, setAssetsInput] = useState('BTC,ETH,ADA'); // Example input
  const [riskToleranceInput, setRiskToleranceInput] = useState('0.5'); // Example input
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [loading, setLoading] = useState(false);

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
    <View style={styles.weightItem}>
      <Text style={styles.assetText}>{item.asset}:</Text>
      <Text style={styles.weightText}>{(item.weight * 100).toFixed(2)}%</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Portfolio Optimization</Text>

      <Text style={styles.label}>Assets (comma-separated, e.g., BTC,ETH):</Text>
      <TextInput
        style={styles.input}
        value={assetsInput}
        onChangeText={setAssetsInput}
        placeholder="Enter asset symbols"
        autoCapitalize="characters"
      />

      <Text style={styles.label}>Risk Tolerance (0.0 to 1.0):</Text>
      <TextInput
        style={styles.input}
        value={riskToleranceInput}
        onChangeText={setRiskToleranceInput}
        placeholder="Enter risk tolerance (e.g., 0.5)"
        keyboardType="numeric"
      />

      <Button title="Optimize Portfolio" onPress={handleOptimizePortfolio} disabled={loading} />

      {loading && <ActivityIndicator size="large" color="#0000ff" style={styles.loader} />}

      {optimizationResult && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>Optimization Result:</Text>
          <Text>Expected Return: {optimizationResult.expected_return.toFixed(2)}%</Text>
          <Text>Volatility: {optimizationResult.volatility.toFixed(2)}%</Text>
          <Text>Sharpe Ratio: {optimizationResult.sharpe_ratio.toFixed(2)}</Text>
          <Text style={styles.weightsTitle}>Optimal Weights:</Text>
          <FlatList
            data={optimizationResult.weightedAssets}
            renderItem={renderWeightItem}
            keyExtractor={(item) => item.asset}
          />
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  label: {
    fontSize: 16,
    marginBottom: 5,
  },
  input: {
    backgroundColor: '#fff',
    paddingHorizontal: 15,
    paddingVertical: 10,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#ddd',
    marginBottom: 15,
  },
  loader: {
    marginTop: 20,
  },
  resultContainer: {
    marginTop: 20,
    padding: 15,
    backgroundColor: '#e0f2f7',
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#b2dcef',
  },
  resultTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  weightsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 10,
    marginBottom: 5,
  },
  weightItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 5,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  assetText: {
    fontSize: 16,
  },
  weightText: {
    fontSize: 16,
    fontWeight: '500',
  },
});

export default PortfolioScreen;

