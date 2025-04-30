import React, { useState } from 'react';
import { View, Text, StyleSheet, Button, TextInput, ActivityIndicator, Alert } from 'react-native';
import { getPrediction } from '../services/api';

const PredictionScreen = () => {
  const [asset, setAsset] = useState('BTC');
  const [timeframe, setTimeframe] = useState('7d');
  const [currentPrice, setCurrentPrice] = useState('59000'); // Default example price
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGetPrediction = async () => {
    if (!asset || !timeframe || !currentPrice) {
      Alert.alert('Input Error', 'Please fill in all fields.');
      return;
    }
    setLoading(true);
    setPredictionResult(null);
    try {
      const price = parseFloat(currentPrice);
      if (isNaN(price)) {
        Alert.alert('Input Error', 'Current price must be a valid number.');
        setLoading(false);
        return;
      }
      const response = await getPrediction(asset, timeframe, price);
      if (response.data.success) {
        setPredictionResult(response.data);
      } else {
        Alert.alert('Prediction Failed', response.data.error || 'Could not get prediction.');
      }
    } catch (error) {
      console.error("Error getting prediction:", error);
      Alert.alert('Error', 'Failed to get prediction. Check API connection.');
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Market Prediction</Text>
      
      <Text style={styles.label}>Asset (e.g., BTC, ETH):</Text>
      <TextInput
        style={styles.input}
        value={asset}
        onChangeText={setAsset}
        placeholder="Enter asset symbol"
        autoCapitalize="characters"
      />

      <Text style={styles.label}>Timeframe (e.g., 1d, 7d, 30d):</Text>
      <TextInput
        style={styles.input}
        value={timeframe}
        onChangeText={setTimeframe}
        placeholder="Enter timeframe"
      />

      <Text style={styles.label}>Current Price:</Text>
      <TextInput
        style={styles.input}
        value={currentPrice}
        onChangeText={setCurrentPrice}
        placeholder="Enter current price"
        keyboardType="numeric"
      />

      <Button title="Get Prediction" onPress={handleGetPrediction} disabled={loading} />

      {loading && <ActivityIndicator size="large" color="#0000ff" style={styles.loader} />}

      {predictionResult && (
        <View style={styles.resultContainer}>
          <Text style={styles.resultTitle}>Prediction Result:</Text>
          <Text>Asset: {predictionResult.asset}</Text>
          <Text>Timeframe: {predictionResult.timeframe}</Text>
          <Text>Predicted Price: ${predictionResult.prediction.toFixed(2)}</Text>
          <Text>Confidence: {(predictionResult.confidence * 100).toFixed(1)}%</Text>
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
    backgroundColor: '#e0f7fa',
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#b2ebf2',
  },
  resultTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
});

export default PredictionScreen;

