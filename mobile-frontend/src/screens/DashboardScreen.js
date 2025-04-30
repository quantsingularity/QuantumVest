import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Button, FlatList, ActivityIndicator, Alert } from 'react-native';
import { checkApiHealth, getBlockchainData } from '../services/api';

const DashboardScreen = ({ navigation }) => {
  const [apiStatus, setApiStatus] = useState('Checking...');
  const [btcData, setBtcData] = useState([]);
  const [ethData, setEthData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        // Check API Health
        const healthResponse = await checkApiHealth();
        if (healthResponse.data.status === 'healthy') {
          setApiStatus('Online');
        } else {
          setApiStatus('Offline');
        }

        // Fetch Blockchain Data (Mock)
        const btcResponse = await getBlockchainData('BTC');
        setBtcData(btcResponse.data.data || []);

        const ethResponse = await getBlockchainData('ETH');
        setEthData(ethResponse.data.data || []);

      } catch (error) {
        console.error("Error fetching dashboard data:", error);
        setApiStatus('Error');
        Alert.alert('Error', 'Failed to fetch data from the backend. Please ensure the backend server is running.');
      }
      setLoading(false);
    };

    fetchData();
  }, []);

  const renderDataItem = ({ item }) => (
    <View style={styles.dataItem}>
      <Text>Timestamp: {new Date(item.timestamp * 1000).toLocaleDateString()}</Text>
      <Text>Price: ${item.price}</Text>
      <Text>Volume: {item.volume.toLocaleString()}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.title}>QuantumVest Dashboard</Text>
      <Text style={styles.statusText}>API Status: {apiStatus}</Text>
      
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <View style={styles.dataContainer}>
          <Text style={styles.sectionTitle}>BTC Data (Mock)</Text>
          <FlatList
            data={btcData}
            renderItem={renderDataItem}
            keyExtractor={(item, index) => index.toString()}
            style={styles.list}
          />
          
          <Text style={styles.sectionTitle}>ETH Data (Mock)</Text>
          <FlatList
            data={ethData}
            renderItem={renderDataItem}
            keyExtractor={(item, index) => index.toString()}
            style={styles.list}
          />
        </View>
      )}

      <View style={styles.buttonContainer}>
        <Button 
          title="Go to Predictions" 
          onPress={() => navigation.navigate('Prediction')} 
        />
        <Button 
          title="Go to Portfolio Optimization" 
          onPress={() => navigation.navigate('Portfolio')} 
        />
      </View>
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
    marginBottom: 10,
    textAlign: 'center',
  },
  statusText: {
    fontSize: 16,
    marginBottom: 20,
    textAlign: 'center',
    color: 'grey',
  },
  dataContainer: {
    flex: 1, // Ensure data container takes available space
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 15,
    marginBottom: 5,
  },
  list: {
    maxHeight: 150, // Limit height to prevent excessive scrolling
    marginBottom: 10,
  },
  dataItem: {
    backgroundColor: '#fff',
    padding: 10,
    marginBottom: 5,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#ddd',
  },
  buttonContainer: {
    marginTop: 20,
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
});

export default DashboardScreen;

