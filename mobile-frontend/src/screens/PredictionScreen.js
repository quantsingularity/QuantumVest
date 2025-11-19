import React, { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Appbar, Card, Text, TextInput, Button, ActivityIndicator, useTheme } from 'react-native-paper';
import { getPrediction } from '../services/api';

const PredictionScreen = ({ navigation }) => {
  const [asset, setAsset] = useState('BTC');
  const [timeframe, setTimeframe] = useState('7d');
  const [currentPrice, setCurrentPrice] = useState('59000'); // Default example price
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const theme = useTheme();

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
    <View style={[styles.container, { backgroundColor: theme.colors.background }]}>
      <Appbar.Header>
        {/* Add a back action if needed, or just the title */}
        {navigation.canGoBack() && <Appbar.BackAction onPress={() => navigation.goBack()} />}
        <Appbar.Content title="Market Predictions" />
      </Appbar.Header>

      <View style={styles.contentContainer}>
        <Card style={styles.card} elevation={2}>
          <Card.Content>
            <TextInput
              label="Asset (e.g., BTC, ETH)"
              value={asset}
              onChangeText={setAsset}
              mode="outlined"
              style={styles.input}
              autoCapitalize="characters"
            />
            <TextInput
              label="Timeframe (e.g., 1d, 7d, 30d)"
              value={timeframe}
              onChangeText={setTimeframe}
              mode="outlined"
              style={styles.input}
            />
            <TextInput
              label="Current Price"
              value={currentPrice}
              onChangeText={setCurrentPrice}
              mode="outlined"
              style={styles.input}
              keyboardType="numeric"
            />
            <Button
              mode="contained"
              onPress={handleGetPrediction}
              disabled={loading}
              loading={loading}
              style={styles.button}
              icon="chart-bell-curve-cumulative" // Example icon
            >
              Get Prediction
            </Button>
          </Card.Content>
        </Card>

        {loading && <ActivityIndicator animating={true} size="large" style={styles.loader} />}

        {predictionResult && (
          <Card style={[styles.card, styles.resultCard]} elevation={2}>
            <Card.Title title="Prediction Result" titleVariant="headlineSmall" />
            <Card.Content>
              <Text variant="bodyLarge">Asset: {predictionResult.asset}</Text>
              <Text variant="bodyLarge">Timeframe: {predictionResult.timeframe}</Text>
              <Text variant="bodyLarge">Predicted Price: ${predictionResult.prediction.toFixed(2)}</Text>
              <Text variant="bodyLarge">Confidence: {(predictionResult.confidence * 100).toFixed(1)}%</Text>
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
    // Example: backgroundColor: theme.colors.surfaceVariant
  },
});

export default PredictionScreen;
